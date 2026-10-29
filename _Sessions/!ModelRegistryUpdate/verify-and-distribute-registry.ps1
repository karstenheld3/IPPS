param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("Gate1", "Gate2", "Gate567", "Gate94", "Distribute", "VerifyAll")]
  [string]$Mode,

  [Parameter(Mandatory = $true)]
  [string]$RunFolder,

  [Parameter(Mandatory = $true)]
  [string]$Date,

  [Parameter(Mandatory = $true)]
  [string]$SkillFolder,

  [Parameter(Mandatory = $true)]
  [string]$InventoryFile,

  [Parameter(Mandatory = $false)]
  [string]$AgentFolder = "e:\dev\IPPS\.devin",

  [Parameter(Mandatory = $false)]
  [string]$PromptSystemFolder = "e:\dev\IPPS\PromptSystemV4.5",

  [Parameter(Mandatory = $false)]
  [switch]$IncludeExternal,

  [Parameter(Mandatory = $false)]
  [switch]$AllowSameDateReRun
)

$ErrorActionPreference = "Stop"

function Invoke-Gate1 {
  $p = Get-Content "$SkillFolder\model-pricing.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  $r = Get-Content "$SkillFolder\model-registry.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  $m = Get-Content "$SkillFolder\model-parameter-mapping.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  Write-Output "Gate 1 Pre-Flight: pricing=$($p.last_updated), registry=$($r._updated) ($($r._version)), mapping=$($m._updated) ($($m._version))"
  if (-not $AllowSameDateReRun -and ($p.last_updated -eq $Date) -and ($r._updated -eq $Date)) {
    Write-Output "Gate 1 INFO: JSON dates already equal $Date (re-run in progress)"
  }
  Write-Output "Gate 1: PASS"
}

function Invoke-Gate2 {
  $domFiles = Get-ChildItem "$RunFolder\${Date}_*-DOM.json" -ErrorAction SilentlyContinue
  if (-not $domFiles -or $domFiles.Count -lt 4) {
    throw "Gate 2 FAIL: Expected at least 4 ${Date}_*-DOM.json files in $RunFolder, found $(@($domFiles).Count)"
  }
  foreach ($df in $domFiles) {
    if ($df.Length -lt 50) { throw "Gate 2 FAIL: Empty or truncated DOM file $($df.Name)" }
    $null = Get-Content $df.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  }
  Write-Output "Gate 2: PASS ($($domFiles.Count) valid DOM JSON files verified in $RunFolder)"
}

function Invoke-Gate567 {
  # Gate 5
  $r = Get-Content "$SkillFolder\model-registry.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($r._updated -ne $Date) { throw "Gate 5 FAIL: registry _updated ($($r._updated)) != $Date" }
  $knownNonText = @("computer-use-preview", "gpt-image-1.5")
  $unmatched = @()
  foreach ($m in $r.models) {
    $matched = $r.model_id_startswith | Where-Object { $m.model_id.StartsWith($_.prefix) }
    if (-not $matched) {
      if ($knownNonText -contains $m.model_id) {
        Write-Warning "No prefix match (non-text SKU): $($m.model_id)"
      } else {
        $unmatched += $m.model_id
      }
    }
  }
  if ($unmatched.Count -gt 0) { throw "Gate 5 FAIL: Unmatched model_id_startswith prefixes: $($unmatched -join ', ')" }
  $ids = $r.models.model_id
  if (($ids | Sort-Object -Unique).Count -ne $ids.Count) { throw "Gate 5 FAIL: Duplicate model_ids in model-registry.json" }
  Write-Output "Gate 5: PASS (models=$($ids.Count), 0 unexpected unmatched prefixes)"

  # Gate 6
  $p = Get-Content "$SkillFolder\model-pricing.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($p.last_updated -ne $Date) { throw "Gate 6 FAIL: pricing last_updated ($($p.last_updated)) != $Date" }
  $csPath = "$RunFolder\${Date}_ChangeSet.json"
  if (Test-Path $csPath) {
    $cs = Get-Content $csPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $newIds = @($cs.newPricingIds) + @($cs.changedPricingIds) | Select-Object -Unique
    foreach ($id in $newIds) {
      if (-not $p.pricing.anthropic.$id -and -not $p.pricing.openai.$id -and -not $p.pricing.google.$id -and -not $p.pricing.zai.$id) {
        throw "Gate 6 FAIL: Missing $id in model-pricing.json"
      }
    }
    Write-Output "Gate 6: PASS (verified $($newIds.Count) new/changed pricing IDs)"
  } else {
    Write-Output "Gate 6: PASS (last_updated=$Date)"
  }

  # Gate 7
  $m = Get-Content "$SkillFolder\model-parameter-mapping.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  $methods = $r.model_id_startswith | ForEach-Object { $_.method } | Sort-Object -Unique
  foreach ($method in $methods) {
    $key = switch ($method) {
      "temperature"        { "temperature_factor" }
      "reasoning_effort"   { "openai_reasoning_effort" }
      "effort"             { "openai_reasoning_effort" }
      "thinking"           { "anthropic_thinking_factor" }
      "adaptive_thinking"  { "anthropic_adaptive_effort" }
      default              { $method }
    }
    if (-not ($m.effort_mapping.medium.PSObject.Properties.Name -contains $key)) {
      throw "Gate 7 FAIL: Missing effort_mapping for method '$method' (key '$key')"
    }
  }
  Write-Output "Gate 7: PASS (methods=$($methods -join ', '))"
}

function Invoke-Gate94 {
  $r = Get-Content "$SkillFolder\model-registry.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  $p = Get-Content "$SkillFolder\model-pricing.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  $m = Get-Content "$SkillFolder\model-parameter-mapping.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  $inv = Get-Content $InventoryFile -Raw -Encoding UTF8

  if ($inv -notmatch "model-registry\.json.\s+$([regex]::Escape($r._version))\s+\($([regex]::Escape($r._updated))\)") {
    throw "Gate 9.4 FAIL: model-registry.json version/date in MODEL_INVENTORY.md does not match $($r._version) ($($r._updated))"
  }
  if ($inv -notmatch "model-pricing\.json.\s+\($([regex]::Escape($p.last_updated))\)") {
    throw "Gate 9.4 FAIL: model-pricing.json date in MODEL_INVENTORY.md does not match ($($p.last_updated))"
  }
  if ($inv -notmatch "model-parameter-mapping\.json.\s+$([regex]::Escape($m._version))\s+\($([regex]::Escape($m._updated))\)") {
    throw "Gate 9.4 FAIL: model-parameter-mapping.json version/date in MODEL_INVENTORY.md does not match $($m._version) ($($m._updated))"
  }

  if ($inv -notmatch "\|\s*Model\s*\|\s*Label\s*\|\s*Comp (\d{2})\s*\|\s*Profile\s*\|\s*Context\s*\|\s*Efforts\s*\|\s*WF\s*\|\s*In USD\s*\|\s*Cache USD\s*\|\s*Out USD\s*\|") {
    throw "Gate 9.4 FAIL: MODEL_INVENTORY.md header is not 'Model | Label | Comp YY | Profile | Context | Efforts | WF | In USD | Cache USD | Out USD | ...'"
  }
  $compYear = [int]$Matches[1]
  $runDate = [datetime]::ParseExact($Date, "yyyy-MM-dd", $null)
  $expectedCompYear = if ($runDate -ge [datetime]::new($runDate.Year, 5, 1)) { $runDate.Year % 100 } else { ($runDate.Year - 1) % 100 }
  if ($compYear -ne $expectedCompYear) {
    throw "Gate 9.4 FAIL: Comp header year $compYear does not match the comparison year $expectedCompYear for $Date (wraps May 1)"
  }

  $sec31 = ($inv -split "### 3\.1 API Models")[1] -split "### 3\.2|## 4\." | Select-Object -First 1
  $rows = $sec31 -split "`r?`n" | Where-Object { $_ -cmatch "^\| [a-z0-9]" }
  $mismatches = @()
  $prevKey = $null
  foreach ($row in $rows) {
    $cols = ($row -split "\|") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    $mid = $cols[0]
    $lbl = $cols[1]
    $comp = $cols[2]
    $prof = $cols[3]
    $inUsd = $cols[7]
    $cacheUsd = $cols[8]
    $outUsd = $cols[9]

    $regEntry = $r.models | Where-Object { $_.model_id -eq $mid } | Select-Object -First 1
    if (-not $regEntry) {
      $regEntry = $r.models | Where-Object { $_.model_id.StartsWith("$mid-") } | Select-Object -First 1
    }
    if (-not $regEntry) {
      $mismatches += "Missing in registry: $mid"
    } else {
      if ($regEntry.capability_label -ne $lbl -or $regEntry.behavior_profile -ne $prof) {
        $mismatches += "Mismatch on ${mid}: inv=($lbl,$prof) vs reg=($($regEntry.capability_label),$($regEntry.behavior_profile))"
      }
      if ($regEntry.release_date -and $regEntry.eci_band) {
        $yy = [int]$regEntry.release_date.Substring(2, 2)
        $band = [int]$regEntry.eci_band.Substring(1)
        $idx = [int][math]::Floor((170 + 15 * ($yy - 26) - $band) / 5)
        if ($idx -lt 0) { $idx = 0 }
        $expLbl = "{0:D2}-{1}" -f $yy, [char][int](65 + $idx)
        $cidx = [int][math]::Floor((170 + 15 * ($compYear - 26) - $band) / 5)
        if ($cidx -lt 0) { $cidx = 0 }
        $expComp = "{0:D2}-{1}" -f $compYear, [char][int](65 + $cidx)
        if ($expLbl -ne $lbl -or $expComp -ne $comp) {
          $mismatches += "Derivation mismatch on ${mid}: inv=($lbl,$comp) vs release_date+eci_band=($expLbl,$expComp)"
        }
      } else {
        $mismatches += "Registry entry ${mid} lacks release_date or eci_band"
      }
      $prov = $regEntry.provider
      $pMap = $p.pricing.$prov
      $pEntry = $pMap.($regEntry.model_id)
      if (-not $pEntry) { $pEntry = $pMap.$mid }
      if (-not $pEntry) {
        $mismatches += "Missing in model-pricing.json: $prov/$mid"
      } else {
        $expCache = if ($null -ne $pEntry.cached_per_1m) { [double]$pEntry.cached_per_1m } else { $null }
        $actCache = if ($cacheUsd -ne "-") { [double]$cacheUsd } else { $null }
        if ([double]$inUsd -ne [double]$pEntry.input_per_1m -or [double]$outUsd -ne [double]$pEntry.output_per_1m -or $actCache -ne $expCache) {
          $mismatches += "Price mismatch on ${mid}: inv=($inUsd/$cacheUsd/$outUsd) vs pricing=($($pEntry.input_per_1m)/$($pEntry.cached_per_1m)/$($pEntry.output_per_1m))"
        }
      }
    }

    $parts = $lbl -split "-"
    $curKey = [pscustomobject]@{
      Model = $mid; CompRank = [int][char](($comp -split "-")[1]); YearRank = -[int]$parts[0]; LetterRank = [int][char]$parts[1]
      NameKey = $mid.ToLowerInvariant()
    }
    if ($prevKey) {
      $outOfOrder = $false
      if ($curKey.CompRank -lt $prevKey.CompRank) { $outOfOrder = $true }
      elseif ($curKey.CompRank -eq $prevKey.CompRank) {
        if ($curKey.YearRank -lt $prevKey.YearRank) { $outOfOrder = $true }
        elseif ($curKey.YearRank -eq $prevKey.YearRank) {
          if ($curKey.LetterRank -lt $prevKey.LetterRank) { $outOfOrder = $true }
          elseif ($curKey.LetterRank -eq $prevKey.LetterRank -and [string]::CompareOrdinal($curKey.NameKey, $prevKey.NameKey) -lt 0) { $outOfOrder = $true }
        }
      }
      if ($outOfOrder) {
        $mismatches += "Sort order violation (1. Comp, 2. Label year desc, 3. Model asc): '$($prevKey.Model)' before '$($curKey.Model)'"
      }
    }
    $prevKey = $curKey
  }
  if ($mismatches.Count -gt 0) { throw "Gate 9.4 FAIL: $($mismatches -join '; ')" }
  Write-Output "Gate 9.4: PASS (verified $($rows.Count) Section 3.1 rows, Label/Comp derivation for comparison year $compYear, In/Cache/Out USD prices, sort order, and source versions/dates)"
}

function Invoke-Distribute {
  $jsonFiles = @("model-pricing.json", "model-registry.json", "model-parameter-mapping.json")
  $agentEvalDst = "$AgentFolder\skills\llm-evaluation"
  foreach ($f in $jsonFiles) {
    Copy-Item "$SkillFolder\$f" "$agentEvalDst\$f" -Force
  }
  if (Test-Path "$SkillFolder\test-call-llm.py") {
    Copy-Item "$SkillFolder\test-call-llm.py" "$agentEvalDst\test-call-llm.py" -Force
  }
  Copy-Item $InventoryFile "$AgentFolder\skills\write-documents\MODEL_INVENTORY.md" -Force

  $dependentSkills = @(
    "$AgentFolder\skills\llm-transcription",
    "$PromptSystemFolder\skills\llm-transcription"
  )
  foreach ($dst in $dependentSkills) {
    foreach ($f in $jsonFiles) {
      if (Test-Path "$dst\$f") {
        Copy-Item "$SkillFolder\$f" "$dst\$f" -Force
      }
    }
  }

  $externalTargets = @("e:\Dev\Lana-V1\config", "e:\Dev\Lana-V2\config")
  if ($IncludeExternal) {
    foreach ($dst in $externalTargets) {
      foreach ($f in $jsonFiles) {
        if (Test-Path "$dst\$f") {
          Copy-Item "$SkillFolder\$f" "$dst\$f" -Force
        }
      }
    }
  }

  Invoke-Gate9
}

function Invoke-Gate9 {
  $jsonFiles = @("model-pricing.json", "model-registry.json", "model-parameter-mapping.json")
  $targets = @(
    "$AgentFolder\skills\llm-evaluation",
    "$AgentFolder\skills\llm-transcription",
    "$PromptSystemFolder\skills\llm-transcription"
  )
  if ($IncludeExternal) {
    $targets += @("e:\Dev\Lana-V1\config", "e:\Dev\Lana-V2\config")
  }
  $matchCount = 0
  foreach ($dst in $targets) {
    foreach ($f in $jsonFiles) {
      if (Test-Path "$dst\$f") {
        if ((Get-FileHash "$SkillFolder\$f").Hash -ne (Get-FileHash "$dst\$f").Hash) {
          throw "Gate 9 FAIL: SHA-256 mismatch at $dst\$f"
        }
        $matchCount++
      }
    }
  }
  if ((Get-FileHash $InventoryFile).Hash -ne (Get-FileHash "$AgentFolder\skills\write-documents\MODEL_INVENTORY.md").Hash) {
    throw "Gate 9 FAIL: SHA-256 mismatch on MODEL_INVENTORY.md"
  }
  $matchCount++
  Write-Output "Gate 9: PASS ($matchCount/$matchCount SHA-256 hashes verified identical)"
}

switch ($Mode) {
  "Gate1"      { Invoke-Gate1 }
  "Gate2"      { Invoke-Gate2 }
  "Gate567"    { Invoke-Gate567 }
  "Gate94"     { Invoke-Gate94 }
  "Distribute" { Invoke-Distribute }
  "VerifyAll"  {
    Invoke-Gate2
    Invoke-Gate567
    Invoke-Gate94
    Invoke-Gate9
    $tmpFiles = Get-ChildItem "$RunFolder\_agent_work\.tmp_*" -ErrorAction SilentlyContinue
    if ($tmpFiles) { throw "VerifyAll FAIL: Leftover .tmp_ files in _agent_work: $($tmpFiles.Name -join ', ')" }
    if (-not (Test-Path "$RunFolder\${Date}_RunReport.md")) { throw "VerifyAll FAIL: Missing ${Date}_RunReport.md" }
    Write-Output "VerifyAll: PASS (All Gates 2, 5, 6, 7, 9, 9.4 + RunReport + 0 temp files verified)"
  }
}

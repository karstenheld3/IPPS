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
  [string]$PromptSystemFolder = "e:\dev\IPPS\PromptSystemV4.7",

  [Parameter(Mandatory = $false)]
  [ValidateSet("FULL", "PRICES", "NEWMODEL", "")]
  [string]$RunMode = "",

  [Parameter(Mandatory = $false)]
  [string]$Providers = "",

  [Parameter(Mandatory = $false)]
  [switch]$IncludeExternal,

  [Parameter(Mandatory = $false)]
  [switch]$AllowSameDateReRun
)

$ErrorActionPreference = "Stop"

$ExternalTargets = @("e:\Dev\Lana-V1\.agent-data\config")

# release_date and the Released column: YYYY-MM-DD, or YYYY-MM when the day is unknown
$ReleaseDatePattern = "^\d{4}-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?$"

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
  $effectiveRunMode = $RunMode
  $changeSetPath = "$RunFolder\${Date}_ChangeSet.json"
  if (-not $effectiveRunMode -and (Test-Path $changeSetPath)) {
    $effectiveRunMode = (Get-Content $changeSetPath -Raw -Encoding UTF8 | ConvertFrom-Json)._run_mode
  }
  if ($effectiveRunMode -eq "NEWMODEL") {
    Write-Output "Gate 2: SKIPPED (run mode NEWMODEL reads provider pages ad hoc; DOM extracts not required)"
    return
  }
  $domFiles = Get-ChildItem "$RunFolder\${Date}_*-DOM.json" -ErrorAction SilentlyContinue
  if (-not $domFiles -or $domFiles.Count -lt 4) {
    throw "Gate 2 FAIL: Expected at least 4 ${Date}_*-DOM.json files in $RunFolder, found $(@($domFiles).Count)"
  }
  foreach ($df in $domFiles) {
    if ($df.Length -lt 50) { throw "Gate 2 FAIL: Empty or truncated DOM file $($df.Name)" }
    $null = Get-Content $df.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  }
  $missingProviders = @()
  foreach ($providerName in ($Providers -split ",")) {
    $providerKey = ($providerName -replace "[^A-Za-z0-9]", "")
    if (-not $providerKey) { continue }
    $providerFiles = Get-ChildItem "$RunFolder\${Date}_${providerKey}-*-DOM.json" -ErrorAction SilentlyContinue
    if (-not $providerFiles) { $missingProviders += $providerName.Trim() }
  }
  if ($missingProviders.Count -gt 0) { throw "Gate 2 FAIL: No ${Date}_[Provider]-*-DOM.json for: $($missingProviders -join ', ')" }
  if ($Providers -match "Devin") {
    $devinDom = Get-Content "$RunFolder\${Date}_Devin-Models-DOM.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    $devinTabs = @($devinDom.tabs.PSObject.Properties)
    if ($devinTabs.Count -ne 3) { throw "Gate 2 FAIL: Devin DOM file has $($devinTabs.Count) tabs, expected 3 (Self-serve, Enterprise (ACUs), Legacy enterprise (credits))" }
    foreach ($tab in $devinTabs) {
      if (@($tab.Value).Count -lt 2) { throw "Gate 2 FAIL: Devin tab '$($tab.Name)' has no data rows" }
    }
  }
  Write-Output "Gate 2: PASS ($($domFiles.Count) valid DOM JSON files verified in $RunFolder, providers checked: $(if ($Providers) { $Providers } else { 'none given' }))"
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

  # Gate 5.2: context_window = total vendor-page window; every checked model must equal its vendor value, every new model must be checked or listed as unverified
  $csCheckPath = "$RunFolder\${Date}_ChangeSet.json"
  if (Test-Path $csCheckPath) {
    $csCheck = Get-Content $csCheckPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $contextMismatches = @()
    $checkedIds = @()
    foreach ($check in @($csCheck.contextChecks)) {
      if ($null -eq $check) { continue }
      $checkedIds += $check.model_id
      $regModel = $r.models | Where-Object { $_.model_id -eq $check.model_id } | Select-Object -First 1
      if (-not $regModel) { $contextMismatches += "$($check.model_id) not in registry"; continue }
      if ([int64]$regModel.context_window -ne [int64]$check.vendor_context_window) {
        $contextMismatches += "$($check.model_id): registry=$($regModel.context_window) vendor=$($check.vendor_context_window) ($($check.source))"
      }
    }
    foreach ($newId in @($csCheck.newRegistryIds)) {
      if ($null -eq $newId) { continue }
      $regModel = $r.models | Where-Object { $_.model_id -eq $newId } | Select-Object -First 1
      if ($regModel -and $null -ne $regModel.context_window -and ($checkedIds -notcontains $newId) -and (@($csCheck.contextUnverified) -notcontains $newId)) {
        $contextMismatches += "$newId has context_window but no entry in contextChecks or contextUnverified"
      }
    }
    if ($contextMismatches.Count -gt 0) { throw "Gate 5.2 FAIL: $($contextMismatches -join '; ')" }
    Write-Output "Gate 5.2: PASS ($($checkedIds.Count) context_window values equal vendor page, $(@($csCheck.contextUnverified).Count) listed unverified)"
  }

  # Gate 6
  $p = Get-Content "$SkillFolder\model-pricing.json" -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($p.last_updated -ne $Date) { throw "Gate 6 FAIL: pricing last_updated ($($p.last_updated)) != $Date" }
  $csPath = "$RunFolder\${Date}_ChangeSet.json"
  if (Test-Path $csPath) {
    $cs = Get-Content $csPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $newIds = @($cs.newPricingIds) + @($cs.changedPricingIds) | Select-Object -Unique
    foreach ($id in $newIds) {
      $found = $false
      foreach ($providerName in $p.pricing.PSObject.Properties.Name) {
        if ($p.pricing.$providerName.$id) { $found = $true }
      }
      if (-not $found) { throw "Gate 6 FAIL: Missing $id in model-pricing.json" }
    }
    Write-Output "Gate 6: PASS (verified $($newIds.Count) new/changed pricing IDs)"
  } else {
    Write-Output "Gate 6: PASS (last_updated=$Date)"
  }

  # Gate 5.3: pricing context_window_k = floor(registry context_window / 1000); null when the registry window is null
  $contextKMismatches = @()
  $contextKChecked = 0
  foreach ($providerName in $p.pricing.PSObject.Properties.Name) {
    foreach ($priceProperty in $p.pricing.$providerName.PSObject.Properties) {
      $regModel = $r.models | Where-Object { $_.model_id -eq $priceProperty.Name } | Select-Object -First 1
      if (-not $regModel) { continue }
      $expectedK = if ($null -eq $regModel.context_window) { $null } else { [int64][math]::Floor([int64]$regModel.context_window / 1000) }
      $actualK = $priceProperty.Value.context_window_k
      $contextKChecked++
      if ($null -eq $expectedK -and $null -eq $actualK) { continue }
      if ($null -eq $expectedK -or $null -eq $actualK -or [int64]$actualK -ne $expectedK) {
        $contextKMismatches += "$($priceProperty.Name): pricing=$actualK expected=$expectedK (registry context_window=$($regModel.context_window))"
      }
    }
  }
  if ($contextKMismatches.Count -gt 0) { throw "Gate 5.3 FAIL: $($contextKMismatches -join '; ')" }
  Write-Output "Gate 5.3: PASS ($contextKChecked pricing entries: context_window_k = floor(registry context_window / 1000))"

  # Gate 5.4: every registry release_date is YYYY-MM-DD or YYYY-MM, release_date_assumed no longer exists, and every released[] value of the run's DOM files agrees with the registry
  $releaseProblems = @()
  foreach ($regModel in $r.models) {
    if ($regModel.PSObject.Properties.Name -contains "release_date_assumed") { $releaseProblems += "$($regModel.model_id): release_date_assumed is retired (day unknown = YYYY-MM)" }
    if (-not $regModel.release_date) { $releaseProblems += "$($regModel.model_id): release_date missing"; continue }
    if ([string]$regModel.release_date -notmatch $ReleaseDatePattern) { $releaseProblems += "$($regModel.model_id): release_date '$($regModel.release_date)' is neither YYYY-MM-DD nor YYYY-MM" }
  }
  $domReleaseChecked = 0
  if (Test-Path $RunFolder) {
    foreach ($domFile in @(Get-ChildItem -LiteralPath $RunFolder -Filter "${Date}_*-DOM.json")) {
      $domDoc = Get-Content $domFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
      foreach ($domRelease in @($domDoc.released)) {
        if ($null -eq $domRelease -or -not $domRelease.released) { continue }
        $domValue = [string]$domRelease.released
        if ($domValue -notmatch $ReleaseDatePattern) {
          $releaseProblems += "$($domFile.Name) $($domRelease.model_id): released '$domValue' is neither YYYY-MM-DD nor YYYY-MM"
          continue
        }
        $datedIdPattern = "^$([regex]::Escape($domRelease.model_id))-\d{8}$"
        $regModel = $r.models | Where-Object { $_.model_id -eq $domRelease.model_id -or $_.model_id -match $datedIdPattern } | Select-Object -First 1
        if (-not $regModel) { continue }
        $domReleaseChecked++
        $registryValue = [string]$regModel.release_date
        $sameValue = ($registryValue -ceq $domValue)
        $registryMoreExact = ($domValue.Length -eq 7 -and $registryValue.Length -eq 10 -and $registryValue.StartsWith($domValue))
        if (-not ($sameValue -or $registryMoreExact)) { $releaseProblems += "$($regModel.model_id): registry release_date $registryValue != $($domFile.Name) released $domValue" }
      }
    }
  }
  if ($releaseProblems.Count -gt 0) { throw "Gate 5.4 FAIL: $($releaseProblems -join '; ')" }
  Write-Output "Gate 5.4: PASS ($(@($r.models).Count) registry release_date values are YYYY-MM-DD or YYYY-MM, $domReleaseChecked DOM released values agree with the registry)"

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

  if ($inv -notmatch "\|\s*Model\s*\|\s*Generation\s*\|\s*ECI Score\s*\|\s*Items\s*\|\s*Context\s*\|\s*Efforts\s*\|\s*In USD\s*\|\s*Cache USD\s*\|\s*Out USD\s*\|\s*Value\s*\|\s*Released\s*\|\s*Notes\s*\|") {
    throw "Gate 9.4 FAIL: MODEL_INVENTORY.md header is not 'Model | Generation | ECI Score | Items | Context | Efforts | In USD | Cache USD | Out USD | Value | Released | Notes'"
  }

  # Registry: every non-retired text model has generation; every higher_than item has all five fields (FR-10, IG-03)
  $knownNonText = @("computer-use-preview", "gpt-image-1.5")
  $mismatches = @()
  $textModels = @($r.models | Where-Object { ($knownNonText -notcontains $_.model_id) -and ($_.status -ne "retired") })
  $maxGeneration = 0
  foreach ($model in $textModels) {
    if ($null -eq $model.generation) { $mismatches += "No generation: $($model.model_id)"; continue }
    if ([int]$model.generation -gt $maxGeneration) { $maxGeneration = [int]$model.generation }
    foreach ($item in @($model.higher_than)) {
      if ($null -eq $item) { continue }
      foreach ($field in @("model", "kind", "source", "accessed", "statement")) {
        if (-not $item.$field) { $mismatches += "higher_than on $($model.model_id) > $($item.model) lacks '$field'" }
      }
      if (@("E1", "E4") -notcontains $item.kind) { $mismatches += "higher_than on $($model.model_id) has kind '$($item.kind)' (E1 or E4 only)" }
    }
  }

  # Registry: no generation differs from git HEAD except generation_estimated -> measured (IG-01)
  $previousOutputEncoding = [Console]::OutputEncoding
  [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
  $headText = (& git -C $SkillFolder show "HEAD:./model-registry.json" 2>$null) -join "`n"
  $gitExit = $LASTEXITCODE
  [Console]::OutputEncoding = $previousOutputEncoding
  $comparedCount = 0
  if ($gitExit -eq 0 -and $headText) {
    $head = $headText | ConvertFrom-Json
    foreach ($headModel in $head.models) {
      if ($null -eq $headModel.generation) { continue }
      $current = $r.models | Where-Object { $_.model_id -eq $headModel.model_id } | Select-Object -First 1
      if (-not $current) { $mismatches += "Model removed since HEAD: $($headModel.model_id)"; continue }
      $comparedCount++
      if ([int]$current.generation -ne [int]$headModel.generation) {
        $wasEstimate = [bool]$headModel.generation_estimated
        $nowMeasured = -not [bool]$current.generation_estimated
        if (-not ($wasEstimate -and $nowMeasured)) { $mismatches += ("Generation changed since HEAD on {0}: G{1:D2} -> G{2:D2}" -f $headModel.model_id, [int]$headModel.generation, [int]$current.generation) }
      }
    }
  } else {
    Write-Warning "Gate 9.4: git HEAD registry not readable from $SkillFolder; generation stability not compared"
  }

  if ($inv -notmatch "Top rung: G(\d+) \(\d{4}-\d{2}-\d{2}\)") { throw "Gate 9.4 FAIL: 'Top rung: G[nn] (YYYY-MM-DD)' line missing in MODEL_INVENTORY.md" }
  if ([int]$Matches[1] -ne $maxGeneration) { $mismatches += ("Top rung G{0} != maximum registry generation G{1:D2}" -f $Matches[1], $maxGeneration) }

  $sec31 = ($inv -split "### 3\.1 API Models")[1] -split "### 3\.2|## 4\." | Select-Object -First 1
  $rows = $sec31 -split "`r?`n" | Where-Object { $_ -cmatch "^\| [a-z0-9]" }
  if (@($rows).Count -ne $textModels.Count) { $mismatches += "Section 3.1 has $(@($rows).Count) rows, registry has $($textModels.Count) non-retired text models" }
  $prevKey = $null
  $valueRows = @()
  foreach ($row in $rows) {
    $cols = ($row -split "\|") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    $mid = $cols[0]
    $generationCell = $cols[1]
    $eciCell = $cols[2]
    $itemsCell = $cols[3]
    $inUsd = $cols[6]
    $cacheUsd = $cols[7]
    $outUsd = $cols[8]
    $valueCell = $cols[9]
    $releasedCell = $cols[10]
    $cost = $null
    $parsedIn = 0.0
    $parsedOut = 0.0
    $invariant = [System.Globalization.CultureInfo]::InvariantCulture
    if ([double]::TryParse($inUsd, [System.Globalization.NumberStyles]::Float, $invariant, [ref]$parsedIn) -and [double]::TryParse($outUsd, [System.Globalization.NumberStyles]::Float, $invariant, [ref]$parsedOut)) {
      $cost = [math]::Max(0.8 * $parsedIn + 0.2 * $parsedOut, 0.01)
    }
    $valueRows += [pscustomobject]@{ Model = $mid; Generation = [int]($generationCell.TrimStart("G").TrimEnd("*")); Cost = $cost; Value = $valueCell; In = $inUsd; Cache = $cacheUsd; Out = $outUsd }

    $regEntry = $r.models | Where-Object { $_.model_id -eq $mid } | Select-Object -First 1
    if (-not $regEntry) {
      $regEntry = $r.models | Where-Object { $_.model_id -match "^$([regex]::Escape($mid))-\d{8}$" } | Select-Object -First 1
    }
    if (-not $regEntry) {
      $mismatches += "Missing in registry: $mid"
    } else {
      $expGeneration = ("G{0:D2}" -f [int]$regEntry.generation) + $(if ($regEntry.generation_estimated) { "*" } else { "" })
      $g = [int]$regEntry.generation
      $expItems = if ($regEntry.items) { "$($regEntry.items)m" } elseif ($g -ge 10) { "8" } elseif ($g -ge 7) { "6" } elseif ($g -ge 4) { "5" } else { "4" }
      $eciValue = 0.0
      if ($null -eq $regEntry.eci_score) {
        if ($eciCell -ne "-") { $mismatches += "ECI Score mismatch on ${mid}: inv=$eciCell vs registry=none" }
      } elseif (-not [double]::TryParse($eciCell, [System.Globalization.NumberStyles]::Float, [System.Globalization.CultureInfo]::InvariantCulture, [ref]$eciValue) -or [math]::Abs($eciValue - [double]$regEntry.eci_score) -gt 0.0501) {
        $mismatches += "ECI Score mismatch on ${mid}: inv=$eciCell vs registry=$($regEntry.eci_score)"
      }
      if ($generationCell -ne $expGeneration -or $itemsCell -ne $expItems) {
        $mismatches += "Mismatch on ${mid}: inv=($generationCell,$itemsCell) vs registry=($expGeneration,$expItems)"
      }
      $expReleased = if ($regEntry.release_date) { [string]$regEntry.release_date } else { "-" }
      if ($releasedCell -cne $expReleased) { $mismatches += "Released mismatch on ${mid}: inv=$releasedCell vs registry=$expReleased" }
      if ($releasedCell -ne "-" -and $releasedCell -notmatch $ReleaseDatePattern) { $mismatches += "Released on ${mid} is '$releasedCell', expected YYYY-MM-DD or YYYY-MM" }
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

    $curKey = [pscustomobject]@{ Model = $mid; Generation = [int]($generationCell.TrimStart("G").TrimEnd("*")); NameKey = $mid.ToLowerInvariant() }
    if ($prevKey) {
      $outOfOrder = ($curKey.Generation -gt $prevKey.Generation) -or (($curKey.Generation -eq $prevKey.Generation) -and ([string]::CompareOrdinal($curKey.NameKey, $prevKey.NameKey) -lt 0))
      if ($outOfOrder) { $mismatches += "Sort order violation (1. Generation desc, 2. Model asc): '$($prevKey.Model)' before '$($curKey.Model)'" }
    }
    $prevKey = $curKey
  }
  # Value (DD-20): recompute the score per rung from the displayed prices; the star symbols must follow the displayed number
  $starFull = [string][char]0x2605
  $starHalf = [string][char]0x2BEA
  $starEmpty = [string][char]0x2606
  $costsByGeneration = @{}
  foreach ($valueRow in $valueRows) {
    if ($null -ne $valueRow.Cost) { $costsByGeneration[$valueRow.Generation] = @($costsByGeneration[$valueRow.Generation]) + $valueRow.Cost }
  }
  foreach ($valueRow in $valueRows) {
    $expectedScore = $null
    if ($null -ne $valueRow.Cost) {
      $peerCosts = @($costsByGeneration[$valueRow.Generation])
      $lowCost = ($peerCosts | Measure-Object -Minimum).Minimum
      $highCost = ($peerCosts | Measure-Object -Maximum).Maximum
      if ($peerCosts.Count -ge 2 -and $highCost -gt $lowCost * (1 + 1e-9)) {
        $expectedScore = 1 + 4 * ([math]::Log($highCost) - [math]::Log($valueRow.Cost)) / ([math]::Log($highCost) - [math]::Log($lowCost))
      }
    }
    if ($null -eq $expectedScore) {
      if ($valueRow.Value -ne "-") { $mismatches += "Value on $($valueRow.Model) is '$($valueRow.Value)', expected '-'" }
      continue
    }
    if ($valueRow.Value -notmatch "^(\S{5}) \((\d\.\d)\)$") { $mismatches += "Value on $($valueRow.Model) is '$($valueRow.Value)', expected five star symbols and (n.n)"; continue }
    $shownStars = $Matches[1]
    $shownScore = [double]::Parse($Matches[2], [System.Globalization.CultureInfo]::InvariantCulture)
    if ([math]::Abs($shownScore - $expectedScore) -gt 0.0501) { $mismatches += "Value on $($valueRow.Model): shown $shownScore, recomputed $([math]::Round($expectedScore, 2))"; continue }
    $halfSteps = [int][math]::Floor($shownScore * 2 + 0.5)
    $expectedStars = ($starFull * [math]::Floor($halfSteps / 2)) + $(if ($halfSteps % 2 -eq 1) { $starHalf } else { "" })
    $expectedStars = $expectedStars + ($starEmpty * (5 - $expectedStars.Length))
    if ($shownStars -ne $expectedStars) { $mismatches += "Value stars on $($valueRow.Model) do not match score $shownScore" }
  }

  # Section 3.2 (DD-22): header; every row is absent from Section 3.1 or priced differently
  $sec32Text = [regex]::Match($inv, "### 3\.2 Devin Model Deviations[\s\S]*?(?=\r?\n## 4\.)")
  $sec32Count = 0
  if (-not $sec32Text.Success) {
    $mismatches += "Section 3.2 is not titled 'Devin Model Deviations'"
  } else {
    if ($sec32Text.Value -notmatch "\|\s*Model\s*\|\s*Generation\s*\|\s*Items\s*\|\s*Efforts\s*\|\s*In USD\s*\|\s*Cache USD\s*\|\s*Out USD\s*\|\s*Released\s*\|\s*Notes\s*\|") {
      $mismatches += "Section 3.2 header is not 'Model | Generation | Items | Efforts | In USD | Cache USD | Out USD | Released | Notes'"
    }
    $devinRows = $sec32Text.Value -split "`r?`n" | Where-Object { ($_ -cmatch "^\| [A-Za-z0-9]") -and ($_ -notmatch "^\| Model ") }
    foreach ($devinRow in $devinRows) {
      $sec32Count++
      $devinCols = ($devinRow -split "\|") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
      $devinReleased = $devinCols[7]
      if ($devinReleased -ne "-" -and $devinReleased -notmatch $ReleaseDatePattern) {
        $mismatches += "Section 3.2 Released on $($devinCols[0]) is '$devinReleased', expected YYYY-MM-DD, YYYY-MM, or -"
      }
      $peerRegistry = $r.models | Where-Object { $_.model_id -ceq $devinCols[0] } | Select-Object -First 1
      if ($peerRegistry -and $devinReleased -cne [string]$peerRegistry.release_date) {
        $mismatches += "Section 3.2 Released on $($devinCols[0]) is '$devinReleased', registry release_date is '$($peerRegistry.release_date)'"
      }
      $peerRow = $valueRows | Where-Object { $_.Model -ceq $devinCols[0] } | Select-Object -First 1
      if (-not $peerRow) { continue }
      $allEqual = $true
      $pairs = @(@($devinCols[4], $peerRow.In), @($devinCols[5], $peerRow.Cache), @($devinCols[6], $peerRow.Out))
      foreach ($pair in $pairs) {
        if ($pair[0] -eq "-" -and $pair[1] -eq "-") { continue }
        if ($pair[0] -eq "-" -or $pair[1] -eq "-") { $allEqual = $false; continue }
        $devinPrice = [double]::Parse($pair[0], [System.Globalization.CultureInfo]::InvariantCulture)
        $inventoryPrice = [double]::Parse($pair[1], [System.Globalization.CultureInfo]::InvariantCulture)
        if ([math]::Abs($devinPrice - $inventoryPrice) -gt 0.005 * [math]::Max([math]::Abs($inventoryPrice), 1e-9)) { $allEqual = $false }
      }
      if ($allEqual) { $mismatches += "Section 3.2 row $($devinCols[0]) has the same prices as Section 3.1" }
    }
  }
  if ($mismatches.Count -gt 0) { throw "Gate 9.4 FAIL: $($mismatches -join '; ')" }
  Write-Output "Gate 9.4: PASS ($($textModels.Count) models with generation, $comparedCount compared against git HEAD, Top rung $("G{0:D2}" -f $maxGeneration), $(@($rows).Count) Section 3.1 rows with Generation/Items/prices/Value/Released, $sec32Count Section 3.2 rows, sort order, and source versions/dates)"
}

function Invoke-Distribute {
  # Since 2026-10-29 the three model JSONs and MODEL_INVENTORY.md live only in skills/llm-tools/ (no replicas in other skills).
  $jsonFiles = @("model-pricing.json", "model-registry.json", "model-parameter-mapping.json")
  $agentToolsDst = "$AgentFolder\skills\llm-tools"
  foreach ($f in $jsonFiles) {
    Copy-Item "$SkillFolder\$f" "$agentToolsDst\$f" -Force
  }
  if (Test-Path "$SkillFolder\test-call-llm.py") {
    Copy-Item "$SkillFolder\test-call-llm.py" "$agentToolsDst\test-call-llm.py" -Force
  }
  Copy-Item $InventoryFile "$agentToolsDst\MODEL_INVENTORY.md" -Force

  if ($IncludeExternal) {
    foreach ($dst in $ExternalTargets) {
      if (-not (Test-Path $dst)) { throw "Distribute FAIL: external target folder missing: $dst" }
      foreach ($f in $jsonFiles) {
        Copy-Item "$SkillFolder\$f" "$dst\$f" -Force
      }
    }
  }

  Invoke-Gate9
}

function Invoke-Gate9 {
  $jsonFiles = @("model-pricing.json", "model-registry.json", "model-parameter-mapping.json")
  $targets = @(
    "$AgentFolder\skills\llm-tools"
  )
  if ($IncludeExternal) {
    $targets += $ExternalTargets
  }
  $matchCount = 0
  foreach ($dst in $targets) {
    foreach ($f in $jsonFiles) {
      if (-not (Test-Path "$dst\$f")) { throw "Gate 9 FAIL: missing $dst\$f" }
      if ((Get-FileHash "$SkillFolder\$f").Hash -ne (Get-FileHash "$dst\$f").Hash) {
        throw "Gate 9 FAIL: SHA-256 mismatch at $dst\$f"
      }
      $matchCount++
    }
  }
  if ((Get-FileHash $InventoryFile).Hash -ne (Get-FileHash "$AgentFolder\skills\llm-tools\MODEL_INVENTORY.md").Hash) {
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
    $tmpFiles = Get-ChildItem "$RunFolder\_agentwork\.tmp_*" -ErrorAction SilentlyContinue
    if ($tmpFiles) { throw "VerifyAll FAIL: Leftover .tmp_ files in _agentwork: $($tmpFiles.Name -join ', ')" }
    if (-not (Test-Path "$RunFolder\${Date}_RunReport.md")) { throw "VerifyAll FAIL: Missing ${Date}_RunReport.md" }
    Write-Output "VerifyAll: PASS (All Gates 2, 5, 6, 7, 9, 9.4 + RunReport + 0 temp files verified)"
  }
}

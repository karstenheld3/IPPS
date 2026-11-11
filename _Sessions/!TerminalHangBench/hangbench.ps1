# HANGBENCH harness: runs every case of hang-cases.ps1 under every selected solution with identical conditions.
# Terminal emulation (Cascade terminal tool, TERMROBUSTNESS @I001.012): stdin = open pipe that never receives input,
# stdout/stderr = pipes, command counts as finished only when the process exited AND both streams reached EOF.
# Usage:
#   pwsh -NoProfile -File hangbench.ps1 -Setup                      # download procgov + processkit-py into _download_gitignore
#   pwsh -NoProfile -File hangbench.ps1 -ListSolutions
#   pwsh -NoProfile -File hangbench.ps1 -Solutions raw,killtree -Cases HC-04,HC-11
#   pwsh -NoProfile -File hangbench.ps1 -HookTest                   # Cascade pre_run_command hook candidate against command-line samples
#   pwsh -NoProfile -File hangbench.ps1 -Report -RunId <id>
param(
  [string[]]$Solutions = @(),
  [string[]]$Cases = @(),
  [int]$HangCap = 5,
  [int]$IdleTimeout = 6,
  [int]$WatchdogMargin = 15,
  [string]$RunId = '',
  [switch]$Setup,
  [switch]$ListSolutions,
  [switch]$HookTest,
  [switch]$Report
)

$ErrorActionPreference = 'Stop'
# pwsh -File passes "a,b" as one string; split comma lists
$Solutions = @($Solutions | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
$Cases = @($Cases | ForEach-Object { $_ -split ',' } | Where-Object { $_ })
$benchDir = $PSScriptRoot
$casesScript = Join-Path $benchDir 'hang-cases.ps1'
$wrappersScript = Join-Path $benchDir 'wrappers.ps1'
$downloadDir = Join-Path $benchDir '_download_gitignore'
$resultsDir = Join-Path $benchDir 'results'
$workDir = Join-Path $benchDir '_agentwork\.tmp_runs'
$pwshExe = (Get-Process -Id $PID).Path
$gnuTimeoutExe = 'C:\Program Files\Git\usr\bin\timeout.exe'
$procgovExe = Join-Path $downloadDir 'procgov\procgov.exe'
$processkitExe = Join-Path $downloadDir 'venv\Scripts\processkit.exe'
$runnerScript = [System.IO.Path]::GetFullPath((Join-Path $benchDir '..\..\PromptSystemV4.7\skills\terminal-robustness\run-supervised.ps1'))

# Shipped runner takes a script path; write a one-line case script per run. The runner has no deadline: for Hang cases the harness plays the agent and creates the stop file at -HangCap seconds
function Get-RunnerArgs([string]$CaseId, [string]$Tag, $Cap, [string]$OutBase, [string]$ProcessKit) {
  $caseLine = "& '$pwshExe' $((Get-CaseArgs $CaseId $Tag $false | ForEach-Object { "'$_'" }) -join ' '); exit `$LASTEXITCODE"
  Set-Content -LiteralPath "$OutBase.ps1" -Value $caseLine -Encoding utf8
  return @('-NoProfile', '-NonInteractive', '-File', $runnerScript, '-Script', "$OutBase.ps1", '-Expected', "$Cap", '-ProcessKit', $ProcessKit)
}
foreach ($folder in @($resultsDir, $workDir)) { New-Item -ItemType Directory -Force -Path $folder | Out-Null }

# Case invocation is identical for all solutions (no -NonInteractive) unless the solution itself prescribes the flag (card line)
function Get-CaseArgs([string]$CaseId, [string]$Tag, [bool]$NonInteractive) {
  $retVal = @('-NoProfile')
  if ($NonInteractive) { $retVal += '-NonInteractive' }
  $retVal += @('-File', $casesScript, '-Case', $CaseId, '-RunTag', $Tag)
  return $retVal
}

function Get-WrapperArgs([string]$Mode, $Cap, [string]$OutBase, [string[]]$CaseArgs, [string[]]$Extra = @()) {
  $json = ConvertTo-Json -InputObject (@($pwshExe) + $CaseArgs) -Compress
  $encoded = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($json))
  return @('-NoProfile', '-NonInteractive', '-File', $wrappersScript, '-Mode', $Mode, '-Cap', "$Cap", '-OutBase', $OutBase) + $Extra + @('-CommandB64', $encoded)
}

# Each solution returns @{ Exe; Args } for one case run. Cap = seconds the solution is told to allow
$solutionRegistry = [ordered]@{
  'raw'        = @{ Kind = 'Baseline'; Origin = 'none'; Available = { $true }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-CaseArgs $caseId $tag $false) } } }
  'cardline'   = @{ Kind = 'Pattern'; Origin = 'robustness card tier 1 (tmp script + -NonInteractive + redirect)'; Available = { $true }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-WrapperArgs 'Redirect' $cap $outBase (Get-CaseArgs $caseId $tag $true)) } } }
  'cardtree'   = @{ Kind = 'Pattern'; Origin = 'robustness card tier 2 (CIM Stop-ProcessTree)'; Available = { $true }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-WrapperArgs 'CardTree' $cap $outBase (Get-CaseArgs $caseId $tag $false)) } } }
  'killtree'   = @{ Kind = 'Pattern'; Origin = 'PowerShell 7 built-in Kill($true) + empty stdin'; Available = { $true }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-WrapperArgs 'KillTree' $cap $outBase (Get-CaseArgs $caseId $tag $false)) } } }
  'watchtree'  = @{ Kind = 'Pattern'; Origin = 'in-house reference: KillTree + descendant snapshot + idle timeout'; Available = { $true }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-WrapperArgs 'WatchTree' $cap $outBase (Get-CaseArgs $caseId $tag $false) @('-Idle', "$script:IdleTimeout")) } } }
  'gnutimeout' = @{ Kind = 'Tool'; Origin = 'Git for Windows GNU coreutils timeout.exe (GPL)'; Available = { Test-Path $gnuTimeoutExe }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $gnuTimeoutExe; Args = (@('-k', '2', "$cap", $pwshExe) + (Get-CaseArgs $caseId $tag $false)) } } }
  'procgov'    = @{ Kind = 'Tool'; Origin = 'Process Governor 4.1.26190 (MIT), Job Object'; Available = { Test-Path $procgovExe }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $procgovExe; Args = (@('-t', "${cap}s", '--recursive', '--terminate-job-on-exit', '--', $pwshExe) + (Get-CaseArgs $caseId $tag $false)) } } }
  'processkit' = @{ Kind = 'Tool'; Origin = 'processkit-py 1.5.0 (MIT), Job Object, deadline, stdio inherited'; Available = { Test-Path $processkitExe }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $processkitExe; Args = (@('run', '--timeout', "$cap", '--kill-on-parent-death', '--', $pwshExe) + (Get-CaseArgs $caseId $tag $false)) } } }
  'runner'     = @{ Kind = 'Shipped'; Origin = 'skills/terminal-robustness/run-supervised.ps1 with processkit'; Available = { (Test-Path $runnerScript) -and (Test-Path $processkitExe) }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-RunnerArgs $caseId $tag $cap $outBase $processkitExe) } } }
  'runnerfb'   = @{ Kind = 'Shipped'; Origin = 'run-supervised.ps1 fallback without processkit (Kill true)'; Available = { Test-Path $runnerScript }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $pwshExe; Args = (Get-RunnerArgs $caseId $tag $cap $outBase 'none') } } }
  'pkidle'     = @{ Kind = 'Tool'; Origin = 'processkit-py 1.5.0 (MIT), deadline + idle timeout (output piped and re-emitted)'; Available = { Test-Path $processkitExe }
    Build = { param($caseId, $tag, $cap, $outBase) @{ Exe = $processkitExe; Args = (@('run', '--timeout', "$cap", '--idle-timeout', "$script:IdleTimeout", '--kill-on-parent-death', '--', $pwshExe) + (Get-CaseArgs $caseId $tag $false)) } } }
}

function Get-ProcessSnapshot { Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId, CreationDate, Name, CommandLine }

function Get-DescendantMap([int]$RootId, $Snapshot) {
  $retVal = @{}
  $queue = [System.Collections.Generic.Queue[int]]::new(); $queue.Enqueue($RootId)
  while ($queue.Count -gt 0) {
    $current = $queue.Dequeue()
    foreach ($process in $Snapshot) {
      if ($process.ParentProcessId -eq $current -and $process.ProcessId -ne $RootId -and -not $retVal.ContainsKey($process.ProcessId)) {
        $retVal[$process.ProcessId] = @{ Created = $process.CreationDate; Name = $process.Name }; $queue.Enqueue($process.ProcessId)
      }
    }
  }
  return $retVal
}

# Survivors = processes seen as descendants (same PID + creation time) or carrying the run tag, still alive now
function Get-Survivors([hashtable]$Known, [string]$Tag) {
  $snapshot = Get-ProcessSnapshot
  $retVal = @{}
  foreach ($process in $snapshot) {
    if ($process.ProcessId -eq $PID) { continue }
    $isKnown = $Known.ContainsKey($process.ProcessId) -and $Known[$process.ProcessId].Created -eq $process.CreationDate
    $isTagged = $process.CommandLine -and $process.CommandLine.Contains($Tag) -and $process.Name -ne 'WmiPrvSE.exe'
    if ($isKnown -or $isTagged) { $retVal[$process.ProcessId] = $process.Name }
  }
  return $retVal
}

function Stop-Survivors([hashtable]$Survivors) {
  foreach ($processId in $Survivors.Keys) { try { Stop-Process -Id $processId -Force -ErrorAction Stop } catch {} }
}

# conhost.exe hosts the console of a CreateNoWindow child and exits with its clients; not counted as orphan
function Get-OrphanCount([hashtable]$Survivors) {
  $retVal = 0
  foreach ($name in $Survivors.Values) { if ($name -ne 'conhost.exe') { $retVal++ } }
  return $retVal
}

function Invoke-CaseRun($Solution, [string]$SolutionName, $CaseInfo) {
  $caseId = $CaseInfo.Id
  $tag = "hb$script:RunId$($SolutionName)$($caseId -replace '-', '')"
  $outBase = Join-Path $workDir $tag
  $solutionCap = if ($CaseInfo.Class -eq 'Legit') { [int]$CaseInfo.Cap } else { $HangCap }
  $watchdog = $solutionCap + $WatchdogMargin
  $command = & $Solution.Build $caseId $tag $solutionCap $outBase
  $startInfo = [System.Diagnostics.ProcessStartInfo]::new($command.Exe)
  foreach ($argument in $command.Args) { $startInfo.ArgumentList.Add([string]$argument) }
  $startInfo.UseShellExecute = $false; $startInfo.CreateNoWindow = $true
  $startInfo.RedirectStandardInput = $true; $startInfo.RedirectStandardOutput = $true; $startInfo.RedirectStandardError = $true
  $stdoutFile = "$outBase-harness-out.txt"; $stderrFile = "$outBase-harness-err.txt"
  $stdoutStream = [System.IO.File]::Create($stdoutFile); $stderrStream = [System.IO.File]::Create($stderrFile)
  $clock = [System.Diagnostics.Stopwatch]::StartNew()
  $process = [System.Diagnostics.Process]::Start($startInfo)
  $stdoutTask = $process.StandardOutput.BaseStream.CopyToAsync($stdoutStream)
  $stderrTask = $process.StandardError.BaseStream.CopyToAsync($stderrStream)
  $known = @{}; $exitSec = $null; $eofSec = $null; $watchdogFired = $false; $cancelSent = $false; $stopSent = $false; $lastSnap = -1
  while ($true) {
    $elapsed = $clock.Elapsed.TotalSeconds
    if ($elapsed - $lastSnap -ge 0.3) {
      $lastSnap = $elapsed
      foreach ($entry in (Get-DescendantMap -RootId $process.Id -Snapshot (Get-ProcessSnapshot)).GetEnumerator()) { $known[$entry.Key] = $entry.Value }
    }
    if ($null -eq $exitSec -and $process.HasExited) { $exitSec = [math]::Round($clock.Elapsed.TotalSeconds, 2) }
    if ($null -eq $eofSec -and $stdoutTask.IsCompleted -and $stderrTask.IsCompleted) { $eofSec = [math]::Round($clock.Elapsed.TotalSeconds, 2) }
    if ($null -ne $exitSec -and $null -ne $eofSec) { break }
    if ($CaseInfo.Class -eq 'Cancel' -and -not $cancelSent -and $elapsed -ge 3) { $cancelSent = $true; try { $process.Kill($false) } catch {} }
    if ($Solution.Kind -eq 'Shipped' -and $CaseInfo.Class -eq 'Hang' -and -not $stopSent -and $elapsed -ge $HangCap) { $stopSent = $true; Set-Content -LiteralPath "${outBase}_stop.txt" -Value 'bench hang verdict' }
    if ($cancelSent -and $elapsed -ge 6) { break }
    if ($elapsed -ge $watchdog) { $watchdogFired = $true; break }
    Start-Sleep -Milliseconds 100
  }
  # Shipped runner after a cancel: the harness plays the agent and runs the kill script the cancelled runner left behind
  $killScript = Join-Path $workDir '.tmp_kill.ps1'
  if ($Solution.Kind -eq 'Shipped' -and $CaseInfo.Class -eq 'Cancel' -and (Test-Path -LiteralPath $killScript)) { $null = & $pwshExe -NoProfile -NonInteractive -File $killScript }
  # Grace period, then orphan check (processes left behind by the solution after it reported completion)
  Start-Sleep -Milliseconds 1500
  $survivors = Get-Survivors -Known $known -Tag $tag
  $orphanCount = Get-OrphanCount -Survivors $survivors
  # Harness cleanup: whatever the solution left behind dies now so later runs are not polluted
  if (-not $process.HasExited) { try { $process.Kill($true) } catch {} }
  Stop-Survivors -Survivors $survivors
  Stop-Survivors -Survivors (Get-Survivors -Known $known -Tag $tag)
  try { $process.StandardInput.Close() } catch {}
  $null = [System.Threading.Tasks.Task]::WaitAll(@($stdoutTask, $stderrTask), 3000)
  $stdoutStream.Dispose(); $stderrStream.Dispose()
  $exitCode = if ($process.HasExited) { $process.ExitCode } else { $null }
  $outputText = (Get-Content -Raw -Path $stdoutFile -ErrorAction SilentlyContinue) ?? ''
  if (Test-Path "$outBase-out.txt") { $outputText += (Get-Content -Raw -Path "$outBase-out.txt" -ErrorAction SilentlyContinue) ?? '' }
  if (Test-Path "${outBase}_out.txt") { $outputText += (Get-Content -Raw -Path "${outBase}_out.txt" -ErrorAction SilentlyContinue) ?? '' }
  $hasDone = $outputText -match '(?m)^DONE'
  $doneSec = if ($null -ne $exitSec -and $null -ne $eofSec) { [math]::Max($exitSec, $eofSec) } else { $null }
  $verdict = 'FAIL'
  switch ($CaseInfo.Class) {
    'Hang'   { if (-not $watchdogFired -and $null -ne $doneSec -and $doneSec -le ($HangCap + 5) -and $orphanCount -eq 0) { $verdict = 'PASS' } }
    'Legit'  { if (-not $watchdogFired -and $exitCode -eq 0 -and $hasDone -and $orphanCount -eq 0) { $verdict = 'PASS' } }
    'Cancel' { if ($orphanCount -eq 0) { $verdict = 'PASS' } }
  }
  $note = ''
  $timeoutLine = [regex]::Match($outputText, '(?m)^(TIMEOUT|IDLE|KILLED)[^\r\n]*'); if ($timeoutLine.Success) { $note = $timeoutLine.Value }
  if ($watchdogFired) { $note = "harness watchdog at $watchdog s; $note" }
  $retVal = [pscustomobject]@{
    RunId = $script:RunId; Solution = $SolutionName; Case = $caseId; Class = $CaseInfo.Class; Name = $CaseInfo.Name
    Verdict = $verdict; ExitCode = $exitCode; ExitSec = $exitSec; EofSec = $eofSec; DoneSec = $doneSec; SolutionCap = $solutionCap
    Watchdog = $watchdogFired; SurvivorCount = $orphanCount; Survivors = (($survivors.Values | Where-Object { $_ -ne 'conhost.exe' } | Sort-Object) -join ',')
    StdoutBytes = (Get-Item $stdoutFile).Length; StderrBytes = (Get-Item $stderrFile).Length; Note = $note.Trim()
  }
  return $retVal
}

function Get-CaseCatalog { (& $pwshExe -NoProfile -NonInteractive -File $casesScript -List) | ConvertFrom-Json }

function Invoke-Setup {
  New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null
  $log = Join-Path $downloadDir 'setup-log.txt'
  Set-Content -Path $log -Value "setup $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Encoding utf8
  # Process Governor: latest GitHub release ZIP
  $release = Invoke-RestMethod -Uri 'https://api.github.com/repos/lowleveldesign/process-governor/releases/latest' -TimeoutSec 30
  $asset = $release.assets | Where-Object { $_.name -like '*.zip' } | Select-Object -First 1
  $zipPath = Join-Path $downloadDir $asset.name
  Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath -TimeoutSec 120 -UseBasicParsing
  Expand-Archive -Path $zipPath -DestinationPath (Join-Path $downloadDir 'procgov') -Force
  Add-Content -Path $log -Value "procgov $($release.tag_name) $($asset.name)" -Encoding utf8
  # processkit-py in an isolated venv
  $venvDir = Join-Path $downloadDir 'venv'
  $basePython = (Get-Command python -ErrorAction Stop).Source
  & $basePython -m venv $venvDir >> $log 2>> "$log.err"
  & (Join-Path $venvDir 'Scripts\python.exe') -m pip install --disable-pip-version-check --no-input 'processkit-py==1.5.0' >> $log 2>> "$log.err"
  Add-Content -Path $log -Value "pip exit $LASTEXITCODE" -Encoding utf8
  Get-ChildItem -Path $downloadDir -Recurse -Filter 'procgov*.exe' | ForEach-Object { Add-Content -Path $log -Value "found $($_.FullName)" -Encoding utf8 }
  Write-Output "SETUP LOG $log"
}

function Invoke-HookTest {
  $hookScript = Join-Path $benchDir 'hook-candidate.ps1'
  $samples = @(
    @{ Expect = 'Block'; Source = 'observed sequence prompt 08 screenshot'; Command = 'Select-String -Path "e:\dev\x\file.md" -Pattern "\[\{""type"": ""file_url""" | Select-Object -First 5' }
    @{ Expect = 'Block'; Source = 'observed sequence prompt 08 screenshot'; Command = '$lines = Get-Content x.md; $verdictLines = $lines | Where-Object { $_ -match ''Verdict'' }; Write-Output "Count: $($verdictLines.Count)"' }
    @{ Expect = 'Block'; Source = 'HERAV1HRNS-FL-0001'; Command = 'bun test --timeout 20000 tests/unit/prompt_assemble.test.ts 2>&1' }
    @{ Expect = 'Block'; Source = 'pager rule'; Command = 'git log' }
    @{ Expect = 'Block'; Source = 'GLOB-FL-020'; Command = 'git diff | Select-String -Pattern foo' }
    @{ Expect = 'Block'; Source = 'GROKUPDATE card'; Command = 'pwsh -Command "Get-ChildItem -Recurse"' }
    @{ Expect = 'Block'; Source = 'GLOB-FL-020'; Command = 'python -c "print(f''{x}'')"' }
    @{ Expect = 'Block'; Source = 'stdin rule'; Command = 'Read-Host "Continue"' }
    @{ Expect = 'Block'; Source = 'unbounded child rule'; Command = 'npm run dev' }
    @{ Expect = 'Block'; Source = 'SharePoint-GPT-Middleware-Dev NOTES'; Command = 'curl -s http://localhost:8000/ | python -c "import sys; sys.stdin.read()"' }
    @{ Expect = 'Block'; Source = 'whitelist length'; Command = ('Get-ChildItem -Path "e:\dev\' + ('a' * 200) + '"') }
    @{ Expect = 'Block'; Source = 'REPL rule'; Command = 'python' }
    @{ Expect = 'Block'; Source = 'multi-line'; Command = "Write-Output 1`nWrite-Output 2" }
    @{ Expect = 'Block'; Source = 'follow rule'; Command = 'Get-Content log.txt -Wait' }
    @{ Expect = 'Block'; Source = 'editor rule'; Command = 'git commit' }
    @{ Expect = 'Block'; Source = 'continuation prompt'; Command = 'Write-Output "unterminated' }
    @{ Expect = 'Allow'; Source = 'card tmp-script line'; Command = 'pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_scan.ps1 > _agentwork/.tmp_scan_out.txt 2> _agentwork/.tmp_scan_err.txt' }
    @{ Expect = 'Allow'; Source = 'whitelist'; Command = 'git --no-pager status --short' }
    @{ Expect = 'Allow'; Source = 'whitelist'; Command = 'git --no-pager log -n 5 --oneline' }
    @{ Expect = 'Allow'; Source = 'whitelist'; Command = 'where.exe rg python pwsh' }
    @{ Expect = 'Allow'; Source = 'whitelist'; Command = 'git commit -m "fix: message"' }
    @{ Expect = 'Allow'; Source = 'wrapper line'; Command = 'procgov -t 60s --recursive -- pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_x.ps1' }
    @{ Expect = 'Allow'; Source = 'python script line'; Command = 'python _agentwork/.tmp_check.py > _agentwork/.tmp_check_out.txt 2> _agentwork/.tmp_check_err.txt' }
  )
  $retVal = foreach ($sample in $samples) {
    $payload = @{ agent_action_name = 'pre_run_command'; tool_info = @{ command_line = $sample.Command; cwd = $benchDir } } | ConvertTo-Json -Compress -Depth 4
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new($pwshExe)
    foreach ($argument in @('-NoProfile', '-NonInteractive', '-File', $hookScript)) { $startInfo.ArgumentList.Add($argument) }
    $startInfo.UseShellExecute = $false; $startInfo.RedirectStandardInput = $true; $startInfo.RedirectStandardError = $true; $startInfo.RedirectStandardOutput = $true
    $clock = [System.Diagnostics.Stopwatch]::StartNew()
    $hook = [System.Diagnostics.Process]::Start($startInfo)
    $errTask = $hook.StandardError.ReadToEndAsync(); $outTask = $hook.StandardOutput.ReadToEndAsync()
    $hook.StandardInput.Write($payload); $hook.StandardInput.Close()
    if (-not $hook.WaitForExit(10000)) { $hook.Kill($true); $actual = 'HUNG' } else { $actual = if ($hook.ExitCode -eq 2) { 'Block' } else { 'Allow' } }
    $null = $outTask.Wait(2000); $null = $errTask.Wait(2000)
    [pscustomobject]@{ Verdict = if ($actual -eq $sample.Expect) { 'PASS' } else { 'FAIL' }; Expect = $sample.Expect; Actual = $actual; Ms = $clock.ElapsedMilliseconds; Source = $sample.Source; Command = $sample.Command; Reason = $errTask.Result.Trim() }
  }
  $file = Join-Path $resultsDir "hooktest-$(Get-Date -Format 'yyyyMMddHHmmss').json"
  $retVal | ConvertTo-Json -Depth 3 | Set-Content -Path $file -Encoding utf8
  foreach ($row in $retVal) { Write-Output ("{0} expect={1,-5} actual={2,-5} {3,5}ms {4}" -f $row.Verdict, $row.Expect, $row.Actual, $row.Ms, $row.Source) }
  Write-Output "HOOKTEST $file"
}

function Invoke-Report {
  $file = if ($RunId) { Join-Path $resultsDir "$RunId.jsonl" } else { (Get-ChildItem -Path $resultsDir -Filter '*.jsonl' | Sort-Object LastWriteTime | Select-Object -Last 1).FullName }
  $rows = Get-Content -Path $file -Encoding utf8 | ForEach-Object { $_ | ConvertFrom-Json }
  $solutionNames = @($rows | ForEach-Object { $_.Solution } | Select-Object -Unique)
  $caseIds = @($rows | ForEach-Object { $_.Case } | Select-Object -Unique | Sort-Object)
  $lines = [System.Collections.Generic.List[string]]::new()
  $lines.Add('<PromptSystem MarkdownTablesAllowed=true />'); $lines.Add("# HANGBENCH Results: $([System.IO.Path]::GetFileNameWithoutExtension($file))"); $lines.Add('')
  $lines.Add("Hang cap $HangCap s, idle timeout $IdleTimeout s, watchdog margin $WatchdogMargin s. Cell = verdict, done seconds (exit and pipe EOF), survivors."); $lines.Add('')
  $lines.Add('| Solution | Pass | Hang pass | Legit pass | Cancel pass |'); $lines.Add('|---|---|---|---|---|')
  foreach ($name in $solutionNames) {
    $mine = @($rows | Where-Object { $_.Solution -eq $name })
    $counts = foreach ($class in @('Hang', 'Legit', 'Cancel')) { $classRows = @($mine | Where-Object { $_.Class -eq $class }); "$(@($classRows | Where-Object { $_.Verdict -eq 'PASS' }).Count)/$($classRows.Count)" }
    $lines.Add("| $name | $(@($mine | Where-Object { $_.Verdict -eq 'PASS' }).Count)/$($mine.Count) | $($counts -join ' | ') |")
  }
  $lines.Add(''); $lines.Add("| Case | Class | Name | $($solutionNames -join ' | ') |"); $lines.Add("|---|---|---|$(($solutionNames | ForEach-Object { '---' }) -join '|')|")
  foreach ($caseId in $caseIds) {
    $first = $rows | Where-Object { $_.Case -eq $caseId } | Select-Object -First 1
    $cells = foreach ($name in $solutionNames) {
      $row = $rows | Where-Object { $_.Case -eq $caseId -and $_.Solution -eq $name } | Select-Object -Last 1
      if (-not $row) { '-' } else { $done = if ($null -ne $row.DoneSec) { "$($row.DoneSec)s" } else { 'wd' }; $orphans = if ($row.SurvivorCount -gt 0) { " +$($row.SurvivorCount) orphan" } else { '' }; "$($row.Verdict) $done$orphans" }
    }
    $lines.Add("| $caseId | $($first.Class) | $($first.Name) | $($cells -join ' | ') |")
  }
  $reportFile = [System.IO.Path]::ChangeExtension($file, '.md')
  $lines | Set-Content -Path $reportFile -Encoding utf8
  Write-Output "REPORT $reportFile"
}

if ($Setup) { Invoke-Setup; exit 0 }

if ($ListSolutions) {
  foreach ($name in $solutionRegistry.Keys) {
    $solution = $solutionRegistry[$name]
    Write-Output ("{0,-11} {1,-9} available={2,-5} {3}" -f $name, $solution.Kind, (& $solution.Available), $solution.Origin)
  }
  exit 0
}

if ($HookTest) { Invoke-HookTest; exit 0 }

if ($Report) { Invoke-Report; exit 0 }

if (-not $RunId) { $RunId = Get-Date -Format 'yyyyMMddHHmmss' }
$catalog = Get-CaseCatalog
if ($Cases.Count -gt 0) { $catalog = $catalog | Where-Object { $Cases -contains $_.Id } }
$selected = if ($Solutions.Count -gt 0) { $Solutions } else { @($solutionRegistry.Keys) }
$resultsFile = Join-Path $resultsDir "$RunId.jsonl"
foreach ($solutionName in $selected) {
  $solution = $solutionRegistry[$solutionName]
  if (-not $solution) { Write-Output "SKIP $solutionName (unknown)"; continue }
  if (-not (& $solution.Available)) { Write-Output "SKIP $solutionName (not installed, run -Setup)"; continue }
  foreach ($caseInfo in $catalog) {
    $result = Invoke-CaseRun -Solution $solution -SolutionName $solutionName -CaseInfo $caseInfo
    Add-Content -Path $resultsFile -Value ($result | ConvertTo-Json -Compress) -Encoding utf8
    Write-Output ("{0,-11} {1} {2,-6} {3} exit={4} done={5}s survivors={6} {7}" -f $solutionName, $result.Case, $result.Class, $result.Verdict, $result.ExitCode, $result.DoneSec, $result.SurvivorCount, $result.Note)
  }
}
Write-Output "RESULTS $resultsFile"
Write-Output 'DONE'

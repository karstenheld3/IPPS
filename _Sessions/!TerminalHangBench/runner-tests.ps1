# Runner contract tests for run-supervised.ps1 (AGENTTERMINAL-IP01 TC-01..TC-10). ASCII-only output: one PASS/FAIL line per test.
# Usage: pwsh -NoProfile -NonInteractive -File runner-tests.ps1 [-Runner <path>] [-ProcessKit <path>]
param(
  [string]$Runner = (Join-Path $PSScriptRoot '..\..\PromptSystemV4.7\skills\terminal-robustness\run-supervised.ps1'),
  [string]$ProcessKit = (Join-Path $PSScriptRoot '_download_gitignore\venv\Scripts\processkit.exe')
)
$ErrorActionPreference = 'Stop'
$Runner = (Resolve-Path -LiteralPath $Runner).Path
$pwshExe = (Get-Process -Id $PID).Path
$work = Join-Path $PSScriptRoot '_agentwork\.tmp_runner tests'
if (Test-Path -LiteralPath $work) { Remove-Item -LiteralPath $work -Recurse -Force }
$null = New-Item -ItemType Directory -Path $work
$utf8Strict = [System.Text.UTF8Encoding]::new($false, $true)
$results = @()

function Invoke-Runner([string]$ScriptPath, [int]$Expected, [string]$Supervisor, [int]$Alive = 0) {
  $runnerArgs = @('-NoProfile', '-NonInteractive', '-File', $Runner, '-Script', $ScriptPath, '-Expected', "$Expected")
  if ($Supervisor) { $runnerArgs += @('-ProcessKit', $Supervisor) }
  if ($Alive -gt 0) { $runnerArgs += @('-AliveSeconds', "$Alive") }
  $null = & $pwshExe @runnerArgs
  $retVal = @{ Exit = $LASTEXITCODE; Base = ($ScriptPath -replace '\.(ps1|py)$', '') }
  $retVal.Log = if (Test-Path -LiteralPath "$($retVal.Base)_log.txt") { Get-Content -LiteralPath "$($retVal.Base)_log.txt" -Raw } else { '' }
  return $retVal
}
function Add-Result([string]$Id, [bool]$Pass, [string]$Detail) {
  $script:results += $Pass
  $state = if ($Pass) { 'PASS' } else { 'FAIL' }
  Write-Output ("{0} {1} {2}" -f $state, $Id, ($Detail -replace '[^\x20-\x7E]', '?' -replace '\s+', ' '))
}
function New-TestScript([string]$Name, [string]$Content) {
  $path = Join-Path $work $Name
  [System.IO.File]::WriteAllText($path, $Content, [System.Text.UTF8Encoding]::new($true))
  return $path
}

# TC-01 PowerShell, 3 lines, exit 0 (folder name with space = TC-08)
$run = Invoke-Runner (New-TestScript 'tc01.ps1' "1..3 | ForEach-Object { Write-Output `"line `$_`" }") 30 $ProcessKit
$lines = (Get-Content -LiteralPath "$($run.Base)_out.txt").Count
Add-Result 'TC-01+TC-08' (($run.Exit -eq 0) -and ($run.Log -match 'DONE exit=0') -and ($lines -eq 3)) "exit=$($run.Exit) lines=$lines"

# TC-02 Python output is live before exit
$pyScript = New-TestScript 'tc02.py' "import time`nfor i in range(1, 5):`n    print(f'line {i}')`n    time.sleep(1)`n"
$job = Start-Process -FilePath $pwshExe -ArgumentList @('-NoProfile', '-NonInteractive', '-File', "`"$Runner`"", '-Script', "`"$pyScript`"", '-Expected', '30', '-ProcessKit', "`"$ProcessKit`"") -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 3
$liveBase = $pyScript -replace '\.py$', ''
$liveText = ''
if (Test-Path -LiteralPath "${liveBase}_out.txt") {
  $stream = [System.IO.File]::Open("${liveBase}_out.txt", 'Open', 'Read', 'ReadWrite, Delete')
  $reader = [System.IO.StreamReader]::new($stream); $liveText = $reader.ReadToEnd(); $reader.Dispose()
}
$liveLines = ([regex]::Matches($liveText, 'line \d')).Count
$stillRunning = -not $job.HasExited
$null = $job.WaitForExit(30000)
Add-Result 'TC-02' (($liveLines -ge 1) -and $stillRunning) "lines@3s=$liveLines running=$stillRunning"

# TC-03 missing script -> ERROR, exit 2
$run = Invoke-Runner (Join-Path $work 'missing.ps1') 30 $ProcessKit
Add-Result 'TC-03' (($run.Exit -eq 2) -and ($run.Log -match 'ERROR reason=script-not-found') -and ($run.Log -notmatch 'START')) "exit=$($run.Exit) log=$($run.Log)"

# TC-04 no Python reachable -> ERROR interpreter-not-found (runner copy without .tools, PATH reduced)
$isolated = Join-Path $work 'a\b\c\d'
$null = New-Item -ItemType Directory -Path $isolated -Force
Copy-Item -LiteralPath $Runner -Destination $isolated
$savedPath = $env:PATH
$env:PATH = "$env:SystemRoot\System32;$(Split-Path -Parent $pwshExe)"
$savedRunner = $Runner; $Runner = Join-Path $isolated 'run-supervised.ps1'
$run = Invoke-Runner (New-TestScript 'tc04.py' "print('x')`n") 30 $ProcessKit
$Runner = $savedRunner; $env:PATH = $savedPath
Add-Result 'TC-04' (($run.Exit -eq 2) -and ($run.Log -match 'ERROR reason=interpreter-not-found')) "exit=$($run.Exit) log=$($run.Log)"

# TC-05 non-ASCII output decodes as strict UTF-8 (PowerShell and Python)
foreach ($case in @(@{ Name = 'tc05.ps1'; Body = "Write-Output 'Gr$([char]0xFC)$([char]0xDF)e $([char]0x2013) test'" }, @{ Name = 'tc05.py'; Body = "print('Gr\u00fc\u00dfe \u2013 test')`n" })) {
  $run = Invoke-Runner (New-TestScript $case.Name $case.Body) 30 $ProcessKit
  $decoded = ''; $ok = $true
  try { $decoded = $utf8Strict.GetString([System.IO.File]::ReadAllBytes("$($run.Base)_out.txt")) } catch { $ok = $false }
  $ok = $ok -and $decoded.Contains("Gr$([char]0xFC)$([char]0xDF)e")
  Add-Result "TC-05 $($case.Name)" $ok "exit=$($run.Exit) utf8=$ok"
}

# TC-06 exit code propagation
$run = Invoke-Runner (New-TestScript 'tc06.ps1' "Write-Output 'x'; exit 3") 30 $ProcessKit
Add-Result 'TC-06 ps1' (($run.Exit -eq 3) -and ($run.Log -match 'DONE exit=3')) "exit=$($run.Exit)"
$run = Invoke-Runner (New-TestScript 'tc06.py' "import sys`nsys.exit(3)`n") 30 $ProcessKit
Add-Result 'TC-06 py' (($run.Exit -eq 3) -and ($run.Log -match 'DONE exit=3')) "exit=$($run.Exit)"

# TC-07 stop file -> tree killed, KILLED exit=124 with the reason from the file
$stopScript = New-TestScript 'tc07.ps1' "Start-Sleep -Seconds 120"
$job = Start-Process -FilePath $pwshExe -ArgumentList @('-NoProfile', '-NonInteractive', '-File', "`"$Runner`"", '-Script', "`"$stopScript`"", '-Expected', '5', '-ProcessKit', "`"$ProcessKit`"") -WindowStyle Hidden -PassThru
$null = $job.Handle
Start-Sleep -Seconds 4
$stopBase = $stopScript -replace '\.ps1$', ''
Set-Content -LiteralPath "${stopBase}_stop.txt" -Value 'hang: no progress'
$ended = $job.WaitForExit(20000)
$stopLog = Get-Content -LiteralPath "${stopBase}_log.txt" -Raw
Add-Result 'TC-07' ($ended -and ($job.ExitCode -eq 124) -and ($stopLog -match 'KILLED exit=124 .*reason=hang: no progress')) "ended=$ended exit=$($job.ExitCode)"

# TC-09 no deadline: 7 s of work with expected 2 s finishes; ALIVE lines carry elapsed, cpu, out, err, procs
$run = Invoke-Runner (New-TestScript 'tc09.ps1' "1..7 | ForEach-Object { Start-Sleep -Seconds 1; Write-Output `"line `$_`" }") 2 $ProcessKit 2
$aliveLines = ([regex]::Matches($run.Log, 'ALIVE elapsed=\d+s cpu=[\d.]+s out=\d+ err=\d+ procs=\d+')).Count
Add-Result 'TC-09' (($run.Exit -eq 0) -and ($run.Log -match 'DONE exit=0 .*expected=2s') -and ($aliveLines -ge 2)) "exit=$($run.Exit) alive=$aliveLines"

# TC-10 a script that exits with its own code 124 is DONE, not KILLED
$run = Invoke-Runner (New-TestScript 'tc10.ps1' "exit 124") 30 $ProcessKit
Add-Result 'TC-10' (($run.Exit -eq 124) -and ($run.Log -match 'DONE exit=124') -and ($run.Log -notmatch 'KILLED')) "exit=$($run.Exit)"

# TC-11 kill script: line while running; runner cancelled -> next runner logs LEFTOVER; kill script ends the survivors; file deleted after a normal end
$killScript = Join-Path $work '.tmp_kill.ps1'
$cancelScript = New-TestScript 'tc11.ps1' "& '$pwshExe' -NoProfile -NonInteractive -Command 'Start-Sleep -Seconds 120'"
$job = Start-Process -FilePath $pwshExe -ArgumentList @('-NoProfile', '-NonInteractive', '-File', "`"$Runner`"", '-Script', "`"$cancelScript`"", '-Expected', '5', '-ProcessKit', "`"$ProcessKit`"") -WindowStyle Hidden -PassThru
$null = $job.Handle
Start-Sleep -Seconds 6
$killLine = if (Test-Path -LiteralPath $killScript) { @(Get-Content -LiteralPath $killScript | Where-Object { $_ -match 'script=tc11\.ps1$' })[0] } else { '' }
$treePids = @(); if ($killLine -match '^Get-Process -Id ([\d,]+) ') { $treePids = [int[]]($Matches[1] -split ',') }
$job.Kill(); $null = $job.WaitForExit(5000); Start-Sleep -Seconds 1
$aliveBefore = @(Get-Process -Id $treePids -ErrorAction SilentlyContinue).Count
$run = Invoke-Runner (New-TestScript 'tc11b.ps1' "Write-Output 'x'") 5 $ProcessKit
$leftoverLogged = $run.Log -match 'LEFTOVER script=tc11\.ps1 pids=[\d,]+ kill=\.tmp_kill\.ps1'
if (Test-Path -LiteralPath $killScript) { $null = & $pwshExe -NoProfile -NonInteractive -File $killScript }
Start-Sleep -Seconds 1
$aliveAfter = @(Get-Process -Id $treePids -ErrorAction SilentlyContinue).Count
$run = Invoke-Runner (New-TestScript 'tc11c.ps1' "Write-Output 'x'") 5 $ProcessKit
$fileGone = -not (Test-Path -LiteralPath $killScript)
Add-Result 'TC-11' (($treePids.Count -ge 2) -and ($aliveAfter -eq 0) -and $fileGone -and (($aliveBefore -eq 0) -or $leftoverLogged)) "pids=$($treePids.Count) aliveBefore=$aliveBefore leftover=$leftoverLogged aliveAfter=$aliveAfter fileGone=$fileGone"

# TC-12 -Topic: own kill script per topic in one folder; a runner of another topic still reports the leftover; files deleted when empty
$topicScript = New-TestScript 'tc12.ps1' "Start-Sleep -Seconds 120"
$job = Start-Process -FilePath $pwshExe -ArgumentList @('-NoProfile', '-NonInteractive', '-File', "`"$Runner`"", '-Script', "`"$topicScript`"", '-Expected', '5', '-Topic', 'P01-Demo', '-ProcessKit', "`"$ProcessKit`"") -WindowStyle Hidden -PassThru
$null = $job.Handle
Start-Sleep -Seconds 5
$topicFile = Join-Path $work '.tmp_kill_P01-Demo.ps1'
$topicFileExists = Test-Path -LiteralPath $topicFile
$defaultFileExists = Test-Path -LiteralPath $killScript
$job.Kill(); $null = $job.WaitForExit(5000); Start-Sleep -Seconds 1
$otherArgs = @('-NoProfile', '-NonInteractive', '-File', $Runner, '-Script', (New-TestScript 'tc12b.ps1' "Write-Output 'x'"), '-Expected', '5', '-Topic', 'P02-Other', '-ProcessKit', $ProcessKit)
$null = & $pwshExe @otherArgs
$otherLog = Get-Content -LiteralPath (Join-Path $work 'tc12b_log.txt') -Raw
$leftoverLogged = $otherLog -match 'LEFTOVER script=tc12\.ps1 pids=[\d,]+ kill=\.tmp_kill_P01-Demo\.ps1'
if ($topicFileExists) { $null = & $pwshExe -NoProfile -NonInteractive -File $topicFile }
Start-Sleep -Seconds 1
$null = & $pwshExe @otherArgs
$filesGone = @(Get-ChildItem -LiteralPath $work -Filter '.tmp_kill*.ps1' -File).Count -eq 0
Add-Result 'TC-12' ($topicFileExists -and (-not $defaultFileExists) -and $leftoverLogged -and $filesGone) "topicFile=$topicFileExists defaultFile=$defaultFileExists leftover=$leftoverLogged filesGone=$filesGone"

# Fallback mode (no processkit): WARN line and normal result
$run = Invoke-Runner (New-TestScript 'tcfb.ps1' "Write-Output 'x'") 30 (Join-Path $work 'no-processkit.exe')
Add-Result 'TC-FB' (($run.Exit -eq 0) -and ($run.Log -match 'WARN processkit not found') -and ($run.Log -match 'DONE exit=0')) "exit=$($run.Exit)"

$passed = @($results | Where-Object { $_ }).Count
Write-Output "SUMMARY $passed/$($results.Count) passed"
Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue

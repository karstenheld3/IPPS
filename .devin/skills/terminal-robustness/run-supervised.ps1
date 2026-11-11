# Runs one agent tmp script inside a process-tree container and writes a log the agent reads with read_file.
# No deadline: work that makes progress runs to its end. The runner reports liveness (ALIVE lines); the agent decides whether the script hangs.
# Containment is done by processkit (Windows Job Object); this script only wires it: log, empty stdin, unbuffered output, exit code, stop file.
# Usage: pwsh -NoProfile -NonInteractive -File [AGENT_FOLDER]/skills/terminal-robustness/run-supervised.ps1 -Script _agentwork/.tmp_[purpose].ps1 -Expected 60 -Topic [TOPIC]
# Writes beside the script (live while running): .tmp_[purpose]_log.txt (START, ALIVE every -AliveSeconds, one end line: DONE, KILLED, or ERROR), _out.txt, _err.txt (UTF-8)
# End a hang: create .tmp_[purpose]_stop.txt (first line = reason); the runner kills the whole process tree and writes KILLED
# Kill script: .tmp_kill_[Topic].ps1 beside the script (.tmp_kill.ps1 without -Topic) holds one line per running runner call of that topic (living process IDs of its tree).
# -Topic names the source (prompt file or STRUT topic), so several sequences sharing one _agentwork folder keep separate kill scripts. The runner removes its line at the end and deletes the empty file.
# After a cancelled runner the line stays: `pwsh -NoProfile -File .tmp_kill_[Topic].ps1` ends the leftover processes (agent or human); the next runner start in the folder logs LEFTOVER while they live
# Exit codes: script exit code; 124 = killed on stop file; 2 = runner error before start (ERROR line)
param(
  [Parameter(Mandatory)][string]$Script,
  [int]$Expected = 0,
  [int]$AliveSeconds = 30,
  [string]$Topic = '',
  [string]$ProcessKit = ''
)
$ErrorActionPreference = 'Stop'
$scriptPath = [System.IO.Path]::GetFullPath($Script, (Get-Location).Path)
$base = $scriptPath -replace '\.(ps1|py)$', ''
$logFile = "${base}_log.txt"; $outFile = "${base}_out.txt"; $errFile = "${base}_err.txt"; $inFile = "${base}_in.txt"; $stopFile = "${base}_stop.txt"
$killName = if ($Topic -replace '[^\w-]', '') { ".tmp_kill_$($Topic -replace '[^\w-]', '').ps1" } else { '.tmp_kill.ps1' }
$killFile = Join-Path (Split-Path -Parent $scriptPath) $killName
$killTag = "# runner=$PID script=$(Split-Path -Leaf $scriptPath)"

function Write-Log([string]$Text) { Add-Content -LiteralPath $logFile -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Text" -Encoding utf8 }

# Runner error before the child starts: one ERROR end line, exit 2, so the agent never waits for a log that never comes
function Stop-WithError([string]$Reason) {
  Write-Log "ERROR reason=$Reason script=$(Split-Path -Leaf $scriptPath)"
  Write-Output "ERROR reason=$Reason log=$logFile"
  exit 2
}

foreach ($path in @($logFile, $outFile, $errFile, $stopFile)) { Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue }
if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) { Stop-WithError 'script-not-found' }

# Start-Process joins -ArgumentList without quoting; quote every argument so paths with spaces and quotes survive
function ConvertTo-ArgumentString([string[]]$Arguments) {
  $retVal = @()
  foreach ($argument in $Arguments) { $retVal += '"' + ($argument -replace '(\\*)"', '$1$1\"' -replace '(\\+)$', '$1$1') + '"' }
  return ($retVal -join ' ')
}

# Kill script shared by all runner calls of one topic. Replaces this call's line with $OwnLine (empty = remove); exclusive open = lock between parallel runners.
# $ReportLeftovers: lines of runners that no longer exist are dropped when none of their processes lives, else kept and returned as LEFTOVER messages
function Update-KillScript([string]$Path, [string]$OwnLine, [bool]$ReportLeftovers) {
  for ($attempt = 0; $attempt -lt 50; $attempt++) {
    $stream = $null; $retVal = @(); $kept = @()
    try {
      $stream = [System.IO.File]::Open($Path, 'OpenOrCreate', 'ReadWrite', 'Delete')
      $reader = [System.IO.StreamReader]::new($stream, [System.Text.Encoding]::UTF8, $true, 4096, $true)
      $lines = @($reader.ReadToEnd() -split "`r?`n" | Where-Object { $_.Trim() })
      $reader.Dispose()
      foreach ($line in $lines) {
        if ($line.EndsWith($killTag)) { continue }
        $parts = [regex]::Match($line, "^Get-Process -Id ([\d,]+) .*\[datetime\]'([^']+)'.*# runner=(\d+) script=(.+)$")
        if ($ReportLeftovers -and $parts.Success) {
          $stamp = [datetime]$parts.Groups[2].Value
          $owner = Get-Process -Id ([int]$parts.Groups[3].Value) -ErrorAction SilentlyContinue
          if (-not ($owner -and $owner.StartTime -le $stamp)) {
            $alive = @(Get-Process -Id ([int[]]($parts.Groups[1].Value -split ',')) -ErrorAction SilentlyContinue | Where-Object { $_.StartTime -le $stamp } | ForEach-Object { $_.Id })
            if ($alive.Count -eq 0) { continue }
            $retVal += "LEFTOVER script=$($parts.Groups[4].Value) pids=$($alive -join ',') kill=$(Split-Path -Leaf $Path)"
          }
        }
        $kept += $line
      }
      if ($OwnLine) { $kept += $OwnLine }
      $stream.Position = 0; $stream.SetLength(0)
      if ($kept.Count -gt 0) { $bytes = [System.Text.UTF8Encoding]::new($false).GetBytes(($kept -join "`r`n") + "`r`n"); $stream.Write($bytes, 0, $bytes.Length) }
      else { [System.IO.File]::Delete($Path) }
      $stream.Dispose()
      return $retVal
    } catch { if ($stream) { $stream.Dispose() }; Start-Sleep -Milliseconds 100 }
  }
  return @()
}

# Interpreter: same pwsh as this script; Python from the shared venv, else PATH
$workspaceTools = Join-Path $PSScriptRoot '..\..\..\..\.tools'
$pwshExe = (Get-Process -Id $PID).Path
# Child output is UTF-8 so read_file can decode it: Python via PYTHONIOENCODING, PowerShell via console output encoding
if ($scriptPath -like '*.py') {
  $pythonExe = Join-Path $workspaceTools 'llm-venv\Scripts\python.exe'
  if (-not (Test-Path -LiteralPath $pythonExe)) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) { Stop-WithError 'interpreter-not-found' }
    $pythonExe = $pythonCommand.Source
  }
  $env:PYTHONIOENCODING = 'utf-8'
  $command = @($pythonExe, '-u', $scriptPath)
} else {
  $quotedScript = $scriptPath -replace "'", "''"
  $childCommand = "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(`$false); `$global:LASTEXITCODE = 0; & '$quotedScript'; exit `$LASTEXITCODE"
  $command = @($pwshExe, '-NoProfile', '-NonInteractive', '-Command', $childCommand)
}

# Container: processkit Job Object; fallback Kill($true) with a WARN line (HANGBENCH results: DevinCascade guide)
if (-not $ProcessKit) {
  $candidate = Join-Path $workspaceTools 'llm-venv\Scripts\processkit.exe'
  if (Test-Path -LiteralPath $candidate) { $ProcessKit = $candidate }
  elseif (Get-Command processkit -ErrorAction SilentlyContinue) { $ProcessKit = (Get-Command processkit).Source }
}
$useProcessKit = $ProcessKit -and (Test-Path -LiteralPath $ProcessKit)

Set-Content -LiteralPath $inFile -Value '' -NoNewline
$env:PYTHONUNBUFFERED = '1'
if (-not $useProcessKit) { Write-Log 'WARN processkit not found, fallback Kill($true) misses orphaned grandchildren' }
# Leftover check over every kill script of the folder, so a cancelled command of another topic is reported too
$killFiles = @(Get-ChildItem -LiteralPath (Split-Path -Parent $scriptPath) -Filter '.tmp_kill*.ps1' -File -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName })
foreach ($path in $killFiles) { foreach ($message in @(Update-KillScript $path '' $true)) { Write-Log $message } }
Write-Log "START expected=${Expected}s pid=$PID script=$(Split-Path -Leaf $scriptPath)"

if ($useProcessKit) { $exe = $ProcessKit; $arguments = @('run', '--kill-on-parent-death', '--') + $command }
else { $exe = $command[0]; $arguments = $command[1..($command.Count - 1)] }

# Size of a file another process is writing: the directory entry lags, the open handle does not
function Get-LiveLength([string]$Path) {
  $retVal = 0
  try { $stream = [System.IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite, Delete'); $retVal = $stream.Length; $stream.Dispose() } catch {}
  return $retVal
}

# Liveness of the whole tree: CPU seconds of every process seen as descendant (kept after it or its parent exited, so the sum never drops) and count of living ones
$seen = @{}
function Get-TreeState([int]$RootId) {
  $retVal = @{ Cpu = '?'; Count = '?'; Pids = ''; Stamp = '' }
  try {
    $snapshot = @(Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId, CreationDate, KernelModeTime, UserModeTime -OperationTimeoutSec 10)
    $members = @{ $RootId = $true }
    foreach ($item in $snapshot) { if ($seen.ContainsKey("$($item.ProcessId)|$($item.CreationDate)")) { $members[[int]$item.ProcessId] = $true } }
    do {
      $added = 0
      foreach ($item in $snapshot) {
        if ($members.ContainsKey([int]$item.ParentProcessId) -and -not $members.ContainsKey([int]$item.ProcessId)) { $members[[int]$item.ProcessId] = $true; $added++ }
      }
    } while ($added -gt 0)
    $count = 0; $alivePids = @()
    foreach ($item in $snapshot) {
      if (-not $members.ContainsKey([int]$item.ProcessId)) { continue }
      $seen["$($item.ProcessId)|$($item.CreationDate)"] = ($item.KernelModeTime + $item.UserModeTime) / 1e7; $count++; $alivePids += [int]$item.ProcessId
    }
    $total = 0.0
    foreach ($value in $seen.Values) { $total += $value }
    $retVal = @{ Cpu = [math]::Round($total, 1); Count = $count; Pids = (($alivePids | Sort-Object) -join ','); Stamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss.fff') }
  } catch {}
  return $retVal
}

$clock = [System.Diagnostics.Stopwatch]::StartNew()
$process = Start-Process -FilePath $exe -ArgumentList (ConvertTo-ArgumentString $arguments) -NoNewWindow -PassThru `
  -RedirectStandardInput $inFile -RedirectStandardOutput $outFile -RedirectStandardError $errFile
$null = $process.Handle
# No deadline. The loop ends when the script exits or when the agent creates the stop file after a hang verdict
# Tree scan at 1, 2, 3, 4, 5 s (the tree builds up), then every 5 s; the kill script line is rewritten when the set of living processes changed
$nextAlive = $AliveSeconds; $killReason = ''; $nextScan = 1; $lastPids = ''; $tree = @{ Cpu = '?'; Count = '?' }
while (-not $process.WaitForExit(500)) {
  if (Test-Path -LiteralPath $stopFile) {
    $killReason = ("$(Get-Content -LiteralPath $stopFile -TotalCount 1 -ErrorAction SilentlyContinue)" -replace '[^\w .:-]', '').Trim()
    if (-not $killReason) { $killReason = 'stop-file' }
    break
  }
  if ($clock.Elapsed.TotalSeconds -ge $nextScan) {
    $nextScan += if ($nextScan -lt 5) { 1 } else { 5 }
    $tree = Get-TreeState $process.Id
    if ($tree.Pids -and $tree.Pids -ne $lastPids) {
      $lastPids = $tree.Pids
      $null = Update-KillScript $killFile "Get-Process -Id $($tree.Pids) -ErrorAction SilentlyContinue | Where-Object { `$_.StartTime -le [datetime]'$($tree.Stamp)' } | Stop-Process -Force  $killTag" $false
    }
  }
  if ($clock.Elapsed.TotalSeconds -ge $nextAlive) {
    $nextAlive += $AliveSeconds
    Write-Log "ALIVE elapsed=$([math]::Round($clock.Elapsed.TotalSeconds))s cpu=$($tree.Cpu)s out=$(Get-LiveLength $outFile) err=$(Get-LiveLength $errFile) procs=$($tree.Count)"
  }
}
if ($killReason) { try { $process.Kill($true) } catch {}; $null = $process.WaitForExit(10000); $exitCode = 124 }
else { $exitCode = $process.ExitCode }
$elapsed = [math]::Round($clock.Elapsed.TotalSeconds, 1)
$null = Update-KillScript $killFile '' $false

$status = if ($killReason) { 'KILLED' } else { 'DONE' }
$reasonText = if ($killReason) { " reason=$killReason" } else { '' }
Write-Log "$status exit=$exitCode elapsed=${elapsed}s expected=${Expected}s$reasonText"
Write-Output "$status exit=$exitCode elapsed=${elapsed}s log=$logFile"
foreach ($path in @($inFile, $stopFile)) { Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue }
exit $exitCode

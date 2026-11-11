# In-house solution wrappers for HANGBENCH. Usage: pwsh -NoProfile -File wrappers.ps1 -Mode <Mode> -Cap <sec> -OutBase <path> -CommandB64 <base64 of JSON array [exe, args...]>
# Command is Base64 JSON because pwsh -File would bind dash-arguments of the inner command to this script
# Modes:
#   Redirect  - card tier 1: run command with stdout/stderr redirected to files, no cap
#   CardTree  - card tier 2 verbatim (DevinCascade guide Section 3): Start-Process + WaitForExit + recursive CIM Stop-ProcessTree
#   KillTree  - PowerShell 7 built-in: Start-Process + empty-file stdin + WaitForExit + Process.Kill($true)
#   WatchTree - KillTree + descendant snapshot every 250 ms (kills orphans that lost their parent) + idle timeout on output file growth
param(
  [Parameter(Mandatory)][ValidateSet('Redirect', 'CardTree', 'KillTree', 'WatchTree')][string]$Mode,
  [int]$Cap = 10,
  [int]$Idle = 0,
  [Parameter(Mandatory)][string]$OutBase,
  [Parameter(Mandatory)][string]$CommandB64
)

$ErrorActionPreference = 'Stop'
$Command = @([System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($CommandB64)) | ConvertFrom-Json)
$exe = $Command[0]
$arguments = @(); if ($Command.Count -gt 1) { $arguments = $Command[1..($Command.Count - 1)] }
$outFile = "$OutBase-out.txt"; $errFile = "$OutBase-err.txt"; $inFile = "$OutBase-in.txt"

function Stop-ProcessTree {
  param([int]$ProcessId)
  $children = Get-CimInstance Win32_Process | Where-Object { $_.ParentProcessId -eq $ProcessId }
  foreach ($child in $children) { Stop-ProcessTree -ProcessId $child.ProcessId }
  try { Stop-Process -Id $ProcessId -Force } catch {}
}

function Get-Descendants([int]$RootId) {
  $all = Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId, CreationDate
  $retVal = @{}
  $queue = [System.Collections.Generic.Queue[int]]::new(); $queue.Enqueue($RootId)
  while ($queue.Count -gt 0) {
    $current = $queue.Dequeue()
    foreach ($process in $all) {
      if ($process.ParentProcessId -eq $current -and -not $retVal.ContainsKey($process.ProcessId)) {
        $retVal[$process.ProcessId] = $process.CreationDate; $queue.Enqueue($process.ProcessId)
      }
    }
  }
  return $retVal
}

if ($Mode -eq 'Redirect') {
  & $exe @arguments > $outFile 2> $errFile
  exit $LASTEXITCODE
}

Set-Content -Path $inFile -Value $null -NoNewline
$startParams = @{ FilePath = $exe; ArgumentList = $arguments; PassThru = $true; NoNewWindow = $true; RedirectStandardOutput = $outFile; RedirectStandardError = $errFile }
if ($Mode -ne 'CardTree') { $startParams['RedirectStandardInput'] = $inFile }
$process = Start-Process @startParams
$null = $process.Handle

if ($Mode -eq 'CardTree') {
  if (-not $process.WaitForExit($Cap * 1000)) { Stop-ProcessTree -ProcessId $process.Id; Write-Output "TIMEOUT: exceeded $Cap s cap"; exit 124 }
  exit $process.ExitCode
}

if ($Mode -eq 'KillTree') {
  if (-not $process.WaitForExit($Cap * 1000)) { $process.Kill($true); Write-Output "TIMEOUT: exceeded $Cap s cap"; exit 124 }
  exit $process.ExitCode
}

# WatchTree
$known = @{}
$deadline = (Get-Date).AddSeconds($Cap)
$lastSize = -1; $lastGrowth = Get-Date
$reason = ''
while (-not $process.HasExited) {
  foreach ($entry in (Get-Descendants -RootId $process.Id).GetEnumerator()) { $known[$entry.Key] = $entry.Value }
  $size = 0; foreach ($file in @($outFile, $errFile)) { if (Test-Path $file) { $size += (Get-Item $file).Length } }
  if ($size -ne $lastSize) { $lastSize = $size; $lastGrowth = Get-Date }
  if ((Get-Date) -gt $deadline) { $reason = 'TIMEOUT'; break }
  if ($Idle -gt 0 -and ((Get-Date) - $lastGrowth).TotalSeconds -gt $Idle) { $reason = 'IDLE'; break }
  Start-Sleep -Milliseconds 250
}
if ($reason) { try { $process.Kill($true) } catch {} }
# Kill every descendant seen during the run that is still alive (same PID and same creation time = same process)
$survivors = 0
foreach ($entry in $known.GetEnumerator()) {
  $alive = Get-CimInstance Win32_Process -Filter "ProcessId = $($entry.Key)" -ErrorAction SilentlyContinue
  if ($alive -and $alive.CreationDate -eq $entry.Value) { $survivors++; try { Stop-Process -Id $entry.Key -Force } catch {} }
}
if ($reason -eq 'TIMEOUT') { Write-Output "TIMEOUT: exceeded $Cap s cap (survivors killed: $survivors)"; exit 124 }
if ($reason -eq 'IDLE') { Write-Output "IDLE: no output growth for $Idle s (survivors killed: $survivors)"; exit 123 }
exit $process.ExitCode

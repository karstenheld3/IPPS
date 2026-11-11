# RC-8 live probe: run by the agent through the real Cascade run_command tool (not through the harness).
# Measures whether the terminal tool detects completion of a command that ends in under 1 second.
# Usage: pwsh -NoProfile -NonInteractive -File live-probe.ps1 -Id P1a [-Lines 1] [-Python] [-Pad xxxx]
# Writes results\live-probe.jsonl (one line per run) with own start/end timestamps; the agent adds the tool verdict.
param(
  [Parameter(Mandatory)][string]$Id,
  [int]$Lines = 1,
  [switch]$Python,
  [string]$Pad = ''
)
$ErrorActionPreference = 'Stop'
$startTime = Get-Date
if ($Python) {
  # Same shape as OAIAPI ledger: pwsh script calls python which prints one line and exits
  & 'C:\Python312\python.exe' -c "print('probe python line')"
}
for ($index = 1; $index -le $Lines; $index++) { Write-Output "probe $Id line $index" }
$endTime = Get-Date
$record = [ordered]@{
  Id = $Id; Start = $startTime.ToString('yyyy-MM-dd HH:mm:ss.fff'); End = $endTime.ToString('yyyy-MM-dd HH:mm:ss.fff')
  Ms = [int]($endTime - $startTime).TotalMilliseconds; Lines = $Lines; Python = [bool]$Python; PadLength = $Pad.Length
  StdoutRedirected = [Console]::IsOutputRedirected; ParentId = (Get-CimInstance Win32_Process -Filter "ProcessId = $PID").ParentProcessId
}
Add-Content -Path (Join-Path $PSScriptRoot 'results\live-probe.jsonl') -Value ($record | ConvertTo-Json -Compress) -Encoding utf8
Write-Output 'DONE'

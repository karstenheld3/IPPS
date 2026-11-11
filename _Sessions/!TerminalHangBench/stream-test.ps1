# HC-28 / HC-29 streaming test: can the agent read progress of an UNMODIFIED script while it runs under processkit?
# Each variant: outer pwsh (like the Cascade terminal) runs processkit > out 2> err; processkit runs a wrapper; wrapper logs START/DONE and runs the vanilla script.
# Sampler counts visible lines every second in: wrapper log, inner output file, outer out file.
# Usage: pwsh -NoProfile -NonInteractive -File stream-test.ps1 [-Lines 10] [-SampleSeconds 14] [-Variants A,B]
param([int]$Lines = 10, [int]$SampleSeconds = 14, [string[]]$Variants = @())
$ErrorActionPreference = 'Stop'
$bench = $PSScriptRoot
$work = Join-Path $bench '_agentwork\.tmp_stream'
New-Item -ItemType Directory -Force -Path $work | Out-Null
$processkitExe = Join-Path $bench '_download_gitignore\venv\Scripts\processkit.exe'
$pythonExe = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\.tools\llm-venv\Scripts\python.exe'))
$pwshExe = (Get-Process -Id $PID).Path
$resultFile = Join-Path $bench 'results\streamtest.jsonl'

# Vanilla scripts: one line per second, no flush, no logging (stand-ins for existing user scripts)
$vanillaPy = Join-Path $work 'vanilla.py'
$pyCode = @'
import time
for i in range(1, __LINES__ + 1):
    print(f"line {i}")
    time.sleep(1)
'@
Set-Content -Path $vanillaPy -Encoding utf8 -Value ($pyCode -replace '__LINES__', $Lines)
$vanillaPs = Join-Path $work 'vanilla.ps1'
$psCode = 'for ($i = 1; $i -le __LINES__; $i++) { Write-Output "line $i"; Start-Sleep -Seconds 1 }'
Set-Content -Path $vanillaPs -Encoding utf8 -Value ($psCode -replace '__LINES__', $Lines)

$redirectPy = "& '__PY__' '__VPY__' > '__INNEROUT__' 2> '__INNERERR__'"
$startProcessPy = "`$p = Start-Process -FilePath '__PY__' -ArgumentList '`"__VPY__`"' -RedirectStandardOutput '__INNEROUT__' -RedirectStandardError '__INNERERR__' -NoNewWindow -Wait -PassThru; `$global:LASTEXITCODE = `$p.ExitCode"
$variantRegistry = [ordered]@{
  'A' = @{ Name = 'python, pwsh redirect inside wrapper'; Body = $redirectPy }
  'B' = @{ Name = 'python unbuffered env, pwsh redirect inside wrapper'; Body = "`$env:PYTHONUNBUFFERED = '1'; $redirectPy" }
  'C' = @{ Name = 'python, Start-Process redirect inside wrapper'; Body = $startProcessPy }
  'D' = @{ Name = 'python unbuffered env, Start-Process redirect inside wrapper'; Body = "`$env:PYTHONUNBUFFERED = '1'; $startProcessPy" }
  'E' = @{ Name = 'pwsh script, pwsh redirect inside wrapper'; Body = "& '__PWSH__' -NoProfile -NonInteractive -File '__VPS__' > '__INNEROUT__' 2> '__INNERERR__'" }
  'F' = @{ Name = 'python unbuffered env, output to outer out.txt'; Body = "`$env:PYTHONUNBUFFERED = '1'; & '__PY__' '__VPY__'" }
  'G' = @{ Name = 'python, output to outer out.txt'; Body = "& '__PY__' '__VPY__'" }
  'H' = @{ Name = 'pwsh script, output to outer out.txt'; Body = "& '__PWSH__' -NoProfile -NonInteractive -File '__VPS__'" }
  'I' = @{ Name = 'pwsh script, Start-Process redirect inside wrapper'
    Body = "`$p = Start-Process -FilePath '__PWSH__' -ArgumentList '-NoProfile -NonInteractive -File `"__VPS__`"' -RedirectStandardOutput '__INNEROUT__' -RedirectStandardError '__INNERERR__' -NoNewWindow -Wait -PassThru; `$global:LASTEXITCODE = `$p.ExitCode" }
}

$wrapperTemplate = @'
$log = '__LOG__'
function Write-Log([string]$Text) { Add-Content -Path $log -Value "$(Get-Date -Format 'HH:mm:ss.fff') $Text" }
Write-Log 'START'
__BODY__
Write-Log "DONE exit=$LASTEXITCODE"
'@

# Count matches in a file that another process is writing (shared read)
function Get-MatchCount([string]$Path, [string]$Pattern) {
  if (-not (Test-Path -LiteralPath $Path)) { return -1 }
  try {
    $stream = [System.IO.File]::Open($Path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]'ReadWrite, Delete')
    $reader = [System.IO.StreamReader]::new($stream); $text = $reader.ReadToEnd(); $reader.Dispose()
    return [regex]::Matches($text, $Pattern).Count
  } catch { return -2 }
}

$selected = if ($Variants.Count -gt 0) { $Variants } else { @($variantRegistry.Keys) }
foreach ($variantId in $selected) {
  $variant = $variantRegistry[$variantId]
  $prefix = Join-Path $work "v$variantId"
  $paths = @{ Log = "$prefix-log.txt"; InnerOut = "$prefix-inner-out.txt"; InnerErr = "$prefix-inner-err.txt"; Out = "$prefix-out.txt"; Err = "$prefix-err.txt" }
  foreach ($path in $paths.Values) { Remove-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue }
  $body = $variant.Body -replace '__PY__', $pythonExe -replace '__VPY__', $vanillaPy -replace '__VPS__', $vanillaPs -replace '__PWSH__', $pwshExe
  $body = $body -replace '__INNEROUT__', $paths.InnerOut -replace '__INNERERR__', $paths.InnerErr
  $wrapper = "$prefix-wrapper.ps1"
  Set-Content -Path $wrapper -Encoding utf8 -Value ($wrapperTemplate -replace '__LOG__', $paths.Log -replace '__BODY__', $body)
  # Outer script = what the agent types into the Cascade terminal
  $outer = "$prefix-outer.ps1"
  Set-Content -Path $outer -Encoding utf8 -Value "& '$processkitExe' run --timeout 30 --kill-on-parent-death -- '$pwshExe' -NoProfile -NonInteractive -File '$wrapper' > '$($paths.Out)' 2> '$($paths.Err)'"
  $clock = [System.Diagnostics.Stopwatch]::StartNew()
  $process = Start-Process -FilePath $pwshExe -ArgumentList @('-NoProfile', '-NonInteractive', '-File', "`"$outer`"") -WindowStyle Hidden -PassThru
  $samples = @(); $firstStartSec = $null; $firstInnerSec = $null; $firstOuterSec = $null; $atFive = $null
  for ($second = 1; $second -le $SampleSeconds; $second++) {
    while ($clock.Elapsed.TotalSeconds -lt $second) { Start-Sleep -Milliseconds 50 }
    $logCount = Get-MatchCount $paths.Log 'START|DONE'
    $innerCount = Get-MatchCount $paths.InnerOut 'line \d+'
    $outerCount = Get-MatchCount $paths.Out 'line \d+'
    $samples += "${second}s:$logCount/$innerCount/$outerCount"
    if ($null -eq $firstStartSec -and $logCount -ge 1) { $firstStartSec = $second }
    if ($null -eq $firstInnerSec -and $innerCount -ge 1) { $firstInnerSec = $second }
    if ($null -eq $firstOuterSec -and $outerCount -ge 1) { $firstOuterSec = $second }
    if ($second -eq 5) { $atFive = [math]::Max($innerCount, $outerCount) }
  }
  $null = $process.WaitForExit(20000)
  $doneVisible = (Get-MatchCount $paths.Log 'DONE') -ge 1
  $finalLines = [math]::Max((Get-MatchCount $paths.InnerOut 'line \d+'), (Get-MatchCount $paths.Out 'line \d+'))
  $streams = ($null -ne $atFive -and $atFive -ge 2)
  $record = [ordered]@{
    Variant = $variantId; Name = $variant.Name; StartVisibleSec = $firstStartSec; FirstInnerLineSec = $firstInnerSec; FirstOuterLineSec = $firstOuterSec
    LinesVisibleAt5s = $atFive; Streams = $streams; DoneVisible = $doneVisible; FinalLines = $finalLines; Samples = ($samples -join ' ')
  }
  Add-Content -Path $resultFile -Value ($record | ConvertTo-Json -Compress) -Encoding utf8
  Write-Output ("{0} streams={1,-5} start@{2}s lines@5s={3} done={4} final={5}  {6}" -f $variantId, $streams, $firstStartSec, $atFive, $doneVisible, $finalLines, $variant.Name)
}
Write-Output 'DONE'

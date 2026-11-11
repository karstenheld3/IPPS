# HANGBENCH case library. One case per invocation: pwsh -NoProfile -File hang-cases.ps1 -Case HC-04 -RunTag <tag>
# Every spawned process carries HANGBENCH_RUNTAG=<tag> in its command line (or is a descendant of one that does) so the harness can sweep orphans.
# Every case is self-limited by -SelfLimit seconds as a second safety net behind the harness watchdog.
param(
  [string]$Case = '',
  [string]$RunTag = 'manual',
  [int]$SelfLimit = 60,
  [int]$Depth = 0,
  [switch]$List
)

$ErrorActionPreference = 'Stop'
$tagText = "HANGBENCH_RUNTAG=$RunTag"
$pwshExe = (Get-Process -Id $PID).Path
$tmpDir = Join-Path $PSScriptRoot '_agentwork\.tmp_cases'
$rgExe = Join-Path $env:LOCALAPPDATA 'Programs\Microsoft VS Code\resources\app\node_modules\@vscode\ripgrep\bin\rg.exe'

# Class: Hang = must be stopped by the solution within cap; Legit = must complete with exit 0 (no false kill); Cancel = harness kills only the top process, tree must die
$catalog = @(
  @{ Id = 'HC-01'; Class = 'Legit'; Cap = 10; Name = 'Control: fast exit'; Mechanism = 'none'; Evidence = 'TERMROBUSTNESS @I001.003 C1' }
  @{ Id = 'HC-02'; Class = 'Legit'; Cap = 15; Name = 'Legit 8s with progress every 1s'; Mechanism = 'none (false-kill check)'; Evidence = 'Knowledgebundler PROBLEMS 2026-09-23 slow suite not a hang' }
  @{ Id = 'HC-03'; Class = 'Legit'; Cap = 15; Name = 'Legit 8s silent, output at end'; Mechanism = 'zero-progress long run'; Evidence = 'GLOB-FL-0005 (filter-repo 9 min empty log), TERMROBUSTNESS-IV-15' }
  @{ Id = 'HC-04'; Class = 'Hang'; Name = 'Sleep forever (idle, no CPU)'; Mechanism = 'unbounded wait'; Evidence = 'full test suite hang WRTPRMPT-PR-0005' }
  @{ Id = 'HC-05'; Class = 'Hang'; Name = 'CPU spin forever'; Mechanism = 'infinite loop'; Evidence = 'generic' }
  @{ Id = 'HC-06'; Class = 'Hang'; Name = 'Read-Host'; Mechanism = 'stdin wait (PowerShell host)'; Evidence = 'cards: Read-Host, pause, Get-Credential; downstream workspace deploy script' }
  @{ Id = 'HC-07'; Class = 'Hang'; Name = 'cmd pause'; Mechanism = 'stdin wait (native child)'; Evidence = 'downstream project build scripts contain pause' }
  @{ Id = 'HC-08'; Class = 'Hang'; Name = 'Pager (more reads stdin)'; Mechanism = 'pager waits for input'; Evidence = 'git log/diff/show without --no-pager (all cards)' }
  @{ Id = 'HC-09'; Class = 'Hang'; Name = 'python without script'; Mechanism = 'REPL / script-from-stdin wait'; Evidence = 'cards: node/python without script argument' }
  @{ Id = 'HC-10'; Class = 'Hang'; Name = 'Continuation prompt in pwsh -Command -'; Mechanism = 'incomplete statement waits for more stdin (>>)'; Evidence = 'observed update sequence/GROKUPDATE/ANTAPIUPDATE cards 2026-11-11, screenshot' }
  @{ Id = 'HC-11'; Class = 'Hang'; Name = 'Grandchild inherits pipe, parent exits'; Mechanism = 'tool waits for pipe EOF, not child exit'; Evidence = 'TERMROBUSTNESS @I001.008, @I001.013' }
  @{ Id = 'HC-12'; Class = 'Legit'; Cap = 20; Name = 'stderr flood 1MB unmerged'; Mechanism = 'stderr drain throttle (near-hang at 2.3KB/s)'; Evidence = 'TERMROBUSTNESS @I001.014-015' }
  @{ Id = 'HC-13'; Class = 'Legit'; Cap = 20; Name = 'stderr flood 1MB merged with 2>&1'; Mechanism = 'pwsh merge point: OOM or wrong exit code'; Evidence = 'HERAV1HRNS-FL-0001, TERMROBUSTNESS @I001.016-017' }
  @{ Id = 'HC-14'; Class = 'Legit'; Cap = 20; Name = 'stdout flood 5MB'; Mechanism = 'volume control'; Evidence = 'TERMROBUSTNESS @I001.003 C4' }
  @{ Id = 'HC-15'; Class = 'Hang'; Name = 'HTTP request to server that never answers'; Mechanism = 'network stall without timeout'; Evidence = 'cards: Invoke-WebRequest/curl without timeout; SharePoint curl | python; FOPROCESS hung API call' }
  @{ Id = 'HC-16'; Class = 'Hang'; Name = 'Wait for lock file that never disappears'; Mechanism = 'lock wait'; Evidence = 'Knowledgebundler PR-0004 held processes block spawning; git index.lock' }
  @{ Id = 'HC-17'; Class = 'Hang'; Name = 'Wait-Process without -Timeout'; Mechanism = 'unbounded wait on child'; Evidence = 'cards: Wait-Process without -Timeout' }
  @{ Id = 'HC-18'; Class = 'Hang'; Name = 'Get-Content -Wait'; Mechanism = 'follow mode never ends'; Evidence = 'cards: Get-Content -Wait, tail -f' }
  @{ Id = 'HC-19'; Class = 'Legit'; Cap = 10; Name = 'Detached child with file handles outlives parent'; Mechanism = 'orphan without pipe hold'; Evidence = 'LLM-Research FAILS orphaned terminals; Lana BL-06' }
  @{ Id = 'HC-20'; Class = 'Hang'; Name = 'Deep tree (3 levels) sleeping'; Mechanism = 'flat kill leaves descendants'; Evidence = 'DevinCascade guide 3: Stop-Job does not kill children' }
  @{ Id = 'HC-21'; Class = 'Hang'; Name = 'Grandchild whose parent already exited'; Mechanism = 'parent link broken, tree walk misses it'; Evidence = 'DevinCascade guide 3 gotcha: orphans lose parent PID' }
  @{ Id = 'HC-22'; Class = 'Hang'; Name = 'rg without path reads stdin'; Mechanism = 'tool falls back to stdin'; Evidence = 'cards: rg.exe with Unicode patterns hangs the pipe' }
  @{ Id = 'HC-23'; Class = 'Hang'; Name = 'Native y/n prompt (set /p)'; Mechanism = 'stdin prompt not stopped by -NonInteractive'; Evidence = 'TERMROBUSTNESS @I001.025 npm create Ok to proceed' }
  @{ Id = 'HC-24'; Class = 'Legit'; Cap = 15; Name = 'Select-Object -Last buffers 8s producer'; Mechanism = 'pipeline buffering looks silent'; Evidence = 'downstream card: Select-Object buffers indefinitely; Knowledgebundler NOTES' }
  @{ Id = 'HC-25'; Class = 'Hang'; Name = 'GUI program waits (editor)'; Mechanism = 'GUI child never exits'; Evidence = 'Lana card: Start-Process of an editor; git commit without -m' }
  @{ Id = 'HC-26'; Class = 'Hang'; Name = 'Read stdin to EOF'; Mechanism = 'consumer waits for EOF on open stdin'; Evidence = 'SharePoint-GPT-Middleware-Dev NOTES curl | python sys.stdin.read()' }
  @{ Id = 'HC-27'; Class = 'Cancel'; Name = 'UI cancel kills only the top process'; Mechanism = 'cancel does not kill tree'; Evidence = 'GLOB-FL-0005, TERMROBUSTNESS-IV-14, Lana BL-02' }
)

if ($List) { $catalog | ForEach-Object { [pscustomobject]$_ } | ConvertTo-Json -Depth 3; exit 0 }

New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null
$startTime = Get-Date

function Wait-SelfLimit {
  while (((Get-Date) - $startTime).TotalSeconds -lt $SelfLimit) { Start-Sleep -Milliseconds 200 }
}

# Child pwsh that sleeps until self-limit; tag in command line; inherits std handles (pipes) of this process
function Start-SleeperInherit([int]$Seconds) {
  $code = "Start-Sleep -Seconds $Seconds # $tagText"
  Start-Process -FilePath $pwshExe -ArgumentList '-NoProfile', '-NonInteractive', '-Command', $code -NoNewWindow -PassThru
}

# Child pwsh that sleeps; std handles go to files, so no pipe is held
function Start-SleeperFiles([int]$Seconds, [string]$Name) {
  $code = "Start-Sleep -Seconds $Seconds # $tagText"
  $out = Join-Path $tmpDir "$RunTag-$Name-out.txt"
  $err = Join-Path $tmpDir "$RunTag-$Name-err.txt"
  Start-Process -FilePath $pwshExe -ArgumentList '-NoProfile', '-NonInteractive', '-Command', $code -PassThru -WindowStyle Hidden -RedirectStandardOutput $out -RedirectStandardError $err
}

$pythonExe = 'C:\Python312\python.exe'
Write-Output "START $Case $tagText"

switch ($Case) {
  'HC-01' { Write-Output 'hello'; Write-Output 'DONE'; exit 0 }
  'HC-02' { for ($index = 1; $index -le 8; $index++) { Start-Sleep -Seconds 1; Write-Output "progress $index/8" }; Write-Output 'DONE'; exit 0 }
  'HC-03' { Start-Sleep -Seconds 8; Write-Output 'DONE'; exit 0 }
  'HC-04' { Wait-SelfLimit; exit 3 }
  'HC-05' { $counter = 0; while (((Get-Date) - $startTime).TotalSeconds -lt $SelfLimit) { $counter++ }; exit 3 }
  'HC-06' { $answer = Read-Host 'Continue? (y/n)'; Write-Output "got $answer"; exit 3 }
  'HC-07' { & cmd.exe /c "pause & rem $tagText"; exit 3 }
  'HC-08' { & cmd.exe /c "more & rem $tagText"; exit 3 }
  'HC-09' { & $pythonExe -X "HANGBENCH_RUNTAG=$RunTag"; exit 3 }
  'HC-10' {
    # Feed an unterminated string to a pwsh that reads commands from stdin; keep stdin open (like a terminal)
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new($pwshExe)
    foreach ($argument in @('-NoProfile', '-Command', '-')) { $startInfo.ArgumentList.Add($argument) }
    $startInfo.UseShellExecute = $false; $startInfo.RedirectStandardInput = $true
    $child = [System.Diagnostics.Process]::Start($startInfo)
    $child.StandardInput.WriteLine("Write-Output `"unterminated string # $tagText")
    $child.StandardInput.Flush()
    if (-not $child.WaitForExit($SelfLimit * 1000)) { $child.Kill($true); exit 3 }
    exit $child.ExitCode
  }
  'HC-11' { $null = Start-SleeperInherit -Seconds $SelfLimit; Write-Output 'parent done, grandchild holds pipes'; exit 0 }
  'HC-12' {
    $chunk = 'E' * 1023
    for ($index = 0; $index -lt 1024; $index++) { [Console]::Error.WriteLine($chunk) }
    Write-Output 'DONE'; exit 0
  }
  'HC-13' {
    $code = "`$chunk = 'E' * 1023; for (`$i = 0; `$i -lt 1024; `$i++) { [Console]::Error.WriteLine(`$chunk) } # $tagText"
    & $pwshExe -NoProfile -NonInteractive -Command $code 2>&1 | ForEach-Object { $_ }
    Write-Output "DONE childexit=$LASTEXITCODE"; exit $LASTEXITCODE
  }
  'HC-14' {
    $chunk = 'O' * 1023
    for ($index = 0; $index -lt 5120; $index++) { [Console]::Out.WriteLine($chunk) }
    Write-Output 'DONE'; exit 0
  }
  'HC-15' {
    # Listener accepts TCP in the kernel backlog but never answers HTTP; client has no timeout (TimeoutSec 0 = infinite)
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
    $listener.Start()
    $port = $listener.LocalEndpoint.Port
    Invoke-WebRequest -Uri "http://127.0.0.1:$port/" -UseBasicParsing | Out-Null
    exit 3
  }
  'HC-16' {
    $lockFile = Join-Path $tmpDir "$RunTag.lock"
    Set-Content -Path $lockFile -Value 'locked'
    while ((Test-Path $lockFile) -and ((Get-Date) - $startTime).TotalSeconds -lt $SelfLimit) { Start-Sleep -Milliseconds 200 }
    exit 3
  }
  'HC-17' { $child = Start-SleeperFiles -Seconds $SelfLimit -Name 'hc17'; Wait-Process -Id $child.Id; exit 3 }
  'HC-18' {
    $followFile = Join-Path $tmpDir "$RunTag-follow.txt"
    Set-Content -Path $followFile -Value 'line 1'
    Get-Content -Path $followFile -Wait | ForEach-Object { Write-Output $_ }
    exit 3
  }
  'HC-19' { $null = Start-SleeperFiles -Seconds 8 -Name 'hc19'; Write-Output 'DONE parent exits, detached child keeps running'; exit 0 }
  'HC-20' {
    # Three levels: case -> child -> grandchild -> great-grandchild, all sleeping, all tagged
    $level3 = "Start-Sleep -Seconds $SelfLimit # $tagText L3"
    $level2 = "& '$pwshExe' -NoProfile -NonInteractive -Command '$level3' # $tagText L2"
    & $pwshExe -NoProfile -NonInteractive -Command $level2
    exit 3
  }
  'HC-21' {
    # Child starts a file-handle grandchild and exits at once; grandchild loses its parent; case then waits forever
    $inner = "Start-Process -FilePath '$pwshExe' -ArgumentList '-NoProfile','-NonInteractive','-Command','Start-Sleep -Seconds $SelfLimit # $tagText L2' -WindowStyle Hidden -RedirectStandardOutput '$tmpDir\$RunTag-hc21-out.txt' -RedirectStandardError '$tmpDir\$RunTag-hc21-err.txt'"
    & $pwshExe -NoProfile -NonInteractive -Command $inner
    Wait-SelfLimit; exit 3
  }
  'HC-22' { & $rgExe -e "HANGBENCH_RUNTAG=$RunTag"; exit 3 }
  'HC-23' { & cmd.exe /c "set /p answer=Ok to proceed? (y) & rem $tagText"; exit 3 }
  'HC-24' { & { for ($index = 1; $index -le 8; $index++) { Start-Sleep -Seconds 1; "line $index" } } | Select-Object -Last 2; Write-Output 'DONE'; exit 0 }
  'HC-25' { Start-Process -FilePath 'cmd.exe' -ArgumentList '/k', "rem $tagText" -WindowStyle Hidden -Wait; exit 3 }
  'HC-26' { & $pythonExe -X "HANGBENCH_RUNTAG=$RunTag" -c 'import sys; sys.stdin.read()'; exit 3 }
  'HC-27' {
    $level3 = "Start-Sleep -Seconds $SelfLimit # $tagText L3"
    $level2 = "& '$pwshExe' -NoProfile -NonInteractive -Command '$level3' # $tagText L2"
    & $pwshExe -NoProfile -NonInteractive -Command $level2
    exit 3
  }
  default { Write-Output "UNKNOWN CASE $Case"; exit 2 }
}

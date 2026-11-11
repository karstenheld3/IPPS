# Cascade pre_run_command hook candidate. Reads hook JSON from stdin; exit 2 = block (stderr shown to the agent), exit 0 = allow.
# Rules mirror agent-behavior.md "Terminal Hang Prevention" inline whitelist plus banned commands from robustness cards.
# Fail-open by contract: any internal error exits 0 (Cascade runs the command on any exit code other than 2).
$ErrorActionPreference = 'Stop'
try {
  $payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
  $commandLine = [string]$payload.tool_info.command_line
  $trimmed = $commandLine.Trim()
  $advice = 'Write the command into _agentwork/.tmp_[purpose].ps1 and run: pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_[purpose].ps1 > _agentwork/.tmp_[purpose]_out.txt 2> _agentwork/.tmp_[purpose]_err.txt, then read_file both files.'
  $rules = @(
    @{ Test = { $commandLine -match "[\r\n]" }; Reason = 'multi-line command (continuation prompt risk)' }
    @{ Test = { $trimmed.Length -gt 200 }; Reason = "command longer than 200 characters ($($trimmed.Length))" }
    @{ Test = { $commandLine -match '2>&1' }; Reason = '2>&1 stream merge (pwsh merge point, OOM or backpressure hang)' }
    @{ Test = { $commandLine -match '\|' }; Reason = 'pipe in inline command' }
    @{ Test = { $commandLine -match ';' }; Reason = 'multiple statements (;)' }
    @{ Test = { $commandLine -match '[{}]' }; Reason = 'script block or braces in inline command' }
    @{ Test = { $commandLine -match '\$' }; Reason = '$ in inline command (outer shell expansion breaks quoting)' }
    @{ Test = { (($commandLine.ToCharArray() | Where-Object { $_ -eq '"' }).Count % 2) -eq 1 }; Reason = 'unbalanced double quotes (continuation prompt)' }
    @{ Test = { (($commandLine.ToCharArray() | Where-Object { $_ -eq "'" }).Count % 2) -eq 1 }; Reason = 'unbalanced single quotes (continuation prompt)' }
    @{ Test = { $trimmed -match '(?i)^(pwsh|powershell)(\.exe)?\b.*\s-(c|command|encodedcommand|ec)\b' }; Reason = 'pwsh -Command with script text' }
    @{ Test = { $trimmed -match '(?i)^(python[0-9.]*|py|node)(\.exe)?\s+-(c|e)\b' }; Reason = 'inline interpreter code (python -c / node -e)' }
    @{ Test = { $trimmed -match '(?i)^(python[0-9.]*|py|node|pwsh|powershell|cmd|bash)(\.exe)?$' }; Reason = 'interpreter without script (REPL waits on stdin)' }
    @{ Test = { $trimmed -match '(?i)^git\s+(log|diff|show|blame)\b' }; Reason = 'git pager command without --no-pager' }
    @{ Test = { $trimmed -match '(?i)^git\s+commit\b' -and $trimmed -notmatch '\s-(m|F)\b|--message|--file' }; Reason = 'git commit without -m (opens editor)' }
    @{ Test = { $commandLine -match '(?i)\b(Read-Host|pause|Get-Credential)\b' }; Reason = 'stdin wait (Read-Host, pause, Get-Credential)' }
    @{ Test = { $commandLine -match '(?i)Get-Content\b.*\s-Wait\b|\btail\s+-f\b' }; Reason = 'follow mode never ends' }
    @{ Test = { $commandLine -match '(?i)\bnpm\s+(run\s+dev|start)\b|--watch\b' }; Reason = 'unbounded child (dev server, watch mode)' }
  )
  foreach ($rule in $rules) {
    if (& $rule.Test) { [Console]::Error.WriteLine("BLOCKED by hang-prevention hook: $($rule.Reason). $advice"); exit 2 }
  }
  exit 0
} catch {
  exit 0
}

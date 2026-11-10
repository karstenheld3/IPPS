<#
.SYNOPSIS
    Discovers all downstream repos configured to pull from IPPS and runs a batch preview or execution.
.DESCRIPTION
    Scans E:\dev (or a user-supplied search root) for promptsystem-sync.json files whose targets
    reference IPPS. Generates a consolidated summary across all discovered targets without
    requiring manual per-repo invocation.
.PARAMETER Root
    Directory root to search for promptsystem-sync.json files. Default: 'E:\dev'.
.PARAMETER Diff
    Preview mode: runs sync.ps1 -diff for each discovered config. (Default)
.PARAMETER Execute
    Apply mode: runs sync.ps1 -execute for each discovered config.
.PARAMETER FilterRepo
    Optional regex to restrict execution to matching repo names (e.g. 'KarstensWorkspace|Hera').
.PARAMETER OutputFile
    Optional file path to write the markdown summary table.
.EXAMPLE
    summary-sync.ps1 -Diff
.EXAMPLE
    summary-sync.ps1 -Diff -FilterRepo "KarstensWorkspace"
.EXAMPLE
    summary-sync.ps1 -Execute
#>

[CmdletBinding(DefaultParameterSetName = 'DiffSet')]
param(
    [Parameter(ParameterSetName = 'DiffSet')]
    [switch]$Diff,

    [Parameter(ParameterSetName = 'ExecuteSet', Mandatory = $true)]
    [switch]$Execute,

    [string]$Root = 'E:\dev',
    [string]$FilterRepo,
    [string]$OutputFile
)

$ErrorActionPreference = 'Stop'

# Locate sync.ps1 relative to this script
$syncScript = Join-Path $PSScriptRoot 'sync.ps1'
if (-not (Test-Path -LiteralPath $syncScript -PathType Leaf)) {
    throw "sync.ps1 not found beside this script at: '$syncScript'."
}

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
    throw "Search root does not exist: '$Root'."
}

Write-Host "Discovering downstream sync configurations under '$Root'..." -ForegroundColor Cyan
$configs = Get-ChildItem -Path $Root -Filter "promptsystem-sync.json" -Recurse -Depth 2 -ErrorAction SilentlyContinue

$ippsConfigs = @()
foreach ($c in $configs) {
    try {
        $raw = Get-Content -LiteralPath $c.FullName -Raw -Encoding UTF8
        if ($raw -match 'IPPS') {
            if ($FilterRepo -and ($c.DirectoryName -notmatch $FilterRepo)) {
                continue
            }
            $ippsConfigs += $c
        }
    } catch {
        Write-Warning "Failed to read config '$($c.FullName)': $_"
    }
}

if ($ippsConfigs.Count -eq 0) {
    Write-Host "No downstream configs referencing IPPS found." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($ippsConfigs.Count) downstream config(s). Running $(if ($Execute) { 'EXECUTE' } else { 'DIFF' }) mode..." -ForegroundColor Cyan

$rows = @()

foreach ($c in $ippsConfigs) {
    $dir = $c.DirectoryName
    $repoName = Split-Path $dir -Leaf
    Push-Location $dir
    try {
        $output = if ($Execute) {
            & $syncScript -execute -config $c.FullName 2>&1 | Out-String
        } else {
            & $syncScript -diff -config $c.FullName 2>&1 | Out-String
        }
        $summaries = [regex]::Matches($output, "Summary: '([^']+)' - (\d+) add, (\d+) modify, (\d+) locally_modified, (\d+) breaking_change, (\d+) delete, (\d+) skip, (\d+) unchanged\.")
        if ($summaries.Count -gt 0) {
            foreach ($m in $summaries) {
                $rows += [PSCustomObject]@{
                    Repo            = $repoName
                    Target          = $m.Groups[1].Value
                    Add             = [int]$m.Groups[2].Value
                    Modify          = [int]$m.Groups[3].Value
                    LocallyModified = [int]$m.Groups[4].Value
                    BreakingChange  = [int]$m.Groups[5].Value
                    Delete          = [int]$m.Groups[6].Value
                    Skip            = [int]$m.Groups[7].Value
                    Unchanged       = [int]$m.Groups[8].Value
                    Status          = if ($Execute) { 'APPLIED' } elseif ([int]$m.Groups[5].Value -gt 0) { 'BREAKING' } elseif ([int]$m.Groups[4].Value -gt 0) { 'LOCALLY_MODIFIED' } elseif ([int]$m.Groups[2].Value -gt 0 -or [int]$m.Groups[3].Value -gt 0 -or [int]$m.Groups[6].Value -gt 0) { 'CHANGES_PENDING' } else { 'UP_TO_DATE' }
                }
            }
        } else {
            # Capture error if summary regex didn't match
            $rows += [PSCustomObject]@{
                Repo            = $repoName
                Target          = $dir
                Add             = 0
                Modify          = 0
                LocallyModified = 0
                BreakingChange  = 0
                Delete          = 0
                Skip            = 0
                Unchanged       = 0
                Status          = 'FAILED_OR_NO_TARGETS'
            }
        }
    } catch {
        $rows += [PSCustomObject]@{
            Repo            = $repoName
            Target          = $dir
            Add             = 0
            Modify          = 0
            LocallyModified = 0
            BreakingChange  = 0
            Delete          = 0
            Skip            = 0
            Unchanged       = 0
            Status          = "ERROR: $_"
        }
    } finally {
        Pop-Location
    }
}

Write-Host ""
$rows | Format-Table -Property Repo, Target, Add, Modify, LocallyModified, BreakingChange, Delete, Skip, Unchanged, Status -AutoSize

if ($OutputFile) {
    $sb = [System.Text.StringBuilder]::new()
    [void]$sb.AppendLine("# Downstream Sync Summary")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("| Repo | Target | Add | Modify | LocMod | Break | Del | Skip | Same | Status |")
    [void]$sb.AppendLine("|---|---|---|---|---|---|---|---|---|---|")
    foreach ($r in $rows) {
        [void]$sb.AppendLine("| $($r.Repo) | $($r.Target) | $($r.Add) | $($r.Modify) | $($r.LocallyModified) | $($r.BreakingChange) | $($r.Delete) | $($r.Skip) | $($r.Unchanged) | $($r.Status) |")
    }
    $targetFull = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputFile)
    [System.IO.File]::WriteAllText($targetFull, $sb.ToString(), (New-Object System.Text.UTF8Encoding $false))
    Write-Host "Summary written to: '$targetFull'" -ForegroundColor Green
}

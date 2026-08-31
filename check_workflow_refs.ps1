# Check for references to non-existing workflows across DevSystem
# Usage: .\check_workflow_refs.ps1 [-DevSystemFolder <path>]
param(
    [string]$DevSystemFolder = (Join-Path $PSScriptRoot (Get-Content (Join-Path $PSScriptRoot "NOTES.md") | Where-Object { $_ -match 'Current \[DEVSYSTEM\]: (\S+)' } | ForEach-Object { $Matches[1] }))
)

$workspace = $PSScriptRoot
$workflowDir = Join-Path $DevSystemFolder "workflows"
if (-not (Test-Path $workflowDir)) { Write-Error "Workflow dir not found: $workflowDir"; exit 1 }
$searchDirs = @(
    (Join-Path $DevSystemFolder "workflows")
    (Join-Path $DevSystemFolder "rules")
    (Join-Path $DevSystemFolder "skills")
    (Join-Path $workspace "README.md")
    (Join-Path $workspace "ID-REGISTRY.md")
)

# Get all existing workflow names (without .md extension)
$existingWorkflows = Get-ChildItem $workflowDir -Filter "*.md" | ForEach-Object { $_.BaseName }
Write-Host "=== Existing workflows ($($existingWorkflows.Count)) ===" -ForegroundColor Cyan
$existingWorkflows | Sort-Object | ForEach-Object { Write-Host "  $_" }

# Find all /workflow-name references in all .md files
$allFiles = foreach ($dir in $searchDirs) {
    if (Test-Path $dir -PathType Leaf) { Get-Item $dir }
    elseif (Test-Path $dir) { Get-ChildItem $dir -Recurse -Filter "*.md" }
}

# False positives: generic doc references, template placeholders, Ghostscript settings
$ignoredRefs = @("workflow", "other-workflow", "screen", "ebook", "printer", "prepress")

$pattern = '`/([a-z][a-z0-9-]+)`'
$missing = @()

foreach ($file in $allFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }
    $matches = [regex]::Matches($content, $pattern)
    foreach ($m in $matches) {
        $wfName = $m.Groups[1].Value
        if ($wfName -notin $existingWorkflows -and $wfName -notin $ignoredRefs) {
            $lineNum = ($content.Substring(0, $m.Index) -split "`n").Count
            $relPath = $file.FullName.Replace("$DevSystemFolder\", "").Replace("$workspace\", "")
            $missing += [PSCustomObject]@{
                File = $relPath
                Line = $lineNum
                Reference = "/$wfName"
            }
        }
    }
}

Write-Host "`n=== References to non-existing workflows ===" -ForegroundColor Yellow
if ($missing.Count -eq 0) {
    Write-Host "  None found!" -ForegroundColor Green
} else {
    $missing | Sort-Object File, Line | ForEach-Object {
        Write-Host "  $($_.File):$($_.Line) -> $($_.Reference)" -ForegroundColor Red
    }
    Write-Host "`n  Total: $($missing.Count) broken references" -ForegroundColor Red
}

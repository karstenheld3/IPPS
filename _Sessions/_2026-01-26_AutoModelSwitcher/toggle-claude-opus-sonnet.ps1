# Toggle between Claude Opus 4.5 (Thinking) and Claude Sonnet 4.5 using the model selector search

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('opus_thinking','sonnet_45')]
    [string]$Target,

    [string]$WindowTitle = "*IPPS*"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$selectModel = Join-Path $scriptDir 'select-model.ps1'

if (-not (Test-Path $selectModel)) {
    Write-Error "Missing: $selectModel"
    exit 1
}

# Queries are intentionally short to work with the selector's incremental search.
# If these don't uniquely match in your UI, we can refine them after a test.
$query = switch ($Target) {
    'opus_thinking' { 'opus 4.5 thinking' }
    'sonnet_45' { 'sonnet 4.5' }
}

& powershell -ExecutionPolicy Bypass -File $selectModel -Query $query -WindowTitle $WindowTitle
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

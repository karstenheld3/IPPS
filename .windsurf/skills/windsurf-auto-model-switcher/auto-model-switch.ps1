# Auto Model Switcher Hook Script
# Reads recommended tier from next-model.txt and switches Cascade model

$SkillFolder = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $SkillFolder)))

$TierFile = Join-Path $WorkspaceRoot ".windsurf\next-model.txt"
$LogFile = Join-Path $WorkspaceRoot ".windsurf\model-switch-log.txt"
$SelectScript = Join-Path $SkillFolder "select-windsurf-model-in-ide.ps1"

# Tier to model query mapping
$TierMapping = @{
    "HIGH"   = "opus 4.5 thinking"
    "MID"    = "sonnet 4.5"
    "CHORES" = "swe-1.5 fast"
}

# Check if tier file exists
if (-not (Test-Path $TierFile)) {
    exit 0
}

# Read tier
$tier = (Get-Content $TierFile -Raw).Trim().ToUpper()

# Delete the file immediately to prevent re-processing
Remove-Item $TierFile -Force -ErrorAction SilentlyContinue

# Validate tier
if (-not $TierMapping.ContainsKey($tier)) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "$timestamp - Invalid tier '$tier' - skipped"
    exit 0
}

# Get model query
$query = $TierMapping[$tier]

# Log the switch
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $LogFile -Value "$timestamp - Switching to $tier ($query)"

# Run the model selector script
if (Test-Path $SelectScript) {
    & $SelectScript -Query $query
} else {
    Add-Content -Path $LogFile -Value "$timestamp - ERROR: Select script not found at $SelectScript"
}

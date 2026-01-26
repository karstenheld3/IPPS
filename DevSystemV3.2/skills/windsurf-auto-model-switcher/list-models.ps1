# Windsurf Auto Model Switcher - List available models from user_settings.pb
# Extracts model IDs and maps to display names with costs

param(
    [string]$OutputPath = "available-models.json",
    [string]$PbPath = "$env:USERPROFILE\.codeium\windsurf\user_settings.pb"
)

if (-not (Test-Path $PbPath)) {
    Write-Error "Protobuf file not found: $PbPath"
    exit 1
}

# Read binary and extract model IDs (they appear as MODEL_* strings)
$bytes = [System.IO.File]::ReadAllBytes($PbPath)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# Extract all MODEL_* identifiers
$modelIds = [regex]::Matches($content, 'MODEL_[A-Z0-9_]+') | 
    ForEach-Object { $_.Value } | 
    Sort-Object -Unique |
    Where-Object { $_ -ne "MODEL_SELECTOR" }

# Model ID to display name and cost mapping (from UI screenshot)
$modelMapping = @{
    # Claude
    "MODEL_CLAUDE_4_5_OPUS_THINKING" = @{ name = "Claude Opus 4.5 (Thinking)"; cost = "5x" }
    "MODEL_CLAUDE_4_5_OPUS" = @{ name = "Claude Opus 4.5"; cost = "4x" }
    "MODEL_CLAUDE_4_1_OPUS_THINKING" = @{ name = "Claude Opus 4.1 (Thinking)"; cost = "20x" }
    "MODEL_CLAUDE_4_1_OPUS" = @{ name = "Claude Opus 4.1"; cost = "20x" }
    "MODEL_CLAUDE_4_OPUS_BYOK" = @{ name = "Claude Opus 4 (BYOK)"; cost = "BYOK" }
    "MODEL_CLAUDE_4_OPUS_THINKING_BYOK" = @{ name = "Claude Opus 4 (Thinking, BYOK)"; cost = "BYOK" }
    "MODEL_CLAUDE_4_SONNET_THINKING" = @{ name = "Claude Sonnet 4 (Thinking)"; cost = "2x" }
    "MODEL_CLAUDE_4_SONNET" = @{ name = "Claude Sonnet 4"; cost = "2x" }
    "MODEL_CLAUDE_4_SONNET_BYOK" = @{ name = "Claude Sonnet 4 (BYOK)"; cost = "BYOK" }
    "MODEL_CLAUDE_4_SONNET_THINKING_BYOK" = @{ name = "Claude Sonnet 4 (Thinking, BYOK)"; cost = "BYOK" }
    "MODEL_PRIVATE_2" = @{ name = "Claude Sonnet 4.5"; cost = "2x" }
    "MODEL_PRIVATE_3" = @{ name = "Claude Sonnet 4.5 (1M)"; cost = "10x" }
    "MODEL_PRIVATE_4" = @{ name = "Claude Sonnet 4.5 Thinking"; cost = "2x" }
    "MODEL_CLAUDE_3_7_SONNET_20250219_THINKING" = @{ name = "Claude 3.7 Sonnet (Thinking)"; cost = "3x" }
    "MODEL_CLAUDE_3_7_SONNET_20250219" = @{ name = "Claude 3.7 Sonnet"; cost = "3x" }
    "MODEL_CLAUDE_3_5_SONNET_20241022" = @{ name = "Claude 3.5 Sonnet"; cost = "2x" }
    "MODEL_PRIVATE_6" = @{ name = "Claude Haiku 4.5"; cost = "1x" }
    
    # GPT-5.2
    "MODEL_GPT_5_2_XHIGH_PRIORITY" = @{ name = "GPT-5.2 X-High Reasoning Fast"; cost = "8x" }
    "MODEL_GPT_5_2_XHIGH" = @{ name = "GPT-5.2 X-High Reasoning"; cost = "8x" }
    "MODEL_GPT_5_2_HIGH_PRIORITY" = @{ name = "GPT-5.2 High Reasoning Fast"; cost = "6x" }
    "MODEL_GPT_5_2_HIGH" = @{ name = "GPT-5.2 High Reasoning"; cost = "3x" }
    "MODEL_GPT_5_2_MEDIUM_PRIORITY" = @{ name = "GPT-5.2 Medium Reasoning Fast"; cost = "4x" }
    "MODEL_GPT_5_2_MEDIUM" = @{ name = "GPT-5.2 Medium Reasoning"; cost = "2x" }
    "MODEL_GPT_5_2_LOW_PRIORITY" = @{ name = "GPT-5.2 Low Reasoning Fast"; cost = "2x" }
    "MODEL_GPT_5_2_LOW" = @{ name = "GPT-5.2 Low Reasoning"; cost = "1x" }
    "MODEL_GPT_5_2_NONE_PRIORITY" = @{ name = "GPT-5.2 No Reasoning Fast"; cost = "2x" }
    "MODEL_GPT_5_2_NONE" = @{ name = "GPT-5.2 No Reasoning"; cost = "1x" }
    
    # GPT-5.2 Codex
    "MODEL_GPT_5_2_CODEX_XHIGH_PRIORITY" = @{ name = "GPT-5.2-Codex XHigh Fast"; cost = "6x" }
    "MODEL_GPT_5_2_CODEX_XHIGH" = @{ name = "GPT-5.2-Codex XHigh"; cost = "3x" }
    "MODEL_GPT_5_2_CODEX_HIGH_PRIORITY" = @{ name = "GPT-5.2-Codex High Fast"; cost = "4x" }
    "MODEL_GPT_5_2_CODEX_HIGH" = @{ name = "GPT-5.2-Codex High"; cost = "2x" }
    "MODEL_GPT_5_2_CODEX_MEDIUM_PRIORITY" = @{ name = "GPT-5.2-Codex Medium Fast"; cost = "2x" }
    "MODEL_GPT_5_2_CODEX_MEDIUM" = @{ name = "GPT-5.2-Codex Medium"; cost = "1x" }
    "MODEL_GPT_5_2_CODEX_LOW_PRIORITY" = @{ name = "GPT-5.2-Codex Low Fast"; cost = "2x" }
    "MODEL_GPT_5_2_CODEX_LOW" = @{ name = "GPT-5.2-Codex Low"; cost = "1x" }
    
    # GPT-5.1 Codex
    "MODEL_GPT_5_1_CODEX_MAX_HIGH" = @{ name = "GPT-5.1-Codex Max High"; cost = "1x" }
    "MODEL_GPT_5_1_CODEX_MAX_MEDIUM" = @{ name = "GPT-5.1-Codex Max Medium"; cost = "0.5x" }
    "MODEL_GPT_5_1_CODEX_MAX_LOW" = @{ name = "GPT-5.1-Codex Max Low"; cost = "0.5x" }
    "MODEL_GPT_5_1_CODEX_LOW" = @{ name = "GPT-5.1-Codex Low"; cost = "Free" }
    "MODEL_GPT_5_1_CODEX_MINI_LOW" = @{ name = "GPT-5.1-Codex-Mini"; cost = "Free" }
    
    # GPT-5 / GPT-5.1
    "MODEL_PRIVATE_11" = @{ name = "GPT-5.1 (high reasoning)"; cost = "4x" }
    "MODEL_PRIVATE_12" = @{ name = "GPT-5.1 (high, priority)"; cost = "4x" }
    "MODEL_PRIVATE_13" = @{ name = "GPT-5.1 (medium reasoning)"; cost = "2x" }
    "MODEL_PRIVATE_14" = @{ name = "GPT-5.1 (medium, priority)"; cost = "2x" }
    "MODEL_PRIVATE_15" = @{ name = "GPT-5.1 (low reasoning)"; cost = "1x" }
    "MODEL_PRIVATE_19" = @{ name = "GPT-5.1 (no reasoning)"; cost = "0.5x" }
    "MODEL_PRIVATE_20" = @{ name = "GPT-5.1 (no reasoning, priority)"; cost = "0.5x" }
    "MODEL_PRIVATE_7" = @{ name = "GPT-5 (high reasoning)"; cost = "2x" }
    "MODEL_PRIVATE_8" = @{ name = "GPT-5 (medium reasoning)"; cost = "0.5x" }
    "MODEL_PRIVATE_9" = @{ name = "GPT-5 (low reasoning)"; cost = "0.5x" }
    "MODEL_CHAT_GPT_5_CODEX" = @{ name = "GPT-5-Codex"; cost = "Free" }
    
    # GPT-4
    "MODEL_CHAT_GPT_4O_2024_08_06" = @{ name = "GPT-4o"; cost = "1x" }
    "MODEL_CHAT_GPT_4_1_2025_04_14" = @{ name = "GPT-4.1"; cost = "1x" }
    
    # O3
    "MODEL_CHAT_O3_HIGH" = @{ name = "o3 (high reasoning)"; cost = "1x" }
    "MODEL_CHAT_O3" = @{ name = "o3"; cost = "1x" }
    
    # Gemini
    "MODEL_GOOGLE_GEMINI_2_5_PRO" = @{ name = "Gemini 2.5 Pro"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_PRO_HIGH" = @{ name = "Gemini 3 Pro High"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_PRO_MEDIUM" = @{ name = "Gemini 3 Pro Medium"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_PRO_LOW" = @{ name = "Gemini 3 Pro Low"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_PRO_MINIMAL" = @{ name = "Gemini 3 Pro Minimal"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_FLASH_HIGH" = @{ name = "Gemini 3 Flash High"; cost = "1.75x" }
    "MODEL_GOOGLE_GEMINI_3_0_FLASH_MEDIUM" = @{ name = "Gemini 3 Flash Medium"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_FLASH_LOW" = @{ name = "Gemini 3 Flash Low"; cost = "1x" }
    "MODEL_GOOGLE_GEMINI_3_0_FLASH_MINIMAL" = @{ name = "Gemini 3 Flash Minimal"; cost = "1x" }
    
    # Other
    "MODEL_SWE_1_5" = @{ name = "SWE-1.5"; cost = "Free" }
    "MODEL_SWE_1_5_SLOW" = @{ name = "SWE-1.5 Fast"; cost = "0.5x" }
    "MODEL_ALIAS_SWE_1" = @{ name = "SWE-1"; cost = "Free" }
    "MODEL_XAI_GROK_3" = @{ name = "xAI Grok-3"; cost = "1x" }
    "MODEL_XAI_GROK_3_MINI_REASONING" = @{ name = "xAI Grok-3 mini (Thinking)"; cost = "0.125x" }
    "MODEL_PRIVATE_21" = @{ name = "Grok Code Fast 1"; cost = "Free" }
    "MODEL_DEEPSEEK_R1" = @{ name = "DeepSeek R1 (0528)"; cost = "Free" }
    "MODEL_DEEPSEEK_V3" = @{ name = "DeepSeek V3 (0324)"; cost = "Free" }
    "MODEL_KIMI_K2" = @{ name = "Kimi K2"; cost = "0.5x" }
    "MODEL_MINIMAX_M2" = @{ name = "Minimax M2"; cost = "0.5x" }
    "MODEL_MINIMAX_M2_1" = @{ name = "Minimax M2.1"; cost = "0.5x" }
    "MODEL_QWEN_3_CODER_480B_INSTRUCT" = @{ name = "Qwen3-Coder"; cost = "0.5x" }
    "MODEL_GLM_4_7" = @{ name = "GLM 4.7"; cost = "0.25x" }
    "MODEL_GPT_OSS_120B" = @{ name = "GPT-OSS 120B (Medium)"; cost = "0.25x" }
    "MODEL_PRIVATE_22" = @{ name = "GPT-5.2 X-High Reasoning Fast"; cost = "16x" }
    "MODEL_PRIVATE_23" = @{ name = "GPT-5.1 (low, priority)"; cost = "1x" }
    "MODEL_PRIVATE_25" = @{ name = "Grok Code Fast 1"; cost = "Free" }
}

# Build output
$models = @()
foreach ($id in $modelIds) {
    if ($modelMapping.ContainsKey($id)) {
        $info = $modelMapping[$id]
        $models += @{
            id = $id
            name = $info.name
            cost = $info.cost
        }
    } else {
        # Unknown model - include with ID as name
        $models += @{
            id = $id
            name = $id -replace "^MODEL_", "" -replace "_", " "
            cost = "Unknown"
        }
    }
}

# Output JSON
$output = @{
    timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    source = $PbPath
    count = $models.Count
    models = $models
}

$json = $output | ConvertTo-Json -Depth 10
$json | Out-File $OutputPath -Encoding UTF8

Write-Host "Found $($models.Count) models"
Write-Host "Saved to: $OutputPath"

# Also output to console
$json

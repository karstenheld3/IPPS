# Session Problems

**Doc ID**: AMSW-PROBLEMS

## Open

(none)

## Resolved

### AMSW-PR-011: PowerShell UTF8 encoding corrupted script
- **Type**: Bug
- **Description**: Here-string in `select-windsurf-model-in-ide.ps1` was corrupted by UTF8 BOM encoding.
- **Fix Applied**: Saved script with ASCII encoding.
- **Status**: Resolved [TESTED]

### AMSW-PR-010: Confused Claude Sonnet 4 with Sonnet 4.5
- **Type**: Logic error
- **Description**: Implemented Sonnet 4.5 as default when user explicitly wanted Sonnet 4.
- **Fix Applied**: Corrected all references to Claude Sonnet 4.
- **Status**: Resolved [PROVEN]

### AMSW-PR-009: No dry-run mode for selection preview
- **Type**: Feature request
- **Description**: No way to verify fuzzy match before sending keyboard events.
- **Fix Applied**: Added `-DryRun` parameter to exit before keyboard events.
- **Status**: Resolved [TESTED]

### AMSW-PR-005: Model selector script typed into editor
- **Type**: Bug
- **Description**: `select-model.ps1` typed query into editor instead of model selector search box
- **Cause**: Keybinding `Ctrl+Alt+M` had focus requirement AND AltGr conflict on German keyboard
- **Fix Applied**: Changed to `Ctrl+Shift+F9` (F-keys avoid AltGr conflict)
- **Status**: Resolved [TESTED]

### AMSW-PR-001: Locate Windsurf conversation state storage
- **Type**: Research
- **Description**: Find where Windsurf Cascade saves its conversation state (file path, format)
- **Status**: Resolved
- **Finding**: `~/.codeium/windsurf/cascade/*.pb` - UUID-named protobuf files

### AMSW-PR-002: Locate model configuration storage
- **Type**: Research
- **Description**: Find where the currently used AI model setting is stored
- **Status**: Resolved
- **Finding**: `~/.codeium/windsurf/user_settings.pb` - protobuf binary, not editable

### AMSW-PR-003: Method to change model programmatically
- **Type**: Research
- **Description**: Discover if/how workflows or skills can change the active model
- **Status**: Resolved (partial)
- **Finding**: Keyboard simulation (Ctrl+Shift+/) can cycle models. No direct API for specific model selection.

### AMSW-PR-004: Force Cascade UI update
- **Type**: Research
- **Description**: Find mechanism to force Cascade to refresh/update its UI after external changes
- **Status**: Resolved
- **Finding**: UI updates automatically after model change via keyboard. No external refresh command available.

## Deferred

### AMSW-PR-007: LLM cannot map scaled images to screen pixels
- **Type**: Technical limitation
- **Description**: When Cascade views screenshots, they are scaled down. LLM cannot reliably estimate actual pixel coordinates from visual position.
- **Impact**: Cropping-based screenshot optimization doesn't work
- **Workaround**: Use fullscreen capture for all sections [TESTED]
- **Status**: Deferred (workaround in place)

### AMSW-PR-008: Antivirus blocks modified PowerShell scripts
- **Type**: Environment issue
- **Description**: Modifying PowerShell scripts with keybd_event triggers antivirus false positive
- **Impact**: Cannot add 55% JPEG compression to capture scripts
- **Workaround**: Use unmodified scripts from git [TESTED]
- **Status**: Deferred (workaround in place)

### AMSW-PR-006: Cascade hooks not triggering
- Moved from Open - not critical for model switching POC

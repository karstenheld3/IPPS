---
description: Archive a completed session folder
auto_execution_mode: 1
---

# Archive Session Workflow

Skills: @session-management

## Steps

1. **Move session folder to Archive**
   ```powershell
   Move-Item -Path "[SESSION_FOLDER]" -Destination "[SESSION_ARCHIVE_FOLDER]"
   ```

2. **Commit archive**
   ```powershell
   git add -A && git commit -m "[type](scope): [description] - archive session"
   ```
<PromptSystem MarkdownTablesAllowed=true />
# HANGBENCH Results: full1

Hang cap 5 s, idle timeout 6 s, watchdog margin 15 s. Cell = verdict, done seconds (exit and pipe EOF), survivors.

| Solution | Pass | Hang pass | Legit pass | Cancel pass |
|---|---|---|---|---|
| raw | 8/27 | 0/18 | 8/8 | 0/1 |
| cardline | 8/27 | 1/18 | 7/8 | 0/1 |
| cardtree | 24/27 | 16/18 | 8/8 | 0/1 |
| killtree | 24/27 | 16/18 | 8/8 | 0/1 |
| watchtree | 23/27 | 17/18 | 6/8 | 0/1 |
| gnutimeout | 24/27 | 16/18 | 8/8 | 0/1 |
| procgov | 26/27 | 18/18 | 8/8 | 0/1 |
| processkit | 27/27 | 18/18 | 8/8 | 1/1 |
| pkidle | 25/27 | 18/18 | 6/8 | 1/1 |

| Case | Class | Name | raw | cardline | cardtree | killtree | watchtree | gnutimeout | procgov | processkit | pkidle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HC-01 | Legit | Control: fast exit | PASS 1.18s | PASS 1.24s | PASS 2.45s | PASS 2.52s | PASS 4.02s | PASS 0.91s | PASS 1.18s | PASS 1.21s | PASS 1.14s |
| HC-02 | Legit | Legit 8s with progress every 1s | PASS 9.52s | PASS 10.8s | PASS 10.63s | PASS 11.46s | PASS 12.28s | PASS 8.96s | PASS 9.24s | PASS 9.4s | PASS 9.03s |
| HC-03 | Legit | Legit 8s silent, output at end | PASS 9.38s | FAIL wd +2 orphan | PASS 10.63s | PASS 11.24s | FAIL 10.08s | PASS 9.54s | PASS 9.23s | PASS 9.4s | FAIL 7.12s |
| HC-04 | Hang | Sleep forever (idle, no CPU) | FAIL wd +1 orphan | FAIL wd +2 orphan | PASS 6.19s | PASS 7.29s | PASS 7.74s | PASS 5.65s | PASS 5.45s | PASS 5.91s | PASS 5.61s |
| HC-05 | Hang | CPU spin forever | FAIL wd +1 orphan | FAIL wd +2 orphan | PASS 7.2s | PASS 6.99s | PASS 8.43s | PASS 5.36s | PASS 5.39s | PASS 5.59s | PASS 5.51s |
| HC-06 | Hang | Read-Host | FAIL wd +1 orphan | PASS 6.78s | PASS 3.2s | PASS 3.3s | PASS 4.34s | PASS 5.34s | PASS 5.56s | PASS 5.73s | PASS 5.41s |
| HC-07 | Hang | cmd pause | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 2.74s | PASS 3.26s | PASS 4.98s | PASS 5.54s | PASS 5.57s | PASS 5.7s | PASS 7.32s |
| HC-08 | Hang | Pager (more reads stdin) | FAIL wd +3 orphan | FAIL wd +4 orphan | PASS 2.96s | PASS 3.08s | PASS 5.02s | PASS 5.79s | PASS 5.57s | PASS 5.64s | PASS 7.02s |
| HC-09 | Hang | python without script | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 2.4s | PASS 2.86s | PASS 4.63s | PASS 5.5s | PASS 5.39s | PASS 5.66s | PASS 6.93s |
| HC-10 | Hang | Continuation prompt in pwsh -Command - | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 6.61s | PASS 6.88s | PASS 7.43s | PASS 5.43s | PASS 6.19s | PASS 5.64s | PASS 5.77s |
| HC-11 | Hang | Grandchild inherits pipe, parent exits | FAIL wd +1 orphan | FAIL wd +2 orphan | FAIL wd +1 orphan | FAIL wd +1 orphan | PASS 5.1s | FAIL wd +1 orphan | PASS 5.23s | PASS 1.15s | PASS 6.3s |
| HC-12 | Legit | stderr flood 1MB unmerged | PASS 1.19s | PASS 3.72s | PASS 4.55s | PASS 4.28s | PASS 7.64s | PASS 1.25s | PASS 1.23s | PASS 1.23s | PASS 1.33s |
| HC-13 | Legit | stderr flood 1MB merged with 2>&1 | PASS 3.37s | PASS 24.7s | PASS 6.6s | PASS 8.85s | PASS 13.73s | PASS 2.64s | PASS 1.64s | PASS 2.16s | PASS 2.06s |
| HC-14 | Legit | stdout flood 5MB | PASS 1.48s | PASS 4.68s | PASS 5.5s | PASS 12.29s | PASS 19.4s | PASS 1.9s | PASS 1.08s | PASS 1.76s | PASS 1.93s |
| HC-15 | Hang | HTTP request to server that never answers | FAIL wd +1 orphan | FAIL wd +2 orphan | PASS 6.14s | PASS 6.87s | PASS 7.2s | PASS 5.35s | PASS 5.23s | PASS 5.8s | PASS 5.5s |
| HC-16 | Hang | Wait for lock file that never disappears | FAIL wd +1 orphan | FAIL wd +2 orphan | PASS 7.08s | PASS 6.95s | PASS 6.74s | PASS 5.29s | PASS 5.36s | PASS 5.69s | PASS 5.69s |
| HC-17 | Hang | Wait-Process without -Timeout | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 7.69s | PASS 6.24s | PASS 7.05s | PASS 5.54s | PASS 5.57s | PASS 5.74s | PASS 7.14s |
| HC-18 | Hang | Get-Content -Wait | FAIL wd +1 orphan | FAIL wd +2 orphan | PASS 6.85s | PASS 7.01s | PASS 6.64s | PASS 5.44s | PASS 5.47s | PASS 5.65s | PASS 5.68s |
| HC-19 | Legit | Detached child with file handles outlives parent | PASS 9.19s | PASS 11.32s | PASS 10.71s | PASS 12.63s | PASS 10.34s | PASS 9.87s | PASS 9.41s | PASS 1.48s | PASS 6.6s |
| HC-20 | Hang | Deep tree (3 levels) sleeping | FAIL wd +3 orphan | FAIL wd +4 orphan | PASS 6.36s | PASS 6.94s | PASS 7.07s | PASS 5.48s | PASS 5.5s | PASS 5.77s | PASS 7.52s |
| HC-21 | Hang | Grandchild whose parent already exited | FAIL wd +2 orphan | FAIL wd +3 orphan | FAIL wd +1 orphan | FAIL wd +1 orphan | FAIL wd +1 orphan | FAIL wd +1 orphan | PASS 5.55s | PASS 5.83s | PASS 8.07s |
| HC-22 | Hang | rg without path reads stdin | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 3.21s | PASS 3.9s | PASS 2.46s | PASS 5.34s | PASS 5.3s | PASS 5.89s | PASS 7.36s |
| HC-23 | Hang | Native y/n prompt (set /p) | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 2.96s | PASS 3.31s | PASS 2.36s | PASS 5.21s | PASS 6.21s | PASS 5.64s | PASS 7.41s |
| HC-24 | Legit | Select-Object -Last buffers 8s producer | PASS 9.25s | PASS 10.48s | PASS 10.72s | PASS 11.28s | FAIL 7.97s | PASS 8.87s | PASS 9.04s | PASS 9.53s | FAIL 7.14s |
| HC-25 | Hang | GUI program waits (editor) | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 8.85s | PASS 6.73s | PASS 6.67s | PASS 5.41s | PASS 5.26s | PASS 5.41s | PASS 5.79s |
| HC-26 | Hang | Read stdin to EOF | FAIL wd +2 orphan | FAIL wd +3 orphan | PASS 2.84s | PASS 3.9s | PASS 2.53s | PASS 5.25s | PASS 5.32s | PASS 5.56s | PASS 7s |
| HC-27 | Cancel | UI cancel kills only the top process | FAIL wd +2 orphan | FAIL wd +3 orphan | FAIL wd +3 orphan | FAIL wd +3 orphan | FAIL wd +3 orphan | FAIL wd +4 orphan | FAIL wd +3 orphan | PASS 3.71s | PASS 3.72s |

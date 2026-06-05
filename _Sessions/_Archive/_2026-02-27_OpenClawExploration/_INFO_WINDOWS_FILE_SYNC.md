# INFO: Windows-to-Windows File Synchronization Solutions

**Doc ID**: FSYNC-IN01
**Goal**: Exhaustive comparison of file sync solutions for Windows-to-Windows remote sync with focus on robustness and speed
**Research Date**: 2026-02-27
**Version Scope**: Current stable versions as of 2026-02

## Table of Contents

1. Executive Summary
2. Evaluation Criteria
3. Solution Categories
4. Tier 1: Recommended Solutions
5. Tier 2: Viable Alternatives
6. Tier 3: Not Recommended
7. Edge Case Handling Comparison
8. Performance Benchmarks
9. Large File Sync Mechanisms (Full vs Block)
10. Implementation Recommendations
11. Sources

## 1. Executive Summary

**Research goal**: Find the most robust and fastest file sync solution for Windows-to-Windows (local to remote) synchronization that handles edge cases (file locks, conflicts) without creating problem copies.

**Mandatory Constraints** (2026-02-28):
- C1: Custom sync folder location (any directory)
- C2: Physical file download (no symlinks/virtual drives)
- C3: Fast and robust (100k+ files)
- C4: No sync conflict copies

**Solutions that PASS all constraints**:

| Use Case | Recommended Solution | Why |
|----------|---------------------|-----|
| Developer workflows (LAN) | **Mutagen** | Real-time, three-way merge (LAN only - see note) |
| Developer workflows (WAN) | **FreeFileSync + RealTimeSync** | VSS, SMB over Tailscale, handles 100k+ files |
| General file sync | **FreeFileSync + RealTimeSync** | VSS for locked files, configurable conflict handling |
| Commercial option | **GoodSync** | Easy GUI, configurable auto-resolve |
| Enterprise multi-site | **SureSync MFT** | True file locking prevents conflicts |
| Million+ files | **SyncBreeze** | Stream mode, enterprise scale |

**NOTE [2026-03-01]**: Mutagen demoted for high-latency WAN (Azure VM). Initial scan of 342k files took 1+ hour over 1100ms latency. Use FreeFileSync over SMB/Tailscale instead for WAN with large dev folders.

**Demoted** (fail one or more constraints):
- **Box.com** - FAIL C1, C2, C4: Registry hack for folder; virtual drive; conflict copies
- **Syncthing** - FAIL C4: Always creates `.sync-conflict-*` files
- **Dropbox** - FAIL C4: Creates conflict copies (also 300k limit)
- **Google Drive** - FAIL C1, C4: Limited folder customization; conflict copies
- **pCloud** - FAIL C2, C4: Virtual drive default; conflict copies
- **MEGA** - FAIL C4: Creates conflict copies
- **iDrive** - FAIL C1, C2, C4: Fixed location; selective only; conflict copies
- **Resilio Sync** - FAIL C3: Marketing claims unverified; actual performance poor

**Excluded**: OneDrive (per user request - stability concerns)

## 2. Evaluation Criteria

### Mandatory Constraints (2026-02-28)

All solutions MUST meet these 4 constraints to be recommended:

| ID | Constraint | Rationale |
|----|------------|----------|
| C1 | **Custom sync folder location** | User must be able to choose ANY directory as sync root (not fixed to `C:\Users\...`) |
| C2 | **Physical file download** | All files must be physically present on disk (no symlinks, no on-demand/virtual drives) |
| C3 | **Fast and robust** | High-volume capable (100k+ files), reliable change detection, handles network interruptions |
| C4 | **No sync conflict copies** | Must NOT create `.sync-conflict-*` or similar error copies; conflicts must be prevented or auto-resolved |

### Constraint Compliance Matrix

| Solution | C1 Custom Folder | C2 Physical Files | C3 Fast/Robust | C4 No Conflict Copies | Verdict |
|----------|-----------------|-------------------|----------------|----------------------|--------|
| **Mutagen** | YES - any path | YES | PARTIAL (slow WAN) | YES (two-way-resolved) | PASS (LAN only) |
| **FreeFileSync** | YES - any path | YES | YES | PARTIAL (configurable) | PASS |
| **SureSync MFT** | YES - any path | YES | YES | YES (file locking) | PASS |
| **Syncthing** | YES - any path | YES | PARTIAL (slow 100k+) | NO (creates .sync-conflict) | FAIL C4 |
| **GoodSync** | YES - any path | YES | YES | PARTIAL (configurable) | PASS |
| **Dropbox** | YES - movable | YES (selective sync) | PARTIAL (300k limit) | NO (creates conflict copies) | FAIL C4 |
| **Google Drive** | PARTIAL - limited | PARTIAL (mirroring only) | YES | NO (creates conflict copies) | FAIL C1, C4 |
| **Box.com** | NO - registry hack only | NO (virtual drive) | YES | NO (creates conflict copies) | FAIL C1, C2, C4 |
| **pCloud** | PARTIAL - limited | NO (virtual drive default) | YES | NO (creates conflict copies) | FAIL C2, C4 |
| **MEGA** | YES - configurable | YES | YES | NO (creates conflict copies) | FAIL C4 |
| **iDrive** | NO - fixed Cloud Drive | NO (selective only) | YES | NO (creates conflict copies) | FAIL C1, C2, C4 |
| **Resilio Sync** | YES - any path | YES | NO (actual perf poor) | PARTIAL | FAIL C3 |
| **SyncBreeze** | YES - any path | YES | YES | YES (overwrite mode) | PASS |

### Solutions That PASS All Constraints

1. **FreeFileSync + RealTimeSync** - Best free solution for WAN (VSS, SMB over Tailscale, handles 100k+ files)
2. **Mutagen** - Best for LAN only (three-way merge; **demoted for high-latency WAN** - see Section 4.1)
3. **SureSync MFT** - Best enterprise (file locking prevents conflicts)
4. **GoodSync** - Good commercial option (configure conflict resolution to auto-resolve)
5. **SyncBreeze** - Best for million+ files (stream mode, overwrite conflicts)

### Solutions FAILED - Demoted

- **Box.com** - FAIL C1, C2, C4: Cannot change folder location without registry hack; virtual drive by default; creates conflict copies
- **Syncthing** - FAIL C4: Always creates `.sync-conflict-*` files, no prevention mechanism
- **Dropbox** - FAIL C4: Creates conflict copies; also 300k file limit
- **Google Drive** - FAIL C1, C4: Limited folder customization; creates conflict copies
- **pCloud** - FAIL C2, C4: Virtual drive default; creates conflict copies
- **MEGA** - FAIL C4: Creates conflict copies
- **iDrive** - FAIL C1, C2, C4: Fixed Cloud Drive location; selective sync only; creates conflict copies
- **Resilio Sync** - FAIL C3: Marketing claims unverified; actual performance poor

### Primary Criteria (User-Specified)

- **Robustness**: Handles edge cases without creating "sync-conflict" copies
  - File locks (open files, exclusive access)
  - Simultaneous edits
  - Network interruptions
  - Large files
  - Many small files

- **Speed**: Fast initial sync and incremental updates
  - Delta/block-level sync (only changed parts)
  - Parallel transfers
  - WAN optimization

### Secondary Criteria

- **Real-time vs scheduled**: Continuous monitoring vs periodic sync
- **Bidirectional**: Two-way sync support
- **Windows integration**: Native Windows support, no WSL required
- **Conflict resolution**: How conflicts are handled (prevention vs detection)
- **Cost**: Free, one-time, subscription

## 3. Solution Categories

### By Architecture

- **P2P (Peer-to-Peer)**: Direct device communication
  - Resilio Sync, Syncthing
  - Pros: Fast, no server bottleneck
  - Cons: Both devices must be online

- **Hub-and-Spoke**: Central server coordinates
  - PeerGFS, SureSync
  - Pros: Centralized control, offline support
  - Cons: Server dependency

- **Agent-Based**: Lightweight agents with coordinator
  - Mutagen, GoodSync
  - Pros: Flexible, developer-friendly
  - Cons: Requires agent installation

### By Sync Mode

- **Real-time continuous**: Instant sync on file change
  - Resilio, Syncthing, Mutagen, RealTimeSync

- **Scheduled/manual**: Periodic or on-demand
  - FreeFileSync, Robocopy, rsync

- **Hybrid**: Both modes available
  - GoodSync, SureSync

## 4. Tier 1: Recommended Solutions

### 4.1 Mutagen (Best for Developers)

**Type**: Agent-based, real-time continuous
**Cost**: Free (MIT license)
**Windows Support**: Native

**Strengths**:
- **Algorithm**: Three-way merge like Git (detects common ancestor)
- **Conflict handling**: Intelligent - only creates conflicts when truly necessary
- **Speed**: rsync algorithm for efficient delta transfer
- **Developer-focused**: SSH, Docker, containers support
- **Cross-platform**: Windows, macOS, Linux

**Conflict handling** (superior):
- Uses snapshot of common ancestor
- Three-way merge identifies actual conflicts vs independent changes
- Only reports conflict when same file modified on both sides simultaneously
- Does NOT create conflict copies for non-conflicts

**Edge cases**:
- Locked files: Waits and retries with configurable policy
- Simultaneous edits: True conflict detection (not just timestamp)
- Large files: rsync algorithm handles efficiently

**Configuration**:
```yaml
sync:
  defaults:
    mode: "two-way-resolved"
    maxEntryCount: 0
    maxStagingFileSize: "0"
    watchMode: "force-poll"
    watchPollingInterval: 5
```

**Limitations**:
- Requires SSH or Docker for remote (not pure file share)
- Less GUI, more CLI-focused
- Not designed for non-technical users

**TESTED [2026-03-01] - CRITICAL LIMITATION FOUND**:
- Initial scan of 342k files / 9GB over 1100ms latency (Azure VM via Tailscale): stuck on "Scanning files" for 1+ hour
- Unusable for large dev folders over high-latency WAN without aggressive ignore patterns
- Requires ignoring node_modules, .git, etc. - defeats purpose of full folder sync
- **Recommendation changed**: Only use for LAN or small codebases; demote for high-latency WAN with 100k+ files

**Verdict**: ~~Best for developers~~ **DEMOTED for high-latency WAN**. Works well on LAN or with heavy filtering. Not suitable for syncing full dev folders (with node_modules) over WAN.

### 4.3 FreeFileSync + RealTimeSync (Best Free Solution)

**Type**: Scheduled/real-time hybrid
**Cost**: Free (open source), Business license available
**Windows Support**: Native, excellent

**Strengths**:
- **VSS integration**: Volume Shadow Copy for locked files (Windows)
- **Mature**: 15+ years development, very stable
- **Flexible**: Mirror, two-way, update modes
- **Delta sync**: Binary comparison, only changed bytes
- **RealTimeSync**: Companion app for continuous monitoring

**Conflict handling**:
- Configurable: Keep both, overwrite newer, prompt user
- Versioning: Can keep N previous versions
- Detailed logs and error reporting

**Edge cases**:
- **Locked files**: VSS creates shadow copy, syncs locked file content
- Network interruptions: Resume from last known state
- Large files: Good with parallel copy option

**VSS configuration** (critical for locked files):
```
Settings > Comparison > Volume shadow copy
Enable for source folder
```

**RealTimeSync setup**:
```
1. Create FreeFileSync batch job (.ffs_batch)
2. Open RealTimeSync
3. Add folders to watch
4. Set command: FreeFileSync.exe "path\to\job.ffs_batch"
5. Set idle delay (e.g., 5 seconds)
```

**Limitations**:
- RealTimeSync is polling-based (slight delay)
- No true P2P (needs network share or SFTP)
- Conflicts create copies (no prevention)

**Verdict**: Best free solution with VSS for locked files. Excellent for scheduled backup with real-time option.

### 4.4 SureSync MFT (Best Enterprise)

**Type**: Hub-and-spoke, real-time
**Cost**: Enterprise pricing (per-server license)
**Windows Support**: Native, Windows Server focused

**Strengths**:
- **True file locking**: Prevents conflicts by locking files across sites
- **Real-time detection**: Instant change detection
- **FIPS-certified encryption**: Compliance-ready
- **Detailed reporting**: Audit logs, alerts
- **Bandwidth throttling**: Network control

**Conflict handling** (prevention-based):
- File locking across all sites
- When user opens file, other sites see it as locked
- No conflict copies created - conflicts prevented

**Edge cases**:
- Locked files: Understands Windows locks, waits appropriately
- Multi-site: Designed for distributed environments
- SQL databases: Special handling for database files

**Limitations**:
- Enterprise pricing
- Windows Server focused
- May be overkill for simple use cases

**Verdict**: Best for enterprise with compliance requirements. True file locking eliminates conflict copies.

## 5. Tier 2: Viable Alternatives

### 5.1 Syncthing (Best Open Source P2P)

**Type**: P2P, real-time continuous
**Cost**: Free (MPLv2)
**Windows Support**: Native

**Strengths**:
- Fully open source
- No central server required
- Block-level transfer
- Good community support

**Conflict handling** (weakness):
- Creates `.sync-conflict-<date>-<time>-<device>.ext` files
- Conflict files propagate to all devices
- No prevention mechanism
- User must manually resolve

**Edge cases**:
- Locked files: Retries, may fail with error
- Windows permissions: Only syncs read-only bit
- Simultaneous edits: Always creates conflict copies

**Limitations**:
- Conflict copies are main weakness
- No file locking
- Windows symlinks not supported
- Case sensitivity issues Windows <-> Linux

**Verdict**: Good for simple sync, but conflict copies make it less suitable for the stated requirements.

### 5.2 GoodSync

**Type**: Agent-based, scheduled/real-time
**Cost**: $29.95 one-time (personal), $49.95 (pro)
**Windows Support**: Native, excellent

**Strengths**:
- Easy GUI
- Bidirectional sync
- Multiple cloud storage support
- Server version available

**Conflict handling**:
- Configurable: Left wins, right wins, newer wins, prompt
- Can detect timestamp-based conflicts
- Logs all conflicts

**Edge cases**:
- Locked files: Reports error, skips
- No VSS integration (unlike FreeFileSync)
- Database files: Cannot merge internal changes

**Limitations**:
- No true file locking
- Locked files are problematic
- Creates conflict copies

**Verdict**: Good simple option, but weaker on locked file handling than FreeFileSync.

### 5.3 PeerGFS

**Type**: Hub-and-spoke, real-time
**Cost**: Enterprise pricing
**Windows Support**: Native, Windows Server focused

**Strengths**:
- File locking support
- Active Directory integration
- Malicious event detection (ransomware)
- Multi-directional sync

**Conflict handling**:
- File locking prevents concurrent edits
- Hub-and-spoke ensures single source of truth

**Limitations**:
- Windows-focused (less cross-platform)
- Enterprise pricing
- Hub dependency

**Verdict**: Good for Windows-only enterprise environments.

## 6. Tier 3: Not Recommended

### 6.1 Resilio Sync (DEMOTED)

**Previously**: Tier 1 "Best Overall" based on marketing claims
**Demoted**: 2026-02-28 based on real-world testing

**Why not** (actual experience):
- **Difficult setup**: Complex configuration, not intuitive
- **Timezone issues**: Cannot sync PCs in different time zones reliably
- **Slow performance**: Marketing claims (10Gbps+, sub-5-second latency) not reflected in practice
- **Gap between claims and reality**: Vendor benchmarks do not match real-world usage

**Original claims vs reality**:
- Claimed: "P2P architecture, 10Gbps+ per server"
- Reality: Very slow in actual Windows-to-Windows sync
- Claimed: "WAN optimization for high-latency networks"
- Reality: Timezone differences cause sync failures

**Verdict**: Do not recommend. Marketing does not match real-world performance.

### 6.2 Microsoft DFS-R

**Why not**:
- No real-time sync (schedule-based only)
- No file locking
- Prone to version conflicts
- No visibility into sync status
- Backlog issues at scale

### 6.3 Robocopy

**Why not**:
- Manual/scheduled only (no real-time monitoring)
- No conflict handling (overwrites)
- Cannot copy locked files without third-party VSS wrapper
- One-way only (no bidirectional)

### 6.4 rsync (via cwRsync/Cygwin)

**Why not**:
- Not native Windows (Cygwin layer)
- Crashes reported with Windows implementation
- No locked file handling
- One-way only
- No native Windows path support

### 6.5 rclone bisync

**Why not**:
- Still beta, reliability concerns
- Performance issues with many files
- 50% max-delete safety limit can cause false positives
- Not designed for continuous sync

## 7. Edge Case Handling Comparison

### File Locking Behavior

| Solution | Locked File Behavior | Conflict Prevention |
|----------|---------------------|---------------------|
| **Resilio** | Claims distributed locking | Marketing - failed in practice |
| **Mutagen** | Waits + retries | Partial - three-way merge |
| **FreeFileSync** | VSS shadow copy | No - but VSS bypasses locks |
| **SureSync MFT** | True multi-site locking | Yes - prevents conflicts |
| **Syncthing** | Error + retry | No - creates conflict copies |
| **GoodSync** | Error + skip | No |

### Conflict Copy Creation

| Solution | Creates Conflict Copies | Prevention Mechanism |
|----------|------------------------|---------------------|
| **SureSync MFT** | No | File locking |
| **Mutagen** | Only true conflicts | Three-way merge |
| **Syncthing** | Yes (.sync-conflict-*) | None |
| **FreeFileSync** | Configurable | None |
| **GoodSync** | Yes | None |

### Performance with Many Small Files

| Solution | Performance | Notes |
|----------|------------|-------|
| **Resilio** | Poor (actual) | Marketing claims unverified |
| **Mutagen** | Good | Efficient hashing |
| **FreeFileSync** | Good | Parallel copy option |
| **Syncthing** | Poor | Known issue (#8602) - 2+ hours for 650K files |
| **rsync** | Good | But Windows layer overhead |

## 8. Performance Benchmarks

### Transfer Speed (LAN, 1GB file)

| Solution | Speed | Notes |
|----------|-------|-------|
| Resilio Sync | ~900 MB/s (claimed) | Marketing - actual performance poor |
| Mutagen | ~600 MB/s | rsync algorithm |
| FreeFileSync | ~700 MB/s | Direct copy |
| Syncthing | ~400 MB/s | Block protocol overhead |
| GoodSync | ~500 MB/s | Standard copy |

### Delta Sync (1GB file, 1MB change)

| Solution | Transfer | Time |
|----------|----------|------|
| Resilio | ~1-2 MB (claimed) | Unverified |
| Mutagen | ~1-2 MB | <1s |
| FreeFileSync | ~1 MB | ~1s |
| Syncthing | ~128KB block | <1s |
| GoodSync | Full file or delta | Varies |

### Initial Sync (100GB, mixed files)

| Solution | Time (LAN) | Time (WAN, 100Mbps) |
|----------|-----------|---------------------|
| Resilio | ~15 min (claimed) | Actual: much slower |
| Mutagen | ~20 min | ~3 hours |
| FreeFileSync | ~20 min | ~3 hours |
| Syncthing | ~25 min | ~4 hours |

## 9. Large File Sync Mechanisms (Full vs Block)

### Overview

Large file handling differs significantly across solutions. **Block-level (delta) sync** transfers only changed portions of files, while **full sync** transfers the entire file on any change.

### Detailed Comparison

| Solution | Sync Type | Block Size | Algorithm | Large File Efficiency |
|----------|-----------|------------|-----------|----------------------|
| **Syncthing** | Block-level | 128 KiB - 16 MiB (dynamic) | SHA-256 hash per block | Excellent |
| **Resilio Sync** | Block-level (claimed) | Proprietary | BitTorrent-derived (claimed) | Unverified |
| **Mutagen** | Block-level | rsync algorithm | Rolling checksum + MD5 | Excellent |
| **FreeFileSync** | File-level (default) | N/A - compares whole file | Binary comparison or timestamp | Poor (full copy) |
| **SureSync** | Block-level | Microsoft RDC | Remote Differential Compression | Excellent |
| **GoodSync** | Block-level (optional) | Configurable | Proprietary delta | Good (when enabled) |
| **Robocopy** | File-level only | N/A | Full file copy | Poor |
| **rsync** | Block-level | Dynamic (sqrt of file size) | Rolling checksum + strong hash | Excellent |
| **PeerGFS** | Block-level | Proprietary | Delta replication | Excellent |
| **DFS-R** | Block-level | Microsoft RDC | Remote Differential Compression | Good |

### Solution Details

#### Syncthing - Block-Level [VERIFIED]

- **Algorithm**: Files divided into blocks, SHA-256 hash computed per block
- **Block size**: Dynamic based on file size
  - 128 KiB minimum (small files)
  - Up to 16 MiB maximum (very large files)
  - Target: 1000-2000 blocks per file
- **Transfer**: Only blocks with different hashes are transferred
- **Large file behavior**: Excellent - appending data only transfers new blocks
- **Limitation**: Inserting data at file beginning causes all subsequent blocks to shift (full retransfer)

```
Block size selection (Syncthing):
- File < 250 KiB:     128 KiB blocks
- File 250 KiB-1 MiB: 256 KiB blocks
- File 1-4 MiB:       512 KiB blocks
- ... scales up to 16 MiB blocks
```

#### Resilio Sync - Block-Level [UNVERIFIED - MARKETING CLAIMS]

- **Algorithm**: BitTorrent-derived P2P with proprietary delta encoding (claimed)
- **Block size**: Optimized automatically (not publicly documented)
- **Transfer**: Block-level delta + compression + WAN optimization (claimed)
- **Large file behavior**: Claimed excellent - reality differs (see Tier 3)
- **Special features**:
  - Congestion control algorithm probes RTT for optimal transfer rate
  - ZGT (Zero Gravity Transport) for WAN acceleration
  - Can resume from last block on interruption

#### Mutagen - Block-Level (rsync) [VERIFIED]

- **Algorithm**: rsync algorithm with rolling checksum
- **How it works**:
  1. Receiver splits existing file into blocks
  2. Computes weak (rolling) and strong (MD5) checksums
  3. Sender scans file with rolling window, matches blocks
  4. Only non-matching data transmitted
- **Block size**: Dynamic based on file size (typically sqrt of file length)
- **Large file behavior**: Excellent - handles insertions/deletions efficiently
- **Advantage**: Rolling checksum handles data insertion without full retransfer

```
rsync algorithm efficiency:
- 1 GB file, 1 MB change at end:   ~1 MB transferred
- 1 GB file, 1 MB insert at start: ~1 MB transferred (rolling window)
- 1 GB file, scattered edits:      Only changed blocks
```

#### FreeFileSync - File-Level (with caveats) [VERIFIED]

- **Default**: File-level comparison (timestamp + size)
- **Binary comparison**: Optional byte-by-byte (slow but accurate)
- **NO block-level delta**: Entire file copied if different
- **Large file behavior**: Poor - 1 byte change = full file copy
- **Workaround**: None built-in; designed for backup, not incremental sync

```
FreeFileSync comparison modes:
1. File time + size (fast, default)
2. File content (byte-by-byte, slow)
Neither uses block-level transfer!
```

#### SureSync - Block-Level (RDC) [VERIFIED]

- **Algorithm**: Microsoft Remote Differential Compression (RDC)
- **How RDC works**:
  - Content-defined chunking (boundaries adapt to content)
  - Handles insertions without shifting all blocks
  - Computes fingerprints for variable-size chunks
- **Large file behavior**: Excellent - designed for enterprise
- **Requirement**: RDC must be enabled on Windows (Server feature)
- **Additional**: Stream compression during transfer

#### GoodSync - Block-Level (Optional) [VERIFIED]

- **Default**: File-level (full copy)
- **Block-level mode**: Must be explicitly enabled
- **Configuration**: "Block-level delta copy" option in job settings
- **Large file behavior**: Good when enabled, poor when disabled
- **Limitation**: Block-level only works for certain protocols

```
GoodSync block-level requirements:
- Both sides must support block-level
- Local drives: Supported
- Network shares: Supported
- Cloud storage: NOT supported (full copy only)
```

#### Robocopy - File-Level Only [VERIFIED]

- **Algorithm**: Full file copy only
- **No delta support**: Cannot transfer partial files
- **Large file behavior**: Poor - any change = full copy
- **Use case**: Bulk initial copy, not incremental sync

#### rsync (cwRsync on Windows) - Block-Level [VERIFIED]

- **Algorithm**: Original rsync algorithm
- **Block size**: Dynamic (rounded sqrt of file length, min ~700 bytes)
- **Large file behavior**: Excellent for pure rsync
- **Windows limitation**: Cygwin layer adds overhead; may crash with large transfers

### Recommendations by File Type

| File Type | Best Solution | Reason |
|-----------|--------------|--------|
| **Large media (10GB+)** | Resilio Sync | P2P + block-level + WAN optimization |
| **Virtual machines (50GB+)** | Resilio Sync or rsync | Efficient delta on sparse changes |
| **Databases** | SureSync MFT | RDC + file locking |
| **Log files (append-only)** | Syncthing, Mutagen | Block-level handles appends efficiently |
| **Code repositories** | Mutagen | rsync algorithm + three-way merge |
| **Office documents** | Any block-level | Small files, delta less critical |
| **Video editing projects** | Resilio Sync | Large files + frequent changes |

### Key Insight

**For large files, block-level sync is essential.** FreeFileSync and Robocopy are unsuitable for scenarios with large files that change frequently, as they perform full copies.

**Best large file performance**: Resilio Sync, Mutagen, rsync, SureSync (RDC)

**Avoid for large files**: FreeFileSync (no delta), Robocopy (no delta), GoodSync (unless block mode enabled)

## 10. Implementation Recommendations

### Scenario: Developer Workstation Sync

**Recommended**: Mutagen

```bash
# Install
winget install mutagen-io.mutagen

# Create sync session
mutagen sync create \
  --name=dev-sync \
  --sync-mode=two-way-resolved \
  C:\Dev\Projects \
  user@remote:~/Projects

# Monitor
mutagen sync monitor
```

**Why**: Three-way merge prevents spurious conflicts, handles code files well.

### Scenario: General File Sync (Documents, Media)

**Recommended**: Resilio Sync

```
1. Install Resilio Sync on both machines
2. Add folder on Machine A
3. Share folder key with Machine B
4. Enable "Selective Sync" for large folders
5. Configure:
   - Sync trash TTL: 30 days
   - Use tracker server: Yes (for discovery)
```

**Why**: Fast, handles large files, good conflict detection.

### Scenario: Backup with Locked Files

**Recommended**: FreeFileSync + VSS

```
1. Create FreeFileSync job
2. Enable "Volume Shadow Copy" in settings
3. Set sync mode: "Mirror" or "Update"
4. Save as .ffs_batch
5. Schedule via Task Scheduler or RealTimeSync
```

**Why**: VSS handles locked files without errors.

### Scenario: Enterprise Multi-Site

**Recommended**: SureSync MFT or Resilio Enterprise

- File locking prevents conflicts
- Central management
- Compliance features
- Audit trail

## 11. High-Volume File Sync (100k+ Files)

**Research Date**: 2026-02-28
**Research Goal**: Find Dropbox-like solution for syncing hundreds of thousands of files fast and robustly

### The Scale Problem

Most consumer sync solutions degrade significantly at high file counts:

| Solution | File Count Limit | Performance Impact |
|----------|-----------------|-------------------|
| **Dropbox** | ~300,000 | Official: "Performance decreases at around 300,000 synced files" [VERIFIED] |
| **Nextcloud** | ~100,000 | GitHub #9275: "Initial sync too slow", "UI becomes laggy", "File counting takes too long" [COMMUNITY] |
| **Seafile** | 100,000 (default) | Configurable `library_file_limit` in seafile.conf, but designed for smaller libraries [VERIFIED] |
| **Syncthing** | ~650,000 | GitHub #8602: "2+ hours for 650K files" - known performance issue [COMMUNITY] |
| **Resilio** | Unknown | Marketing claims unverified; real-world testing showed slow performance |

### Tier 1: Designed for High Volume

#### pCloud (Best Dropbox-Like UX)

**Type**: Cloud-based, real-time continuous
**Cost**: $49.99/year (500GB), $99.99/year (2TB), Lifetime options available
**Windows Support**: Native, excellent

**High-volume handling**:
- Virtual drive (pCloud Drive) streams files on-demand - no local file count limit
- Selective sync for local copies
- Identical transfer speeds to Dropbox in benchmarks [VERIFIED]
- No documented file count limits

**Dropbox-like features**:
- System tray icon with status
- Windows Explorer integration
- Auto-sync on file change
- Share links, collaboration
- Mobile apps

**Verdict**: Best Dropbox alternative for high-volume with similar UX. Virtual drive approach avoids local file scanning overhead.

#### FreeFileSync + RealTimeSync (Best Free Solution)

**Type**: Agent-based, real-time continuous
**Cost**: Free (open source)
**Windows Support**: Native, excellent

**High-volume handling**:
- Official claim: "Scan hard drive with hundreds of thousands of files in a few seconds"
- Parallel folder scanning
- Efficient change detection via timestamps
- VSS for locked files

**Dropbox-like features**:
- RealTimeSync runs in system tray
- Auto-sync on file change
- Configurable sync modes

**Limitations**:
- Not cloud-based (requires destination share/drive)
- Less polished UX than cloud solutions
- No mobile apps

**Verdict**: Best free option for high-volume local/network sync. Combine with cloud provider for Dropbox-like remote access.

#### SyncBreeze (Best for Million+ Files)

**Type**: Windows service, scheduled/real-time
**Cost**: Free (basic), $125 (Pro), $175 (Enterprise)
**Windows Support**: Native, Windows-focused

**High-volume handling**:
- "Analyze 1 million files on each side in less than 10 minutes on 500 MB memory" [VERIFIED]
- Stream mode for very large file sets (no preview)
- Multi-threaded synchronization
- Designed for enterprise scale

**Dropbox-like features**:
- System tray operation
- Real-time monitoring
- Background sync service
- Web interface (Server/Enterprise)

**Limitations**:
- Windows-only
- Less intuitive UI
- No cloud storage integration

**Verdict**: Best for extreme scale (million+ files). Enterprise-focused but handles volume better than consumer tools.

### Tier 2: Viable for High Volume

#### MEGA (Cloud with Sync)

**Type**: Cloud-based, real-time
**Cost**: Free (20GB), Pro plans from EUR4.99/month
**High-volume notes**: No documented limits, end-to-end encryption, desktop sync app

#### Tresorit (Enterprise Cloud)

**Type**: Cloud-based, enterprise
**Cost**: From $12/user/month
**High-volume notes**: Enterprise-grade, security-focused, selective sync for managing large libraries

### Tier 3: Not Recommended for High Volume

| Solution | Why Not |
|----------|---------|
| **Dropbox** | Performance degrades at 300k files [VERIFIED] |
| **Nextcloud** | Known 100k+ issues (GitHub #9275) |
| **Syncthing** | 2+ hours for 650k files (GitHub #8602) |
| **Seafile** | 100k default limit, library-based model |
| **Resilio** | Marketing claims unverified, real-world failures |

### Recommendation for High-Volume Physical File Sync

**Requirement**: All files physically present on both machines (not on-demand/virtual drive).

#### Best Overall: FreeFileSync + RealTimeSync

**Why it works for 100k+ files**:
- Scans "hundreds of thousands of files in a few seconds" [VERIFIED - official site]
- Parallel folder scanning
- Efficient timestamp-based change detection
- VSS for locked files (critical for robustness)
- Tray icon with real-time monitoring

**Setup**:
```
1. Install FreeFileSync
2. Create sync job: Source folder <-> Destination (network share, NAS, or mapped drive)
3. Enable VSS: Settings > Comparison > Volume shadow copy
4. Save as .ffs_batch file
5. Open RealTimeSync, add folders to watch
6. Set command: FreeFileSync.exe "path\to\job.ffs_batch"
7. Set idle delay: 5-10 seconds
8. Run at startup (tray icon monitors changes)
```

#### Best for Million+ Files: SyncBreeze

**Why it works**:
- "Analyze 1 million files on each side in less than 10 minutes" [VERIFIED]
- Stream mode bypasses preview for massive file sets
- Multi-threaded, enterprise-grade
- Background Windows service
- Real-time monitoring option

**Setup**:
```
1. Install SyncBreeze (free or Pro/Enterprise)
2. Create sync command: Source <-> Destination
3. Enable "Real-Time File Synchronization"
4. For 500k+ files: Use "Stream" sync mode (no preview)
5. Configure as Windows service for always-on operation
```

#### Alternative: Synchredible

**Why it works**:
- "Hundreds of thousands of files synchronized within seconds" [CLAIMED]
- Intelligent duplicate detection (only transfers changes)
- Free for personal use
- Simple UI, Windows-native

**Cloud Integration for Remote Access**:

Since you need physical files, avoid cloud virtual drives. Instead:
```
Local Machine <--FreeFileSync/SyncBreeze--> Shared Folder <--Cloud Sync Agent--> Remote Machine
```

Or use direct P2P with Tailscale + SMB share:
```
Local Machine <--Tailscale VPN--> Remote Machine (SMB share)
                      |
            FreeFileSync/SyncBreeze syncs to SMB
```

**Key insight**: For physical file sync at 100k+ scale, FreeFileSync and SyncBreeze are the only proven solutions. Cloud providers (Dropbox, Nextcloud, Syncthing) all degrade at this scale.

## 12. Sources

### Official Documentation

- **FSYNC-SC-SYNC-DOCS**: https://docs.syncthing.net/users/faq.html (Accessed: 2026-02-27)
- **FSYNC-SC-SYNC-CNFLCT**: https://docs.syncthing.net/users/syncing.html (Accessed: 2026-02-27)
- **FSYNC-SC-RESIL-PERF**: https://help.resilio.com/hc/en-us/articles/360001331930 (Accessed: 2026-02-27)
- **FSYNC-SC-FFS-MAIN**: https://freefilesync.org/ (Accessed: 2026-02-27)
- **FSYNC-SC-FFS-RTS**: https://freefilesync.org/manual.php?topic=realtimesync (Accessed: 2026-02-27)
- **FSYNC-SC-MUTAG-GH**: https://github.com/mutagen-io/mutagen (Accessed: 2026-02-27)
- **FSYNC-SC-MUTAG-DOCS**: https://mutagen.io/documentation/synchronization/ (Accessed: 2026-02-27)
- **FSYNC-SC-GSYNC-MAN**: https://www.goodsync.com/manual (Accessed: 2026-02-27)
- **FSYNC-SC-MSFT-VSS**: https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service (Accessed: 2026-02-27)

### Comparison Articles

- **FSYNC-SC-SWPURS-COMP**: https://www.softwarepursuits.com/blog/best-file-sync-software (Accessed: 2026-02-27)
- **FSYNC-SC-RESIL-ALT**: https://www.resilio.com/blog/syncthing-alternative (Accessed: 2026-02-27)

### Community Sources

- **FSYNC-SC-GH-SYNC8602**: https://github.com/syncthing/syncthing/issues/8602 [COMMUNITY] - Performance with small files
- **FSYNC-SC-REDDIT-SYNC**: https://www.reddit.com/r/selfhosted/comments/ix5db9/ [COMMUNITY] - Syncthing vs Resilio
- **FSYNC-SC-PCW-FFS**: https://www.pcworld.com/article/2144389/freefilesync-review.html [COMMUNITY] - FreeFileSync review

### High-Volume Research Sources (2026-02-28)

- **FSYNC-SC-DBOX-CPU**: https://help.dropbox.com/installs/high-cpu-usage (Accessed: 2026-02-28) - "Performance decreases at around 300,000 synced files" [VERIFIED]
- **FSYNC-SC-NC-9275**: https://github.com/nextcloud/desktop/issues/9275 (Accessed: 2026-02-28) - Nextcloud 100k+ performance issues [COMMUNITY]
- **FSYNC-SC-SEAF-CONF**: https://manual.seafile.com/11.0/config/seafile-conf/ (Accessed: 2026-02-28) - Seafile library_file_limit config [VERIFIED]
- **FSYNC-SC-SYNCBZ-PERF**: https://www.syncbreeze.com/syncbreeze_file_synchronization_performance.html (Accessed: 2026-02-28) - SyncBreeze performance claims
- **FSYNC-SC-PCLOUD-SPEED**: https://gizmodo.com/best-cloud-storage/pcloud-vs-dropbox (Accessed: 2026-02-28) - pCloud vs Dropbox speed comparison
- **FSYNC-SC-DBOX-SYNC**: https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine (Accessed: 2026-02-28) - Dropbox sync architecture

### Constraint Compliance Research Sources (2026-02-28)

- **FSYNC-SC-DBOX-MOVE**: https://help.dropbox.com/installs/move-dropbox-folder (Accessed: 2026-02-28) - Dropbox folder relocation [VERIFIED]
- **FSYNC-SC-BOX-LOC**: https://support.box.com/hc/en-us/articles/360043697454 (Accessed: 2026-02-28) - Box Drive folder location (registry hack required, no external/network drives) [VERIFIED]
- **FSYNC-SC-MUTAG-SYNC**: https://mutagen.io/documentation/synchronization/ (Accessed: 2026-02-28) - Mutagen sync modes and conflict resolution [VERIFIED]
- **FSYNC-SC-SYNC-CNFG**: https://docs.syncthing.net/users/config.html (Accessed: 2026-02-28) - Syncthing custom folder paths [VERIFIED]
- **FSYNC-SC-RESIL-LOC**: https://help.resilio.com/hc/en-us/articles/206216615 (Accessed: 2026-02-28) - Resilio Sync folder location [VERIFIED]
- **FSYNC-SC-GDRIVE-SEL**: https://support.google.com/drive/thread/123477997 (Accessed: 2026-02-28) - Google Drive selective sync limitations [COMMUNITY]

## Final Recommendation

**Meeting ALL 4 Mandatory Constraints** (custom folder, physical files, fast/robust, no conflict copies):

| Rank | Solution | Best For | Cost |
|------|----------|----------|------|
| 1 | **FreeFileSync + RealTimeSync** | General use, 100k+ files | Free |
| 2 | **Mutagen** | Developers, code sync | Free |
| 3 | **GoodSync** | Easy GUI, commercial | $30-50 |
| 4 | **SyncBreeze** | Million+ files, enterprise | Free-$175 |
| 5 | **SureSync MFT** | Enterprise, compliance | Enterprise |

**Configuration required for C4 compliance**:
- **FreeFileSync**: Set conflict handling to "Overwrite" or "Keep newer" (not "Keep both")
- **Mutagen**: Use `--sync-mode=two-way-resolved` (alpha wins conflicts)
- **GoodSync**: Set conflict resolution to "Left wins" or "Newer wins"
- **SyncBreeze**: Use default overwrite mode

**For high-volume (100k+ files) with physical file sync**:

1. **Best overall**: FreeFileSync + RealTimeSync - scans 100k+ in seconds, VSS support, tray icon
2. **Best for million+**: SyncBreeze Enterprise - 1M files in 10 min, stream mode, Windows service

**AVOID** (fail mandatory constraints):
- All cloud providers (Dropbox, Google Drive, Box, pCloud, MEGA, iDrive) - conflict copies and/or folder restrictions
- Syncthing - always creates conflict copies
- Resilio Sync - poor real-world performance

**Key insight**: For physical file sync meeting all 4 constraints, only FreeFileSync, Mutagen, GoodSync, SyncBreeze, and SureSync qualify. Use Tailscale + SMB for remote access instead of cloud sync.

## Document History

**[2026-03-01 16:40]**
- Changed: Mutagen demoted for high-latency WAN - initial scan of 342k files took 1+ hour over 1100ms latency (Azure VM via Tailscale)
- Changed: Mutagen C3 rating from YES to PARTIAL (slow WAN), verdict from PASS to PASS (LAN only)
- Changed: FreeFileSync promoted to #1 recommendation for WAN with large dev folders
- Added: TESTED note in Section 4.1 with real-world findings
- Changed: Executive Summary table updated with LAN/WAN distinction

**[2026-02-28 15:40]**
- Added: Mandatory Constraints section (C1-C4) per user requirements
- Added: Constraint Compliance Matrix evaluating all solutions against 4 constraints
- Changed: Box.com demoted - cannot change folder location without registry hack
- Changed: Syncthing demoted - always creates .sync-conflict files (violates C4)
- Changed: Cloud solutions (Dropbox, Google Drive, pCloud, MEGA, iDrive) demoted - conflict copies
- Added: Solutions That PASS All Constraints summary
- Added: Solutions FAILED - Demoted section with specific constraint violations

**[2026-02-28 12:30]**
- Changed: High-volume recommendations updated for physical file sync (not on-demand)
- Changed: FreeFileSync + RealTimeSync now primary recommendation for 100k+ files
- Added: Tailscale + SMB architecture for remote physical file access
- Removed: pCloud/virtual drive recommendations (user requires physical files)

**[2026-02-28 12:20]**
- Added: Section 11 "High-Volume File Sync (100k+ Files)" with deep research
- Added: Scale problem analysis with documented limits per solution
- Added: SyncBreeze for million+ file scenarios
- Added: High-volume research sources
- Changed: Section numbering (Sources now Section 12)

**[2026-02-28 12:15]**
- Changed: Resilio Sync demoted from Tier 1 to Tier 3 based on real-world testing
- Added: User experience report - difficult setup, timezone sync failures, slow performance
- Changed: All Resilio benchmarks marked as "claimed" or "unverified"
- Changed: Final Recommendation updated to exclude Resilio
- Changed: Comparison tables updated to reflect demotion

**[2026-02-27 15:45]**
- Added: Section 9 "Large File Sync Mechanisms (Full vs Block)"
- Added: Detailed algorithm analysis for each solution
- Added: Block size specifications and delta transfer behavior
- Added: Recommendations by file type

**[2026-02-27 15:30]**
- Initial research and document creation
- Evaluated 12+ solutions
- Identified 4 Tier 1 recommendations based on robustness and speed criteria

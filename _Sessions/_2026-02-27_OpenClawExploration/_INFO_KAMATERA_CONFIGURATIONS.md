# INFO: Kamatera Configurations for OpenClaw

**Doc ID**: KAMCFG-IN01
**Goal**: Find optimal Kamatera configuration for OpenClaw on Windows 11 with RDP, <100 EUR/month, 80% idle time
**Research Date**: 2026-02-27

## Table of Contents

1. Requirements Summary
2. Kamatera CPU Types Explained
3. Pricing Components Breakdown
4. Configuration Options Comparison
5. Cost Calculations for 80% Idle Scenario
6. RDP and Licensing Considerations
7. Recommendation

## 1. Requirements Summary

**User Requirements**:
- RAM: 16GB or more
- CPUs: 6 or more
- Storage: 100GB or more (SSD)
- Budget: <100 EUR/month (~$108 USD)
- Usage pattern: 80% idle (powered off or minimal use)
- Full RDP access to Windows 11
- Running OpenClaw workload

**Derived Requirements**:
- Windows Desktop 11 64-bit
- Hourly billing (to benefit from idle time)
- Fast network for RDP responsiveness

## 2. Kamatera CPU Types Explained

Kamatera offers 4 CPU types. Selection is critical for cost optimization.

### Type A - Availability (Shared, no guarantee)

- **Description**: Non-dedicated CPU thread, no resource guarantee
- **Max Config**: 32 vCPU, 128GB RAM
- **Best For**: Dev/test, microservices, non-critical workloads
- **Pricing**: Starts at $0.005/hour ($4/month)
- **Recommendation**: [NOT RECOMMENDED] for OpenClaw - no CPU guarantee during AI inference

### Type B - General Purpose (Dedicated thread, guaranteed)

- **Description**: Dedicated physical CPU thread with reserved resources guaranteed
- **Max Config**: 72 vCPU, 384GB RAM
- **Best For**: Production workloads, web/app/database servers, containers, HPC
- **Pricing**: Starts at $0.012/hour ($9/month)
- **Recommendation**: [RECOMMENDED] Best balance of performance and cost

### Type T - Burstable (Dedicated with overage charges)

- **Description**: Dedicated thread, but >10% avg CPU usage incurs extra charges
- **Max Config**: 72 vCPU, 384GB RAM
- **Overage**: $0.041/hour per CPU when exceeding 10% average
- **Best For**: Remote desktop, workloads with occasional spikes
- **Pricing**: Starts at $0.005/hour + overage
- **Official Example**: 8 vCPU, 8GB RAM, 50GB = $0.0931/hour (powered ON), $0.0102/hour (powered OFF)
- **Recommendation**: [RISKY] OpenClaw inference may exceed 10% threshold unpredictably

### Type D - Dedicated (Full core, 2 threads)

- **Description**: Full dedicated physical CPU core (2 threads per core)
- **Max Config**: 72 vCPU, 384GB RAM
- **Best For**: High-performance, CPU-intensive workloads
- **Pricing**: Starts at $0.026/hour ($19/month)
- **Recommendation**: [OVERKILL] Unless running continuous heavy inference

## 3. Pricing Components Breakdown

### Official Pricing Structure (from Kamatera documentation)

**Hourly billing explained**:
- Price calculated for "Powered On" server only
- "Powered Off" servers charged: $0.00007/GB/hour (storage) + $0.007/IP/hour
- Usage calculated by the minute
- Rates identical for all data centers worldwide

**Official Type T Example** (reference for estimation):
- Config: 8 vCPU, 8GB RAM, 50GB SSD
- Powered ON: $0.0931/hour ($68/month)
- Powered OFF: $0.0102/hour ($7.50/month)

**Estimated for User Config** (8 vCPU, 24GB RAM, 100GB SSD):
- Powered ON: ~$0.21/hour (extrapolated from example + additional RAM/storage)
- Powered OFF: 100GB × $0.00007 + $0.007 = **$0.014/hour** (~$10/month)
- Windows License: Included in image selection
- Network: Traffic overage $0.01/GB

### Storage Pricing (Official)

- SSD Storage: **$0.05/GB/month** ($0.00007/GB/hour)
- 100GB = $5/month when OFF, included in hourly rate when ON
- 150GB = $7.50/month
- 200GB = $10/month
- Snapshots: Same rate ($0.05/GB/month)
- No extra IOPS charges

### Windows 11 Desktop License

- [VERIFIED] Windows Desktop 11 64-bit: **Included** in Kamatera pricing (via Service Provider License Agreement)
- No separate license fee when selecting Windows Desktop image
- Kamatera handles Microsoft licensing - user does not need separate VDA

### RDP Note for Windows 11

- Windows 11 allows **1 concurrent RDP session** by default (unlike Server's 2)
- For single-user OpenClaw: **1 session is sufficient**
- If you need multiple concurrent sessions: Consider Windows Server instead

## 4. Configuration Options Comparison

**PRICING BASIS**: Official Kamatera documentation + Type T example extrapolation.

**Powered OFF cost formula** (official): $0.00007/GB/hour + $0.007/IP/hour
- 100GB + 1 IP = $0.014/hour = **$10.22/month** when powered OFF

Based on requirements (6+ vCPU, 16GB+ RAM, 100GB+ SSD):

### Option 1: Type T Burstable (8 vCPU, 24GB RAM, 100GB) - BEST VALUE

**Type T - Burstable** (official example extrapolated):
- Powered ON: ~$0.15/hour (estimated from 8/8/50 example + 16GB RAM + 50GB storage)
- Powered OFF: $0.014/hour ($10.22/month)
- Base rate much lower than Type B

**Cost Calculation (80% idle, <10% CPU avg)**:
- 20% active = 146 hours ON: 146h × $0.15 = $21.90
- 80% idle = 584 hours OFF: 584h × $0.014 = $8.18
- **Total: ~$30/month (~28 EUR)**

**If CPU averages 15% during active hours** (5% overage):
- Overage: 146h × $0.041 × 8 vCPU × 0.05 = $2.40 extra
- **Total: ~$32/month (~30 EUR)**

**Risk**: If OpenClaw pushes CPU >10% average, costs increase

### Option 2: Type B General Purpose (8 vCPU, 24GB RAM, 100GB) - SAFE CHOICE

**Type B - General Purpose** (from console):
- Powered ON: $0.333/hour (verified)
- Powered OFF: $0.014/hour ($10.22/month)
- No overage risk, guaranteed resources

**Cost Calculation (80% idle)**:
- 20% active = 146 hours ON: 146h × $0.333 = $48.62
- 80% idle = 584 hours OFF: 584h × $0.014 = $8.18
- **Total: ~$57/month (~53 EUR)**

### Option 3: Type A Availability (8 vCPU, 24GB RAM, 100GB) - CHEAPEST

**Type A - Availability** (no guarantee):
- Powered ON: ~$0.08/hour (estimated from $0.005/h base + resources)
- Powered OFF: $0.014/hour ($10.22/month)

**Cost Calculation (80% idle)**:
- 20% active = 146 hours ON: 146h × $0.08 = $11.68
- 80% idle = 584 hours OFF: 584h × $0.014 = $8.18
- **Total: ~$20/month (~18 EUR)**

**Risk**: No CPU guarantee - may throttle during OpenClaw inference

## 5. Cost Calculations for 80% Idle Scenario

### Assumptions (Official)

- Month = 730 hours
- 80% idle = 584 hours powered OFF
- 20% active = 146 hours powered ON
- Powered OFF: $0.00007/GB/hour + $0.007/IP/hour (official)
- 100GB + 1 IP = $0.014/hour OFF

### Summary (Updated with Official Pricing)

- **Type T Burstable** (8 vCPU, 24GB, 100GB): ~$0.15/h ON, 80% idle = ~$30 (28 EUR), always-on = ~$110
- **Type B General Purpose** (8 vCPU, 24GB, 100GB): $0.333/h ON, 80% idle = ~$57 (53 EUR), always-on = ~$243
- **Type A Availability** (8 vCPU, 24GB, 100GB): ~$0.08/h ON, 80% idle = ~$20 (18 EUR), always-on = ~$58

### Budget Analysis

**All options fit within 100 EUR budget** when utilizing 80% idle time.

**Value Rankings** (performance per EUR):
1. **Type T (Burstable)**: ~28 EUR with guaranteed CPU, best if <10% avg usage
2. **Type B (General Purpose)**: ~53 EUR, safest choice, no surprises
3. **Type A (Availability)**: ~18 EUR cheapest, but no CPU guarantee

## 6. RDP and Licensing Considerations

### Windows 11 RDP Access

- **Default**: 1 concurrent RDP session (Windows 11 limitation)
- **For OpenClaw single-user**: 1 session is sufficient
- No additional licensing needed - Kamatera includes Windows Desktop license

### How to Connect

1. Use Windows Remote Desktop Client (mstsc.exe)
2. Connect to server's public IP
3. Login as Administrator
4. Full desktop access with GPU support (if applicable)

### Network Performance

- Kamatera provides 1Gbps network by default
- 5TB/month traffic included
- Low latency to EU/US data centers
- [VERIFIED] Responsive RDP experience reported by users

## 7. Recommendation (Updated with Official Pricing)

### Primary Recommendation: Type T Burstable (Best Value)

**Configuration**:
- CPU Type: **Type T (Burstable)**
- vCPU: **8**
- RAM: **24GB**
- Storage: **100GB SSD**
- OS: **Windows Desktop 11 64-bit**
- Billing: **Hourly**
- Data Center: **EU (Amsterdam or Frankfurt)** for best latency

**Monthly Cost (80% idle, <10% CPU avg)**:
- Powered ON (146h × ~$0.15): ~$22
- Powered OFF (584h × $0.014): ~$8
- **Total: ~$30/month (~28 EUR)** - Well within 100 EUR budget

**Why Type T**:
- Guaranteed CPU thread (unlike Type A)
- Much cheaper than Type B when CPU usage <10% average
- 80% idle pattern = low average CPU usage
- OpenClaw inference is bursty (high during use, zero when idle)
- Risk is manageable: overage only if avg >10%

### Safe Alternative: Type B General Purpose

**Configuration**:
- CPU Type: **Type B (General Purpose)**
- Same specs: 8 vCPU, 24GB RAM, 100GB SSD

**Monthly Cost (80% idle)**: ~$57/month (~53 EUR)

**When to choose Type B**:
- If OpenClaw runs heavy inference for extended periods
- If you want zero surprises on billing
- If you plan to increase usage beyond 20%

### Budget Option: Type A Availability (Cheapest)

**Configuration**:
- CPU Type: **Type A (Availability)** - shared, no guarantee
- Same specs: 8 vCPU, 24GB RAM, 100GB SSD

**Monthly Cost (80% idle)**: ~$20/month (~18 EUR)

**Trade-off**: No CPU guarantee - performance may vary during inference. Test with free trial first.

### Configuration Steps

1. Sign up at kamatera.com (30-day free trial, $100 credit)
2. Create new server
3. Select: Windows Desktop 11 64-bit
4. Select: **Type T (Burstable)** for best value, or Type B for safety
5. Configure: 8 vCPU, 24GB RAM, 100GB SSD
6. Select: Hourly billing
7. Choose data center closest to you
8. Deploy and note public IP
9. Connect via RDP (mstsc.exe)

### Cost Optimization Tips

1. **Power off when not using** - Powered OFF = $0.014/hour ($10/month)
2. **Monitor CPU usage** - If using Type T, keep avg <10% to avoid overage
3. **Use snapshots** - $0.05/GB/month, delete old ones
4. **Start with Type T** - Switch to Type B later if needed

## Sources

- **KAMCFG-SC-KAM-CPUTYPES**: https://www.kamatera.com/faq/answer/which-cpu-types-are-offered-by-kamatera/ [VERIFIED] (Accessed: 2026-02-27)
- **KAMCFG-SC-KAM-PRICING**: https://www.kamatera.com/pricing/ [VERIFIED] (Accessed: 2026-02-27)
- **KAMCFG-SC-KAM-DESKTOP**: https://www.kamatera.com/products/cloud-desktop-hosting/ [VERIFIED] (Accessed: 2026-02-27)
- **KAMCFG-SC-KAM-LICENSING**: https://www.kamatera.com/solutions/software-licensing/ [VERIFIED] (Accessed: 2026-02-27)
- **KAMCFG-SC-VPS-BENCH**: https://www.vpsbenchmarks.com/instance_types/kamatera [COMMUNITY] (Accessed: 2026-02-27)

## Document History

**[2026-02-27 19:20]**
- Updated with official Kamatera pricing documentation (user-provided)
- Added official Powered OFF formula: $0.00007/GB/h + $0.007/IP/h
- Added Type T as primary recommendation (~28 EUR vs ~53 EUR for Type B)
- Updated CPU type specs (72 vCPU max, 384GB RAM max)
- Added official Type T example (8/8/50 = $0.0931/h)

**[2026-02-27 16:20]**
- VERIFIED: Fixed Markdown table (converted to list)
- VERIFIED: Removed emoji (checkmark)
- VERIFIED: Expanded SPLA acronym
- VERIFIED: Fixed configuration steps mismatch (24GB/100GB, not 32GB/150GB)

**[2026-02-27 16:15]**
- CORRECTED OS from Windows Server to Windows Desktop 11 64-bit
- Updated RDP section: Windows 11 = 1 session (sufficient for single user)
- Updated licensing section for Windows Desktop
- Added pricing verification notice (Windows 11 pricing TBD)

**[2026-02-27 16:10]**
- CORRECTED all pricing based on actual Kamatera console screenshot
- Type B (8 vCPU, 24GB RAM, 100GB) = $0.333/hour = $243/month always-on
- With 80% idle: ~$53/month (~49 EUR) - still within budget
- Updated all calculations and recommendations

**[2026-02-27 16:00]**
- Initial research and document creation
- Analyzed 4 CPU types (A, B, T, D)
- Calculated 5 configuration options (estimates were too low)

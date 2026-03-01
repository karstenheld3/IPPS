# INFO: Windows Cloud Hosting - Flexible Pay-Per-Use Options

**Doc ID**: WCLHST-IN01
**Goal**: Find best-value Windows cloud VM hosting with flexible pricing that minimizes costs when not in use
**Research Date**: 2026-02-27
**Version Scope**: Current pricing as of 2026-02

## Table of Contents

1. Executive Summary
2. Evaluation Criteria (User + Pitfall-Derived)
3. Provider Deep Dive
4. Comparison Matrix
5. Pitfalls and Limitations
6. Recommendations
7. Sources

## 1. Executive Summary

**Research goal**: Find Windows cloud VM hosting with best value, flexible pay-per-use pricing that stops billing when turned off.

**Key finding**: No provider truly stops ALL billing when VM is off. All charge for storage when stopped. The difference is in compute billing and ease of deallocating.

**Top 2 Recommendations**:

- **Best Overall Value**: **Kamatera** - True per-minute billing, Windows license included, stops compute charges when powered off, excellent scaling UI
- **Best for Occasional Use**: **Azure (Deallocated)** - No compute charges when deallocated, good tooling, but storage + IP still charged

## 2. Evaluation Criteria

### User-Specified Criteria

- **Fast internet** - High bandwidth, low latency
- **Easy management UI** - Web console usability
- **Easy scaling** - Add CPU/RAM without migration
- **100% uptime** - Automatic updates without shutdown (NOTE: impossible for Windows - requires reboots)
- **Full admin access** - RDP with Administrator rights
- **Pay-per-use** - Minimal cost when offline
- **Flexible pricing** - Turn off = pay minimal

### Pitfall-Derived Criteria (From Research)

- **Windows license cost** - Often hidden; can double VM cost
- **Storage when stopped** - All providers charge for disk even when VM off
- **Static IP retention** - Charged separately when VM stopped
- **Egress costs** - Data transfer out can be expensive
- **Deallocate vs Stop** - Must deallocate (not just OS shutdown) to stop compute billing
- **Backup costs** - Often extra charges
- **Pricing complexity** - Simple vs confusing tiers
- **Minimum billing** - Some have 10-minute or 1-hour minimums

### Reality Check: 100% Uptime

**[VERIFIED]** Windows Server cannot achieve 100% uptime with automatic updates. Windows Update requires reboots for:
- Security patches (monthly Patch Tuesday)
- Feature updates
- Driver updates

**Mitigation options**:
- Use Azure Update Management to schedule reboots during off-hours
- Configure Windows Update to download but not auto-install
- Use VM Scale Sets with rolling updates (enterprise)

## 3. Provider Deep Dive

### 3.1 Kamatera

**Overview**: Israel-based cloud provider focused on flexible VPS hosting

**Pricing Model**: Per-minute billing (hourly servers)

**Windows Support**: [VERIFIED] Windows Server 2016/2019/2022 with license included

**Key Pricing** (2 vCPU, 4GB RAM, 40GB SSD):
- Hourly: ~$0.05/hour (~$36/month if always on)
- Windows license: Included in price
- Storage when off: ~$0.05/GB/month (~$2/month for 40GB)
- Bandwidth: 5TB included, $0.01/GB overage

**Stop Billing Behavior**:
- **Compute**: Stops immediately when powered off [VERIFIED]
- **Storage**: Continues (disk persists)
- **IP**: Continues if static IP reserved

**Scaling**: [VERIFIED] Hot-add CPU/RAM via control panel (requires reboot)

**Management UI**: Clean, modern, easy to use

**Pros**:
- True per-minute billing
- Windows license included (no separate charge)
- Easy scaling UI
- 30-day free trial with $100 credit
- 18 global data centers

**Cons**:
- Less enterprise features than Azure/AWS
- Smaller community
- Limited managed services

**Best For**: Users who want simple, flexible Windows hosting with minimal idle costs

### 3.2 Microsoft Azure

**Overview**: Enterprise cloud with comprehensive Windows integration

**Pricing Model**: Per-second billing (1-minute minimum)

**Windows Support**: [VERIFIED] Native, full integration, all Windows Server versions

**Key Pricing** (B2s: 2 vCPU, 4GB RAM):
- Pay-as-you-go: ~$0.0496/hour (~$36/month)
- Windows license: Included OR use Azure Hybrid Benefit (BYOL saves ~40%)
- Storage (P10 128GB SSD): ~$19.71/month (charged always)
- Static IP: ~$3.65/month (charged when VM stopped)

**Stop Billing Behavior**:
- **Stopped (from portal/API)**: Compute stops, storage continues [VERIFIED]
- **Stopped (from OS shutdown)**: Compute CONTINUES billing [VERIFIED - critical pitfall]
- Must use "Stop (Deallocate)" not just shutdown

**Scaling**: [VERIFIED] Resize VM via portal (requires reboot for most changes)

**Management UI**: Azure Portal - powerful but complex

**Pros**:
- Best Windows integration
- Hybrid Benefit for license savings
- Spot VMs for 60-90% savings
- Enterprise features (AD integration, compliance)
- Extensive tooling and automation

**Cons**:
- Complex pricing
- Easy to leave resources running accidentally
- Storage costs continue when stopped
- Must deallocate (not just stop) to avoid compute charges

**Best For**: Enterprise users, existing Microsoft customers, complex workloads

### 3.3 Amazon Web Services (AWS) EC2

**Overview**: Largest cloud provider with extensive Windows support

**Pricing Model**: Per-second billing (1-minute minimum)

**Windows Support**: [VERIFIED] Windows Server 2012-2022, license included

**Key Pricing** (t3.medium: 2 vCPU, 4GB RAM):
- On-Demand: ~$0.0528/hour (~$38/month)
- Windows license: Included
- EBS Storage (100GB gp3): ~$8/month (charged always)
- Elastic IP: Free when attached to running instance, $0.005/hour when detached

**Stop Billing Behavior**:
- **Stopped**: Compute stops, EBS storage continues [VERIFIED]
- **Terminated**: All billing stops (data lost)
- **Hibernated**: Memory saved to EBS, storage charged at higher rate

**Scaling**: [VERIFIED] Change instance type (requires stop/start)

**Management UI**: AWS Console - powerful but steep learning curve

**Pros**:
- Most instance type options
- Spot instances for 70-90% savings
- Savings Plans for predictable workloads
- Global presence (25+ regions)
- Mature ecosystem

**Cons**:
- Complex pricing with many variables
- Egress costs can surprise ($0.09/GB)
- EBS charges continue when stopped
- Learning curve for console

**Best For**: Users comfortable with AWS, need specific instance types, want Spot pricing

### 3.4 Google Cloud Platform (GCP)

**Overview**: Google's cloud with strong automation and networking

**Pricing Model**: Per-second billing (1-minute minimum)

**Windows Support**: [VERIFIED] Windows Server 2012-2022, license included

**Key Pricing** (e2-medium: 2 vCPU, 4GB RAM):
- On-Demand: ~$0.067/hour (~$49/month)
- Windows license: Additional ~$0.04/core/hour
- Persistent Disk (100GB SSD): ~$17/month (charged always)
- Static IP: $0.010/hour when not attached (~$7.30/month)

**Stop Billing Behavior**:
- **Stopped**: Compute stops, disk + IP continue [VERIFIED]
- **Suspended**: Memory preserved, charged for storage
- **Deleted**: All billing stops (data lost)

**Scaling**: [VERIFIED] Change machine type (requires stop)

**Management UI**: Cloud Console - clean, good UX

**Pros**:
- Sustained use discounts (automatic 30% after 25% month usage)
- Preemptible/Spot VMs (60-91% savings)
- Good networking performance
- Clean console UI

**Cons**:
- Windows licensing adds significant cost
- Higher base price than competitors
- Static IP charges add up
- Less Windows-specific features than Azure

**Best For**: Users already on GCP, want automatic sustained use discounts

### 3.5 Hetzner Cloud

**Overview**: German provider known for excellent value in Europe

**Pricing Model**: Hourly billing (capped at 672 hours/month)

**Windows Support**: [ASSUMED - Limited] No official Windows support. Must bring your own license and install manually.

**Key Pricing** (CX22: 2 vCPU, 4GB RAM, 40GB):
- Hourly: €0.0119/hour (~€8.49/month - cheapest!)
- Windows license: NOT included - must purchase separately (~€15-50/month)
- Storage: Included in VM price
- Traffic: 20TB included (EU), 1TB (US)

**Stop Billing Behavior**:
- **Deleted**: Stops billing
- **Stopped**: Still billed (reserves resources) [VERIFIED]

**Scaling**: [VERIFIED] Upgrade via panel (downgrade requires rebuild)

**Management UI**: Simple, clean, fast

**Pros**:
- Extremely low base prices
- Simple pricing model
- 20TB traffic included (EU)
- Good performance for price

**Cons**:
- **No official Windows support** - must self-manage
- Windows license separate and expensive
- Limited regions (EU + US East only)
- No stop-and-save option (must delete)
- Less enterprise features

**Best For**: Linux workloads, NOT recommended for Windows due to license complexity

## 4. Comparison Matrix

### Pricing Comparison (2 vCPU, 4GB RAM, 100GB SSD)

- **Kamatera**
  - Monthly (always on): ~$45
  - Windows license: Included
  - Cost when stopped: ~$5/month (storage)
  - Billing granularity: Per-minute

- **Azure (B2s)**
  - Monthly (always on): ~$55
  - Windows license: Included (or BYOL)
  - Cost when stopped: ~$23/month (storage + IP)
  - Billing granularity: Per-second

- **AWS EC2 (t3.medium)**
  - Monthly (always on): ~$46
  - Windows license: Included
  - Cost when stopped: ~$8/month (EBS)
  - Billing granularity: Per-second

- **GCP (e2-medium)**
  - Monthly (always on): ~$78
  - Windows license: Extra (~$29/month)
  - Cost when stopped: ~$24/month (disk + IP)
  - Billing granularity: Per-second

- **Hetzner (CX22)**
  - Monthly (always on): ~€8 + license
  - Windows license: ~€15-50/month extra
  - Cost when stopped: Full price (no stop option)
  - Billing granularity: Hourly

### Feature Comparison

- **Management UI Ease**
  - Kamatera: Excellent (simple, clean)
  - Azure: Good (powerful but complex)
  - AWS: Fair (steep learning curve)
  - GCP: Good (clean UI)
  - Hetzner: Excellent (minimal)

- **Scaling Ease**
  - Kamatera: Excellent (GUI, reboot required)
  - Azure: Good (portal, most need reboot)
  - AWS: Good (stop/start required)
  - GCP: Good (stop required)
  - Hetzner: Fair (upgrade only, downgrade needs rebuild)

- **True Pay-When-Off**
  - Kamatera: Yes (compute only)
  - Azure: Partial (must deallocate, storage charged)
  - AWS: Partial (EBS charged)
  - GCP: Partial (disk + IP charged)
  - Hetzner: No (delete to stop billing)

## 5. Pitfalls and Limitations

### Critical Pitfalls

1. **OS Shutdown != Deallocate** [VERIFIED]
   - Azure/AWS: Shutting down from within Windows does NOT stop compute billing
   - Must use cloud portal/API to deallocate
   - Easy to forget and leave running

2. **Storage Always Charged** [VERIFIED]
   - All providers charge for persistent disk when VM stopped
   - Only way to avoid: Delete disk (lose data)
   - Mitigation: Use smallest disk possible, snapshot and delete

3. **Windows License Costs** [VERIFIED]
   - Hetzner: No Windows support, BYOL expensive
   - GCP: Adds ~$0.04/core/hour on top of VM cost
   - Azure: Can use Hybrid Benefit if you have SA licenses

4. **Static IP Costs** [VERIFIED]
   - Azure: ~$3.65/month when VM stopped
   - GCP: ~$7.30/month when not attached
   - AWS: Free when attached, $3.60/month when detached
   - Mitigation: Release IP when not needed (IP will change)

5. **Egress Costs**
   - AWS: $0.09/GB (first 10TB/month)
   - Azure: $0.087/GB
   - GCP: $0.12/GB
   - Kamatera: $0.01/GB (after 5TB included)
   - Hetzner: Free up to 20TB (EU)

### Limitations

- **100% Uptime**: Not possible with Windows (requires reboots for updates)
- **Hot Scaling**: CPU/RAM changes require reboot on all providers
- **Live Migration**: Only enterprise tiers support transparent maintenance

## 6. Recommendations

### Primary Recommendation: Kamatera

**Best for**: Flexible pay-per-use Windows hosting with minimal idle costs

**Why**:
- True per-minute billing (compute stops when powered off)
- Windows license included (no hidden costs)
- Simple, easy-to-use management UI
- Easy scaling via control panel
- $100 free trial credit
- Lowest cost when stopped (~$5/month for storage only)

**Configuration for cost optimization**:
1. Choose "Hourly" billing (not monthly)
2. Use smallest disk size needed
3. Power off via Kamatera console (not Windows shutdown)
4. Release static IP if not needed

**Estimated cost** (moderate use, ~40 hours/week):
- Compute: ~$8/month (160 hours × $0.05)
- Storage: ~$5/month
- **Total: ~$13/month**

### Alternative Recommendation: Azure (Deallocated)

**Best for**: Enterprise users, Microsoft ecosystem, Hybrid Benefit license holders

**Why**:
- Best Windows integration
- Hybrid Benefit saves ~40% if you have SA licenses
- Spot VMs for 60-90% savings on interruptible workloads
- Excellent automation (auto-shutdown schedules)
- Enterprise compliance features

**Configuration for cost optimization**:
1. Use B-series (burstable) for variable workloads
2. Enable auto-shutdown schedule
3. Use Azure Hybrid Benefit if eligible
4. Consider Spot VMs for fault-tolerant workloads
5. Use Standard HDD instead of SSD if performance allows

**Estimated cost** (moderate use, auto-shutdown overnight):
- Compute (B2s, 12h/day): ~$18/month
- Storage (128GB Standard HDD): ~$5/month
- Static IP: ~$3.65/month
- **Total: ~$27/month**

## 7. Sources

### Official Documentation

- **WCLHST-SC-AZ-VMPR**: https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/ (Accessed: 2026-02-27)
- **WCLHST-SC-AZ-STATES**: https://learn.microsoft.com/en-us/azure/virtual-machines/states-billing (Accessed: 2026-02-27)
- **WCLHST-SC-AWS-EC2**: https://aws.amazon.com/ec2/pricing/on-demand/ (Accessed: 2026-02-27)
- **WCLHST-SC-GCP-VMPR**: https://cloud.google.com/compute/vm-instance-pricing (Accessed: 2026-02-27)
- **WCLHST-SC-HETZ-WIN**: https://docs.hetzner.com/robot/general/pricing/windows-2025-pricing/ (Accessed: 2026-02-27)
- **WCLHST-SC-KAM-PR**: https://www.kamatera.com/pricing/ (Accessed: 2026-02-27)

### Community Sources

- **WCLHST-SC-DO-AZPR**: https://www.digitalocean.com/resources/articles/azure-vm-pricing [COMMUNITY] - Azure pricing challenges
- **WCLHST-SC-MS-DEALLOC**: https://learn.microsoft.com/en-us/answers/questions/2107793/ [COMMUNITY] - Deallocate billing explained
- **WCLHST-SC-VULTR-BILL**: https://docs.vultr.com/support/platform/billing/are-stopped-instances-still-billed-on-vultr [COMMUNITY] - Vultr billing when stopped
- **WCLHST-SC-HA-KAM**: https://hostadvice.com/hosting-company/kamatera-reviews/ [COMMUNITY] - Kamatera review

## Document History

**[2026-02-27 15:30]**
- Initial research and document creation
- Evaluated 5 providers: Kamatera, Azure, AWS, GCP, Hetzner
- Identified key pitfalls: deallocate vs stop, storage costs, license costs
- Recommended Kamatera (best value) and Azure (best enterprise)

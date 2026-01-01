# Verify $0.00 Monthly Cost - Cost Verification Guide

## 🎯 Goal: Confirm Always-Free Configuration is Working

This guide shows you how to verify that your Oracle Cloud Infrastructure (OCI) instance is **100% Always-Free** and will cost **$0.00/month**.

---

## 📊 What We'll Verify

1. ✅ Instance is using Always-Free shape (`VM.Standard.A1.Flex`)
2. ✅ Instance is in Always-Free region (`us-ashburn-1` or `us-phoenix-1`)
3. ✅ Storage is within Always-Free limits (≤200GB)
4. ✅ No PAYG resources are being used
5. ✅ Bill shows **$0.00**

---

## 🔍 Step 1: Verify Instance Details in OCI Console

### Access OCI Console
1. Go to **https://cloud.oracle.com**
2. Sign in to your Oracle account
3. Verify region (top-right) is **us-ashburn-1** or **us-phoenix-1**

### Check Instance Details
1. Navigate to **"Compute"** → **"Instances"**
2. Find your instance (e.g., `github-actions-ampere-instance`)
3. Click on the instance name to view details
4. Verify the following:

#### ✅ **Shape Configuration**
- **Shape:** Must show `VM.Standard.A1.Flex`
- **OCPU:** Should show **4**
- **Memory:** Should show **24 GB**
- **Architecture:** Should show **ARM**

*If you see `VM.Standard.E2.1.Micro` (AMD), you need to recreate with correct shape*

#### ✅ **Region and Availability Domain**
- **Region:** Must be **us-ashburn-1** or **us-phoenix-1**
- **Availability Domain:** Should show AD-1, AD-2, or AD-3
- **Compartment:** Should be in your Always-Free compartment

*If region is NOT one of these two, you're using PAYG!*

#### ✅ **Storage Configuration**
1. In instance details, scroll to **"Boot Volume"** section
2. Click on the boot volume name
3. Verify:
   - **Size:** Should be **50GB** (or your configured size, max 200GB)
   - **Performance:** Should show **Lower Cost** (not Balanced/High)

*If size > 200GB, you're exceeding Always-Free limits*

---

## 💰 Step 2: Verify Cost Analysis

### Access Cost Analysis
1. In OCI Console, go to **"Billing"** → **"Cost Analysis"**
2. Set the date range to **"Last 30 days"** or **"Current month"**
3. Look for the cost summary

### Expected Results

#### ✅ **Correct Configuration Shows:**
```
Total Cost: $0.00
Service Charges: $0.00
Always-Free Resources: (Your instance listed)
```

#### ❌ **If You See Charges:**
```
Total Cost: $X.XX (any amount > $0.00)
Service Charges: Compute - $X.XX
```

**This indicates PAYG resources! Stop immediately!**

### What to Check for $0.00 Bill

1. **Total is exactly $0.00**
2. **No compute charges listed**
3. **No storage charges listed** (within Always-Free limits)
4. **No network charges** (assuming within free tier)

### Advanced Cost Analysis

1. Click **"Chart"** or **"Table"** view
2. Group by **Service**
3. Expected breakdown:
   - **Compute:** $0.00 (Always-Free)
   - **Storage:** $0.00 (Always-Free)
   - **Total:** $0.00

---

## 📋 Step 3: Review Always-Free Resource Usage

### Check Always-Free Limits

1. In OCI Console, go to **"Governance"** → **"Limits, Quotas and Usage"**
2. Select **"Always-Free Resources"** tab
3. Review your usage:

#### ✅ **Always-Free Resources Should Show:**

| Resource | Limit | Usage | Available |
|----------|-------|-------|-----------|
| **Compute Instances (ARM)** | 2 | 1 | 1 |
| **Storage Volume (GB)** | 200 | 50 | 150 |
| **Autonomous Database** | 2 | 0 | 2 |
| **Load Balancer** | 1 | 0 | 1 |

*If any resource shows "PAYG" or charges, investigate immediately!*

---

## 🔔 Step 4: Set Up Billing Alerts (Optional but Recommended)

### Create Cost Alert

1. **OCI Console** → **"Billing"** → **"Cost Management"**
2. Click **"Cost Alerts"** → **"Create Cost Alert"**
3. Configure:
   - **Alert Type:** "Budget"
   - **Budget:** $0.01 (one cent)
   - **Threshold:** 100% (alert when exceeds $0.01)
   - **Notifications:** Add your email
4. Click **"Create Alert"**

### What This Does
- **Immediate notification** if ANY charge appears
- **Early warning** of accidental PAYG usage
- **Peace of mind** for Always-Free verification

---

## 📧 Step 5: Check Billing Notifications

### Email Notifications from Oracle

Oracle will send emails about:
1. **New invoice available** (monthly)
2. **Any charges incurred**
3. **Payment method issues**
4. **Service limit changes**

**Always-Free accounts:**
- Receive "$0.00 invoice available" monthly
- No charges should appear
- If you see charges, check OCI Console immediately

---

## 📄 Step 6: Download and Review Invoice

### Access Invoice
1. **OCI Console** → **"Billing"** → **"Invoices"**
2. Find latest invoice
3. Click **"Download PDF"** or **"View Online"**

### Expected Invoice Content

#### ✅ **Always-Free Invoice Shows:**
```
Oracle Cloud Invoice
Total Amount Due: $0.00 USD
Payment Method: Not required

Services:
- Oracle Cloud Free Tier Services: $0.00
```

#### ❌ **PAYG Invoice Would Show:**
```
Oracle Cloud Invoice
Total Amount Due: $X.XX USD
Payment Method: Credit Card Required

Services:
- COMPUTE: $X.XX
- STORAGE: $X.XX
```

---

## 🚨 Step 7: Troubleshooting High Charges

### If You See Unexpected Charges

#### Common Causes
1. **Wrong shape selected** (not VM.Standard.A1.Flex)
2. **Wrong region** (not us-ashburn-1 or us-phoenix-1)
3. **Storage exceeded 200GB**
4. **Used PAYG compartment**
5. **Created non-free resources**

#### Immediate Actions

1. **Stop instance immediately** (terminate if needed)
2. **Check which resource incurred charges**
3. **Delete all non-Always-Free resources**
4. **Contact Oracle Support** for billing investigation
5. **Review and fix configuration**
6. **Recreate instance with correct Always-Free settings**

#### Prevent Future Charges

- **Never change shape** to non-A1.Flex
- **Never change region** to non-Always-Free
- **Monitor storage usage** (stay under 200GB)
- **Only create resources in Always-Free compartment**
- **Use this GHA workflow exclusively** (verified Always-Free)

---

## 🎯 Step 8: Monthly Verification Routine

### Set Monthly Reminder

Do this **once a month** to ensure ongoing compliance:

1. **1st of each month:**
   - Log into OCI Console
   - Check Cost Analysis (should be $0.00)
   - Review invoice (should be $0.00)
   - Check Always-Free resource usage

2. **Weekly (optional):**
   - Quick glance at instance status
   - Verify boot volume size hasn't grown unexpectedly
   - Check for any unusual activity

3. **After any changes:**
   - Verify changes didn't affect Always-Free status
   - Check cost impact immediately
   - Rollback if charges appear

---

## 📊 Always-Free Cost Calculator

### Your Configuration (Example)

| Resource | Quantity | Unit Cost | Always-Free Included | Your Cost |
|----------|----------|-----------|---------------------|-----------|
| **VM.Standard.A1.Flex** | 4 OCPU | $0.01/hour | 4 OCPU | $0.00 |
| **Memory** | 24 GB | $0.0015/hour | 24 GB | $0.00 |
| **Storage** | 50 GB | $0.025/GB/month | 200 GB | $0.00 |
| **Network (egress)** | 500 GB | $0.0085/GB | 10 TB | $0.00 |
| **Total** | | | | **$0.00** |

**As long as you stay within these limits, your cost remains $0.00!**

---

## ✅ Confirmation Checklist

Use this after deployment:

- [ ] OCI Console shows **$0.00** in Cost Analysis
- [ ] Instance shape is **VM.Standard.A1.Flex**
- [ ] Region is **us-ashburn-1** or **us-phoenix-1**
- [ ] Storage is **≤200GB** total
- [ ] No unexpected resources in compartment
- [ ] Billing alerts set up (optional)
- [ ] Monthly cost verified as **$0.00**
- [ ] Invoice shows **$0.00 due**

If all checked: **Congratulations! Your configuration is Always-Free compliant! 🎉**

---

## 🆘 If Something Looks Wrong

### Contact Oracle Support
1. **OCI Console** → **"Help"** → **"Support"**
2. Create ticket: **"Billing Question - Always-Free"**
3. Provide:
   - Instance OCID
   - Screenshots of unexpected charges
   - Description of configuration
4. Request: **"Investigate Always-Free compliance issue"**

### Community Help
- **GitHub Issues:** Create issue on this repository
- **Reddit:** r/oraclecloud community
- **Discord:** Self-hosting communities
- **Documentation:** https://guides.viren070.me/selfhosting/oracle

---

## 📚 Additional Resources

- **Setup Guide:** [ALWAYS_FREE_SETUP.md](./ALWAYS_FREE_SETUP.md)
- **CPU Details:** [AMPERE_CPU_EXPLAINED.md](./AMPERE_CPU_EXPLAINED.md)
- **Pre-Flight:** [PREFLIGHT_CHECKLIST.md](./PREFLIGHT_CHECKLIST.md)
- **Secrets Setup:** [GITHUB_SECRETS_GUIDE.md](./GITHUB_SECRETS_GUIDE.md)

---

**Remember:** Regular verification ensures you stay Always-Free forever! 🛡️
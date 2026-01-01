# Oracle Always-Free Tier Comprehensive Setup Guide

## 🚨 CRITICAL: Verified $0.00/Month Configuration

This guide ensures your Oracle Cloud Infrastructure (OCI) instance remains **100% free forever** with **ZERO PAYG (Pay-As-You-Go) charges**.

**Reference Guide:** https://guides.viren070.me/selfhosting/oracle

---

## ✅ What You Get (Always-Free Tier)

- **Shape:** VM.Standard.A1.Flex (Ampere ARM CPU)
- **CPU:** 4 OCPU (Ampere Computing ARM64 processor)
- **Memory:** 24 GB RAM
- **Storage:** Up to 200GB total (all volumes combined)
- **Regions:** us-ashburn-1 or us-phoenix-1 ONLY
- **Operating System:** Canonical Ubuntu 22.04 LTS
- **Cost:** **$0.00/month guaranteed** (if configuration maintained)

---

## ⚠️ CRITICAL SAFETY WARNINGS

### **NEVER DO THESE (Will Trigger PAYG Charges):**

❌ **Never change compute shape** - Only use `VM.Standard.A1.Flex`  
❌ **Never use other regions** - Only `us-ashburn-1` or `us-phoenix-1`  
❌ **Never exceed 200GB storage** - Total across ALL volumes  
❌ **Never accept PAYG upgrade** during Oracle signup  
❌ **Never create resources in non-free compartments**  
❌ **Never change boot volume above 200GB** in code  

### **IMPORTANT REMINDERS:**

✅ **2 ARM instances maximum** on Always-Free tier  
✅ **Instance stops if limits exceeded** (NO charges, just stops)  
✅ **Bandwidth usually free** for Always-Free tier  
✅ **Exit anytime** - No lock-in, no charges  

---

## 📋 Oracle Account Creation (Zero PAYG Risk)

### Step 1: Sign Up for Oracle Cloud Free Tier

1. Go to **https://www.oracle.com/cloud/free/**
2. Click **"Start for free"**
3. Fill in your information

### ⚠️ CRITICAL: Avoid PAYG During Signup

During signup, Oracle will show **PAYG (Pay-As-You-Go) upgrade prompts**. **SKIP THEM ALL:**

- Look for **"Always-Free Tier"** or **"Free Tier Only"** option
- **DECLINE** any "upgrade to PAYG" offers
- **CANCEL** if you accidentally click PAYG
- Verify account type shows **"Always-Free"** not **"PAYG"**

**If you see billing information/credit card prompts beyond the initial verification, you may be in the wrong signup flow. Start over and choose "Always-Free Tier."**

### Step 2: Verify Account Type

After signup:

1. Log into OCI Console: **https://cloud.oracle.com**
2. Go to **"Billing"** → **"Cost Analysis"**
3. Verify it shows **"$0.00"** or **"Always-Free"**
4. Check **"Service Limits"** shows Always-Free tier

---

## 🔑 OCI API Configuration

### Step 3: Generate API Key

1. In OCI Console, go to:
   - **"Identity"** → **"Users"** → **Your Username**
   - Click **"API Keys"** on left sidebar
   - Click **"Add API Key"**
   - Choose **"Generate API Key Pair"**
   - Click **"Download Private Key"** (save as `oci_api_key.pem`)

### Step 4: Collect Required Information

On the same API Key page, note down:

- **User OCID** (starts with `ocid1.user.oc1..`)
- **Tenancy OCID** (starts with `ocid1.tenancy.oc1..`)
- **Fingerprint** (format: `aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp`)

### Step 5: Verify Region

In OCI Console:
- Check top-right region selector
- **Must be:** `us-ashburn-1` or `us-phoenix-1`
- If different, **switch before proceeding**

---

## 🛡️ GitHub Secrets Configuration

### Step 6: Add Secrets to GitHub Repository

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets (ALL REQUIRED):

| Secret Name | Value | Example |
|------------|-------|---------|
| `OCI_USER_ID` | Your User OCID | `ocid1.user.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `OCI_TENANCY_ID` | Your Tenancy OCID | `ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `OCI_FINGERPRINT` | API Key Fingerprint | `aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp` |
| `OCI_PRIVATE_KEY` | **Full Private Key** | Copy ENTIRE 27-line key from `oci_api_key.pem` |
| `OCI_REGION` | **Always-Free Region** | `us-ashburn-1` **or** `us-phoenix-1` |
| `DISCORD_WEBHOOK` | (Optional) Discord webhook | `https://discord.com/api/webhooks/...` |

### ⚠️ CRITICAL: Private Key Format

When adding `OCI_PRIVATE_KEY`:

1. Open `oci_api_key.pem` file
2. Copy **ENTIRE** contents including:
   
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQ... (many lines)
-----END PRIVATE KEY-----
```

3. Paste **exactly as-is** into GitHub secret value
4. **Include all line breaks**

**Mistakes here cause authentication failures!**

---

## 🚀 Launch Your Always-Free Instance

### Step 7: Run GitHub Actions Workflow

1. Go to **Actions** tab in GitHub
2. Click **"Oracle Always-Free VPS Signup"** workflow
3. Click **"Run workflow"**
4. (Optional) Customize:
   - **Instance name** (default: `github-actions-ampere-instance`)
   - **Availability Domain** (default: `AD-1`)
   - **Boot volume size** (default: `50GB`, max: `200GB`)
5. Click **"Run workflow"**

### Step 8: Monitor Progress

- Workflow runs up to **330 minutes** (5.5 hours)
- Auto-retries every **60 seconds** until success
- Check **"Actions"** tab for real-time logs
- On success: Downloads `INSTANCE_CREATED` file

---

## 💰 Verify $0.00 Monthly Cost

### Step 9: Confirm Always-Free Billing

After instance creation:

1. Go to **OCI Console** → **Billing** → **Cost Analysis**
2. Verify **Total: $0.00**
3. Check **"Always-Free Resources"** section
4. Should see your instance listed there

### Step 10: Set Up Billing Alerts (Optional but Recommended)

1. **OCI Console** → **Billing** → **Cost Management**
2. Create **Cost Alert** with threshold **$0.01**
3. If triggered, check for accidental PAYG resources
4. **You will receive email if any charges appear**

---

## 📊 Always-Free Tier Limits Reference

### Compute Resources
- **2x ARM instances** (max)
- **4 OCPU per instance** (Ampere ARM)
- **24 GB RAM per instance**
- **Always-Free forever**

### Storage Resources
- **200GB max total** (all volumes combined)
- **Includes:** Boot volumes, block volumes
- **If exceeded:** Instance stops (NO charges)

### Networking
- **1x Load Balancer** (optional)
- **10TB outbound** bandwidth/month
- **Usually free** for Always-Free tier

### What Happens If You Exceed Limits?

**GOOD NEWS:** You will **NOT** be charged!

- Instance **stops running**
- OCI sends notification
- Fix the issue (reduce usage)
- Restart instance
- **Still $0.00**

---

## 🔄 What About the E2.Micro Shape?

**IMPORTANT: VM.Standard.E2.1.Micro is NOT Always-Free**

- AMD-based (not Ampere ARM)
- **May trigger PAYG charges**
- **Deprecated in Oracle documentation**
- **This workflow REMOVES E2.Micro option**

**Your safest option: ALWAYS use VM.Standard.A1.Flex**

---

## 🆘 Troubleshooting

### "Invalid OCI Configuration"

- Check all GitHub secrets are set
- Verify private key format (include all lines)
- Confirm region in OCI_CONFIG matches secrets

### "Region Not Always-Free Eligible"

- OCI_REGION must be: `us-ashburn-1` or `us-phoenix-1`
- Check Console → top-right region selector
- Change if needed

### "Shape Not Always-Free Eligible"

- OCI_COMPUTE_SHAPE must be: `VM.Standard.A1.Flex`
- Check GitHub workflow is using correct shape
- Verify code hasn't been modified

### "Boot Volume Exceeds Limit"

- BOOT_VOLUME_SIZE must be ≤ 200GB
- Default 50GB works fine for most use cases

### "Authentication Failed"

- Verify OCI_PRIVATE_KEY format
- Check fingerprint matches API key
- Confirm user has compute permissions

---

## 📚 Additional Resources

- **Ampere CPU Architecture:** [AMPERE_CPU_EXPLAINED.md](./AMPERE_CPU_EXPLAINED.md)
- **Pre-Flight Checklist:** [PREFLIGHT_CHECKLIST.md](./PREFLIGHT_CHECKLIST.md)
- **Cost Verification:** [COST_VERIFICATION.md](./COST_VERIFICATION.md)
- **GitHub Secrets Guide:** [GITHUB_SECRETS_GUIDE.md](./GITHUB_SECRETS_GUIDE.md)
- **Reference Guide:** https://guides.viren070.me/selfhosting/oracle

---

## ❓ Frequently Asked Questions

### Q: Will I ever be charged?
**A:** NO, if you follow this guide exactly. The configuration is verified $0.00/month.

### Q: What if Oracle changes the Always-Free tier?
**A:** Existing instances remain free. Check Oracle announcements for policy changes.

### Q: Can I upgrade to paid later?
**A:** Yes, but you'll need to modify configuration (and this guide won't apply).

### Q: Is the Ampere ARM CPU powerful enough?
**A:** 4 OCPU with 24GB RAM is excellent for personal projects, Docker containers, development servers.

### Q: What happens if workflow fails after 330 minutes?
**A:** Check logs, verify secrets, ensure Always-Free capacity. Retry the workflow.

### Q: Can I run this multiple times?
**A:** Yes, but max 2 ARM instances total on Always-Free. Workflow will skip if already running.

---

## ⚖️ Legal & Disclaimer

This guide is based on Oracle's publicly documented Always-Free tier as of 2024. Always verify current Oracle terms at:
- https://www.oracle.com/cloud/free/
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm

**Not affiliated with Oracle Corporation.**

---

## 🤝 Support & Contributions

- **Issues:** Create GitHub issue for problems
- **Pull Requests:** Welcome for improvements
- **Documentation:** Help improve this guide

**Remember:** Always verify $0.00 cost in OCI Console after deployment!
# Oracle Always-Free Pre-Flight Checklist

⚠️ **DO NOT RUN GITHUB ACTIONS WORKFLOW UNTIL ALL ITEMS ARE CHECKED**

This checklist ensures your configuration is 100% Always-Free compliant and prevents accidental PAYG charges.

---

## 📋 Oracle Account Setup

### Account Verification
- [ ] Created OCI account with **Always-Free tier** (NOT PAYG)
- [ ] Verified account type shows **"Always-Free"** in OCI Console
- [ ] Confirmed region is **ca-toronto-1**, **us-ashburn-1**, or **us-phoenix-1**
- [ ] Checked Billing → Cost Analysis shows **$0.00**
- [ ] Did NOT accept any PAYG upgrade offers during signup
- [ ] Service Limits show "Always-Free" tier enabled

### API Key Generation
- [ ] Generated API key from OCI Console
  - Identity → Users → Your Username → API Keys
- [ ] Downloaded private key file (saved as `oci_api_key.pem`)
- [ ] Copied all three required OCIDs:
  - [ ] User OCID (starts with `ocid1.user.oc1..`)
  - [ ] Tenancy OCID (starts with `ocid1.tenancy.oc1..`)
  - [ ] Fingerprint (format: `aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp`)
- [ ] Private key file saved securely, not shared
- [ ] Verified region in OCI Console (top-right) is Always-Free region

---

## 🔐 GitHub Secrets Configuration

### Critical Secrets (ALL Required)
- [ ] `OCI_USER_ID` set with complete User OCID
- [ ] `OCI_TENANCY_ID` set with complete Tenancy OCID
- [ ] `OCI_FINGERPRINT` set with API key fingerprint
- [ ] `OCI_PRIVATE_KEY` set with **entire 27-line private key** (including BEGIN/END lines)
- [ ] `OCI_REGION` set to **ca-toronto-1**, **us-ashburn-1**, or **us-phoenix-1**
- [ ] `DISCORD_WEBHOOK` (optional) set if Discord notifications wanted

### Secret Verification
- [ ] NO missing secrets (all 5 required secrets populated)
- [ ] Private key pasted **exactly** as downloaded (no missing lines)
- [ ] No extra spaces or characters in OCID values
- [ ] Region is **exactly** one of the Always-Free regions (`ca-toronto-1`, `us-ashburn-1`, `us-phoenix-1`)
- [ ] No "placeholder" values (like "your_user_ocid_here")

---

## 🛠️ Configuration Understanding

### Always-Free Tier Knowledge
- [ ] Understand **VM.Standard.A1.Flex is the ONLY Always-Free shape**
- [ ] Know that **E2.Micro can trigger PAYG charges** (removed from workflow)
- [ ] Understand **ca-toronto-1, us-ashburn-1, and us-phoenix-1 are the allowed Always-Free regions in this repo**
- [ ] Know **max storage is 200GB total** across all volumes
- [ ] Understand **boot volume minimum is 50GB**
- [ ] Know **4 OCPU + 24GB RAM = $0.00/month**
- [ ] Understand **if limits exceeded, instance STOPS (no charges)**
- [ ] Know **max 2 ARM instances** on Always-Free tier

### Cost Awareness
- [ ] Verified OCI Cost Analysis shows **$0.00**
- [ ] Know where to find Cost Analysis (OCI Console → Billing)
- [ ] Understand how to set billing alerts ($0.01 threshold)
- [ ] Know the difference between Always-Free vs PAYG
- [ ] Understand that changing shape/region triggers charges

### GitHub Actions Workflow
- [ ] Read the complete workflow file (`.github/workflows/oci-vps-signup.yml`)
- [ ] Understand workflow validates Always-Free before execution
- [ ] Know workflow job timeout is 350 minutes (GitHub limit) and scheduled runs cap the script runtime to ~20 minutes (to save minutes)
- [ ] Understand auto-retry happens every 60 seconds
- [ ] Know workflow locks shape to VM.Standard.A1.Flex
- [ ] Understand region validation occurs during execution
- [ ] Know logs are uploaded as artifacts on completion

---

## 📖 Documentation Review

### Required Reading
- [ ] Read **ALWAYS_FREE_SETUP.md** completely
- [ ] Read **AMPERE_CPU_EXPLAINED.md** to understand ARM64
- [ ] Reviewed **COST_VERIFICATION.md** for billing verification
- [ ] Understand **PREFLIGHT_CHECKLIST.md** (this document)

### Code Review (Important!)
- [ ] Reviewed changes to **main.py** Always-Free validation
- [ ] Verified `ALWAYS_FREE_SHAPES` only contains VM.Standard.A1.Flex
- [ ] Checked `ALWAYS_FREE_REGIONS` is restricted (ca-toronto-1, us-ashburn-1, us-phoenix-1)
- [ ] Confirmed `ALWAYS_FREE_MAX_STORAGE_GB = 200`
- [ ] Verified `validate_always_free_compliance()` exists and is called first
- [ ] Checked GitHub workflow enforces Always-Free settings

---

## 🎯 Pre-Launch Verification

### Manual Configuration Check
Run these checks **before** launching workflow:

```bash
# Check all secrets are set in GitHub
echo "Checks to perform manually:"
echo "1. Go to repo → Settings → Secrets → Actions"
echo "2. Verify all 5 required secrets exist"
echo "3. Verify OCI_REGION is ca-toronto-1, us-ashburn-1, or us-phoenix-1"
echo "4. Verify OCI_PRIVATE_KEY is full 27-line key"
```

### Expected Values Confirmation
- [ ] `OCI_COMPUTE_SHAPE` will be forced to **VM.Standard.A1.Flex**
- [ ] `OCI_REGION` will be validated against Always-Free regions
- [ ] `BOOT_VOLUME_SIZE` will be checked against 200GB limit
- [ ] Workflow will **FAIL** if any non-compliant setting detected
- [ ] Default boot volume is **50GB** (well within limit)

### Failure Scenarios Understood
- [ ] If wrong shape: **Workflow FAILS before creating instance**
- [ ] If wrong region: **Workflow FAILS during validation**
- [ ] If storage too high: **Workflow FAILS with clear error**
- [ ] If secrets missing: **Workflow FAILS with authentication error**
- [ ] If capacity issues: **Retries automatically for 330 minutes**

---

## 🚀 Launch Readiness

### Final Checklist
- [ ] All GitHub secrets configured (5 required + 1 optional)
- [ ] Oracle account verified as Always-Free ($0.00 in Cost Analysis)
- [ ] Region is us-ashburn-1 or us-phoenix-1
- [ ] API key generated and working
- [ ] Understand shape is locked to VM.Standard.A1.Flex
- [ ] Know boot volume will be 50GB (default)
- [ ] Understand this will cost $0.00/month if configured correctly
- [ ] Know how to verify bill shows $0.00 after deployment
- [ ] Understand Ampere ARM64 is 100% compatible with Linux
- [ ] Committed to NEVER changing Always-Free settings

### Support Resources Ready
- [ ] Bookmarked: Oracle Always-Free documentation
- [ ] Bookmarked: https://guides.viren070.me/selfhosting/oracle
- [ ] Know how to check OCI Console for resource usage
- [ ] Understand workflow logs location (Actions tab)
- [ ] Know artifacts are uploaded after completion

---

## 🚨 EMERGENCY: What If Something Goes Wrong?

### If You See Charges on Bill
1. **STOP** - Do not panic
2. Check OCI Console → Billing → Cost Analysis
3. Identify which resource incurred charges
4. **Terminate** any non-Always-Free resources immediately
5. Contact Oracle Support if charges are unexpected
6. Review configuration to prevent recurrence

### If Workflow Fails
1. Check **Actions** tab for error logs
2. Look for "Always-Free validation failed" messages
3. Fix configuration issues indicated in logs
4. Re-run workflow after fixes
5. Create GitHub issue if problem persists

### If Instance Won't Start
1. Check OCI Console → Compute → Instances
2. Look at instance state and error messages
3. Verify you're within Always-Free limits
4. Check boot volume size (≤200GB)
5. Try different availability domain (AD-1, AD-2, AD-3)

---

## ✨ Success Indicators

### When Everything Works
- [ ] Workflow completes successfully (green checkmark)
- [ ] `INSTANCE_CREATED` file generated
- [ ] OCI Console shows running instance
- [ ] Billing shows **$0.00**
- [ ] Instance details in workflow artifacts
- [ ] SSH keys available for login

### Post-Launch Verification
After successful deployment:
- [ ] Instance state is **"RUNNING"** in OCI Console
- [ ] Cost Analysis shows **$0.00**
- [ ] Instance is in **Always-Free** compartment
- [ ] Can SSH into instance (if public IP assigned)
- [ ] All services working as expected

---

## 🎯 Declaration of Readiness

**By proceeding to run the GitHub Actions workflow, you confirm:**

- [ ] I have read and understood ALL warnings about PAYG charges
- [ ] My configuration is 100% Always-Free compliant
- [ ] All GitHub secrets are correctly configured
- [ ] I verified my Oracle account is Always-Free (not PAYG)
- [ ] I understand this instance costs $0.00/month when configured correctly
- [ ] I know how to verify my bill shows $0.00
- [ ] I will NOT modify OCI_COMPUTE_SHAPE to non-free shapes
- [ ] I will NOT change to non-Always-Free regions
- [ ] I will NOT exceed 200GB total storage
- [ ] I accept that violating these rules may incur charges

---

## 🚀 Ready to Launch?

If you checked **ALL boxes above**, you may proceed to:

1. Go to GitHub repository → Actions tab
2. Select "Oracle Always-Free VPS Signup"
3. Click "Run workflow"
4. Wait for completion (up to 330 minutes)
5. Verify $0.00 bill in OCI Console

**Remember: When in doubt, STOP and re-read the documentation!**

---

## 📚 Additional Resources

- **Setup Guide:** [ALWAYS_FREE_SETUP.md](./ALWAYS_FREE_SETUP.md)
- **CPU Details:** [AMPERE_CPU_EXPLAINED.md](./AMPERE_CPU_EXPLAINED.md)
- **Cost Verification:** [COST_VERIFICATION.md](./COST_VERIFICATION.md)
- **GitHub Secrets:** [GITHUB_SECRETS_GUIDE.md](./GITHUB_SECRETS_GUIDE.md)
- **Reference:** https://guides.viren070.me/selfhosting/oracle

---

**Last Updated:** 2024
**Version:** 1.0
**Purpose:** Prevent accidental PAYG charges and ensure $0.00/month Always-Free deployment
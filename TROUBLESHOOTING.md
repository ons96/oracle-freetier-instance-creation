# 🆘 Oracle Always-Free VPS - Troubleshooting Guide

This guide provides solutions to common issues when setting up Oracle Always-Free VPS instances.

---

## 🔍 Table of Contents

- [1. Authentication Failures](#1-authentication-failures)
- [2. Region Validation Errors](#2-region-validation-errors)
- [3. Shape Configuration Issues](#3-shape-configuration-issues)
- [4. Boot Volume Size Problems](#4-boot-volume-size-problems)
- [5. Capacity Issues](#5-capacity-issues)
- [6. GitHub Actions Workflow Failures](#6-github-actions-workflow-failures)
- [7. Private Key Format Errors](#7-private-key-format-errors)
- [8. OCI Configuration Errors](#8-oci-configuration-errors)
- [9. Instance Creation Failures](#9-instance-creation-failures)
- [10. Billing and Cost Concerns](#10-billing-and-cost-concerns)

---

## 1. Authentication Failures

### ❌ Error: "Authentication failed" or "Invalid private key"

**Symptoms:**
- Workflow fails with authentication errors
- Logs show "401 Unauthorized" or "Invalid private key"

**Solutions:**

1. **Verify private key format:**
   - Open your `oci_api_key.pem` file
   - Ensure it contains:
     ```
     -----BEGIN PRIVATE KEY-----
     [Base64 encoded content - multiple lines]
     -----END PRIVATE KEY-----
     ```
   - Copy the **ENTIRE** content including all line breaks

2. **Check GitHub Secret format:**
   - Go to: Settings → Secrets and variables → Actions
   - Edit `OCI_PRIVATE_KEY` secret
   - Paste the **exact** content from your `.pem` file
   - **Do not modify** the content in any way

3. **Verify fingerprint matches:**
   - Check the fingerprint in `OCI_FINGERPRINT` secret
   - It should match the fingerprint shown in OCI Console
   - Format: `aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp`

4. **Regenerate API key if needed:**
   - Go to OCI Console → Identity → Users → Your Username → API Keys
   - Delete old key and generate a new one
   - Download the new private key
   - Update GitHub secrets with the new key

---

## 2. Region Validation Errors

### ❌ Error: "Region is NOT Always-Free eligible"

**Symptoms:**
- Workflow fails with region validation error
- Error message shows your region is not in the allowed list

**Solutions:**

1. **Check allowed regions:**
   - Only these regions are Always-Free eligible:
     - `us-ashburn-1` (Ashburn, USA)
     - `us-phoenix-1` (Phoenix, USA)
     - `ca-toronto-1` (Toronto, Canada)

2. **Verify OCI Console region:**
   - Log in to [OCI Console](https://cloud.oracle.com)
   - Check the region selector in the top-right corner
   - If different, click and change to one of the allowed regions

3. **Update GitHub Secret:**
   - Go to: Settings → Secrets and variables → Actions
   - Edit `OCI_REGION` secret
   - Set it to one of the allowed regions (e.g., `us-ashburn-1`)

4. **Check OCI_CONFIG file:**
   - If using local setup, verify the region in your `oci_config` file
   - The `region` parameter must match your GitHub secret

---

## 3. Shape Configuration Issues

### ❌ Error: "Shape is NOT Always-Free eligible"

**Symptoms:**
- Workflow fails with shape validation error
- Error mentions `VM.Standard.E2.1.Micro` or other shapes

**Solutions:**

1. **Use only VM.Standard.A1.Flex:**
   - This is the **only** Always-Free eligible shape
   - It provides 4 OCPU and 24GB RAM

2. **Verify workflow configuration:**
   - The workflow should have `OCI_COMPUTE_SHAPE: VM.Standard.A1.Flex`
   - Do not override this in GitHub secrets or workflow inputs

3. **Check for code modifications:**
   - Ensure no one modified `main.py` to use a different shape
   - The shape is hardcoded in the workflow for safety

4. **If you see E2.Micro in logs:**
   - This is a deprecated shape that can trigger PAYG charges
   - **Stop immediately** and check your configuration
   - The workflow should prevent this, so report as a bug if it happens

---

## 4. Boot Volume Size Problems

### ❌ Error: "Boot volume size exceeds 100GB safety limit"

**Symptoms:**
- Workflow fails when trying to use large boot volume
- Error message about 100GB limit

**Solutions:**

1. **Understand the limits:**
   - **Safe limit:** 100GB (recommended)
   - **Maximum allowed:** 200GB (Oracle's official limit)
   - We use 100GB as a safety margin

2. **Reduce boot volume size:**
   - Default: 50GB (works for most use cases)
   - Maximum safe: 100GB
   - Set in workflow inputs or GitHub secrets

3. **Check workflow inputs:**
   - When running workflow, set `boot_volume_size` to 50 or less
   - Or set it to a maximum of 100GB

4. **Verify GitHub Secret (if using):**
   - Some setups use `BOOT_VOLUME_SIZE` in secrets
   - Ensure it's set to 50 or less

---

## 5. Capacity Issues

### ❌ Error: "Out of host capacity" or "Out of capacity for shape"

**Symptoms:**
- Workflow runs but instance never creates
- Logs show capacity errors
- Workflow times out after 330 minutes

**Solutions:**

1. **Understand capacity limitations:**
   - Oracle Always-Free has limited capacity
   - High demand can exhaust available instances
   - The workflow automatically retries across ADs

2. **Try different availability domains:**
   - The workflow tries AD-1 → AD-2 → AD-3 automatically
   - You can specify multiple ADs in workflow inputs
   - Format: `AD-1,AD-2,AD-3`

3. **Run at off-peak times:**
   - Try running during non-business hours
   - Capacity is often available overnight
   - The workflow runs automatically 4× daily

4. **Wait and retry:**
   - Capacity becomes available as other users delete instances
   - Try again in a few hours or the next day
   - The workflow will auto-retry on schedule

5. **Check OCI Console:**
   - Log in to verify if you already have instances
   - You can have **max 2 ARM instances** on Always-Free
   - Delete unused instances to free up capacity

---

## 6. GitHub Actions Workflow Failures

### ❌ Error: "Missing required secrets"

**Symptoms:**
- Workflow fails immediately
- Error lists missing secrets

**Solutions:**

1. **Add all required secrets:**
   - Go to: Settings → Secrets and variables → Actions
   - Add these secrets (ALL REQUIRED):
     - `OCI_USER_ID` - Your User OCID
     - `OCI_TENANCY_ID` - Your Tenancy OCID
     - `OCI_FINGERPRINT` - API Key Fingerprint
     - `OCI_PRIVATE_KEY` - Full Private Key (with BEGIN/END markers)
     - `OCI_REGION` - Always-Free region (us-ashburn-1, us-phoenix-1, or ca-toronto-1)

2. **Verify secret values:**
   - Check for typos in OCID values
   - Ensure private key has proper format
   - Confirm region is one of the allowed values

3. **Check secret permissions:**
   - Ensure your GitHub account has access to secrets
   - Organization repos may have different permission rules

---

### ❌ Error: "Workflow timed out after 330 minutes"

**Symptoms:**
- Workflow runs for full duration
- No instance created
- Logs show capacity issues

**Solutions:**

1. **Check logs for capacity errors:**
   - Look for "Out of host capacity" messages
   - Verify which ADs were tried

2. **Manual retry:**
   - Go to Actions tab
   - Click "Run workflow" again
   - Try with different AD selection

3. **Wait and retry later:**
   - Capacity issues are temporary
   - Try again in a few hours
   - Capacity usually becomes available overnight

4. **Check your existing instances:**
   - Log in to OCI Console
   - Verify you don't have 2 instances already
   - Delete unused instances to free capacity

---

## 7. Private Key Format Errors

### ❌ Error: "Private key is not properly formatted"

**Symptoms:**
- Workflow fails during private key validation
- Error about BEGIN/END markers

**Solutions:**

1. **Check your private key file:**
   - Open `oci_api_key.pem`
   - Verify it starts with: `-----BEGIN PRIVATE KEY-----`
   - Verify it ends with: `-----END PRIVATE KEY-----`

2. **Copy the entire key:**
   - Select **all** text in the file
   - Include **all** line breaks
   - Do not modify or reformat

3. **Paste into GitHub Secret:**
   - Go to: Settings → Secrets and variables → Actions
   - Edit `OCI_PRIVATE_KEY`
   - Paste the **exact** content
   - **Do not** use code blocks or formatting

4. **Regenerate if corrupted:**
   - If key was edited, it may be corrupted
   - Go to OCI Console → Identity → Users → API Keys
   - Delete the key and generate a new one
   - Download fresh private key

---

## 8. OCI Configuration Errors

### ❌ Error: "Error reading the configuration file"

**Symptoms:**
- Workflow fails with config errors
- `ERROR_IN_CONFIG.log` file created

**Solutions:**

1. **Check OCI_CONFIG format:**
   - Should be in INI format:
     ```ini
     [DEFAULT]
     user=ocid1.user.oc1..xxxxxx
     fingerprint=aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp
     key_file=/path/to/oci_private_key.pem
     tenancy=ocid1.tenancy.oc1..xxxxxx
     region=us-ashburn-1
     ```

2. **Verify paths are correct:**
   - `key_file` should be absolute path
   - File should exist at that location
   - Permissions should be 600 (readable only by owner)

3. **Check for extra characters:**
   - No extra spaces or lines
   - No comments or additional text
   - Match the format in `sample_oci_config`

4. **Regenerate config if needed:**
   - Go to OCI Console → Profile → API Keys
   - Download config file again
   - Update with your correct values

---

## 9. Instance Creation Failures

### ❌ Error: "Instance creation failed"

**Symptoms:**
- Workflow completes but no instance created
- No `INSTANCE_CREATED` file
- Logs show various errors

**Solutions:**

1. **Check workflow logs:**
   - Look for specific error messages
   - Note the exact error code and message
   - Search this guide for that error

2. **Verify all prerequisites:**
   - ✅ Always-Free account (not PAYG)
   - ✅ Correct region selected
   - ✅ Proper authentication configured
   - ✅ Valid shape (VM.Standard.A1.Flex)
   - ✅ Boot volume ≤ 100GB

3. **Check OCI Console:**
   - Log in to verify account status
   - Check Billing → Cost Analysis (should show $0.00)
   - Verify Service Limits show Always-Free tier

4. **Try manual creation first:**
   - Attempt to create instance via OCI Console
   - See if you get different error messages
   - This helps isolate the problem

5. **Check for account restrictions:**
   - Some regions have capacity limits
   - New accounts may have temporary restrictions
   - Contact Oracle support if needed

---

## 10. Billing and Cost Concerns

### ❓ "Will I be charged?"

**Answer:** You **should not** be charged if you follow these guidelines:

✅ **Always-Free Configuration:**
- Shape: VM.Standard.A1.Flex only
- Region: us-ashburn-1, us-phoenix-1, or ca-toronto-1
- Boot Volume: ≤ 100GB
- Storage Total: ≤ 200GB

✅ **Account Type:**
- Must be Always-Free tier (not PAYG)
- Verify in OCI Console → Billing → Cost Analysis
- Should show $0.00 or "Always-Free"

✅ **Resource Limits:**
- Max 2 ARM instances
- Max 200GB total storage
- Max 10TB outbound bandwidth/month

### ❌ "I see charges on my bill!"

**Immediate Actions:**

1. **Stop all instances:**
   - Go to OCI Console → Compute → Instances
   - Stop any running instances

2. **Check resource usage:**
   - Go to Billing → Cost Analysis
   - Identify which resources are charged
   - Look for non-Always-Free resources

3. **Terminate non-free resources:**
   - Delete any PAYG instances
   - Remove any block volumes over 200GB
   - Check for load balancers or other services

4. **Contact Oracle Support:**
   - Go to OCI Console → Help → Support
   - Open a ticket about unexpected charges
   - Provide your account details

5. **Review account type:**
   - Ensure you're on Always-Free tier
   - If accidentally signed up for PAYG, contact support
   - May need to create new Always-Free account

---

## 🎯 Prevention Checklist

Before running the workflow, verify:

- [ ] ✅ Account is Always-Free (not PAYG)
- [ ] ✅ Region is us-ashburn-1, us-phoenix-1, or ca-toronto-1
- [ ] ✅ Shape is VM.Standard.A1.Flex
- [ ] ✅ Boot volume ≤ 100GB
- [ ] ✅ All GitHub secrets are set correctly
- [ ] ✅ Private key has proper BEGIN/END markers
- [ ] ✅ Fingerprint matches API key
- [ ] ✅ You have < 2 ARM instances running

---

## 📚 Additional Resources

- **[ALWAYS_FREE_SETUP.md](./ALWAYS_FREE_SETUP.md)** - Complete setup guide
- **[PREFLIGHT_CHECKLIST.md](./PREFLIGHT_CHECKLIST.md)** - Pre-deployment verification
- **[GITHUB_SECRETS_GUIDE.md](./GITHUB_SECRETS_GUIDE.md)** - Secrets configuration
- **[COST_VERIFICATION.md](./COST_VERIFICATION.md)** - Verify $0.00 billing

---

## 🆘 Still Having Issues?

If you've tried everything and still have problems:

1. **Check existing GitHub Issues:**
   - Search [GitHub Issues](https://github.com/mohankumarpaluru/oracle-freetier-instance-creation/issues)
   - Your problem may already have a solution

2. **Create a New Issue:**
   - Include:
     - Exact error message
     - Workflow logs (download artifacts)
     - Your configuration (redact sensitive info)
     - Steps you've already tried

3. **Join the Community:**
   - Check the project's Discord or other community channels
   - Other users may have encountered the same issue

---

**Remember:** Always verify $0.00 cost in OCI Console after deployment!

# GitHub Secrets Configuration - Step-by-Step Guide

This guide walks you through setting up GitHub Secrets for the Oracle Always-Free VPS deployment.

## 📋 What Are GitHub Secrets?

**GitHub Secrets** are encrypted environment variables stored in your repository. They allow you to:
- Store sensitive information (API keys, passwords)
- Use them in GitHub Actions workflows
- Keep them private (not visible in logs or code)
- Share configuration across workflow runs

## 🔐 Required Secrets Overview

| Secret Name | Description | Example Format | Required |
|-------------|-------------|----------------|----------|
| `OCI_USER_ID` | User OCID from OCI | `ocid1.user.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | ✅ Yes |
| `OCI_TENANCY_ID` | Tenancy OCID from OCI | `ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | ✅ Yes |
| `OCI_FINGERPRINT` | API Key fingerprint | `aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp` | ✅ Yes |
| `OCI_PRIVATE_KEY` | Complete private key (27 lines) | `-----BEGIN PRIVATE KEY-----...` | ✅ Yes |
| `OCI_REGION` | Always-Free region | `ca-toronto-1`, `us-ashburn-1`, or `us-phoenix-1` | ✅ Yes |
| `DISCORD_WEBHOOK` | Discord notification webhook | `https://discord.com/api/webhooks/...` | ❌ No |

---

## 📝 Step 1: Gather Your OCI Information

Before adding secrets, you need to collect information from your Oracle Cloud account.

### Log into Oracle Cloud Console

1. Go to **https://cloud.oracle.com**
2. Sign in with your Oracle account
3. Verify you're in an Always-Free eligible region (e.g. **ca-toronto-1**, **us-ashburn-1**, **us-phoenix-1**) (top-right)

---

## 🔑 Step 2: Get Your User OCID

### Method A: From API Key Page (Recommended)

1. Click **"Identity"** → **"Users"** → **Your Username**
2. Click **"API Keys"** in left sidebar
3. If you already have an API key:
   - The User OCID is shown at the top of the page
   - Copy it exactly as shown

### Method B: From User Profile

1. Click **"Identity"** → **"Users"** → **Your Username**
2. Look for **"User OCID"** on the details page
3. Click **"Copy"** button next to it

### Copy User OCID

The User OCID looks like:
```
ocid1.user.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

**Save this in a text file temporarily** - you'll need it soon.

---

## 🏢 Step 3: Get Your Tenancy OCID

1. Click **"Administration"** → **"Tenancy Details"**
   - OR look at top of any page for "Tenancy: ..."
2. Find **"Tenancy OCID"**
3. Click **"Copy"** button

### Copy Tenancy OCID

The Tenancy OCID looks like:
```
ocid1.tenancy.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

**Save this with your User OCID.**

---

## 🔐 Step 4: Generate API Key and Get Fingerprint

### Generate API Key Pair

1. Go to **"Identity"** → **"Users"** → **Your Username**
2. Click **"API Keys"** in left sidebar
3. Click **"Add API Key"**
4. Select **"Generate API Key Pair"**
5. Click **"Download Private Key"**
   - Save as **`oci_api_key.pem`**
   - **Keep this file secure!** Never share it.

### Get Fingerprint

After generating the key:
1. The fingerprint is shown on the API Keys page
2. It looks like: `aa:bb:cc:dd:ee:ff:gg:hh:ii:jj:kk:ll:mm:nn:oo:pp`
3. Copy the entire fingerprint

### Copy Fingerprint

**Save this with your OCIDs.**

---

## 🔑 Step 5: Prepare Private Key

### Open the Private Key File

1. Open **`oci_api_key.pem`** in a text editor
2. You should see something like:

```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB
...
(many more lines)
...
-----END PRIVATE KEY-----
```

### Important: Full Private Key

**You need the ENTIRE file contents** - usually 27 lines total, including:
- `-----BEGIN PRIVATE KEY-----` (first line)
- All middle lines (the key itself)
- `-----END PRIVATE KEY-----` (last line)

**Do NOT modify the private key in any way!**

---

## ⚙️ Step 6: Add Secrets to GitHub

### Navigate to GitHub Secrets

1. Go to your **GitHub repository**
2. Click **"Settings"** tab
3. In left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"**

### Secret 1: OCI_USER_ID

1. **Name:** `OCI_USER_ID`
2. **Value:** Paste your User OCID
3. Click **"Add secret"**

![Add Secret](https://docs.github.com/assets/images/help/settings/actions-secrets-add-secret.png)

### Secret 2: OCI_TENANCY_ID

1. Click **"New repository secret"**
2. **Name:** `OCI_TENANCY_ID`
3. **Value:** Paste your Tenancy OCID
4. Click **"Add secret"**

### Secret 3: OCI_FINGERPRINT

1. Click **"New repository secret"**
2. **Name:** `OCI_FINGERPRINT`
3. **Value:** Paste your API key fingerprint
4. Click **"Add secret"**

### Secret 4: OCI_PRIVATE_KEY (Most Important!)

**⚠️ CRITICAL: This must be done correctly, or authentication will fail!**

1. Open **`oci_api_key.pem`** in a text editor
2. **Select ALL** text (Cmd+A / Ctrl+A)
3. **Copy ALL** text including BEGIN/END lines
4. Go to GitHub Secrets
5. Click **"New repository secret"**
6. **Name:** `OCI_PRIVATE_KEY`
7. **Value:** Paste the ENTIRE private key
8. Click **"Add secret"**

#### Example of correct format:
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB
xk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8cK
Bxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8c
KBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8
cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9U
s8cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt9Us8cKBxk4ks9EiK5VJTUt
... (many more lines)
-----END PRIVATE KEY-----
```

❌ **Do NOT modify the private key!**
- Do not remove line breaks
- Do not add spaces
- Do not remove any lines
- Paste exactly as copied

### Secret 5: OCI_REGION

**⚠️ CRITICAL: Must be Always-Free eligible region!**

1. Check your OCI Console top-right for region
2. **Must be one of:**
   - `us-ashburn-1` (Virginia, USA)
   - `us-phoenix-1` (Arizona, USA)
3. Click **"New repository secret"**
4. **Name:** `OCI_REGION`
5. **Value:** Enter `us-ashburn-1` or `us-phoenix-1`
6. Click **"Add secret"**

❌ **DO NOT USE other regions** - They will trigger PAYG charges!

### Secret 6: DISCORD_WEBHOOK (Optional)

If you want Discord notifications:

1. In Discord, go to Server Settings → Integrations → Webhooks
2. Create new webhook for your channel
3. Copy webhook URL
4. In GitHub Secrets, click **"New repository secret"**
5. **Name:** `DISCORD_WEBHOOK`
6. **Value:** Paste webhook URL
7. Click **"Add secret"**

---

## ✅ Step 7: Verify All Secrets

### Check Secrets List

Your GitHub Secrets page should show:
- ✅ `OCI_USER_ID`
- ✅ `OCI_TENANCY_ID`
- ✅ `OCI_FINGERPRINT`
- ✅ `OCI_PRIVATE_KEY`
- ✅ `OCI_REGION`
- ⭕ `DISCORD_WEBHOOK` (optional)

### Quick Verification

1. All required secrets listed
2. No typos in secret names
3. `OCI_REGION` is `us-ashburn-1` or `us-phoenix-1`
4. Private key is complete (BEGIN to END lines)

---

## 🧪 Step 8: Test Configuration

### Run the GitHub Actions Workflow

1. Go to **Actions** tab in GitHub
2. Select **"Oracle Always-Free VPS Signup"**
3. Click **"Run workflow"**
4. Click the green **"Run workflow"** button

### What to Expect

1. **Step 1** - Validation checks all secrets exist
2. **Step 4** - Private key authentication test
3. **Step 7** - Always-Free configuration validation
4. Workflow will FAIL if secrets are incorrect

### If It Fails

#### "Authentication Failed"
- Private key format is wrong
- Fingerprint doesn't match key
- OCIDs are incorrect

#### "Region Not Always-Free Eligible"
- `OCI_REGION` is not `us-ashburn-1` or `us-phoenix-1`

#### "Missing Secrets"
- One or more required secrets not set
- Secret name typo

---

## 📋 Secrets Summary Table

| Secret | Source | Format | Critical? |
|--------|--------|--------|-----------|
| `OCI_USER_ID` | OCI Console: User Details | `ocid1.user.oc1..xxxx` | ✅ Yes |
| `OCI_TENANCY_ID` | OCI Console: Tenancy Details | `ocid1.tenancy.oc1..xxxx` | ✅ Yes |
| `OCI_FINGERPRINT` | OCI Console: API Keys | `aa:bb:cc:dd:...` | ✅ Yes |
| `OCI_PRIVATE_KEY` | Downloaded `.pem` file | Full 27-line key | ✅ Yes |
| `OCI_REGION` | OCI Console: Top-right | `us-ashburn-1` or `us-phoenix-1` | ✅ Yes |
| `DISCORD_WEBHOOK` | Discord: Server Settings | Webhook URL | ❌ No |

---

## 🔐 Security Best Practices

### Keep Secrets Secret
- ✅ **Never** commit secrets to git
- ✅ **Never** share private keys
- ✅ **Never** post secrets in issues/forums
- ✅ Use GitHub Secrets (never hardcode)
- ✅ Rotate API keys if compromised

### Private Key Storage
- Store original `oci_api_key.pem` safely
- Make backup of private key file
- Set file permissions: `chmod 600 oci_api_key.pem`
- Never share or email the private key

### If Compromised
1. Immediately delete API key from OCI Console
2. Generate new API key
3. Update GitHub Secrets with new key
4. Review OCI audit logs for unauthorized access

---

## 🆘 Troubleshooting

### "Authentication Failed"
- Private key format incorrect (missing lines/not complete)
- Fingerprint doesn't match the key
- OCIDs are wrong
- Private key has extra spaces/newlines

### "Missing Required Variables"
- One of the required secrets not set
- Typo in secret name
- Secret added to wrong repository

### "Invalid OCI Configuration"
- OCID format incorrect
- Region not set correctly
- Config file format issues

---

## ✅ Secrets Configuration Complete!

Once you've added all secrets:

1. ✅ All **required** secrets present (5 required)
2. ✅ Private key complete (BEGIN to END)
3. ✅ Region is Always-Free eligible
4. ✅ OCI_REGION matches your OCI Console region
5. ✅ Ready to run GitHub Actions workflow

### 🕒 Scheduling + Auto-stop (after first success)
- The workflow is scheduled to run **4× daily**.
- After the first successful instance creation, the workflow sets repository variable **`OCI_AUTOSTOP=true`** and future **scheduled** runs will skip automatically.
- Manual runs (`workflow_dispatch`) will still work.

To re-enable scheduling: `Settings` → `Secrets and variables` → `Actions` → `Variables` → delete `OCI_AUTOSTOP` (or set it to `false`).

### 📧 Success notification email (via GitHub)
On success, the workflow opens/updates a GitHub issue assigned to the triggering user. If you have GitHub email notifications enabled, GitHub will email you with the instance details.

**Next Step:** [PREFLIGHT_CHECKLIST.md](./PREFLIGHT_CHECKLIST.md)

---

## 📚 Additional Resources

- [ALWAYS_FREE_SETUP.md](./ALWAYS_FREE_SETUP.md) - Complete setup guide
- [PREFLIGHT_CHECKLIST.md](./PREFLIGHT_CHECKLIST.md) - Pre-launch verification
- [COST_VERIFICATION.md](./COST_VERIFICATION.md) - Verify $0.00 billing

---

**Last Updated:** 2024  
**Version:** 1.0
# Workflow Testing & Verification (GitHub Actions)

This repo’s GitHub Actions workflow (`.github/workflows/oci-vps-signup.yml`) can run on a schedule or manually.

## 1) One-time setup

1. Fork the repository.
2. Add the 5 required secrets:

- `OCI_USER_ID`
- `OCI_TENANCY_ID`
- `OCI_FINGERPRINT`
- `OCI_PRIVATE_KEY` (multi-line)
- `OCI_REGION` (e.g. `ca-toronto-1`)

## 2) Manual test run (workflow_dispatch)

1. Go to **Actions** → **Oracle Always-Free VPS Signup (Verified $0.00/month)**.
2. Click **Run workflow**.
3. (Optional) Set `max_runtime_minutes` (0 = unlimited).

### Pass criteria

- Workflow starts and installs Python dependencies.
- OCI config is written to `~/.oci/config`.
- Script runs without crashing.
- Artifacts are uploaded under `instance-details`.

### What to check in artifacts

Download the `instance-details` artifact and confirm at least:

- `setup_and_info.log`
- `launch_instance.log`

If successful, you should also see:

- `INSTANCE_CREATED`

If the scheduler run hits its time cap (expected while waiting for capacity), you’ll see:

- `MAX_RUNTIME_REACHED`

## 3) Success auto-stop verification

After the first time `INSTANCE_CREATED` is generated:

1. Go to `Settings` → `Secrets and variables` → `Actions` → `Variables`.
2. Confirm repository variable **`OCI_AUTOSTOP`** exists and equals `true`.

After this, scheduled runs will still trigger, but the job will be **skipped** (near-zero Actions minutes).

## 4) Email notification verification (via GitHub)

On success, the workflow creates (or comments on) a GitHub Issue titled:

- **✅ OCI Always-Free VPS created**

If you have GitHub email notifications enabled for issues, you should receive an email containing the `INSTANCE_CREATED` details.

## 5) Re-enable scheduling

To resume scheduled attempts:

- Delete the `OCI_AUTOSTOP` variable (or set it to `false`).

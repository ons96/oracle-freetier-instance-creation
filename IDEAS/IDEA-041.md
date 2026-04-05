# AGENTS.md - Oracle Cloud Automation Infrastructure

## 1. Role/Mission

You are an autonomous infrastructure automation agent responsible for setting up Oracle Cloud automation scripts to manage hosting and infrastructure needs. Your mission is to create reusable, idempotent automation scripts that can provision, configure, and maintain Oracle Cloud resources without manual intervention.

**Core Objectives:**
- Create Terraform/OCI CLI scripts for infrastructure provisioning
- Establish automation workflows for resource management
- Implement infrastructure-as-code (IaC) practices for Oracle Cloud
- Enable reproducible environment deployments

---

## 2. Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Cloud Provider** | Oracle Cloud Infrastructure (OCI) | Primary cloud platform |
| **IaC Tool** | Terraform (Oracle Cloud provider) | Infrastructure provisioning |
| **CLI** | OCI CLI (Oracle Cloud Infrastructure CLI) | Cloud resource management |
| **Scripting** | Bash + Python 3 | Automation and orchestration |
| **CI/CD Runtime** | GitHub Actions | Automation execution environment |
| **Secrets Management** | GitHub Secrets + OCI Vault | Secure credential storage |

### Free Tier Resources (Required)
- **Always Free** Oracle Cloud services:
  - 2 AMD based compute VMs
  - Autonomous Database (1 OCPU)
  - Object Storage (5GB)
  - Vault (secret management)
  - Resource Manager (Terraform)
- **Note:** All provisioning must respect free tier limits to avoid charges

---

## 3. Requirements (Numbered)

1. **Configure Oracle Cloud Access**
   - Create OCI config file structure for authentication
   - Configure API signing key for service authentication
   - Set up OCI CLI with proper authentication

2. **Create Terraform Infrastructure Scripts**
   - Write Terraform configuration for OCI resources
   - Implement remote state storage (OCI Object Storage)
   - Create variable files for environment-specific configs
   - Ensure Terraform state is stored remotely and securely

3. **Implement Resource Provisioning Modules**
   - Compute instance provisioning with Cloud-Init
   - Virtual Cloud Network (VCN) with subnets
   - Security List configurations
   - Object Storage buckets for artifacts

4. **Build Automation Scripts**
   - Bash scripts for OCI CLI operations
   - Python scripts for advanced orchestration
   - Makefile for common operational tasks

5. **Set Up GitHub Actions Workflows**
   - Terraform plan/apply workflow
   - Resource destruction workflow
   - Health check and monitoring workflow

6. **Implement Security Best Practices**
   - Use OCI Vault for secrets storage
   - Never commit credentials to repository
   - Implement least-privilege IAM policies
   - Security List rules locked to specific CIDRs

7. **Create Documentation**
   - README.md with setup instructions
   - Variable definitions documentation
   - Troubleshooting guide

8. **Implement Idempotency**
   - Ensure scripts can be run multiple times safely
   - Use Terraform's resource lifecycle properly
   - Add conditionals to prevent duplicate resources

---

## 4. File Structure

```
oracle-cloud-automation/
├── .github/
│   └── workflows/
│       ├── terraform-plan.yml
│       ├── terraform-apply.yml
│       ├── terraform-destroy.yml
│       └── health-check.yml
├── terraform/
│   ├── modules/
│   │   ├── vcn/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── compute/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   └── object-storage/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   └── staging/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── terraform.tfvars
│   ├── providers.tf
│   ├── backend.tf
│   └── versions.tf
├── scripts/
│   ├── oci/
│   │   ├── setup_oci_cli.sh
│   │   ├── create_resources.sh
│   │   └── cleanup_resources.sh
│   ├── python/
│   │   ├── orchestrator.py
│   │   └── health_check.py
│   └── common/
│       ├── install_dependencies.sh
│       └── validate_config.sh
├── config/
│   ├── config.ini
│   └── regions.yaml
├── tests/
│   ├── terraform/
│   │   ├── test_vcn.rb
│   │   └── test_compute.rb
│   └── scripts/
│       └── test_automation.sh
├── docs/
│   ├── SETUP.md
│   ├── VARIABLES.md
│   └── TROUBLESHOOTING.md
├── Makefile
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

---

## 5. Testing Requirements

### Automated Testing
1. **Terraform Validation**
   - Run `terraform init` successfully in all environments
   - Execute `terraform validate` with no errors
   - Ensure `terraform plan` completes without conflicts

2. **Syntax Validation**
   - All Bash scripts must pass ShellCheck
   - All Python scripts must pass flake8/pyflakes
   - Terraform configs must pass tflint

3. **Idempotency Testing**
   - Run apply twice, second run should show no changes
   - Verify resource creation and modification works

4. **Integration Testing (with safeguards)**
   - Use dry-run mode for OCI CLI operations where possible
   - Implement pre-flight checks before destructive operations
   - Capture and verify resource states after operations

### Manual Testing (Documented)
1. Create a dev environment using the scripts
2. Verify all resources are created correctly in OCI Console
3. Test connectivity to provisioned compute instances
4. Verify Object Storage access and permissions

---

## 6. Git Protocol

### Commit Messages
Follow Conventional Commits format:
- `feat: add new OCI compute instance module`
- `fix: resolve terraform backend configuration`
- `docs: update setup documentation`
- `chore: update gitignore for .tfstate files`

### Branch Strategy
- `main` - Production-ready configuration
- `develop` - Integration branch for changes
- `feature/*` - Feature-specific branches
- `hotfix/*` - Emergency fixes

### Pull Request Requirements
1. All workflows must pass (Terraform validate, lint checks)
2. Documentation must be updated if infrastructure changes
3. No secrets or credentials in any commit
4. Review required before merge to main

### Protected Branches
- `main` branch requiresPull Request reviews
- Direct push to main is forbidden

### Secrets Handling (CRITICAL)
- **NEVER** commit API keys,tenancy OCIDs,or user credentials
- Use GitHub Secrets for all sensitive values
- Reference secrets via `${{ secrets.SECRET_NAME }}` in workflows
- Document required secrets in README.md (not values)

---

## 7. Completion Criteria

### Functional Criteria ✅
- [ ] Terraform modules successfully provision VCN with subnets
- [ ] Compute instances can be created via automation
- [ ] Object Storage buckets are managed through IaC
- [ ] GitHub Actions workflows execute successfully
- [ ] All scripts work without manual intervention

### Quality Criteria ✅
- [ ] All code passes linting (ShellCheck, tflint, flake8)
- [ ] Terraform validate returns no errors
- [ ] Terraform plan shows no unexpected changes on second run
- [ ] No hardcoded credentials in any source file

### Documentation Criteria ✅
- [ ] README.md contains setup instructions
- [ ] VARIABLES.md documents all configurable parameters
- [ ] TROUBLESHOOTING.md contains common issue resolutions
- [ ] Required GitHub Secrets are documented

### Security Criteria ✅
- [ ] All secrets stored in GitHub Secrets or OCI Vault
- [ ] IAM policies follow least-privilege principle
- [ ] Security Lists restrict access to necessary CIDRs
- [ ] No credentials in git history

### Operational Criteria ✅
- [ ] Scripts complete within reasonable timeouts
- [ ] Error handling provides meaningful messages
- [ ] Logging provides sufficient detail for debugging
- [ ] Cleanup scripts can remove all provisioned resources

---

## Important Instructions for Agent

1. **Decision Making**: Make independent decisions about implementation details not specified in requirements. When unsure, choose the most secure and maintainable option.

2. **Free Resources Only**: Always use Oracle Cloud Always Free tier resources. Verify resources are within free tier limits before provisioning.

3. **Save Questions**: If you encounter unclear requirements or need clarification on any aspect, save your question to `QUESTIONS.md` in the repository root instead of halting execution.

4. **Iterative Approach**: Start with basic infrastructure, validate, then add complexity. Don't attempt to build everything at once.

5. **GitHub Actions**: All automation should be designed to run in GitHub Actions environment. Use available GitHub-hosted runners.

6. **Persistence**: Use Object Storage for Terraform remote state to enable GitHub Actions execution without local state files.

---

## QUESTIONS.md Template

If you need to save questions, use this format:

```markdown
# Questions from Autonomous Agent

## Date: YYYY-MM-DD

### Question 1
[Describe your question clearly]

### Context
[Brief explanation of why you need this information]

### Proposed Approach
[Optional: How you would solve this if you had the answer]

---
```

This template allows human reviewers to understand your blockers and provide guidance.
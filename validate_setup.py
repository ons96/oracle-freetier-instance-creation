#!/usr/bin/env python3
"""
Setup Validation Script
This script validates that all necessary files and configurations are in place
for the Oracle Cloud VPS creation script to work properly.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def validate_config_file(filepath):
    """Validate configuration file format."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if '[DEFAULT]' in content or 'user=' in content:
                print(f"✅ Configuration file format looks valid: {filepath}")
                return True
            else:
                print(f"⚠️  Configuration file may have issues: {filepath}")
                return False
    except Exception as e:
        print(f"❌ Error reading configuration file {filepath}: {e}")
        return False

def validate_env_file(filepath):
    """Validate environment file format."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            required_vars = ['OCI_CONFIG', 'OCT_FREE_AD', 'DISPLAY_NAME', 'OCI_COMPUTE_SHAPE']
            found_vars = []
            
            for line in lines:
                if '=' in line and not line.strip().startswith('#'):
                    var_name = line.split('=')[0].strip()
                    found_vars.append(var_name)
            
            missing_vars = [var for var in required_vars if var not in found_vars]
            if not missing_vars:
                print(f"✅ Environment file has required variables: {filepath}")
                return True
            else:
                print(f"⚠️  Missing variables in environment file: {missing_vars}")
                return False
    except Exception as e:
        print(f"❌ Error reading environment file {filepath}: {e}")
        return False

def main():
    """Main validation function."""
    print("🔍 Oracle Cloud VPS Creation - Setup Validation")
    print("=" * 50)
    
    # Check required files
    files_ok = True
    files_ok &= check_file_exists("main.py", "Main Python script")
    files_ok &= check_file_exists("requirements.txt", "Python requirements")
    files_ok &= check_file_exists("oci.env", "Environment configuration")
    files_ok &= check_file_exists("sample_oci_config", "Sample OCI configuration")
    
    # Check CI/CD specific files
    files_ok &= check_file_exists(".github/workflows/oci-vps-signup.yml", "GitHub Actions workflow")
    files_ok &= check_file_exists("setup_ci.sh", "CI/CD setup script")
    files_ok &= check_file_exists("setup_env.sh", "Local setup script")
    
    # Validate configuration files
    print("\n📋 Validating Configuration Files")
    print("-" * 30)
    
    config_ok = True
    if os.path.exists("oci_config"):
        config_ok &= validate_config_file("oci_config")
    else:
        print("⚠️  oci_config file not found - you'll need to create it from sample_oci_config")
    
    env_ok = validate_env_file("oci.env")
    
    # Check directory structure
    print("\n📁 Checking Directory Structure")
    print("-" * 30)
    
    required_dirs = [".github", ".github/workflows"]
    dirs_ok = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Directory missing: {dir_path}")
            dirs_ok = False
    
    # Overall status
    print("\n📊 Validation Summary")
    print("=" * 50)
    
    if files_ok and config_ok and env_ok and dirs_ok:
        print("🎉 All validation checks passed!")
        print("\nNext steps:")
        print("1. Copy sample_oci_config to oci_config and fill in your credentials")
        print("2. Edit oci.env to match your preferences")
        print("3. For local development: ./setup_env.sh")
        print("4. For CI/CD: Use the GitHub Actions workflow")
        print("5. Run: python main.py")
        return 0
    else:
        print("❌ Some validation checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env bash

# setup_ci.sh
# CI/CD environment setup script for Oracle Cloud VPS creation

set -e

echo "🚀 Setting up Oracle Cloud VPS Creation for CI/CD"
echo "=================================================="

# Check if we're in CI/CD environment
if [[ "$CI" != "true" ]] && [[ "$GITHUB_ACTIONS" != "true" ]]; then
    echo "⚠️  This script is designed for CI/CD environments."
    echo "   For local setup, use: ./setup_env.sh"
    echo ""
    read -p "Continue anyway? (y/N): " continue_setup
    if [[ $continue_setup != "y" && $continue_setup != "Y" ]]; then
        exit 1
    fi
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p keys

# Copy sample files if they don't exist
if [[ ! -f "oci_config" ]]; then
    echo "📋 Creating oci_config from sample..."
    cp sample_oci_config oci_config
    echo "⚠️  Please edit oci_config with your actual OCI credentials!"
fi

if [[ ! -f "oci.env" ]]; then
    echo "📋 Creating oci.env from template..."
    cp oci.env oci.env.template 2>/dev/null || true
fi

# Check for required environment variables in CI/CD
if [[ "$CI" == "true" ]] || [[ "$GITHUB_ACTIONS" == "true" ]]; then
    echo "🔍 Checking required environment variables for CI/CD..."
    
    required_vars=("OCI_USER_ID" "OCI_TENANCY_ID" "OCI_FINGERPRINT" "OCI_PRIVATE_KEY" "OCI_REGION")
    missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        echo "❌ Missing required environment variables:"
        printf '   - %s\n' "${missing_vars[@]}"
        echo ""
        echo "Please set these variables in your CI/CD environment:"
        echo "  - OCI_USER_ID: Your OCI user OCID"
        echo "  - OCI_TENANCY_ID: Your OCI tenancy OCID"
        echo "  - OCI_FINGERPRINT: Your API key fingerprint"
        echo "  - OCI_PRIVATE_KEY: Your private key content"
        echo "  - OCI_REGION: Your preferred region (e.g., us-ashburn-1)"
        echo ""
        echo "For GitHub Actions, set these in repository secrets."
        exit 1
    fi
    
    echo "✅ All required environment variables are set"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x setup_env.sh
chmod +x setup_init.sh

echo ""
echo "✅ CI/CD setup completed!"
echo ""
echo "Next steps:"
echo "1. For local development:"
echo "   - Edit oci_config with your credentials"
echo "   - Run: ./setup_env.sh"
echo "   - Run: python main.py"
echo ""
echo "2. For CI/CD (GitHub Actions):"
echo "   - Set secrets in your repository settings"
echo "   - Use workflow_dispatch to trigger the pipeline"
echo "   - See: .github/workflows/oci-vps-signup.yml"
echo ""
echo "3. For testing:"
echo "   - Run: python -c 'import oci; print(\"OCI SDK installed successfully\")'"
echo "   - Run: python -c 'from dotenv import load_dotenv; load_dotenv(\"oci.env\"); print(\"Configuration loaded\")'"
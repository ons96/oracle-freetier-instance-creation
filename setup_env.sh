#!/usr/bin/env bash

# oci_config_setup.sh
# This script sets up the OCI configuration interactively and creates an oci.env file.
# For CI/CD usage, see .github/workflows/oci-vps-signup.yml

display_choices(){
cat <<EOF
Choose one of the two free shapes

1. VM.Standard.A1.Flex (4 CPUs, 24GB RAM) - RECOMMENDED
2. VM.Standard.E2.1.Micro (1 CPU, 1GB RAM)
EOF
}

# Check if running in CI/CD environment
if [[ "$CI" == "true" ]] || [[ "$GITHUB_ACTIONS" == "true" ]]; then
    echo "This script is not designed for CI/CD environments."
    echo "Please use the GitHub Actions workflow instead: .github/workflows/oci-vps-signup.yml"
    exit 1
fi

echo "Welcome to OCI Instance Creation Setup!"
echo "========================================="
echo ""

read -p "Type name of the instance: " INSTANCE_NAME
clear

while true; do
    display_choices
    
    read -p "Enter your choice (1 or 2): " SHAPE
    
    case $SHAPE in
        1)
            SHAPE="VM.Standard.A1.Flex"
            break
            ;;
        2)
            SHAPE="VM.Standard.E2.1.Micro"
            break
            ;;
        *)
            clear
            echo "Invalid choice. Please try again. (CTRL+C to quit)"
            ;;
    esac
done
clear

while true; do
    read -p "Use the script for your second free tier Micro Instance? (y/n): " BOOL_MICRO
    
    BOOL_MICRO=$(echo "$BOOL_MICRO" | tr '[:upper:]' '[:lower:]')

    case $BOOL_MICRO in
        y)
            BOOL_MICRO="True"
            break
            ;;
        n)
            BOOL_MICRO="False"
            break
            ;;
        *)
            clear
            echo "Invalid choice. Please try again (CTRL+C to quit)"
            ;;
    esac
done
clear

read -p "Enter the Subnet OCID (or press Enter to skip): " SUBNET_ID
clear

read -p "Enter the Image OCID (or press Enter to skip): " IMAGE_ID
clear

while true; do
    read -p "Enable Gmail notification? (y/n): " BOOL_MAIL
    
    BOOL_MAIL=$(echo "$BOOL_MAIL" | tr '[:upper:]' '[:lower:]')

    case $BOOL_MAIL in
        y)
            BOOL_MAIL="True"
            break
            ;;
        n)
            BOOL_MAIL="False"
            break
            ;;
        *)
            clear
            echo "Invalid choice. Please try again (CTRL+C to quit)"
            ;;
    esac
done
clear

if [[ $BOOL_MAIL == "True" ]]; then
    read -p "Enter your email: " EMAIL
    clear

    read -p "Enter email app password (16 characters without spaces): " EMAIL_PASS
    clear
else
    EMAIL=""
    EMAIL_PASS=""
fi

read -p "Enter Discord webhook URL (or press Enter to skip): " DISCORD_WEBHOOK
clear

read -p "Enter Telegram bot token (or press Enter to skip): " TELEGRAM_TOKEN
clear

read -p "Enter Telegram user ID (or press Enter to skip): " TELEGRAM_USER_ID
clear

# Backup existing oci.env if exists
if [ -f oci.env ]; then
    mv oci.env oci.env.bak
    echo "Existing oci.env file backed up as oci.env.bak"
fi

# Get the current directory for relative paths
CURRENT_DIR=$(pwd)

# Create the new oci.env file with the gathered configuration
cat <<EOF > oci.env
# OCI Configuration - Use environment variables for CI/CD compatibility
# OCI_CONFIG: Path to OCI config file (relative or absolute)
OCI_CONFIG=oci_config

# Availability Domain - comma-separated list for fallback
OCT_FREE_AD=AD-1

# Instance configuration
DISPLAY_NAME=$INSTANCE_NAME

# The free shapes are:
# ARM: VM.Standard.A1.Flex (4 CPUs, 24GB RAM) - Recommended
# AMD: VM.Standard.E2.1.Micro (1 CPU, 1GB RAM)
OCI_COMPUTE_SHAPE=$SHAPE

# Set to True if creating a second free tier Micro Instance
SECOND_MICRO_INSTANCE=$BOOL_MICRO

# Wait time between retries (seconds)
REQUEST_WAIT_TIME_SECS=60

# SSH keys - Use relative paths for CI/CD compatibility
SSH_AUTHORIZED_KEYS_FILE=id_rsa.pub

# Optional: Specify subnet ID (leave empty to auto-detect)
OCI_SUBNET_ID=$SUBNET_ID

# Optional: Specify image ID (leave empty to auto-detect based on OS)
OCI_IMAGE_ID=$IMAGE_ID

# OS Configuration (used if OCI_IMAGE_ID is not specified)
OPERATING_SYSTEM=Canonical Ubuntu
OS_VERSION=22.04

# Network configuration
ASSIGN_PUBLIC_IP=false

# Boot volume size in GB (minimum is 50)
BOOT_VOLUME_SIZE=50

# Notification Settings
# Set NOTIFY_EMAIL=true to enable Gmail notifications
NOTIFY_EMAIL=$BOOL_MAIL

# Email credentials should be set via environment variables in CI/CD
# For local usage, you can set them here (NOT recommended for production)
# EMAIL=$EMAIL
# EMAIL_PASSWORD=$EMAIL_PASS

# Discord webhook (optional)
# DISCORD_WEBHOOK=$DISCORD_WEBHOOK

# Telegram notifications (optional)
# TELEGRAM_TOKEN=$TELEGRAM_TOKEN
# TELEGRAM_USER_ID=$TELEGRAM_USER_ID
EOF

echo "OCI env configuration saved to oci.env"
echo ""
echo "Next steps:"
echo "1. Place your OCI config file as 'oci_config' in the current directory"
echo "2. Or set OCI_CONFIG environment variable to point to your config file"
echo "3. Run the script with: python main.py"
echo ""
echo "For CI/CD usage, see .github/workflows/oci-vps-signup.yml"

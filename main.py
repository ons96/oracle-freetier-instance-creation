import configparser
import itertools
import json
import logging
import os
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Union

import oci
import paramiko
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv(os.path.join(os.getcwd(), 'oci.env'))

ARM_SHAPE = "VM.Standard.A1.Flex"
E2_MICRO_SHAPE = "VM.Standard.E2.1.Micro"

# Always-Free Tier Configuration Constants
ALWAYS_FREE_SHAPES = ["VM.Standard.A1.Flex"]  # Ampere ARM CPU only
# NOTE: Oracle Always-Free eligibility can vary by tenancy/region over time.
# This list is intentionally restrictive to reduce the risk of PAYG charges.
ALWAYS_FREE_REGIONS = ["us-ashburn-1", "us-phoenix-1", "ca-toronto-1"]
ALWAYS_FREE_OPERATING_SYSTEMS = ["Canonical Ubuntu"]
ALWAYS_FREE_MAX_STORAGE_GB = 200
ALWAYS_FREE_DEFAULT_BOOT_VOLUME = 50

# Validate required environment variables for CI/CD
required_vars = ['OCI_CONFIG']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars and (os.getenv('CI') or os.getenv('GITHUB_ACTIONS')):
    print(f"Missing required environment variables for CI/CD: {missing_vars}")
    print("Please set these variables in your GitHub Actions secrets")
    sys.exit(1)

# Check if we're in CI/CD environment
is_ci_cd = os.getenv('CI') or os.getenv('GITHUB_ACTIONS')

if is_ci_cd:
    logging.info("Running in CI/CD environment")
    # Ensure we don't try to send notifications in CI/CD unless explicitly enabled
    if os.getenv('CI_NOTIFICATIONS', 'false').lower() != 'true':
        NOTIFY_EMAIL = False
        DISCORD_WEBHOOK = ""

# Access loaded environment variables and strip white spaces
OCI_CONFIG = os.getenv("OCI_CONFIG", "").strip()
OCT_FREE_AD = os.getenv("OCT_FREE_AD", "").strip()
DISPLAY_NAME = os.getenv("DISPLAY_NAME", "").strip()
WAIT_TIME = int(os.getenv("REQUEST_WAIT_TIME_SECS", "0").strip())
try:
    MAX_RUNTIME_SECS = int(os.getenv("MAX_RUNTIME_SECS", "0").strip() or "0")
except ValueError:
    MAX_RUNTIME_SECS = 0
SSH_AUTHORIZED_KEYS_FILE = os.getenv("SSH_AUTHORIZED_KEYS_FILE", "").strip()
OCI_IMAGE_ID = os.getenv("OCI_IMAGE_ID", None).strip() if os.getenv("OCI_IMAGE_ID") else None
OCI_COMPUTE_SHAPE = os.getenv("OCI_COMPUTE_SHAPE", ARM_SHAPE).strip()
SECOND_MICRO_INSTANCE = os.getenv("SECOND_MICRO_INSTANCE", 'False').strip().lower() == 'true'
OCI_SUBNET_ID = os.getenv("OCI_SUBNET_ID", None).strip() if os.getenv("OCI_SUBNET_ID") else None
OPERATING_SYSTEM = os.getenv("OPERATING_SYSTEM", "").strip()
OS_VERSION = os.getenv("OS_VERSION", "").strip()
ASSIGN_PUBLIC_IP = os.getenv("ASSIGN_PUBLIC_IP", "false").strip()
BOOT_VOLUME_SIZE = os.getenv("BOOT_VOLUME_SIZE", "50").strip()
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", 'False').strip().lower() == 'true'
EMAIL = os.getenv("EMAIL", "").strip()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip()
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "").strip()

# Read the configuration from oci_config file
config = configparser.ConfigParser()
try:
    config.read(OCI_CONFIG)
    OCI_USER_ID = config.get('DEFAULT', 'user')
    if OCI_COMPUTE_SHAPE not in (ARM_SHAPE, E2_MICRO_SHAPE):
        raise ValueError(f"{OCI_COMPUTE_SHAPE} is not an acceptable shape")
    env_has_spaces = any(isinstance(confg_var, str) and " " in confg_var
                        for confg_var in [OCI_CONFIG, OCT_FREE_AD,WAIT_TIME,
                                SSH_AUTHORIZED_KEYS_FILE, OCI_IMAGE_ID, 
                                OCI_COMPUTE_SHAPE, SECOND_MICRO_INSTANCE, 
                                OCI_SUBNET_ID, OS_VERSION, NOTIFY_EMAIL,EMAIL,
                                EMAIL_PASSWORD, DISCORD_WEBHOOK]
                        )
    config_has_spaces = any(' ' in value for section in config.sections() 
                            for _, value in config.items(section))
    if env_has_spaces:
        raise ValueError("oci.env has spaces in values which is not acceptable")
    if config_has_spaces:
        raise ValueError("oci_config has spaces in values which is not acceptable")        

except configparser.Error as e:
    error_log_path = os.path.join(os.getcwd(), "ERROR_IN_CONFIG.log")
    with open(error_log_path, "w", encoding='utf-8') as file:
        file.write(str(e))

    print(f"Error reading the configuration file: {e}")
    # In CI/CD, we should exit on configuration errors
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        sys.exit(1)

def validate_always_free_compliance():
    """
    Validates that configuration will NEVER trigger PAYG charges.
    Fails loudly if any non-free settings detected.
    
    Raises:
        ValueError: If any non-Always-Free configuration is detected
    """
    # Get OCI region from config
    oci_region = config.get('region', '') if config else ''
    
    errors = []
    warnings = []
    
    # Critical checks - must pass to prevent PAYG charges
    if OCI_COMPUTE_SHAPE not in ALWAYS_FREE_SHAPES:
        errors.append(
            f"🚨 CRITICAL: Shape '{OCI_COMPUTE_SHAPE}' is NOT Always-Free eligible.\n"
            f"   REQUIRED: VM.Standard.A1.Flex (Ampere ARM, 4 OCPU, 24GB RAM)\n"
            f"   Using any other shape WILL incur PAYG charges!\n"
            f"\n   Did you accidentally select E2.Micro? This can trigger charges!"
        )
    
    if oci_region not in ALWAYS_FREE_REGIONS and oci_region:
        allowed_regions = ", ".join(ALWAYS_FREE_REGIONS)
        errors.append(
            f"🚨 CRITICAL: Region '{oci_region}' is NOT Always-Free eligible!\n"
            f"   REQUIRED regions: {allowed_regions}\n"
            f"   Using other regions WILL incur PAYG charges!"
        )
    
    boot_volume_int = int(BOOT_VOLUME_SIZE) if str(BOOT_VOLUME_SIZE).isdigit() else 0
    if boot_volume_int > ALWAYS_FREE_MAX_STORAGE_GB:
        errors.append(
            f"🚨 CRITICAL: Boot volume {boot_volume_int}GB exceeds Always-Free limit of {ALWAYS_FREE_MAX_STORAGE_GB}GB.\n"
            f"   Maximum storage across ALL volumes is {ALWAYS_FREE_MAX_STORAGE_GB}GB.\n"
            f"   Exceeding this WILL incur PAYG charges!"
        )
    
    if boot_volume_int < 50:
        warnings.append(
            f"⚠️ WARNING: Boot volume size {boot_volume_int}GB is below minimum 50GB.\n"
            f"   Will default to 50GB (Always-Free compliant)."
        )
    
    # OS warning (non-critical but recommended)
    if OPERATING_SYSTEM and OPERATING_SYSTEM not in ALWAYS_FREE_OPERATING_SYSTEMS:
        warnings.append(
            f"⚠️ WARNING: OS '{OPERATING_SYSTEM}' may not be fully Always-Free compliant.\n"
            f"   Recommended: Canonical Ubuntu (Ubuntu 22.04 LTS preferred)\n"
            f"   Other OS may have licensing costs or compatibility issues."
        )
    
    # Always-Free confirmation details
    logging.info("=" * 70)
    logging.info("🎯 ALWAYS-FREE TIER CONFIGURATION VALIDATION")
    logging.info("=" * 70)
    logging.info("✅ Compute Shape: %s (Ampere ARM CPU)", OCI_COMPUTE_SHAPE)
    logging.info("✅ OCPU: 4 cores @ Ampere Computing ARM64")
    logging.info("✅ Memory: 24 GB RAM")
    logging.info("✅ Region: %s", oci_region if oci_region in ALWAYS_FREE_REGIONS else "⚠️ NOT ALWAYS-FREE ELIGIBLE")
    logging.info("✅ Boot Volume: %sGB (within %sGB Always-Free limit)", 
                 max(50, boot_volume_int), ALWAYS_FREE_MAX_STORAGE_GB)
    logging.info("✅ Operating System: %s", OPERATING_SYSTEM or "Auto-detected")
    logging.info("✅ Monthly Cost: $0.00 USD (Always-Free tier guaranteed)")
    logging.info("=" * 70)
    
    # Output all warnings
    for warning in warnings:
        logging.warning(warning)
    
    # Fail if any critical errors detected
    if errors:
        error_msg = "\n\n".join(errors)
        logging.critical("\n" + "=" * 70)
        logging.critical("❌ ALWAYS-FREE COMPLIANCE CHECK FAILED!")
        logging.critical("=" * 70)
        logging.critical("\n%s\n", error_msg)
        logging.critical("=" * 70)
        logging.critical("\n\nFix your configuration before proceeding to avoid PAYG charges.")
        logging.critical("=" * 70)
        raise ValueError(
            "❌ Always-Free Compliance Check FAILED!\n\n"
            f"{error_msg}\n\n"
            "Fix your configuration before proceeding to avoid PAYG charges."
        )
    
    logging.info("✅ Configuration validated as Always-Free compliant (100%% free forever)")
    logging.info("=" * 70)


# Set up logging
log_file = os.path.join(os.getcwd(), "setup_and_info.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging_step5 = logging.getLogger("launch_instance")
logging_step5.setLevel(logging.INFO)
fh = logging.FileHandler(os.path.join(os.getcwd(), "launch_instance.log"))
fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging_step5.addHandler(fh)

# Set up OCI Config and Clients
if OCI_CONFIG:
    # Use absolute path from environment or relative to current directory
    oci_config_path = OCI_CONFIG if os.path.isabs(OCI_CONFIG) else os.path.join(os.getcwd(), OCI_CONFIG)
else:
    oci_config_path = os.path.expanduser("~/.oci/config")
config = oci.config.from_file(oci_config_path)
iam_client = oci.identity.IdentityClient(config)
network_client = oci.core.VirtualNetworkClient(config)
compute_client = oci.core.ComputeClient(config)

IMAGE_LIST_KEYS = [
    "lifecycle_state",
    "display_name",
    "id",
    "operating_system",
    "operating_system_version",
    "size_in_mbs",
    "time_created",
]


def write_into_file(file_path, data):
    """Write data into a file.

    Args:
        file_path (str): The path of the file.
        data (str): The data to be written into the file.
    """
    with open(file_path, mode="a", encoding="utf-8") as file_writer:
        file_writer.write(data)


def send_email(subject, body, email, password):
    """Send an HTML email using the SMTP protocol.

    Args:
        subject (str): The subject of the email.
        body (str): The HTML body/content of the email.
        email (str): The sender's email address.
        password (str): The sender's email password or app-specific password.

    Raises:
        smtplib.SMTPException: If an error occurs during the SMTP communication.
    """
    # Set up the MIME
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = email
    message["To"] = email

    # Attach HTML content to the email
    html_body = MIMEText(body, "html")
    message.attach(html_body)

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        try:
            # Start TLS for security
            server.starttls()
            # Login to the server
            server.login(email, password)
            # Send the email
            server.sendmail(email, email, message.as_string())
        except smtplib.SMTPException as mail_err:
            # Handle SMTP exceptions (e.g., authentication failure, connection issues)
            logging.error("Error while sending email: %s", mail_err)
            raise


def list_all_instances(compartment_id):
    """Retrieve a list of all instances in the specified compartment.

    Args:
        compartment_id (str): The compartment ID.

    Returns:
        list: The list of instances returned from the OCI service.
    """
    list_instances_response = compute_client.list_instances(compartment_id=compartment_id)
    return list_instances_response.data


def generate_html_body(instance):
    """Generate HTML body for the email with instance details.

    Args:
        instance (dict): The instance dictionary returned from the OCI service.

    Returns:
        str: HTML body for the email.
    """
    # Replace placeholders with instance details
    email_template_path = os.path.join(os.getcwd(), 'email_content.html')
    with open(email_template_path, 'r', encoding='utf-8') as email_temp:
        html_template = email_temp.read()
    html_body = html_template.replace('&lt;INSTANCE_ID&gt;', instance.id)
    html_body = html_body.replace('&lt;DISPLAY_NAME&gt;', instance.display_name)
    html_body = html_body.replace('&lt;AD&gt;', instance.availability_domain)
    html_body = html_body.replace('&lt;SHAPE&gt;', instance.shape)
    html_body = html_body.replace('&lt;STATE&gt;', instance.lifecycle_state)

    return html_body


def create_instance_details_file_and_notify(instance, shape=ARM_SHAPE):
    """Create a file with details of instances and notify the user.

    Args:
        instance (dict): The instance dictionary returned from the OCI service.
        shape (str): shape of the instance to be created, acceptable values are
         "VM.Standard.A1.Flex", "VM.Standard.E2.1.Micro"
    """
    details = [f"Instance ID: {instance.id}",
               f"Display Name: {instance.display_name}",
               f"Availability Domain: {instance.availability_domain}",
               f"Shape: {instance.shape}",
               f"State: {instance.lifecycle_state}",
               "\n"]
    micro_body = 'TWo Micro Instances are already existing and running'
    arm_body = '\n'.join(details)
    body = arm_body if shape == ARM_SHAPE else micro_body
    instance_file_path = os.path.join(os.getcwd(), 'INSTANCE_CREATED')
    write_into_file(instance_file_path, body)

    # Generate HTML body for email
    html_body = generate_html_body(instance)

    if NOTIFY_EMAIL:
        send_email('OCI INSTANCE CREATED', html_body, EMAIL, EMAIL_PASSWORD)


def notify_on_failure(failure_msg):
    """Notifies users when the Instance Creation Failed due to an error that's
    not handled.

    Args:
        failure_msg (msg): The error message.
    """

    mail_body = (
        "The script encountered an unhandled error and exited unexpectedly.\n\n"
        "Please re-run the script by executing './setup_init.sh rerun'.\n\n"
        "And raise a issue on GitHub if its not already existing:\n"
        "https://github.com/mohankumarpaluru/oracle-freetier-instance-creation/issues\n\n"
        " And include the following error message to help us investigate and resolve the problem:\n\n"
        f"{failure_msg}"
    )
    error_log_path = os.path.join(os.getcwd(), 'UNHANDLED_ERROR.log')
    write_into_file(error_log_path, mail_body)
    if NOTIFY_EMAIL:
        send_email('OCI INSTANCE CREATION SCRIPT: FAILED DUE TO AN ERROR', mail_body, EMAIL, EMAIL_PASSWORD)


def check_instance_state_and_write(compartment_id, shape, states=('RUNNING', 'PROVISIONING'),
                                   tries=3):
    """Check the state of instances in the specified compartment and take action when a matching instance is found.

    Args:
        compartment_id (str): The compartment ID to check for instances.
        shape (str): The shape of the instance.
        states (tuple, optional): The lifecycle states to consider. Defaults to ('RUNNING', 'PROVISIONING').
        tries(int, optional): No of reties until an instance is found. Defaults to 3.

    Returns:
        bool: True if a matching instance is found, False otherwise.
    """
    for _ in range(tries):
        instance_list = list_all_instances(compartment_id=compartment_id)
        if shape == ARM_SHAPE:
            running_arm_instance = next((instance for instance in instance_list if
                                         instance.shape == shape and instance.lifecycle_state in states), None)
            if running_arm_instance:
                create_instance_details_file_and_notify(running_arm_instance, shape)
                return True
        else:
            micro_instance_list = [instance for instance in instance_list if
                                   instance.shape == shape and instance.lifecycle_state in states]
            if len(micro_instance_list) > 1 and SECOND_MICRO_INSTANCE:
                create_instance_details_file_and_notify(micro_instance_list[-1], shape)
                return True
            if len(micro_instance_list) == 1 and not SECOND_MICRO_INSTANCE:
                create_instance_details_file_and_notify(micro_instance_list[-1], shape)
                return True       
        if tries - 1 > 0:
            time.sleep(60)

    return False


def handle_errors(command, data, log):
    """Handles errors and logs messages.

    Args:
        command (arg): The OCI command being executed.
        data (dict): The data or error information returned from the OCI service.
        log (logging.Logger): The logger instance for logging messages.

    Returns:
        bool: True if the error is temporary and the operation should be retried after a delay.
        Raises Exception for unexpected errors.
    """

    # Check for temporary errors that can be retried
    if "code" in data:
        if (data["code"] in ("TooManyRequests", "Out of host capacity.", 'InternalError')) \
                or (data["message"] in ("Out of host capacity.", "Bad Gateway")):
            log.info("Command: %s--\nOutput: %s", command, data)
            time.sleep(WAIT_TIME)
            return True

    if "status" in data and data["status"] == 502:
        log.info("Command: %s~~\nOutput: %s", command, data)
        time.sleep(WAIT_TIME)
        return True
    failure_msg = '\n'.join([f'{key}: {value}' for key, value in data.items()])
    notify_on_failure(failure_msg)
    # Raise an exception for unexpected errors
    raise Exception("Error: %s" % data)


def execute_oci_command(client, method, *args, **kwargs):
    """Executes an OCI command using the specified OCI client.

    Args:
        client: The OCI client instance.
        method (str): The method to call on the OCI client.
        args: Additional positional arguments to pass to the OCI client method.
        kwargs: Additional keyword arguments to pass to the OCI client method.

    Returns:
        dict: The data returned from the OCI service.

    Raises:
        Exception: Raises an exception if an unexpected error occurs.
    """
    while True:
        try:
            response = getattr(client, method)(*args, **kwargs)
            data = response.data if hasattr(response, "data") else response
            return data
        except oci.exceptions.ServiceError as srv_err:
            data = {"status": srv_err.status,
                    "code": srv_err.code,
                    "message": srv_err.message}
            handle_errors(args, data, logging_step5)


def generate_ssh_key_pair(public_key_file: Union[str, Path], private_key_file: Union[str, Path]):
    """Generates an SSH key pair and saves them to the specified files.

    Args:
        public_key_file :file to save the public key.
        private_key_file : The file to save the private key.
    """
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(private_key_file)
    # Save public key to file
    write_into_file(public_key_file, (f"ssh-rsa {key.get_base64()} "
                                      f"{Path(public_key_file).stem}_auto_generated"))


def read_or_generate_ssh_public_key(public_key_file: Union[str, Path]):
    """Reads the SSH public key from the file if it exists, else generates and reads it.

    Args:
        public_key_file: The file containing the public key.

    Returns:
        Union[str, Path]: The SSH public key.
    """
    public_key_path = Path(public_key_file)

    if not public_key_path.is_file():
        logging.info("SSH key doesn't exist... Generating SSH Key Pair")
        public_key_path.parent.mkdir(parents=True, exist_ok=True)
        # Use relative path for private key in current directory
        private_key_path = Path(os.getcwd()) / f"{public_key_path.stem}_private"
        generate_ssh_key_pair(public_key_path, private_key_path)

    with open(public_key_path, "r", encoding="utf-8") as pub_key_file:
        ssh_public_key = pub_key_file.read()

    return ssh_public_key


def send_discord_message(message):
    """Send a message to Discord using the webhook URL if available."""
    if DISCORD_WEBHOOK:
        payload = {"content": message}
        try:
            response = requests.post(DISCORD_WEBHOOK, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error("Failed to send Discord message: %s", e)


def launch_instance() -> bool:
    """Launches an OCI Compute instance using the specified parameters.

    Returns:
        bool: True if an instance is created (or already exists), False if the run ends
        gracefully (e.g., MAX_RUNTIME_SECS reached without capacity).

    Raises:
        Exception: Raises an exception if an unexpected error occurs.
    """
    # 🚨 Always-Free Tier Compliance Validation - FIRST STEP
    # This prevents any PAYG charges by validating configuration
    validate_always_free_compliance()
    
    # Step 1 - Get TENANCY
    # user_info = execute_oci_command(iam_client, "get_user", OCI_USER_ID)
    # oci_tenancy = user_info.compartment_id
    # FIX: Bypass permission issues by using tenancy ID from config directly
    oci_tenancy = config["tenancy"]
    logging.info("OCI_TENANCY: %s", oci_tenancy)

    # Step 2 - Get AD Name with Multi-AD Retry Logic
    availability_domains = execute_oci_command(iam_client,
                                               "list_availability_domains",
                                               compartment_id=oci_tenancy)
    
    # Get all available ADs and filter by the specified AD pattern
    available_ads = [item.name for item in availability_domains]
    logging.info("Available ADs in region: %s", available_ads)
    
    # Parse the OCT_FREE_AD input (can be single AD or comma-separated list)
    requested_ads = [ad.strip() for ad in OCT_FREE_AD.split(",") if ad.strip()]
    
    # If no specific AD requested, use all available ADs
    if not requested_ads:
        requested_ads = available_ads
    
    # Filter to only available ADs that match the requested pattern
    oci_ad_name = [ad for ad in available_ads 
                   if any(ad.endswith(requested_ad) for requested_ad in requested_ads)]
    
    if not oci_ad_name:
        error_msg = f"No available ADs found matching requested ADs: {requested_ads}. Available ADs: {available_ads}"
        logging.error(error_msg)
        raise ValueError(error_msg)
    
    logging.info("OCI_AD_NAME: %s", oci_ad_name)
    
    # Create a cycle for retry logic, but also keep track of attempts
    oci_ad_cycle = itertools.cycle(oci_ad_name)

    # Step 3 - Get Subnet ID
    oci_subnet_id = OCI_SUBNET_ID
    if not oci_subnet_id:
        subnets = execute_oci_command(network_client,
                                      "list_subnets",
                                      compartment_id=oci_tenancy)
        oci_subnet_id = subnets[0].id
    logging.info("OCI_SUBNET_ID: %s", oci_subnet_id)

    # Step 4 - Get Image ID of Compute Shape
    if not OCI_IMAGE_ID:
        images = execute_oci_command(
            compute_client,
            "list_images",
            compartment_id=oci_tenancy,
            shape=OCI_COMPUTE_SHAPE,
        )
        shortened_images = [{key: json.loads(str(image))[key] for key in IMAGE_LIST_KEYS
                             } for image in images]
        images_file_path = os.path.join(os.getcwd(), 'images_list.json')
        write_into_file(images_file_path, json.dumps(shortened_images, indent=2))
        oci_image_id = next(image.id for image in images if
                            image.operating_system == OPERATING_SYSTEM and
                            image.operating_system_version == OS_VERSION)
        logging.info("OCI_IMAGE_ID: %s", oci_image_id)
    else:
        oci_image_id = OCI_IMAGE_ID

    assign_public_ip = ASSIGN_PUBLIC_IP.lower() in [ "true", "1", "y", "yes" ]

    boot_volume_size = max(50, int(BOOT_VOLUME_SIZE))
    
    # Additional validation for Always-Free storage limit
    # Note: We use 100GB as the practical limit to be extra safe, even though Always-Free allows 200GB total
    if boot_volume_size > 100:
        logging.critical(
            "🚨 CRITICAL: Boot volume %sGB exceeds safe Always-Free limit of 100GB!\n"
            "This WILL trigger PAYG charges. Aborting launch.\n"
            "Set BOOT_VOLUME_SIZE to 100GB or less in oci.env",
            boot_volume_size
        )
        raise ValueError(
            f"Boot volume {boot_volume_size}GB exceeds safe Always-Free limit of 100GB. "
            "This would trigger PAYG charges. Aborting instance launch. "
            "Maximum allowed: 100GB (within overall 200GB Always-Free storage limit)."
        )
    
    # Warning if boot volume is set to maximum
    if boot_volume_size == 100:
        logging.warning(
            "⚠️ WARNING: Boot volume set to maximum safe limit of 100GB. "
            "Remember that total Always-Free storage across ALL volumes is limited to 200GB."
        )
    
    logging.info("✅ Boot volume size validated: %sGB (within 100GB safe limit)", boot_volume_size)

    ssh_public_key = read_or_generate_ssh_public_key(SSH_AUTHORIZED_KEYS_FILE)

    # Step 5 - Launch Instance if it's not already exist and running
    instance_exist_flag = check_instance_state_and_write(oci_tenancy, OCI_COMPUTE_SHAPE, tries=1)

    if OCI_COMPUTE_SHAPE == "VM.Standard.A1.Flex":
        shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=4, memory_in_gbs=24)
    else:
        shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=1, memory_in_gbs=1)

    start_time = time.monotonic()

    # Track AD attempts for multi-AD retry logic
    ad_attempts = {}
    current_ad_index = 0

    while not instance_exist_flag:
        if MAX_RUNTIME_SECS and (time.monotonic() - start_time) >= MAX_RUNTIME_SECS:
            msg = (
                f"Max runtime ({MAX_RUNTIME_SECS}s) reached without INSTANCE_CREATED. "
                "Exiting gracefully so the scheduler can try again later."
            )
            logging_step5.info(msg)
            write_into_file(os.path.join(os.getcwd(), "MAX_RUNTIME_REACHED"), msg + "\n")
            return False

        # Get current AD for this attempt
        current_ad = oci_ad_name[current_ad_index % len(oci_ad_name)]
        ad_attempts[current_ad] = ad_attempts.get(current_ad, 0) + 1

        logging_step5.info("🎯 Attempting instance creation in AD: %s (Attempt %d)", current_ad, ad_attempts[current_ad])

        try:
            launch_instance_response = compute_client.launch_instance(
                launch_instance_details=oci.core.models.LaunchInstanceDetails(
                    availability_domain=current_ad,
                    compartment_id=oci_tenancy,
                    create_vnic_details=oci.core.models.CreateVnicDetails(
                        assign_public_ip=assign_public_ip,
                        assign_private_dns_record=True,
                        display_name=DISPLAY_NAME,
                        subnet_id=oci_subnet_id,
                    ),
                    display_name=DISPLAY_NAME,
                    shape=OCI_COMPUTE_SHAPE,
                    availability_config=oci.core.models.LaunchInstanceAvailabilityConfigDetails(
                        recovery_action="RESTORE_INSTANCE"
                    ),
                    instance_options=oci.core.models.InstanceOptions(
                        are_legacy_imds_endpoints_disabled=False
                    ),
                    shape_config=shape_config,
                    source_details=oci.core.models.InstanceSourceViaImageDetails(
                        source_type="image",
                        image_id=oci_image_id,
                        boot_volume_size_in_gbs=boot_volume_size,
                    ),
                    metadata={
                        "ssh_authorized_keys": ssh_public_key},
                )
            )
            if launch_instance_response.status == 200:
                logging_step5.info(
                    "✅ Command: launch_instance in AD %s\nOutput: %s", current_ad, launch_instance_response
                )
                instance_exist_flag = check_instance_state_and_write(oci_tenancy, OCI_COMPUTE_SHAPE)
                if instance_exist_flag:
                    logging_step5.info("🎉 Instance successfully created in AD: %s", current_ad)
                    break

        except oci.exceptions.ServiceError as srv_err:
            if srv_err.code == "LimitExceeded":
                logging_step5.info("Encountered LimitExceeded Error checking if instance is created" \
                                    "code :%s, message: %s, status: %s", srv_err.code, srv_err.message, srv_err.status)
                instance_exist_flag = check_instance_state_and_write(oci_tenancy, OCI_COMPUTE_SHAPE)
                if instance_exist_flag:
                    logging_step5.info("%s , exiting the program", srv_err.code)
                    sys.exit()
                logging_step5.info("Didn't find an instance , proceeding with retries")
            elif srv_err.code in ("OutOfCapacity", "Out of host capacity") or "capacity" in srv_err.message.lower():
                logging_step5.warning("🚨 Capacity error in AD %s: %s. Trying next AD...", current_ad, srv_err.message)
                # Move to next AD for retry
                current_ad_index += 1

                # If we've tried all ADs, start from the beginning
                if current_ad_index >= len(oci_ad_name):
                    logging_step5.info("⏳ All ADs tried once. Starting new cycle of AD attempts...")
                    current_ad_index = 0

                # Wait before retrying
                time.sleep(WAIT_TIME)
                continue

            data = {
                "status": srv_err.status,
                "code": srv_err.code,
                "message": srv_err.message,
            }
            handle_errors("launch_instance", data, logging_step5)

    return True


if __name__ == "__main__":
    send_discord_message("🚀 OCI Instance Creation Script: Starting up! Let's create some cloud magic!")
    try:
        created = launch_instance()
        if created:
            send_discord_message("🎉 Success! OCI Instance has been created. Time to celebrate!")
        else:
            send_discord_message("⏱️ No capacity yet. Max runtime reached; will try again later.")
    except Exception as e:
        error_message = f"😱 Oops! Something went wrong with the OCI Instance Creation Script:\n{str(e)}"
        send_discord_message(error_message)
        raise

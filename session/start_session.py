import boto3
import configparser
import os
from helpers.validation import assert_profile_configured
from helpers.time_parse import seconds_to_time
from helpers.rc_update import update_rc_file


def start_session(user, account, duration=None, region=None, session_profile=None, mfa_code=None):
    """
    Start an AWS session for a user.
    :param user: Dictionary containing user's name and MFA ARN.
    :param account: Dictionary containing account name.
    :param duration: Session duration in seconds.
    :param region: AWS region.
    :param session_profile: AWS CLI session profile name.
    :param mfa_code: MFA token code.
    """
    source_profile = f"{account['name']}_{user['name']}"
    assert_profile_configured(source_profile)

    duration = duration or 14400
    region = region or "us-west-2"
    session_profile = session_profile or f"mfa-{user['name']}"
    token_code = mfa_code or input("Enter the MFA token code: ")

    session = boto3.Session(profile_name=source_profile)
    sts_client = session.client("sts")

    try:
        credentials = sts_client.get_session_token(
            SerialNumber=user["mfa-arn"], TokenCode=token_code, DurationSeconds=duration
        )
    except Exception as e:
        handle_exception(e)
        exit(1)

    update_default_session(credentials["Credentials"], source_profile)
    update_or_create_profiles(session_profile, region, credentials["Credentials"])
    update_rc_file(f"export AWS_PROFILE={session_profile}")

    print(f"Temporary profile {session_profile} created or updated.")
    print(f"Session expires in {seconds_to_time(duration)}.")


def handle_exception(e):
    """
    Handle exceptions related to AWS session.
    :param e: Exception.
    """
    err_msg = str(e)
    if "AccessDenied" in err_msg:
        print("Invalid MFA code.")
    elif "Parameter validation failed" in err_msg:
        print("Invalid MFA code format.")
    else:
        print(f"An unexpected error occurred: {e}")
    exit(1)


def update_default_session(credentials, source_profile):
    """
    Update the default session credentials.
    :param credentials: Dictionary containing AWS credentials.
    :param source_profile: AWS CLI source profile name.
    """
    boto3.setup_default_session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        profile_name=source_profile,
    )


def update_or_create_profiles(session_profile, region, credentials):
    """
    Update or create AWS CLI profiles.
    :param session_profile: Session Profile name.
    :param region: AWS region.
    :param credentials: Dictionary containing AWS credentials.
    """
    update_config("~/.aws/config", session_profile, {"region": region})
    update_config(
        "~/.aws/credentials",
        session_profile,
        {
            "aws_access_key_id": credentials["AccessKeyId"],
            "aws_secret_access_key": credentials["SecretAccessKey"],
            "aws_session_token": credentials["SessionToken"],
        },
    )


def update_config(file_path, session_profile, values):
    """
    Update an AWS configuration file.
    :param file_path: Path to the file.
    :param session_profile: Session Profile name.
    :param values: Dictionary containing key-value pairs to update.
    """
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(file_path))
    config[session_profile] = values

    with open(os.path.expanduser(file_path), "w") as f:
        config.write(f)

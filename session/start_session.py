import boto3
import configparser
import os
from helpers.time_parse import seconds_to_time
from helpers.rc_update import update_rc_file


def start_session(user, account, duration=900, region='us-west-2', profile_name=None, mfa_code=None):
    print(profile_name)

    region, user_name, mfa_arn = region, user['name'], user['mfa-arn']
    profile_name = profile_name or f"mfa-{user_name}"
    token_code = mfa_code or input('Enter the MFA token code: ')

    session = boto3.Session(profile_name=f"{account['name']}_{user['name']}")
    sts_client = session.client('sts')

    try:
        credentials = sts_client.get_session_token(
            SerialNumber=mfa_arn, TokenCode=token_code, DurationSeconds=duration)
    except Exception as e:
        handle_exception(e)
        exit(1)

    update_default_session(
        credentials['Credentials'], f"{account['name']}_{user['name']}")

    update_or_create_profiles(
        profile_name, region, credentials['Credentials'])

    update_rc_file(f"export AWS_PROFILE={profile_name}")
    
    print(f"Temporary profile {profile_name} created or updated.")
    print(f"Session expires in {seconds_to_time(duration)}.")


def handle_exception(e):
    err_msg = str(e)
    if 'AccessDenied' in err_msg:
        print("Invalid MFA code.")
    elif 'Parameter validation failed' in err_msg:
        print("Invalid MFA code format.")
    else:
        print(f"An unexpected error occurred: {e}")
    print(err_msg)
    exit(1)


def update_default_session(credentials, user_name):
    boto3.setup_default_session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        profile_name=user_name
    )


def update_or_create_profiles(profile_name, region, credentials):
    update_config('~/.aws/config', profile_name, {'region': region})
    update_config(
        '~/.aws/credentials', profile_name, {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken']
        })


def update_config(file_path, profile_name, values):
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(file_path))

    config[profile_name] = values

    with open(os.path.expanduser(file_path), 'w') as f:
        config.write(f)

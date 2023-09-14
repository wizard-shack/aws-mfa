import configparser
import json
import os
import yaml
from textwrap import dedent
from jsonschema import validate, exceptions


def get_valid_config():
    print(os.getenv("AWS_MFA_HOME"))
    print("config-schema.json")

    """Returns the config if it matches the schema"""
    with open(
        os.path.join(os.getenv("AWS_MFA_HOME"), "config-schema.json"), "r"
    ) as file:
        schema = json.load(file)

    with open(os.path.join(os.getenv("AWS_MFA_HOME"), "config.yaml"), "r") as file:
        config = yaml.safe_load(file)

    try:
        validate(config, schema)
    except exceptions.ValidationError as e:
        raise exceptions.ValidationError("config file does not match schema") from e
    else:
        return config


def assert_profile_configured(profile_name):
    """
    Check that a given AWS profile exists in a given AWS configuration or credentials file.

    Parameters:
    - profile_name: str

    Exits program with status 1 if the profile is not found.
    """

    config = configparser.ConfigParser()

    # Check config file
    file_path = os.path.expanduser("~/.aws/config")
    config.read(file_path)

    if f"profile {profile_name}" not in config.sections():
        error_message = dedent(
            f""" 
            ! ERROR ! 
            Source profile not found in {file_path}. 
            Please run `aws configure --profile {{account_name}}_{{user_name}}` 
        """
        )
        print(error_message)
        exit(1)

    # Check credentials file
    file_path = os.path.expanduser("~/.aws/credentials")
    config.read(file_path)

    if profile_name not in config.sections():
        error_message = f"""
        Source profile not found in {file_path}.
        Please run `aws configure --profile {{account_name}}_{{user_name}}`
        """
        print(error_message)
        exit(1)

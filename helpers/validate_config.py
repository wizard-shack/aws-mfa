import json
import os
import yaml
from jsonschema import validate, exceptions

def get_valid_config():

    print(os.getenv('AWS_MFA_HOME'))
    print('config-schema.json')

    '''Returns the config if it matches the schema'''
    with open(os.path.join(os.getenv('AWS_MFA_HOME'), 'config-schema.json'), 'r') as file:
        schema = json.load(file)

    with open(os.path.join(os.getenv('AWS_MFA_HOME'), 'config.yaml'), 'r') as file:
        config = yaml.safe_load(file)

    try:
        validate(config, schema)
    except exceptions.ValidationError as e:
        raise exceptions.ValidationError("config file does not match schema") from e
    else:
        return config

# TODO Add function to compare against local aws profiles
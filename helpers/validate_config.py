import json
import yaml
from jsonschema import validate, exceptions

def get_valid_config():
    '''Returns the config if it matches the schema'''
    with open('config-schema.json', 'r') as file:
        schema = json.load(file)

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    try:
        validate(config, schema)
    except exceptions.ValidationError as e:
        raise exceptions.ValidationError("config file does not match schema") from e
    else:
        return config

# TODO Add function to compare against local aws profiles
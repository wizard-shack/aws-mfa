import subprocess, os

def get_editor():
    return os.environ.get('EDITOR') or os.environ.get('VISUAL') or 'vi'


def edit_config(editor):
    '''Edit the config file'''
    config_file_path = os.path.expanduser("~/.aws-mfa/config.yaml")
    subprocess.run([editor or get_editor(), config_file_path])
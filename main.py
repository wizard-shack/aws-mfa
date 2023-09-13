#!/path/to/python
from helpers import menu, options_parse, config_edit
from session.start_session import start_session


# Parse any script options
options = options_parse.parse_options()

# User wants to edit the config file
if (options.config):
    config_edit.edit_config(options.editor)
    exit(0)

# Get the user and account details
account = menu.get_account()
user = menu.get_user(account)

# Start the session and update profiles
# TODO: Don't do two things in one function
start_session(user,
    account,
    duration=options.duration,
    region=options.region,
    profile_name=options.profile,
    mfa_code=options.mfa_code
    )

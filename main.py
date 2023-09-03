#!/path/to/python
from helpers import menu, options_parse, config_edit
from session.start_session import start_session


options = options_parse.parse_options()

# User wants to edit the config file
if (options.config):
    config_edit.edit_config(options.editor)
    exit(0)

# Get the user details
user = menu.get_user()

print(user)

# Start the session and update profiles
start_session(user,
              duration=options.duration,
              region=options.region,
              profile_name=options.profile,
              mfa_code=options.mfa_code
              )

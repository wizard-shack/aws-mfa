import os

def modify_rc_file(shell_rc_file, line_to_add):
    lines = []
    line_found = False
    
    # Read the existing lines in the rc file
    if os.path.exists(shell_rc_file):
        with open(shell_rc_file, 'r') as f:
            lines = f.readlines()

    # Modify the lines list, adding or replacing the relevant line
    new_lines = []
    for line in lines:
        if "export AWS_PROFILE=" in line:
            line_found = True
            new_lines.append(line_to_add + '\n')
        else:
            new_lines.append(line)

    # If the line was not found, append it
    if not line_found:
        new_lines.append(line_to_add + '\n')

    # Write back to the rc file
    with open(shell_rc_file, 'w') as f:
        f.writelines(new_lines)

def update_rc_file(line_to_add):
    # Identify the default shell and the corresponding rc file
    default_shell = os.environ.get('SHELL', '/bin/bash')
    # line_to_add = "export AWS_PROFILE=blah"

    if 'bash' in default_shell:
        modify_rc_file(os.path.expanduser('~/.bashrc'), line_to_add)
        print(f"Updated ~/.bashrc with {line_to_add}")
    elif 'zsh' in default_shell:
        modify_rc_file(os.path.expanduser('~/.zshrc'), line_to_add)
        print(f"Updated ~/.zshrc with {line_to_add}")
    # TODO: Add additional shells here
    else:
        print(f"Unsupported shell: {default_shell}")

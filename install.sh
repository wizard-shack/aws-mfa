#!/bin/sh

# Global Variables
PROJECT_DIR="$HOME/.aws-mfa"
CONFIG_FILE_SELECTION=0

# Function to display file content with separators
display_file() {
    max_length=$(awk '{ if (length > max) max = length } END { print max }' "$1")
    printf '%*s\n' "$max_length" | tr ' ' "-"
    echo ""
    cat "$1"
    printf '%*s\n' "$max_length" | tr ' ' "-"
    echo ""
}

# Prompt if aws-mfa is already installed
prompt_existing_install() {
    echo "aws-mfa appears to be already installed with a modified config file."
    echo "Select which config file to use:\n"

    echo "1. (Installed file)"
    display_file "$PROJECT_DIR/config.yaml"
    
    echo "2. (New file)"
    display_file "config.yaml"
    
    read -r -p "Keep which config file? [1/2]: " CONFIG_FILE_SELECTION
    
    case "$CONFIG_FILE_SELECTION" in
        "1") echo "Keeping existing config." ;;
        "2") echo "Replacing with new config." ;;
        *) echo "Invalid choice. Exiting."; exit 1 ;;
    esac

    read -r -p "Proceed with reinstall? [y/n]: " reinstall
    [ "$reinstall" != "y" ] && { echo "Exiting."; exit 0; }
}

# Install required Python packages
install_dependencies() {
    echo "Installing python dependencies"
    pip install -q -r requirements.txt
}

# Set Python interpreter path in installed copy of main.py
set_python_path() {
    default_python_path=$(command -v python)
    read -r -p "Python path? [Default: $default_python_path]: " python_path
    : "${python_path:=$default_python_path}"

    if ! command -v "$python_path" > /dev/null 2>&1; then
        echo "Invalid Python path. Exiting."
        exit 1
    fi
    
    sed "1s@.*@#!$python_path@" "$PROJECT_DIR/main.py" > tmp && mv tmp "$PROJECT_DIR/main.py"
    chmod u+x "$PROJECT_DIR/main.py"
}

# Set shell alias for aws-mfa
set_shell_alias() {
    case "$SHELL" in
        *bash) rcfile="$HOME/.bashrc" ;;
        *zsh) rcfile="$HOME/.zshrc" ;;
        *) echo "Unsupported shell. Enter RC file path: "; read -r rcfile ;;
    esac

    [ ! -f "$rcfile" ] && { echo "Invalid RC file. Exiting."; exit 1; }

    # Remove existing alias if present
    sed -i '/^alias aws-mfa=/d' "$rcfile"

    # Add new alias
    echo "alias aws-mfa='$PROJECT_DIR/main.py'" >> "$rcfile"
}

# Export variables
export_variables() {
    case "$SHELL" in
        *bash) rcfile="$HOME/.bashrc" ;;
        *zsh) rcfile="$HOME/.zshrc" ;;
        *) echo "Unsupported shell. Enter RC file path: "; read -r rcfile ;;
    esac

    [ ! -f "$rcfile" ] && { echo "Invalid RC file. Exiting."; exit 1; }

    # Remove existing export if present
    sed -i '/^export AWS_MFA_HOME=/d' "$rcfile"

    # Add new export
    echo "export AWS_MFA_HOME=$PROJECT_DIR" >> "$rcfile"
}


[ -d "$PROJECT_DIR" ] && ! diff -q "$PROJECT_DIR/config.yaml" "config.yaml" > /dev/null && prompt_existing_install

mkdir -p "$PROJECT_DIR"
cp main.py config-schema.json requirements.txt "$PROJECT_DIR"
[ "$CONFIG_FILE_SELECTION" -eq 2 ] && cp config.yaml "$PROJECT_DIR"  # Only copy if option 2 is selected
cp -R helpers session "$PROJECT_DIR"
install_dependencies
set_python_path
export_variables
set_shell_alias

echo "Installation complete. Restart shell and start a session with 'aws-mfa'."

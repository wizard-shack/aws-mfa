# aws-mfa
A lightweight utility to manage local aws user credentials with MFA enabled. 

## Prerequisites
1. Have an AWS IAM user with:
    - An MFA device enabled and synced
    - Permissions to call `sts:GetSessionToken`
    - Access keys
2. Apply an "Explicit Deny All" policy, with an MFA condition, to your user permissions, a permissions boundary, or globally via the Identity Center (preferred).
    ```{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "RequireMFA",
          "Effect": "Deny",
          "Action": "*",
          "Resource": "*",
          "Condition": {
            "BoolIfExists": {
              "aws:MultiFactorAuthPresent": "false"
            }
          }
        }
      ]
    }
    ```


## How it works
Your user should be configured locally with `aws configure`, just as you normally would, but because of the MFA condition (above) it cannot make any API requests without an STS Session Token using MFA. If you were to leak your access keys at this point, they'd be useless without the MFA device because the condition `"aws:MultiFactorAuthPresent": "false"` is met.

By calling [`aws sts get-session-token`](https://docs.aws.amazon.com/cli/latest/reference/sts/get-session-token.html) and providing the MFA code, you will start a timed session for the user, which changes `aws:MultiFactorAuthPresent` to `true`, and in-turn makes the user qualified to make API requests.


## Setup and Installation  
1. Make `config.yaml` in the project root directory and populate it with the required account details.
    1. Account Name (Account ID or Alias)
    2. User Name (Profile name for the active user)
    3. ARN for the User's MFA device

    Notes:
    The User Name 

    ```yaml
    # `config.yaml` example
    ---
    accounts:
      - name: 123412341234
        users :
          - name: bob
            mfa-arn: arn:aws:iam::{ACCOUNTID}:mfa/bob
      - name: accountAlias
        users :
          - name: joan
            mfa-arn: arn:aws:iam::{ACCOUNTID}:mfa/joan
          - name: mike
            mfa-arn: arn:aws:iam::{ACCOUNTID}:mfa/mike
    ```
2. Run the `install.sh` script and follow prompts
    - This will copy neccessary files to `$HOME/.aws-mfa/`
    - Makes `aws-mfa` an alias to executing the `main.py` script
    
3. Start a new shell and run `aws-mfa --help` to see options.

## Usage
`aws-mfa [-h] [--mfa-code MFA_CODE] [--profile PROFILE] [--config] [--editor EDITOR] [--region REGION] [--duration DURATION]`
```
options:
  -h, --help            show this help message and exit
  --mfa-code MFA_CODE, -m MFA_CODE
                        Multi-Factor Authentication code
  --profile PROFILE, -p PROFILE
                        Profile name to store the temporary credentials in. (Default: mfa-{User Profile Name})
  --config, -c          Enable config mode
  --editor EDITOR, -e EDITOR
                        Specify an editor to use. (Default: vi))
  --region REGION, -r REGION
                        Specify an AWS region. (Default: us-west-2)
  --duration DURATION, -d DURATION
                        Session duration in seconds. (Default: 900))
```

## Code Walkthrough



## FAQ
1. Why are files copied to `$HOME/.aws-mfa/` instead of running from the clones repo?
    - **Idempotency** - We want the cloned repo to remain unchanged to ensure predictable behavior.

2. Can I edit the files in `$HOME/.aws-mfa/` ?
    - Ideally, you wouldn't need to. The installed utility has a `--config` option that'll open the `$HOME/.aws-mfa/config.yaml` file for editing. Other files shouldn't need editing.
    - If you'd like to add or expand functionality, edit the source repo and re-install using `install.sh`. (And open a PR! 😃 )
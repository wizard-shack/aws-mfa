import argparse
import os


def parse_options():
    parser = argparse.ArgumentParser(description="Parse command-line options.")

    # --mfa-code or -m
    parser.add_argument(
        "--mfa-code", "-m", type=str, help="Multi-Factor Authentication code"
    )

    # --profile or -p
    parser.add_argument(
        "--session-profile",
        "-s",
        type=str,
        help="The Session Profile name to store the temporary credentials in. (Default: mfa-{Source Profile Name})",
    )

    # --region or -r
    parser.add_argument(
        "--region",
        "-r",
        type=str,
        help="Specify an AWS region. (Default: us-west-2)",
        default="us-west-2",
    )

    # --duration or -d
    parser.add_argument(
        "--duration",
        "-d",
        type=int,
        help="Session duration in seconds. (Default: 14400 (4 hours))",
        default=14400,
    )

    # --config or -c
    parser.add_argument(
        "--config", "-c", action="store_true", help="Enable config mode"
    )

    # --editor or -e
    parser.add_argument(
        "--editor",
        "-e",
        type=str,
        help=f"Specify an editor to use. (Default: {os.environ.get('EDITOR') or os.environ.get('VISUAL') or 'vi'}))",
        default=os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vi",
    )

    args = parser.parse_args()
    return args

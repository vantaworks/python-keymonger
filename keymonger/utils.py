import logging
import argparse


def log_setup(verbosity):
    log_format = "%(asctime)s - %(filename)s:%(lineno)s:%(funcName)s - %(levelname)s - %(message)s"
    if verbosity:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(level=logging.INFO, format=log_format)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    return logging.getLogger(__name__)


def arg_parser():
    args = argparse.ArgumentParser(description="A key management utility")
    args.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        default=False,
        help="Force writeing of the authorized keys file: ignore idempotency (default: False)",
    )
    args.add_argument(
        "-s",
        "--skip-perms",
        dest="skip_perms",
        action="store_true",
        default=False,
        help="Skip setting permissions/ownership (default: False)",
    )
    args.add_argument(
        "-c",
        "--config",
        dest="config_path",
        default="keymonger.conf",
        help="Specify the location of the config file (default: './keymonger.conf')",
    )
    args.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Increase the logging level for debugging (default: False)",
    )
    return args.parse_args()

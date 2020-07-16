import argparse
import logging
import json
import pwd
import os
import sys

LOG = logging.getLogger(__name__)


def update_permissions(user, user_config):
    LOG.debug('Permissions for "%s" ', user_config["destination"])
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(user).pw_gid
    except KeyError as e:
        LOG.error("Unable to find user \"{}\"".format(user))
    chmod = 0o600
    LOG.debug('Setting perms = "%s"', oct(chmod)[2:])
    os.chmod(user_config["destination"], chmod)
    LOG.debug('Setting owner UID = "%s"', uid)
    LOG.debug('Setting owner GID = "%s"', gid)
    os.chown(user_config["destination"], uid, gid)


def write_authorized_keys(destination, keys):
    with open(destination, "w") as authorized_keys_file:
        authorized_keys_file.write(keys)


def load_config(config_path):
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config


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
        default="config.json",
        help="Specify the location of the config file (default: './config.json')",
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

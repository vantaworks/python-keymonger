#!/usr/bin/env python3

__author__ = "Robert Rice"


from .config import load_configs
from .getter import get_remote_keys
from .utils import log_setup, arg_parser
from .writer import (
    set_key_destination,
    read_key_destination,
    write_authorized_keys,
    update_permissions,
)


def main():
    args = arg_parser()
    verbose = args.verbose
    logger = log_setup(verbose)

    force = args.force
    config_path = args.config_path
    logger.debug("Config path = %s", config_path)

    logger.debug("Loading configs")
    [GLOBAL_CONFIG, USER_CONFIG] = load_configs(config_path)
    logger.debug("Configs loaded")

    for user in USER_CONFIG.sections():
        logger.debug("Processing user: %s", user)

        logger.debug("Fetching keys")
        USER_CONFIG[user]["fetched_keys"] = get_remote_keys(
            USER_CONFIG[user]["key_sources"]
        )
        logger.debug("Keys fetched")

        logger.debug("Verifying configs")
        USER_CONFIG[user]["key_destination"] = (
            set_key_destination(user)
            if "key_destination" not in USER_CONFIG[user]
            else USER_CONFIG[user]["key_destination"]
        )
        logger.debug("Configs verified")

        if force != True:
            logger.debug("Force FALSE")

            logger.debug("Reading local keys")
            USER_CONFIG[user]["local_keys"] = read_key_destination(
                USER_CONFIG[user]["key_destination"]
            )
            logger.debug("Local keys read")

            logger.debug("Determing write necessity")
            USER_CONFIG[user]["changed"] = (
                "yes"
                if USER_CONFIG[user]["local_keys"] != USER_CONFIG[user]["fetched_keys"]
                else "no"
            )
            logger.debug("Write necessary = %s", USER_CONFIG[user]["changed"])

        if (
            "changed" in USER_CONFIG[user] and USER_CONFIG[user]["changed"] == "yes"
        ) or force == True:

            logger.debug("Writing config")
            write_authorized_keys(
                USER_CONFIG[user]["key_destination"], USER_CONFIG[user]["fetched_keys"]
            )
            logger.debug("Write complete")

            logger.debug("Updating permissions")
            update_permissions(user, USER_CONFIG[user]["key_destination"])
            logger.debug("Permissions updated")


if __name__ == "__main__":
    main()

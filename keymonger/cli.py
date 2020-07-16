from pathlib import Path
from .funcs import (
    __version__,
    key_grabber,
    data_hasher,
)
from .utils import (
    log_setup,
    arg_parser,
    load_config,
    update_permissions,
    write_authorized_keys,
)


def main():
    args = arg_parser()

    LOG = log_setup(args.verbose)  # pylint: disable=C0103

    config = load_config(args.config_path)

    mapping = config["mapping"]

    for user in mapping:
        user_config = mapping[user]

        LOG.debug("Fetching keys for %s", user)
        fetched_keys = key_grabber(user_config["sources"])
        LOG.debug("Fetching complete")

        if "destination" not in user_config:
            destination = str(Path.home() / ".ssh/authorized_keys")
            LOG.debug(
                'Destination not explicitly set, assuming "%s" as destination',
                destination,
            )
            user_config["destination"] = destination

        if not args.force:
            LOG.debug("Performing idempotency checks")
            data_hash = data_hasher(fetched_keys)
            LOG.debug('Fetched data hash  = "%s"', data_hash)
            try:
                with open(user_config["destination"], "r") as authorized_keys_file:
                    keys_from_file = authorized_keys_file.read()
            except FileNotFoundError:
                LOG.debug("Destination empty")
                keys_from_file = ""
            file_hash = data_hasher(keys_from_file)
            LOG.debug('Existing file hash = "%s"', file_hash)
            write_file = data_hash != file_hash
        else:
            LOG.warning("Ignoring idempotency checks due to `-f` flag")
            write_file = True

        if write_file:
            LOG.info('Creating/updating "%s"', user_config["destination"])
            write_authorized_keys(user_config["destination"], fetched_keys)
        else:
            LOG.debug("No changes to content. Moving on...")

        if not args.skip_perms:
            update_permissions(user, user_config)

        LOG.debug("Finished keys for %s", user)


if __name__ == "__main__":
    main()

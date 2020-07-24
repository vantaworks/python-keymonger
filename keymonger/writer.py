from os.path import expanduser
from os import chmod, chown
from pwd import getpwnam


def set_key_destination(user):
    return expanduser(f"~{user}/.ssh/authorized_keys")


def read_key_destination(key_destination):
    try:
        with open(key_destination, "r") as authorized_keys_file:
            keys_from_file = authorized_keys_file.read()
    except FileNotFoundError:
        keys_from_file = ""
    return keys_from_file


def write_authorized_keys(destination, keys):
    with open(destination, "w") as authorized_keys_file:
        authorized_keys_file.write(keys)


def update_permissions(user, destination):
    uid_value = getpwnam(user).pw_uid
    gid_value = getpwnam(user).pw_gid
    chmod_value = 0o600
    chmod(destination, chmod_value)
    chown(destination, uid_value, gid_value)

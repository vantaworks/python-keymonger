import hashlib
import logging
import requests

__version__ = "0.1"

KEYMONGER_BANNER = "Managed by keymonger"
KEYMONGER_HEADERS = {
    "User-Agent": "keymonger/{}".format(__version__),
}

LOG = logging.getLogger("tests")


def key_grabber(source_list):
    fetched_keys = "#### %s ####" % KEYMONGER_BANNER
    for source in source_list:
        raw_keys = (
            requests.get(source, headers=KEYMONGER_HEADERS)
            .content.decode("utf-8")
            .split("\n")
        )
        LOG.debug("Fetched %s keys from %s", len(raw_keys), source)
        for key_raw in raw_keys:
            if key_raw != "":
                key_split = key_raw.split(" ")
                fetched_keys = (
                    fetched_keys + "\n" + "{} {}".format(key_split[0], key_split[1])
                )
    return fetched_keys


def data_hasher(data):
    hasher = hashlib.md5()
    hasher.update(data.encode("utf-8"))
    return hasher.hexdigest()

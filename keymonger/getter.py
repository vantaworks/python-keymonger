import requests

__version__ = "0.0.2"
KEYMONGER_BANNER = "Managed by keymonger"
KEYMONGER_HEADERS = {
    "User-Agent": "keymonger/{}".format(__version__),
}


def listifier(dubious_list):
    if not isinstance(dubious_list, list):
        if "," in dubious_list:
            indubitable_list = dubious_list.split(",")
        else:
            indubitable_list = [dubious_list]
    else:
        indubitable_list = dubious_list
    return indubitable_list


def get_remote_keys(source_list):
    fetched_keys = "#### %s ####" % KEYMONGER_BANNER
    source_list = listifier(source_list)
    for source in source_list:
        raw_keys = (
            requests.get(source, headers=KEYMONGER_HEADERS)
            .content.decode("utf-8")
            .split("\n")
        )
        for key_raw in raw_keys:
            if key_raw != "":
                key_split = key_raw.split(" ")
                fetched_keys = (
                    fetched_keys + "\n" + "{} {}".format(key_split[0], key_split[1])
                )
    return fetched_keys

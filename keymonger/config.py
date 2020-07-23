import configparser
from glob import glob


def load_configs(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    if "include_config" in config["global"]:
        include_config_paths = glob(config["global"]["include_config"])
        for include_config_path in include_config_paths:
            include_config = configparser.ConfigParser()
            include_config.read(include_config_path)
            for section in include_config.sections():
                config[section] = include_config[section]

    global_config = configparser.ConfigParser()
    global_config["global"] = config["global"]
    config.remove_section("global")
    return [global_config, config]

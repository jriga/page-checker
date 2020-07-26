import json


class MalFormattedConfig(Exception):
    """Exception raised when config file could not be parsed"""
    pass


def load_file(path):
    try:
        with open(path) as io:
            return json.load(io)
    except FileNotFoundError as ex:
        raise ex
    except:
        raise MalFormattedConfig(f"file at {path}")


def load(data):
    config = None
    path = data.pop("configuration", None)
    if path:
        config = load_file(path)

    default_urls = config['urls']
    config.update(data)
    if not config['urls']:
        config['urls'] = default_urls

    if config.get('persist', False) and not config.get('db_path', None):
        raise MalFormattedConfig('Missing "db_path" in config')

    return config

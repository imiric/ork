import yaml


def load_config(path=''):
    if getattr(load_config, '_config', {}):
        return load_config._config

    with open(path) as f:
        load_config._config = yaml.load(f.read())
    return load_config._config

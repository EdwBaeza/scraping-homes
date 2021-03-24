import os
import yaml
import json


class Meta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        cls._instance.__dict__.update(kwargs)

        return cls._instance


class Config(metaclass=Meta):
    def __init__(self, *args, **kwargs):
        pass


def _read_settings_yaml():
    with open('settings.yaml', 'r') as file_stream:
        yaml_loaded = yaml.load(file_stream, Loader=yaml.FullLoader)

    return yaml_loaded

def get_config():
    settings_yaml = _read_settings_yaml()
    return Config(**{ **dict(os.environ), **settings_yaml })

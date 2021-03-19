#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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


def get_config() -> Config:
    return Config(**dict(os.environ))

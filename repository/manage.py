#!/usr/bin/env python
import sys
import os

from migrate.versioning.shell import main

sys.path.append(f"{os.getcwd()}/libs")
from config import get_config


def generate_database_url():
    config = get_config()
    drive = 'postgresql+psycopg2'
    access = f"{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    return f"{drive}://{access}"

if __name__ == '__main__':
    main(url=generate_database_url(), repository='repository', debug='False')

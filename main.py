import argparse
import logging
import commands
from spiders.homes import LaMudi
from libs.browsers.chrome_builder import ChromeBuilder
from libs.config import get_config
from libs.logger import logger_setup

config = get_config()
# TODO: Add flag for select browser
SPIDERS = {
    'la_mudi': lambda: LaMudi(ChromeBuilder(), **config.browser)
}

def main():
    logger_setup()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--spider",
        required=True,
        help="spiders",
        choices=SPIDERS.keys()
    )
    parser.add_argument(
        "-c",
        "--command",
        required=True,
        help="Commands",
        choices=[
            "LinkExtractor"
        ]
    )
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.info("Starting")

    spider = SPIDERS[args.spider]()
    command = getattr(commands, args.command)
    command(spider).execute()

if __name__ == '__main__':
    main()

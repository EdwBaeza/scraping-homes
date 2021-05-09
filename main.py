import argparse
import logging
import commands
from spiders.homes import LaMudi
from libs.browsers.chrome_builder import ChromeBuilder
from libs.logger import logger_setup

# TODO: Add flag for select browser
SPIDERS = {
    'la_mudi': lambda: LaMudi(ChromeBuilder())
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
            "LinkExtractor",
            "HomeExtractor"
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

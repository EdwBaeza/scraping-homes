import logging

def logger_setup():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

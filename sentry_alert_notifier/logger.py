import logging


def config_root_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]  %(message)s')
    lch = logging.StreamHandler()
    lch.setLevel(logging.INFO)
    lch.setFormatter(formatter)
    logger.addHandler(lch)

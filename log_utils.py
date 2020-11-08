import logging.config


def load_config():
    logging.config.fileConfig('config/logging.conf')


def get_logger(test_mode):
    return logging.getLogger('console_logger') if test_mode else logging.getLogger('file_logger')

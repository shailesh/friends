import logging

DEFAULT_FORMAT = '[%(levelname)s]: [%(asctime)s]  [%(name)s] [%(module)s:%(lineno)d] - %(message)s'
DEFAULT_DATE_FORMAT = '%d-%m-%y %H:%M:%S'
DEFAULT_LOG_FILE = 'invite_friends.log'
DEFAULT_FILE_LOGLEVEL = logging.INFO 
DEFAULT_STREAM_LOGLEVEL = logging.ERROR 
DEFAULT_LOGGER_LOGLEVEL = logging.INFO


def get_logger(module_name):
	
	logging.basicConfig(level=DEFAULT_FILE_LOGLEVEL, filename=DEFAULT_LOG_FILE, format=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT)

	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(DEFAULT_STREAM_LOGLEVEL)


	
	formatter = logging.Formatter(DEFAULT_FORMAT, DEFAULT_DATE_FORMAT)

	stream_handler.setFormatter(formatter)

	stream_logger = logging.getLogger(module_name)

	stream_logger.setLevel(DEFAULT_LOGGER_LOGLEVEL)

	stream_logger.addHandler(stream_handler) 

	return stream_logger



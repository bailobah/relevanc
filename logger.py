
import os
import logger
import logging.config

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))

def singleton(cls):
	instances = {}
	def get_instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return get_instance()

@singleton
class Logger():
	"""docstring for Logger"""
	def __init__(self):
		logging.config.fileConfig(logging_conf_path)
		self.log = logging.getLogger(__name__)

		

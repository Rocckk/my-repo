'''
this module is config creator for different job types
'''
from random import randint

class Configurator:
	file_type = ['uniqueness counter', 'file creator' 'directory creator', 'file deleter', 'dir deleter']

	@classmethod
	def get_config(cls, job_type):
		if job_type in cls.file_type:
			pass
		elif job_type == 'dump maker':
			pass
		else:
			conf = randint(1, 10)
			return conf

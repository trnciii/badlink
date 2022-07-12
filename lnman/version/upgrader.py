from .version import version_string

def ug_numbers(config):
	print('upgrading version numbers only.')
	config['header']['version'] = version_string
	return config

def ug_noheader(config):
	print('adding header.')
	return {
		'header': {'version': version_string},
		'sites': config
	}

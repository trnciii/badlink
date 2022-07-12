from . import core, helper
import json


version_string = '1.0.2'

def version():
	return '{} ({})'.format(core.path_lib, version_string)

def to_number(string):
	return [int(s) for s in string.split('.')]

def to_string(numbers):
	return '.'.join(numbers)

def valid(config):
	return ('version' in config.keys()) and (config['version'] == version_string)


def upgrade_config():
	config = core.load()
	if valid(config):
		print('up to date')
		return

	old_text = json.dumps(config, indent=2).splitlines(keepends=True)
	upgrade_config_core(config)
	new_text = json.dumps(config, indent=2).splitlines(keepends=True)
	helper.prettydiff(old_text, new_text)

	if 'n' != input('save? (Y/n)').lower():
		core.write(config)


def upgrade_config_core(config):
	if 'version' not in config.keys():
		if 'n' != input('version is missing. set {}? (Y/n)'.format(version_string)).lower():
			config['version'] = version_string

	elif config['version'] < version_string:
		if 'n' != input('''
			upgrade {} -> {}?. No data will change. (Y/n)
			'''.format(config['version'], version_string)).lower():
			config['version'] = version_string

	return config

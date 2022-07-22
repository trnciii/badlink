from .. import core, helper
import json


version_string = '1.0.3'

def url():
	return 'https://github.com/trnciii/lnman'

def version():
	return '{} ({})'.format(core.path_lib, version_string)

def to_numbers(string):
	return tuple([int(s) for s in string.split('.')])

def to_string(numbers):
	return '.'.join(numbers)

def default_config():
	return {
		'header': {'version': version_string},
		'sites': {}
	}

def validate(config):
	if 'header' not in config.keys():
		return False, 'noheader'

	v_config = to_numbers(config['header']['version'])
	v_current = to_numbers(version_string)

	if v_config < v_current:
		print('config version ({}) is behind app version ({})'.format(v_config, v_current))
		return False, config['header']['version']

	if v_config > v_current:
		print('config version ({}) is ahead app version ({}). upgrade app.'.format(v_config, v_current))
		return False, None

	return True, None


def upgrade_config():
	config = core.load()
	valid, how = validate(config)
	if valid:
		print('up to date')
		return

	old_text = json.dumps(config, indent=2).splitlines(keepends=True)
	config = upgrade_config_core(config, how)
	new_text = json.dumps(config, indent=2).splitlines(keepends=True)
	helper.prettydiff(old_text, new_text)

	if 'n' != input('save? (Y/n)').lower():
		core.write(config)


def upgrade_config_core(config, key):
	from . import upgrader

	if key == None:
		return config

	upgrade_from = {
		'noheader': upgrader.ug_noheader
	}

	ug = upgrade_from[key] if key in upgrade_from.keys() else upgrader.ug_numbers
	return ug(config)

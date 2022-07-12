import os, json
from . import helper

path_lib = os.path.dirname(os.path.abspath(__file__))
path_config = path_lib+"/config.json"


def load():
	config = json.load(open(path_config, 'r'))
	return config

def write(config):
	string = json.dumps(config, indent=2)
	open(path_config, "w").write(string)


def cat():
	return json.dumps(load(), indent=2)

def file():
	return path_config

def set(*args):
	keys = args[0].split('.')
	value = args[1]
	config = load()

	exec('{} = value'.format(helper.ref_keys(keys)))

	write(config)


def get(*args):
	keys = args[0].split('.')
	config = load()
	return eval('str({})'.format(helper.ref_keys(keys)))


def init(key, path):
	if os.path.exists(path_config):
		config = load()
	else:
		config = {}

	path = os.path.abspath(path)
	if os.path.exists(path):
		config[key] = {'path': path, 'packages': {}}
		write(config)
	else:
		print('path does not exist:', path)


def deinit(key):
	config = load()
	del config[key]
	write(config)


def list_packages():
	config = load()

	li = sum([
		[(scope, dic['path'])]
		+ [('{}/{}'.format(scope, name), path) for name, path in dic['packages'].items()]
		for scope, dic in config.items()
	], [])

	w = max([len(name) for name, _ in li])
	text = '\n'.join(['{}  {}'.format(name.ljust(w), path) for (name, path) in li])
	return text


def lsdir(key):
	'''
	returns a list of tuples of each content in the "key" directory and if it is managed
	'''
	path, packages = load()[key].values()
	keys = packages.keys()
	return [(i, (i in keys)) for i in os.listdir(path)]


def ls_pretty(key):
	return '  '.join([helper.term_color(i, 'cyan') if d else i for i, d in lsdir(key)])


def show(key):
	config = load()
	if '/' in key:
		scope, name = key.split('/')
		return '\n'.join([
			'scope: {}'.format(scope),
			'name:  {}'.format(name),
			'path:  {}'.format(config[scope]['packages'][name])
		])
	else:
		packages = config[key]['packages'].keys()
		return '\n'.join([
			'name:     {}'.format(key),
			'path:     {}'.format(config[key]['path']),
			'packages: [ {} ]'.format(', '.join(packages))
		])


def install(dst, src):

	if '/' in dst:
		scope, name = dst.split('/')
	else:
		scope, name = dst, os.path.basename(src)

	config = load()
	src_full = os.path.abspath(src)
	dst_full = os.path.abspath(os.path.join(config[scope]['path'], name))

	if not os.path.exists(src_full):
		print(src_full, 'does not exist')
		return

	if os.path.exists(dst_full):
		print(dst_full, 'already exists')
		return

	print('src', src_full)
	print('dst', dst_full)

	os.symlink(src_full, dst_full)

	config[scope]['packages'][name] = src_full
	write(config)


def add(key):
	config = load()
	scope, path = key.split('/')
	target_full = os.path.abspath(os.path.join(config[scope]['path'], path))

	if not os.path.exists(target_full):
		print(target_full, 'does not exist')
		return

	if not os.path.islink(target_full):
		print(target_full, 'is not a symlink')
		return

	src = os.path.realpath(target_full)
	if not os.path.exists(src):
		print(src, 'does not exist')
		return

	name = os.path.basename(target_full)
	config[scope]['packages'][name] = src

	print('src', src)
	print('dst', target_full)

	write(config)


def remove(key):
	scope, alias = key.split('/')

	config = load()
	os.remove(os.path.join(config[scope]['path'], alias))

	del config[scope]['packages'][alias]
	write(config)

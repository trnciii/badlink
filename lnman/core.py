import os, json
from . import helper, version

path_lib = os.path.dirname(os.path.abspath(__file__))
path_config = path_lib+"/config.json"


def load():
	config = json.load(open(path_config, 'r'))

	valid, _ = version.validate(config)
	if not valid:
		ms = 'config version does not agree. try "lnman upgrade_config"'
		print(helper.term_color(ms, 'red'))

	return config

def write(config):
	string = json.dumps(config, indent=2, sort_keys=True)
	open(path_config, "w").write(string)
	print('saved config')


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
		config = version.default_config()

	path = os.path.abspath(path)
	if os.path.exists(path):
		config['sites'][key] = {'path': path, 'packages': {}}
		write(config)
	else:
		print('path does not exist:', path)


def deinit(key):
	config = load()
	del config['sites'][key]
	write(config)


def list_packages():
	sites = load()['sites']

	li = sum([
		[(scope, dic['path'])]
		+ [('{}/{}'.format(scope, name), path) for name, path in dic['packages'].items()]
		for scope, dic in sites.items()
	], [])

	w = max([len(name) for name, _ in li])
	text = '\n'.join(['{}  {}'.format(name.ljust(w), path) for (name, path) in li])
	return text


def lsdir(key):
	'''
	returns a list of tuples of each content in the "key" directory and if it is managed
	'''
	site = load()['sites'][key]
	keys = site['packages'].keys()
	return [(i, (i in keys)) for i in os.listdir(site['path'])]


def ls_pretty(key):
	return '  '.join([helper.term_color(i, 'cyan') if d else i for i, d in lsdir(key)])


def show(key):
	sites = load()['sites']
	if '/' in key: # package
		site, name = key.split('/')
		return '\n'.join([
			'site: {}'.format(site),
			'name: {}'.format(name),
			'path: {}'.format(sites[site]['packages'][name])
		])
	else: # site
		packages = sites[key]['packages'].keys()
		return '\n'.join([
			'name:     {}'.format(key),
			'path:     {}'.format(sites[key]['path']),
			'packages: [ {} ]'.format(', '.join(packages))
		])


def install(dst, src):

	if '/' in dst:
		sitename, linkname = dst.split('/')
	else:
		sitename, linkname = dst, os.path.basename(src)

	config = load()
	site = config['sites'][sitename]

	src_full = os.path.abspath(src)
	dst_full = os.path.abspath(os.path.join(site['path'], linkname))

	if not os.path.exists(src_full):
		print(src_full, 'does not exist')
		return

	if os.path.exists(dst_full):
		print(dst_full, 'already exists')
		return

	print('src', src_full)
	print('dst', dst_full)

	os.symlink(src_full, dst_full)

	site['packages'][linkname] = src_full

	config['sites'][sitename] = site
	write(config)


def remove(key):
	site, alias = key.split('/')

	config = load()
	os.remove(os.path.join(config['sites'][site]['path'], alias))

	del config['sites'][site]['packages'][alias]
	write(config)


def register(key):
	config = load()
	site, path = key.split('/')
	target_full = os.path.abspath(os.path.join(config['sites'][site]['path'], path))

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
	config['sites'][site]['packages'][name] = src

	print('src', src)
	print('dst', target_full)

	write(config)


def unregister(key):
	site, alias = key.split('/')

	config = load()
	del config['sites'][site]['packages'][alias]

	write(config)

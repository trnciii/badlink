import os, json
from . import helper

path_config = os.path.join(os.path.expanduser('~'), 'lnman.json')
version_string = '1.1.0'

def load():
	return json.load(open(path_config, 'r'))

def write(config):
	with open(path_config, "w") as f:
		f.write(json.dumps(config, indent=2, sort_keys=True))
	print('saved config')


def init(key, path):
	if os.path.exists(path_config):
		config = load()
	else:
		config = {'sites': {}}

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


def list_contents(site=None, as_list=False):
	tree = load()['sites']

	if as_list:
		if site:
			print(' '.join(tree[site]['packages']))
		else:
			print(' '.join(tree.keys()))

	else:
		if site:
			tree = {site:tree[site]}

		li = sum((
			[(f'+ {site}', v['path'])]
			+ [(f'  - {pk}', path) for pk, path in v['packages'].items()]
			for site, v in tree.items()
		), [])

		w = max([len(name) for name, _ in li])
		print('\n'.join(f'{name.ljust(w)} {path}' for name, path in li))


def list_directory(key, as_list=True):
	'''
	print in cyan if the item is managed
	'''
	site = load()['sites'][key]
	keys = site['packages'].keys()
	if as_list:
		print(' '.join(os.listdir(site['path'])))
	else:
		print('\n'.join([
			helper.term_color(i, 'cyan') if i in keys else i
			for i in os.listdir(site['path'])
		]))


def show(key):
	sites = load()['sites']
	if '/' in key: # package
		site, name = key.split('/')
		print('\n'.join([
			'site: {}'.format(site),
			'name: {}'.format(name),
			'path: {}'.format(sites[site]['packages'][name])
		]))
	else: # site
		packages = sites[key]['packages'].keys()
		print('\n'.join([
			'name:     {}'.format(key),
			'path:     {}'.format(sites[key]['path']),
			'packages: [ {} ]'.format(', '.join(packages))
		]))

def create(dst, src):
	if not os.path.exists(src):
		print(src, 'does not exist')
		return

	if os.path.exists(dst):
		print(dst, 'already exists')
		return

	print('src', src)
	print('dst', dst)

	os.symlink(src, dst)


def install(dst, src):
	if '/' in dst:
		sitename, linkname = dst.split('/')
	else:
		sitename, linkname = dst, os.path.basename(src)

	config = load()
	site = config['sites'][sitename]

	src_full = os.path.abspath(src)
	dst_full = os.path.abspath(os.path.join(site['path'], linkname))

	create(dst_full, src_full)

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

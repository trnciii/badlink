from .version import version_string

def ug_numbers(config):
	print('upgrading version numbers only.')
	config['header']['version'] = version_string
	return config

def ug_noheader(config):
	print('adding header.')

	sites = [{
		'name': k,
		'path': v['path']
	} for k, v in config.items()]

	packages = []
	for sitename, sitevalue in config.items():
		for k, v in sitevalue['packages'].items():
			packages.append({
				'name': k,
				'site': sitename,
				'path': v
			})

	return {
		'header': {'version': version_string},
		'sites': sites,
		'packages': packages
	}

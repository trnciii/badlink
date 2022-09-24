import sys
from . import core


def main():
	ftable = {
		'file': lambda:print(core.path_config),

		'init': core.init,
		'deinit': core.deinit,

		'list': core.list_packages,
		'sites': core.list_sites,
		'show': core.show,
		'lsdir': core.list_directory,

		'install': core.install,
		'remove': core.remove,
		'register': core.register,
		'unregister': core.unregister,

		'--version': lambda:print(core.version_string),
		'url': lambda:print('https://github.com/trnciii/lnman')
	}


	argv = sys.argv

	if len(argv)>1 and argv[1] in ftable.keys():
		f, *args = argv[1:]
		ftable[f](*args)
	else:
		print('nothing to do')

if __name__ == '__main__':
	main()
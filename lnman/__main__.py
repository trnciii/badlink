import sys
from . import core, version


def main():
	ftable = {
		'get': core.get,
		'set': core.set,

		'cat': core.cat,
		'file': core.file,

		'init': core.init,
		'deinit': core.deinit,

		'list': core.list_packages,
		'show': core.show,
		'lsdir': core.ls_pretty,

		'install': core.install,
		'add': core.add,
		'remove': core.remove,

		'version': version.version,
		'upgrade_config': version.upgrade_config
	}


	argv = sys.argv

	if len(argv)>1 and argv[1] in ftable.keys():
		f, *args = argv[1:]
		ret = ftable[f](*args)
		if ret: print(ret)
	else:
		print('nothing to do')

if __name__ == '__main__':
	main()
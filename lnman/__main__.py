from . import core
import argparse

def main():
	parser = argparse.ArgumentParser()
	sub = parser.add_subparsers()

	sub.add_parser('file').set_defaults(handler=lambda _:print(core.path_config))

	p = sub.add_parser('init')
	p.add_argument('key')
	p.add_argument('path')
	p.set_defaults(handler=lambda args:core.init(args.key, args.path))

	p = sub.add_parser('deinit')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.deinit(args.key))

	sub.add_parser('list').set_defaults(handler=lambda _:core.list_packages())

	sub.add_parser('sites').set_defaults(handler=lambda _:core.list_sites())

	p = sub.add_parser('show')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.show(args.key))

	p = sub.add_parser('lsdir')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.list_directory(args.key))

	p = sub.add_parser('install')
	p.add_argument('dst')
	p.add_argument('src')
	p.set_defaults(handler=lambda args:core.install(args.dst, args.src))

	p = sub.add_parser('remove')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.remove(args.key))

	p = sub.add_parser('register')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.register(args.key))

	p = sub.add_parser('unregister')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.unregister(args.key))

	sub.add_parser('version').set_defaults(handler=lambda _:print(core.version_string))

	sub.add_parser('url').set_defaults(handler=lambda _:print('https://github.com/trnciii/lnman'))


	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)

if __name__ == '__main__':
	main()
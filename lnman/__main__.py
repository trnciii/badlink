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

	p = sub.add_parser('list')
	p.add_argument('site', nargs='?', type=str, const=None)
	p.add_argument('--as-list', action='store_true')
	p.set_defaults(handler=lambda args:core.list_contents(site=args.site, as_list=args.as_list))

	p = sub.add_parser('show')
	p.add_argument('key')
	p.set_defaults(handler=lambda args:core.show(args.key.rstrip('/')))

	p = sub.add_parser('lsdir')
	p.add_argument('key')
	p.add_argument('--as-list', action='store_true')
	p.set_defaults(handler=lambda args:core.list_directory(args.key, as_list=args.as_list))


	p = sub.add_parser('create')
	p.add_argument('dst')
	p.add_argument('src')
	p.set_defaults(handler=lambda args: core.create(args.dst, args.src))


	p = sub.add_parser('install')
	p.add_argument('dst')
	p.add_argument('src')
	p.set_defaults(handler=lambda args:core.install(args.dst.rstrip('/'), args.src))

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


	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)

if __name__ == '__main__':
	main()
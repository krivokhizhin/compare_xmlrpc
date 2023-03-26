from xmlrpc.server import SimpleXMLRPCServer
from .load import load


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost', type=str,
                        help='Specify server address [default: localhost]')
    parser.add_argument('--port', default=6677, type=int,
                        help='Specify alternate port [default: 6677]')
    parser.add_argument('--processes', type=int, default=1,
                       help='Number of worker processes to process the requests')
    parser.add_argument('--fork', action='store_true',
                       help='Fork a new subprocess to process the request')
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    if args.fork and args.processes > 1:
        from socketserver import ForkingMixIn

        class ForkingXMLRPCServer(ForkingMixIn, SimpleXMLRPCServer):
            max_children = args.processes

        server = ForkingXMLRPCServer((args.host, args.port))
    elif args.processes > 1:
        from .pool_server import PoolXMLRPCServer

        server = PoolXMLRPCServer((args.host, args.port), args.processes)
    else:
        server = SimpleXMLRPCServer((args.host, args.port))

    server.register_introspection_functions()
    server.register_function(load)
    server.serve_forever()
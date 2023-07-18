from xmlrpc.server import SimpleXMLRPCServer

from const import *
from load import load


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=HOST, type=str,
                        help=f'Specify server address [default: {HOST}]')
    parser.add_argument('--port', default=PORT, type=int,
                        help=f'Specify alternate port [default: {PORT}]')
    parser.add_argument('--processes', type=int, default=SYNC_MAX_WORKERS,
                        help=f'Number of worker processes to process the requests [default: {SYNC_MAX_WORKERS}]')
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
        from pool_server import PoolXMLRPCServer

        server = PoolXMLRPCServer((args.host, args.port), args.processes)
    else:
        server = SimpleXMLRPCServer((args.host, args.port))

    server.register_introspection_functions()
    server.register_function(load)
    server.serve_forever()
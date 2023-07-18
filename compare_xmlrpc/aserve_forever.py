import asyncio

from const import *
from load import load


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=HOST, type=str,
                        help=f'Specify server address [default: {HOST}]')
    parser.add_argument('--port', default=PORT, type=int,
                        help=f'Specify alternate port [default: {PORT}]')
    parser.add_argument('--max_workers', type=int, default=ASYNC_MAX_WORKERS,
                       help=f'Number of worker processes in pool to process the request [default: {ASYNC_MAX_WORKERS}]')
    return parser.parse_args()


async def main():
    args = parse_args()

    if args.max_workers:
        from aioserver.aioserver.xmlrpc.pool_server import AsyncPoolXMLRPCServer
        server = AsyncPoolXMLRPCServer((args.host, args.port), args.max_workers)
    else:
        from aioserver.aioserver.xmlrpc.server import AsyncXMLRPCServer
        server = AsyncXMLRPCServer((args.host, args.port))
    server.register_introspection_functions()
    server.register_function(load)

    await server.serve_forever()


asyncio.run(main())
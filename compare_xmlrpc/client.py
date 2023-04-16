import time
import concurrent.futures

from operator import methodcaller
from typing import Any, List
from xmlrpc.client import ServerProxy


class RpcClient:

    @staticmethod
    def remote_call(host:str, port:int, method_name: str, *args, **kwargs) -> Any:
        result = None
        procedure = methodcaller(method_name, *args)
        with ServerProxy(f'http://{host}:{port}') as proxy:
            result = procedure(proxy)
        if not kwargs.get('timeit', False):
            print('.', end='', flush=True)

        return result

    @staticmethod
    def start(host, port, timeout, number, max_workers, method_name, *args):
        duration = '-'
        exceptions = []
        max_workers = min(max_workers, number)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            start = time.time()
            load_futures = [executor.submit(RpcClient.remote_call, host, port, method_name, *args) for _ in range(number)]
            for future in concurrent.futures.as_completed(load_futures, timeout):
                ex = future.exception()
                if ex:
                    exceptions.append(ex)
            
            duration = time.time() - start

        return duration, exceptions

    @staticmethod
    def start_for_timeit(host, port, timeout, number, max_workers, method_name, *args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            load_futures = [executor.submit(RpcClient.remote_call, host, port, method_name, *args, timeit=True) for _ in range(number)]
            concurrent.futures.wait(load_futures, timeout)
    
    
def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=str, help='Calling method')
    parser.add_argument('args', nargs='*', help='Arguments, recognizes the types: int, float, bool and str (default)')
    parser.add_argument('--host', default='localhost', type=str,
                        help='Specify server address [default: localhost]')
    parser.add_argument('--port', default=6677, type=int,
                        help='Specify alternate port [default: 6677]')
    parser.add_argument('--timeout', default=180, type=int,
                        help='Specify the timeout for request [default: 180]')
    parser.add_argument('--number', default=100, type=int,
                        help='Specify the number of requests [default: 100]')
    parser.add_argument('--max_workers', default=20, type=int,
                        help='Specify maximum number of threads that can be used to execute [default: 20]')
    
    return parser.parse_args()


def show(duration, number, errors):
    print(f'\nrequest count: {number}\nduration, s: {duration}')
    if errors:
        print(f'\nfailed requests: {len(errors)}')
        for ex in errors:
            print(f'\n{ex}\n*********')


def classify_args(*args: List[Any]) -> list:
    result = []

    for arg in args:
        try:
            arg = int(arg)
        except TypeError:
            try:
                arg = float(arg)
            except TypeError:
                try:
                    arg_true = arg.lower() == 'true'
                    if not arg_true:
                        arg_false = arg.lower() == 'false'
                        if arg_false:
                            arg = False
                    else:
                        arg = True
                except TypeError:
                    pass
        
        result.append(arg)


    return result


if __name__ == '__main__':
    args = parse_args()
    method_args = classify_args(*args.args)
    duration, errors = RpcClient.start(args.host, args.port, args.timeout, args.number, args.max_workers, args.method, *method_args)
    show(duration, args.number, errors)
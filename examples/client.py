import time
import concurrent.futures
from xmlrpc.client import ServerProxy


class RpcClient:

    @staticmethod
    def load(load_value: int, host:str, port:int, timeit: bool = False) -> float:
        with ServerProxy(f'http://{host}:{port}') as proxy:
            proxy.load(load_value)
        if not timeit:
            print('.', end='', flush=True)

    @staticmethod
    def start(load_value, host, port, timeout, number, max_workers):
        duration = '-'
        exceptions = []
        max_workers = min(max_workers, number)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            start = time.time()
            load_futures = [executor.submit(RpcClient.load, load_value, host, port) for _ in range(number)]
            for future in concurrent.futures.as_completed(load_futures, timeout):
                ex = future.exception()
                if ex:
                    exceptions.append(ex)
            
            duration = time.time() - start

        return duration, exceptions

    @staticmethod
    def start_for_timeit(load_value, host, port, timeout, number, max_workers):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            load_futures = [executor.submit(RpcClient.load, load_value, host, port, True) for _ in range(number)]
            concurrent.futures.wait(load_futures, timeout)
    
    
def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('load_value', type=int, help='load value')
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


if __name__ == '__main__':
    args = parse_args()
    duration, errors = RpcClient.start(args.load_value, args.host, args.port, args.timeout, args.number, args.max_workers)
    show(duration, args.number, errors)
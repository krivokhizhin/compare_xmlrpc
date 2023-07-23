# Comparison of several options XML-RPC server based on xmlrpc.server module.

---

XML-RPC server options:

* Standard;
* Asynchronous;
* Process forks;
* Process pool;
* Asynchronous with the process pool.

---

## Requirements
Python 3.7+

Only standard Python libraries

## Installation
<div class="termy">

```console
$ git clone --recurse-submodules https://github.com/krivokhizhin/compare_xmlrpc.git

---> 100%
$ cd compare_xmlrpc

$ docker build -t comparexmlrpc .

---> 100%
```

</div>

## Usage
- Standard:
<div class="termy">

```console
$ docker run -d --network="host" --name rpc-server-simple comparexmlrpc python3 serve_forever.py

$ docker run -it --network="host" --rm comparexmlrpc python3 -m timeit -s 'from client import start_for_timeit' 'start_for_timeit("load", 150000, max_workers=5)'

$ docker stop rpc-server-simple
```

</div>

- Asynchronous:
<div class="termy">

```console
$ docker run -d --network="host" --name rpc-server-async comparexmlrpc python3 aserve_forever.py

$ docker run -it --network="host" --name rpc-client comparexmlrpc python3 -m timeit -s 'from client import start_for_timeit'  'start_for_timeit("load", 150000)'

$ docker stop rpc-server-async
```

</div>

- Process forks:
<div class="termy">

```console
$ docker run -d --network="host" --name rpc-server-fork10 comparexmlrpc python3 serve_forever.py --processes 10 --fork

$ docker start -a rpc-client

$ docker stop rpc-server-fork10
```

</div>

- Process pool:
<div class="termy">

```console
$ docker run -d --network="host" --name rpc-server-pool10 comparexmlrpc python3 serve_forever.py --processes 10

$ docker start -a rpc-client

$ docker stop rpc-server-pool10
```

</div>

- Asynchronous with the process pool:
<div class="termy">

```console
$ docker run -d --network="host" --name rpc-server-async10 comparexmlrpc python3 aserve_forever.py --max_workers 10

$ docker start -a rpc-client

$ docker stop rpc-server-async10
```

</div>
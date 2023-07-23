# Comparison of several options XML-RPC server based on xmlrpc.server module.

---

XML-RPC server options::

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
$ git clone --recurse-submodules https://github.com/krivokhizhin/comparexmlrpc.git

---> 100%
$ cd comparexmlrpc

$ docker build .

---> 100%
```

</div>

## Usage
- Standard:
<div class="termy">

```console
$ docker run -it --network="host" --name rpc-server-simple comparexmlrpc python3 serve_forever.py
```

```console
$ docker run -it --network="host" --rm comparexmlrpc python3 -m timeit -s 'from client import start_for_timeit' 'start_for_timeit("load", 150000, max_workers=5)'
```

</div>

- Asynchronous:
<div class="termy">

```console
$ docker run -it --network="host" --name rpc-server-async comparexmlrpc python3 aserve_forever.py
```

```console
$ docker run -it --network="host" --name rpc-client comparexmlrpc python3 -m timeit -s 'from client import start_for_timeit'  'start_for_timeit("load", 150000)'
```

</div>

- Process forks:
<div class="termy">

```console
$ docker run -it --network="host" --name rpc-server-fork10 comparexmlrpc python3 serve_forever.py --processes 10 --fork
```

```console
$ docker start rpc-client
```

</div>

- Process pool:
<div class="termy">

```console
$ docker run -it --network="host" --name rpc-server-pool10 comparexmlrpc python3 serve_forever.py --processes 10
```

```console
$ docker start rpc-client
```

</div>

- Asynchronous with the process pool:
<div class="termy">

```console
$ docker run -it --network="host" --name rpc-server-async10 comparexmlrpc python3 aserve_forever.py --max_workers 10
```

```console
$ docker start rpc-client
```

</div>
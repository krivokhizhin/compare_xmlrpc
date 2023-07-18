# Asynchronous XML-RPC in Python

---

The key features are:

* Asynchronous XML-RPC server based on xmlrpc.server module;
* 

---

## Requirements
Python 3.7+

Only standard Python libraries

## Installation
<div class="termy">

```console
$ git clone https://github.com/krivokhizhin/asyncxmlrpc.git

---> 100%
```

</div>

cd

docker run -it --network="host" --name rpc-server-simple comparexmlrpc python3 serve_forever.py
docker run -it --network="host" --name rpc-server-fork10 comparexmlrpc python3 serve_forever.py --processes 10 --fork
docker run -it --network="host" --name rpc-server-pool10 comparexmlrpc python3 serve_forever.py --processes 10

docker run -it --network="host" --name rpc-server-async comparexmlrpc python3 aserve_forever.py
docker run -it --network="host" --name rpc-server-async10 comparexmlrpc python3 aserve_forever.py --max_workers 10

docker run -it --network="host" --name rpc-client comparexmlrpc python3 -m timeit -n 3 -s 'from client import RpcClient'  'RpcClient.start_for_timeit("localhost", 6677, 120, 1000, 20, "load", 83000)'

ps f

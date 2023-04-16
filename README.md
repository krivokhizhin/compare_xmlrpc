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

python3 -m compare_xmlrpc.serve_forever
python3 -m compare_xmlrpc.aserve_forever

python3 -m compare_xmlrpc.client load 250000
python3 -m timeit 'from compare_xmlrpc.client import RpcClient;  RpcClient.start_for_timeit("localhost", 6677, 60, 100, 20, "load", 250000)'

ps f

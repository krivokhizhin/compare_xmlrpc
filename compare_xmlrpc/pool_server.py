import socket
from multiprocessing import Pool
from socketserver import TCPServer
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCDispatcher


def initializer(dispatcher, requestHandlerClass):    
    global server_dispatcher
    server_dispatcher = dispatcher  
    global RequestHandlerClass
    RequestHandlerClass = requestHandlerClass


def pool_process_request(request, client_address):
    global server_dispatcher
    global RequestHandlerClass
    try:
        RequestHandlerClass(request, client_address, server_dispatcher)

    except Exception:
        import sys
        print('-'*40, file=sys.stderr)
        print('Exception occurred in during processing of request from',
            client_address, file=sys.stderr)
        import traceback
        traceback.print_exc()
        print('-'*40, file=sys.stderr)
    finally:        
        try:
            #explicitly shutdown.  socket.close() merely releases
            #the socket and waits for GC to perform the actual close.
            request.shutdown(socket.SHUT_WR)
        except OSError:
            pass #some platforms may raise ENOTCONN here
        request.close()
        

class PoolXMLRPCServer(TCPServer):

    def __init__(self, addr, process_number: int, XMLRPCDispatcher=SimpleXMLRPCDispatcher, 
                 requestHandlerClass=SimpleXMLRPCRequestHandler, logRequests=True, 
                 allow_none=False, encoding=None, bind_and_activate=True, use_builtin_types=False):
        super().__init__(addr, requestHandlerClass, bind_and_activate)
        
        self.requestHandler = requestHandlerClass
        self.dispatcher = XMLRPCDispatcher(allow_none, encoding, use_builtin_types)
        self.dispatcher.logRequests = logRequests

        self.process_number = process_number

    def register_instance(self, instance, allow_dotted_names=False) -> None:
        self.dispatcher.register_instance(instance, allow_dotted_names)

    def register_function(self, function=None, name=None):
        return self.dispatcher.register_function(function, name)

    def register_introspection_functions(self) -> None:
        self.dispatcher.register_introspection_functions()

    def register_multicall_functions(self) -> None:
        self.dispatcher.register_multicall_functions()

    def serve_forever(self, poll_interval=0.5) -> None:
        self.pool = Pool(
            self.process_number, 
            initializer=initializer, 
            initargs=(self.dispatcher,self.requestHandler)
        )
        super().serve_forever(poll_interval)

    def process_request(self, request, client_address) -> None:
        self.pool.apply_async(pool_process_request, args=(request, client_address))

    def server_close(self) -> None:
        super().server_close()
        if hasattr(self, 'pool'):
            self.pool.close()

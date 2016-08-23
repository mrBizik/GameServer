import json

import tornado.websocket

from lib.SequenceGenerator import Sequence


""" Декоратор для удаления приватных методов из списка """
def filter_private_method(method):
    def wrapper(self, *args, **kwargs):
        result = []
        all_methods = method(self, *args, **kwargs)
        for i in all_methods:
            if i[0] != "_":
                result.append(i)
        return result
    return wrapper

class RPCWSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.rpc_methods = self._init_rpc_methods()
        self.id = Sequence()
        super(RPCWSocket, self).__init__(application, request, **kwargs)

    """
      Метод предназначен для определения списка процедур,
      которые можно вызвать в конкретном хэндлере.
      Методы содержащие в имени _(землю) считаются приватными и отбрасываются
    """
    @filter_private_method
    def _init_rpc_methods(self):
        return list(self.__class__.__dict__)

    def _parse_message(self, message):
        parsed =  json.loads(message)
        return parsed["method"], parsed["params"], parsed["id"]

    def open(self):
        self.write_mesage([])

    def on_message(self, message):
        method, params, id = self._parse_mesage(message)
        try:
           method_i = self.rpc_methods.index(method)
           self.method(params)
        except ValueError:
            self.write_mesage(None, {"code": -32601, "message": "Method not found"})


    def on_close(self, message=None):
        self.write_mesage("Server closed socket")

    def write_mesage(self, result, error=None):
        message = {
            "error": {
                "code": error["code"],
                "message": error["message"]
            }
        }
        if not error:
            message = {
                "result": result,
                "id": self.id.next()
            }
        message_json = json.dumps(message)
        super(RPCWSocket, self).write_mesage(self, message_json)

    def check_origin(self, origin):
        return True

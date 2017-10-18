import json
import logging

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler

import uuid

JSON_PARSE_ERR = {
    "code": -1,
    "message": "JSON parse error"
}

METHOD_NOT_FOUND = {
    "code": -32601,
    "message": "Method not found"
}


# TODO: make batch
# TODO: make async answer


class Rpc:
    @staticmethod
    def rpc_method_prefix():
        return 'rpc_'
    """
        Метод предназначен для определения списка процедур,
        которые можно вызвать в конкретном хэндлере.
        Методы содержащие в имени _(землю) считаются приватными и отбрасываются
    """
    @staticmethod
    def init_rpc_methods(context):
        result = []
        all_methods = list(context.__class__.__dict__)
        for i in all_methods:
            if i.startswith(Rpc.rpc_method_prefix()):
                result.append(i)
        return result

    """
        Разобрать json полученный от клиента
    """
    @staticmethod
    def parse_message(message):
        parsed = json.loads(message)
        return parsed["method"], parsed["params"], parsed["id"]

    """
        Распарсить параметры в соответствии с ключами в param_keys
    """
    @staticmethod
    def parse_params(param_keys, raw_params):
        result = {}
        i = 0
        # TODO: проверка длинны raw_param, установка дефолтных значений
        for key in param_keys:
            result[key] = raw_params[i]
            i += 1

        return result

    @staticmethod
    def make_message(result=None):
        error = None
        message = None
        try:
            if result:
                message = json.dumps({
                    "jsonrpc": "2.0",
                    "id": str(uuid.uuid1()),
                    "result": result
                })
            else:
                message = json.dumps({
                    "jsonrpc": "2.0",
                    "id": str(uuid.uuid1())
                })
        except Exception:
            error = Rpc.make_error(JSON_PARSE_ERR)
        finally:
            return message, error

    @staticmethod
    def make_error(error):
        message = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid1()),
            "error": {
                "code": error["code"],
                "message": error["message"]
            }
        }

        return json.dumps(message)

    @staticmethod
    def call_method(context, method, params):
        error = None
        message = None
        method = Rpc.rpc_method_prefix() + method
        try:
            context.rpc_methods.index(method)
            result = context.__class__.__dict__[method](context, params)
            message, error = Rpc.make_message(result)
        # Метод не найден
        except ValueError:
            # TODO add to log message
            error = Rpc.make_error(METHOD_NOT_FOUND)
        finally:
            log_level = logging.getLogger('tornado.Handlers')
            if error:
                log_level.debug('class {}\nmethod {}({}) \nerror {}'.format(context.__class__, method, params, error))
            else:
                log_level.debug('class {}\nmethod {}({}) \nresult {}'.format(context.__class__, method, params, message))
            return message, error


class RpcWebSocket(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.rpc_methods = Rpc.init_rpc_methods(self)
        super(RpcWebSocket, self).__init__(application, request, **kwargs)

    def open(self, *args, **kwargs):
        self.send_message()

    def on_message(self, message):
        method, params, id = Rpc.parse_message(message)
        message, error = Rpc.call_method(self, method, params)
        # TODO: тут же дуплекс соединение, не надо так(пока нормально обрабатывать не научим)
        # self.send_message(message, error)

    def send_message(self, result=None, error=None):
        if not error:
            message, error = Rpc.make_message(result)
        else:
            message = error
        self.write_message(message)


class RpcHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self.rpc_methods = Rpc.init_rpc_methods(self)
        self.template = 'templates/answer.html'
        super(RpcHandler, self).__init__(application, request, **kwargs)

    def post(self, *args, **kwargs):
        self.add_header('content_type', 'application/json-rpc')
        method = self.get_argument('method')
        params = json.loads(self.get_argument('params'))
        result, error = Rpc.call_method(self, method, params)
        if error:
            result = error
        self.render(self.template, result=result)

    def get(self, *args, **kwargs):
        self.add_header('content_type', 'application/json-rpc')
        method, params, id = Rpc.parse_message(self.get_argument('r'))
        result, error = Rpc.call_method(self, method, params)
        if error:
            result = error
        self.render(self.template, result=result)

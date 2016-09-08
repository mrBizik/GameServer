import json

import tornado.websocket

from lib.SequenceGenerator import Sequence


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
    def _init_rpc_methods(self):
        result = []
        all_methods = list(self.__class__.__dict__)
        for i in all_methods:
            if i[0] != "_":
                result.append(i)
        return result

    """
      Разобрать json полученный от клиента
    """
    def _parse_message(self, message):
        parsed =  json.loads(message)
        return parsed["method"], parsed["params"], parsed["id"]

    """
      Распарсить параметры в соответствии с ключами в param_keys
    """
    def _parse_params(self, param_keys, raw_params):
        result = {}
        i = 0
        # TODO: проверка длинны raw_param, установка дефолтных значений
        for key in param_keys:
            result[key] = raw_params[i]
            i += 1

        return result

    def open(self, *args, **kwargs):
        print("self._open_message()")

    """
      Обертка для получения сообщения
    """
    def on_message(self, message):
        # Парсим сообщение от клиента и  вытаскиваем метод, который клиент хочет дернуть
        method, params, id = self._parse_message(message)
        try:
           method_i = self.rpc_methods.index(method)
           print("Call method: " + method + " data = " + str(self.__class__.__dict__[method]))
           # yield self.__class__.__dict__[method](self, params)
           self.__class__.__dict__[method](self, params)
        # Метод не найден
        except ValueError:
            print("ValueError")
            self.write_message(None, {"code": -32601, "message": "Method not found"})


    def on_close(self):
        print("Server closed socket")

    """
      Обертка стандартного write_message
      Формирует json строку с ответом
    """
    def write_message(self, result, error=None):
        if not error:
            message = {
                "result": result,
                "id": self.id.next()
            }
        else:
            message = {
                "error": {
                    "code": error["code"],
                    "message": error["message"]
                }
            }
        message_json = json.dumps(message)
        print("write_message: "+ message_json)
        super(RPCWSocket, self).write_message(message_json)

    def check_origin(self, origin):
        # TODO: Запилить нормальную проверку хоста
        return True

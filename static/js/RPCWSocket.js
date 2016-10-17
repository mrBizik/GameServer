function RPCWSocket(url) {
    this.url = url;
    this.socket = null;
    this.id_pool = [];
}

RPCWSocket.prototype.init = function(onOpen) {
    this.socket = new WebSocket(this.url);
    this.socket.onopen = onOpen;
    this.socket.onclose = this._onclose;
    this.socket.onmessage = this._onmessage;
};

// RPCWSocket.prototype._onopen = function() {
//     console.log('Соединение установлено');
// };

RPCWSocket.prototype._onclose = function(event) {
    if (event.wasClean) {
        console.log('Соединение закрыто чисто');
    } else {
        console.error('Обрыв соединения');
    }
};

RPCWSocket.prototype._onmessage = function(event) {
    var parsed_data = JSON.parse(event.data);
    console.log(parsed_data);
    // this.id_pool.push(parsed_data.id);
    // callback(parsed_data.result);
};

RPCWSocket.prototype.call_method = function(method, params) {
    var request = {
        'method': method,
        'params': params,
        'id':  1// this.id_pool[this.id_pool.lenght-1]
    };
    var message = JSON.stringify(request);

    console.log(message);
    this.socket.send(message);
};
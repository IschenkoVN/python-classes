import socket
import json


HOST = 'localhost'
PORT = 8888


class Server(object):
    """RPC Server.
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(1)
        self.funcs = {}

    def register(self, func):
        self.funcs[func.func_name] = func

    def serve_forever(self):
        while True:
            conn, addr = self.socket.accept()
            print 'Connected by', addr
            data = conn.recv(1024)
            if not data:
                break
            data = json.loads(data)
            if data['func'] in self.funcs:
                func_name = data['func']
                args = data['args']
                kwargs = data['kwargs']
                try:
                    res = self.funcs[func_name](*args, **kwargs)
                except TypeError:
                    conn.send(u'TypeError')
                conn.sendall(json.dumps(res))
            else:
                conn.send(u'Error')
        self.socket.close()


class Client(object):
    """RPC Client.
    """
    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            data = {
                'func': name,
                'args': args,
                'kwargs': kwargs,
            }
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((HOST, PORT))
            self.socket.sendall(json.dumps(data))
            res = json.loads(self.socket.recv(PORT))
            self.socket.close()
            return res
        return wrapper


if __name__ == '__main__':
    s = Server()

    def test(x, y):
        return x + y

    s.register(test)
    s.serve_forever()

    c = Client()
    assert 3 == c.test(1, 2)

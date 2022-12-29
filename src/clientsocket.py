from socket import socket
from socket import AF_INET, SOCK_STREAM
from json import dumps, loads
from threading import Thread


ConnctionError = False


class EndOfFile(Exception):
    pass


class ConnectionRecovery(Exception):
    pass


class ClientSocketHandler(socket):
    __slots__ = (
        "recv_size", "callback", "connection_",
        "hp", "call_after_recovery"
    )

    def __init__(self, host, port, recv_size=1024):

        self.hp = (host, port)
        self.recv_size = recv_size
        self.connection_ = False

        socket.__init__(self, AF_INET, SOCK_STREAM)
        self.connection()

    def recv_handler(self, json_loads=True, decoding=True) -> str:
        received_client = ''
        received_client_b = ''.encode()
        try:
            try:
                while True:
                    if decoding:
                        content = self.recv(self.recv_size).decode()
                        received_client += content
                    else:
                        received_client_b += self.recv(self.recv_size)
                        raise EndOfFile

                    if content and content[-1] == "\0":
                        raise EndOfFile
            except (
                    ConnectionAbortedError,
                    ConnectionResetError, OSError
            ):
                self.connection_ = False
                raise ConnectionRecovery

        except EndOfFile:
            if json_loads:
                response = loads(received_client[:-1])
                if response == "False" or response == "True":
                    response = bool(response)

                return response
            else:
                if decoding:
                    return received_client[:-1]
                else:
                    return received_client_b

    def send_handler(self, content: str,
                     json_dumps=True, encoding=True) -> None:
        try:
            if json_dumps:
                request = dumps(content) + "\0"
                if encoding: self.send(request.encode())
                else: self.send((request))
            else:
                if encoding: self.send((content + "\0").encode())
                else: self.send(content + "\0".encode())

            return True
        except (
                ConnectionAbortedError,
                ConnectionResetError, OSError
        ):
            self.connection_ = False
            raise ConnectionRecovery()

    def connection(self, call_after_recovery=True):
        self.connection_ = False

        while True:
            try:
                self.connect(self.hp); break
            except (ConnectionRefusedError, OSError): pass

        self.connection_ = True
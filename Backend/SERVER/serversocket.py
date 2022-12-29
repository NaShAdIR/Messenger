from socket import socket
from socket import AF_INET, SOCK_STREAM
from json import dumps, loads


class EndOfFile(Exception):
    pass


class ServerSocketHandler(socket):
    __slots__ = (
        "listen_count", "recv_size",
        "client_sockets", "callback"
    )

    def __init__(self, host, port, callback=None,
                 listen_count=0, recv_size=1024):

        socket.__init__(self, AF_INET, SOCK_STREAM)
        hp = (host, port)

        self.callback = callback
        self.recv_size = recv_size
        self.bind(hp)
        self.listen(listen_count)

    def __getattr__(self, attribute):
        if attribute == "getclientsocket":
            client_socket, adders = self.accept()
            return client_socket

    def recv_handler(self, client_socket, json_loads=True, decoding=True):
        received_client = ''
        received_client_b = ''.encode()
        content = ''
        try:
            try:
                while True:
                    if decoding:
                        content = client_socket.recv(self.recv_size).decode()
                        received_client += content
                    else:
                        received_client_b += client_socket.recv(self.recv_size)
                        raise EndOfFile

                    if content and content[-1] == "\0":
                        raise EndOfFile

            except (
                    ConnectionAbortedError,
                    ConnectionResetError, OSError
            ):
                if self.callback:
                    self.callback()

        except EndOfFile:
            if json_loads:
                return self.recv_json(received_client[:-1])
            else:
                if decoding:
                    return received_client[:-1]
                else:
                    return received_client_b

    def send_handler(self, client_socket, content,
                     json_dumps=True, encoding=True):

        # if json_dumps:
        #     request = dumps(content) + "\0"
        #     if encoding: client_socket.send(request.encode())
        #     else: client_socket.send(request)
        # else:
        #     request = content + "\0"
        #     if encoding: client_socket.send(request.encode())
        #     else: client_socket.send(request)

        if json_dumps:
            request = dumps(content) + "\0"
            if encoding: client_socket.send(request.encode())
            else: client_socket.send((request))
        else:
            if encoding: client_socket.send((content + "\0").encode())
            else: client_socket.send(content + "\0".encode())

    def recv_json(self, content):
        return loads(content)


if __name__ == "__main__":
    def call():
        print("Error connecion!")
        input()

    my_socket = ServerSocketHandler("localhost", 5000, callback=call)
    client_socket = my_socket.getclientsocket
    user_widget = f'User_widget:Bob:' \
                  f'Best Messenger:../assets/Images/19.jpg\n'
    while True:
        data = {
            "Username": "Сейран",
            "Surname": "Барсегян",
            "Friends": user_widget
        }
        response = my_socket.recv_handler(client_socket, json_loads=True)
        print(response)
        my_socket.send_handler(client_socket, data, json_dumps=True)

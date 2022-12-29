from serversocket import ServerSocketHandler
from threading import Thread
from mytypes import *
import sqlite3
import json, os


online_users = {}
online_mes_clients = {}
missed_messages = {}


def check_users(search_username, username, cursor):

    if (search_username,) in cursor.execute(
            "SELECT Username FROM Users").fetchall():

        user_widget = f'User_widget:{search_username}:' \
                      f'Best Messenger\n'

        with open(f'profiles/{username}_profile.se', 'r') as profile_read:
            if user_widget not in profile_read.readlines():
                return "STATUS OK", True
            else: return "STATUS OK", "user_is"
    else:
        return "STATUS OK", False


def append_user(request, username):
    appended_user = request["appended_user"]
    user_widget = {
        "UserWidget": {
            "Username": appended_user,
            "Message_text": "Best Messeger!",
        }
    }

    with open(f'profiles/{username}_profile.se', 'a') as profile_write:
        profile_write.write(
            f"User_widget:{user_widget['UserWidget']['Username']}:"
            f"Best Messenger\n"
        )
        return "STATUS OK", user_widget


def remove_user(request, my_username):
    """
    Эта функция позволяет удалить позльзователя!
    Функуция перезаписывает profile таким образом
    что бы не удалялся только пользователь, который
    был удален!
    """
    remove_username = request["Username"]
    user_widgets = []
    user_widget = f'User_widget:{remove_username}:Best Messenger\n'

    try:
        # raise FileNotFoundError
        with open(f"profiles/{my_username}_profile.se", "r") as profile_read:
            for line in profile_read.readlines():
                if user_widget != line:
                    user_widgets.append(line)
            else:
                with open(f"profiles/{my_username}_profile.se", "w") as profile_write:
                    for line in user_widgets:
                        profile_write.writelines(line)
                    else:
                        return "STATUS OK", "STATUS: OK; CODE: 200"

    except FileNotFoundError:
        return "STATUS OK", "STATUS: NOT; CODE: 500"


def send_json_toserver(_json):
    return json.dumps(_json)


def message_handler(server_socket, token_message) -> None:
    for username, socket_token_data in online_users.items():
        client_socket, client_token = socket_token_data[0]
        if client_token == token_message:
            client_mes_socket = online_mes_clients[client_token]
            online_users[username].append([client_mes_socket, token_message])
            online_mes_clients.pop(client_token)
            break
    else:
        client_socket.close()
        return

    if username not in missed_messages:
        missed_messages[username] = {}
    else:
        if username in missed_messages:
            miss_mess = missed_messages[username]
            message_datas = []
            for sender, messages in miss_mess.items():
                response = {
                    MESSAGE_DATA: {
                        "Message": messages,
                        "Chat": sender
                    }
                }
                message_datas.append(response)
            else:
                print(message_datas)
                response = {
                    LIST_MESSAGE_DATA: message_datas
                }
                server_socket.send_handler(
                    content=response,
                    client_socket=online_users[username][1][0],
                    json_dumps=True
                )
                missed_messages[username] = {}

    while True:
        client_request = server_socket.recv_handler(
                         client_socket=client_mes_socket,
                         json_loads=True
        )
        print(client_request)
        if not client_request: client_request = {CLOSE_CONNECTION: True}
        if MESSAGE_DATA in client_request:
            recipient = client_request[MESSAGE_DATA]["Recipient"]
            message = client_request[MESSAGE_DATA]["Message"]
            response = {
                MESSAGE_DATA: {
                    "Message": message,
                    "Chat": username
                }
            }

            if recipient in online_users:
                server_socket.send_handler(
                            content=response,
                            client_socket=online_users[recipient][1][0],
                            json_dumps=True
                )
            else:
                if recipient not in missed_messages:
                    missed_messages[recipient] = {}
                if username not in missed_messages[recipient]:
                    missed_messages[recipient][username] = []

                missed_messages[recipient][username].append(message)
                print(missed_messages)

                server_socket.send_handler(
                    content="User in not onlie",
                    client_socket=online_users[username][1][0],
                    json_dumps=True
                )

        elif CLOSE_CONNECTION in client_request:
            client_socket.close()
            return



def login(request, cursor, trace=True):
    username = request["login"]
    password = request["password"]
    token_server = request["token"]

    cursor.execute("SELECT Username, Password FROM Users")
    if (username, password) in cursor.fetchall():
        cursor.execute(f"SELECT Username, Surname FROM Users \
                WHERE Username = '{username}' AND Password = '{password}'")

        username, surname = cursor.fetchall()[0]
        if username in online_users:
            return ("STATUS NOT", False, False, False)

        with (
            open(f'profiles/{username}_profile.se', 'a'),
            open(f'profiles/{username}_profile.se', 'r') as profile
        ):
            friends = profile.read()
            if trace:
                print(f"User {username} Login!\nHis data:\n"
                      f"\tUsername: {username}\n"
                      f"\tSurname: {surname}\n"
                      f"\tPassword: {password}")

        return (
            "STATUS OK", username, token_server,
            {"Username": username,
             "Surname": surname, "Friends": friends}
        )


    else:
        return "STATUS OK", False, False, False


def registration(request, cursor, database, trace=True):
    username = request['username']
    password = request['password']
    surname = request['surname']
    token_server = request['token']

    if ((username,) not in cursor.execute(
            "SELECT Username FROM Users").fetchall()):

        open(f'profiles/{username}_profile.se', 'w')
        cursor.execute(f"INSERT INTO Users VALUES "
                       f"('{username}', '{surname}', '{password}')")
        database.commit()
        if trace:
            print(f"User {username} Registered!\nHis data:\n"
                    f"\tUsername: {username}\n"
                    f"\tSurname: {surname}\n"
                    f"\tPassword: {password}")

        return "STATUS OK", username, token_server, True

    else:
        return "STATUS NOT", False, False, False


def send_avataricon(serversocket, clientsocket, icon,
                    iconsize, exec, noticon=False):

    if not noticon:
        serversocket.send_handler(
            client_socket=clientsocket,
            content={SET_AVATAR: {AVATAR_SIZE: iconsize, "exec": exec}},
            json_dumps=True, encoding=True
        )
        if serversocket.recv_handler(
            client_socket=clientsocket, json_loads=True,
            decoding=True
        ) == "STATUS OK; CODE 200":

            serversocket.send_handler(
                client_socket=clientsocket,
                content=icon,
                encoding=False,
                json_dumps=False
            )
            if serversocket.recv_handler(
                client_socket=clientsocket, json_loads=True,
                decoding=True
            ) != "SET-AVATAR OK; CODE 200":

                print("Error---------------------------Error")
    else:
        serversocket.send_handler(
            client_socket=clientsocket,
            content=False, json_dumps=True, encoding=True
        )


def client_thread(server_socket, client_socket):
    database = sqlite3.connect('datebase.db')
    cursor = database.cursor()

    while True:
        sendicon = False
        noticon = True
        status = "STATUS NOT"
        client_request = server_socket.recv_handler(
                         client_socket, json_loads=True)
        if not client_request:
            client_request = {CLOSE_CONNECTION: True}

        print(client_request)
        if ACCOUNT_DATA in client_request:
            status, username, token_server, client_response = login(
                client_request[ACCOUNT_DATA], cursor)
            if status == "STATUS OK":
                online_users[username] = [[client_socket, token_server]]

                # for iconfile in os.listdir("profile_icons"):
                #     if iconfile.find(f"{username}_icon") == 0:
                #         with open(f"profile_icons/{iconfile}", "rb") as iconfile_:
                #             icon = iconfile_.read()
                #             iconsize = os.path.getsize(f"profile_icons/{iconfile}")
                #             exec = os.path.splitext(iconfile)[-1]
                #             sendicon = True
                #             noticon = False
                # if not sendicon:
                #     sendicon = True
                #     noticon = True
                #     icon = None
                #     iconsize = None
                #     exec = None

        elif REGIS_DATA in client_request:
            status, username, token_server, client_response = registration(
                client_request[REGIS_DATA], cursor, database)
            if status == "STATUS OK":
                online_users[username] = [[client_socket, token_server]]

        elif SEARCH_DATA in client_request:
            if username and username in online_users:
                status, client_response = check_users(
                    client_request[SEARCH_DATA], username, cursor
                )

        elif APPEND_USER in client_request:
            if username and username in online_users:
                status, client_response = append_user(
                    client_request[APPEND_USER], username
                )

        elif REMOVE_USER in client_request:
            if username and username in online_users:
                status, client_response = remove_user(
                    client_request[REMOVE_USER], username
                )

        elif SET_AVATAR in client_request:
            size = client_request[SET_AVATAR][AVATAR_SIZE]
            exec = client_request[SET_AVATAR]["exec"]
            server_socket.send_handler(
                content="STATUS OK; CODE 200",
                client_socket=client_socket,
                json_dumps=True
            )
            server_socket.recv_size = int(size + 10)
            avatar = server_socket.recv_handler(
                client_socket=client_socket,
                json_loads=False,
                decoding=False
            )
            server_socket.recv_size = 1024
            with open(
                f"profile_icons/{username}_icon{exec}", "wb"
            ) as file:
                # отчистка изображений
                for iconfile in os.listdir("profile_icons"):
                    try:
                        if iconfile.find(f"{username}_icon") == 0:
                            os.remove(f"profile_icons/{iconfile}")
                    except PermissionError: pass
                else:
                    file.write(avatar)

            status = "STATUS OK"
            client_response = "SET-AVATAR OK; CODE 200"

        elif GET_USERICON in client_request:
            username_ = client_request[GET_USERICON]["username"]
            for iconfile in os.listdir("profile_icons"):
                if iconfile.find(f"{username_}_icon") == 0:
                    with open(f"profile_icons/{iconfile}", "rb") as iconfile_:
                        iconfile_ = iconfile_.read()
                        send_avataricon(
                            server_socket, client_socket,
                            iconfile_, os.path.getsize(f"profile_icons/{iconfile}"),
                            os.path.splitext(iconfile)[-1]
                        )

            continue


        elif CLOSE_CONNECTION in client_request:
            if client_request[CLOSE_CONNECTION]:
                for username, sockets in online_users.items():
                    client_socket_ = sockets[0][0]
                    if client_socket == client_socket_:
                        client_socket.close(); client_socket_.close()
                        online_users.pop(username)
                        missed_messages.pop(username); break
                else:
                    client_socket.close()
            break

        print(client_response)
        if status == "STATUS OK":
            server_socket.send_handler(
                client_socket=client_socket, content=client_response,
                json_dumps=True
            )
            # if sendicon:
            #     if sendicon and not noticon:
            #         send_avataricon(server_socket, client_socket,
            #                         icon, iconsize, exec)
            #     elif sendicon and noticon:
            #         send_avataricon(server_socket, client_socket,
            #                         icon, iconsize, exec, noticon=True)
            #     sendicon = False
            #     noticon = True
        else:
            server_socket.send_handler(
                client_socket=client_socket, content=False,
                json_dumps=True
            )


def mes_client_thread(server_socket, client_socket):
    client_request = server_socket.recv_handler(
                        client_socket, json_loads=True)
    if not client_request: return
    if USER_TOKEN in client_request:
        token = client_request[USER_TOKEN]

        online_mes_clients[token] = client_socket
        message_handler(server_socket, token)


def main():
    server_socket = ServerSocketHandler("localhost", 5001)
    server_mes_socket = ServerSocketHandler("localhost", 2001)

    while True:
        client_socket = server_socket.getclientsocket
        client_socket_mes = server_mes_socket.getclientsocket

        print(client_socket)
        print(client_socket_mes)

        Thread(target=client_thread, daemon=True,
               args=(server_socket, client_socket)).start()

        Thread(target=mes_client_thread, daemon=True,
               args=(server_mes_socket, client_socket_mes)).start()


if __name__ == '__main__':
    main()
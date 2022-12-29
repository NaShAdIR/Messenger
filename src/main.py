# Messsenger

from kivy.config import Config

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 600)
Config.set("graphics", "resizable", '0')

from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.screenmanager import (
    ScreenManager, ScreenManagerException)

from clientsocket  import ClientSocketHandler, ConnectionRecovery
from singin_screen import SingInScreen
from singup_screen import SingUpScreen
from chat_screen   import ChatScreen
from main_screen   import MainScreen
from loading_spinner import LoadingWidget
from chat_screen   import Message

from builder_se import Builder_new
from fix_messaage_widget import fix
from threading import Thread
from mytypes import *

import os, sys
import secrets



def connection_check(method):
    def checking_connection(classobject: object, **kwargs):
        try:
            if (
                classobject.server and classobject.server_for_sendmes and
                classobject.server_for_sendmes.connection_ and
                classobject.server.connection_
            ):
                return method(classobject, **kwargs)
            else:
                raise ConnectionRecovery

        except ConnectionRecovery:
            classobject.restart_connection()
            if not classobject.thread_:
                Thread(target=classobject.create_connection_server,
                       args=(kwargs["auto_login"],), daemon=True).start()

    return checking_connection


class MessengerApp(MDApp, Builder_new):
    lock = False
    load = False
    thread_ = False
    spinner = False
    manager_open = False
    set_avatar = False
    account = None

    count = 0
    username = ''
    password = ''
    message = ''
    list_messages = ''
    chat = ''
    ids = {}
    token = secrets.token_hex(256)

    server = None
    server_for_sendmes = None

    def build(self):
        Thread(target=self.create_connection_server, daemon=True).start()

        self.icon = "../assets/images/icon.png"

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(
            SingInScreen(
                press_button_login=self.login,
                press_button_singup=self.get_sing_up
            )
        )
        self.screen_manager.add_widget(
            SingUpScreen(
                press_select_photo=self.change_icon,
                press_leftboldiconbutton=self.get_sing_in,
                press_regisrationbutton=self.registration
            )
        )
        self.screen_manager.add_widget(
            MainScreen(
                press_search_button=self.search_user,
                press_select_photo=self.change_icon
            )
        )

        return self.screen_manager

    def create_connection_server(self, auto_login=False):
        self.server = None
        self.server_for_sendmes = None
        self.thread_ = True

        self.server = ClientSocketHandler("localhost", 5001)
        self.server_for_sendmes = ClientSocketHandler("localhost", 2001)
        if auto_login:
            self.auto_login(auto_login=False)

        self.thread_ = False

    @connection_check
    def auto_login(self, auto_login=False):
        json_data = {
            ACCOUNT_DATA: {
                "login": self.username,
                "password": self.password,
                "token": self.token
            }
        }
        request = {
            USER_TOKEN: self.token
        }
        self.server.send_handler(content=json_data, json_dumps=True)
        if self.server.recv_handler(json_loads=True):
            self.server_for_sendmes.send_handler(content=request, json_dumps=True)

            Clock.schedule_interval(self.handler_message, 1 / 30)
            Thread(target=self.control_message_recv,
                   daemon=True).start()
        else:
            self.dialog = MDDialog(
                title='Messenger',
                text=f'Произошла неизвестная ошибка! Перезапустите приложение!',
                buttons=[MDFlatButton(
                    text='Ок', on_release=lambda ins: self.dialog.dismiss())])
            self.dialog.open()


    def restart_connection(self):
        self.dialog = MDDialog(
            title='Messenger',
            text=f'Потеряно соединение с сервером...',
            buttons=[MDFlatButton(
                text='Ок', on_release=lambda ins: self.dialog.dismiss())])
        self.dialog.open()

    @connection_check
    def registration(self, auto_login=False):
        username = self.screen_manager.get_screen('singup_screen').\
            ids.usernametextfield.text
        password = self.screen_manager.get_screen('singup_screen').\
            ids.passwrodtextfield.text
        surname = self.screen_manager.get_screen('singup_screen').\
            ids.surnametextfield.text

        if (
            3 <= len(username) <= 15 and len(surname) <= 25 and
            8 <= len(password) <= 30
        ):
            json_data = {
                REGIS_DATA: {
                    "username": username,
                    "password": password,
                    "surname" : surname,
                    "token": self.token
                }
            }
            request = {
                USER_TOKEN: self.token
            }
            self.server.send_handler(content=json_data, json_dumps=True)
            if self.server.recv_handler(json_loads=True):
                self.username = username
                self.password = password

                self.data_accaunt(username, None)
                self.screen_manager.transition.direction = 'right'
                self.change_screen("main_screen")

                self.screen_manager.remove_widget(
                    self.screen_manager.get_screen('singin_screen'))
                self.screen_manager.remove_widget(
                    self.screen_manager.get_screen('singup_screen'))

                self.server_for_sendmes.send_handler(
                    content=request, json_dumps=True,
                )
                if not self.set_avatar:
                    with open("../assets/Images/user.png", "rb") as icon:
                        self.avatar = icon.read()
                        self.avatar_size = os.path.getsize("../assets/Images/user.png")
                        self.exec = ".png"

                self.send_avatar_server()
                Clock.schedule_interval(self.handler_message, 1 / 30)
                Thread(target=self.control_message_recv,
                       daemon=True).start()


    @connection_check
    def login(self, auto_login=False):
        # self.loading_widget = LoadingWidget()
        # self.loading_widget.open()
        # self.loading_widget.dismiss()
        login = self.screen_manager.\
            get_screen('singin_screen').ids.login_text_field.text
        password = self.screen_manager.\
            get_screen('singin_screen').ids.password_text_field.text

        if login and password:
            json_data = {
                ACCOUNT_DATA: {
                    "login": login,
                    "password": password,
                    "token": self.token
                }
            }
            request = {
                USER_TOKEN: self.token
            }
            self.server.send_handler(content=json_data, json_dumps=True)
            response = self.server.recv_handler(json_loads=True)
            if response:
                self.username = login
                self.password = password

                self.data_accaunt(response["Username"], response["Friends"])
                geticon_json = {GET_USERICON: {"username": login}}
                self.server.send_handler(
                    content=geticon_json,
                    json_dumps=True, encoding=True)

                self.accepticon(username=login, auto_login=False, returned=False)

                self.screen_manager.transition.direction = 'right'
                self.change_screen('main_screen')

                self.screen_manager.remove_widget(
                    self.screen_manager.get_screen('singin_screen'))
                self.screen_manager.remove_widget(
                    self.screen_manager.get_screen('singup_screen'))

                self.server_for_sendmes.send_handler(
                    content=request, json_dumps=True
                )
                Clock.schedule_interval(self.handler_message, 1 / 30)
                Thread(target=self.control_message_recv,
                       daemon=True).start()

    @connection_check
    def accepticon(self, username=None, auto_login=False, returned=False):
        self.count += 1
        response = self.server.recv_handler(json_loads=True, decoding=True)
        if not response: return
        if SET_AVATAR in response:
            size = response[SET_AVATAR][AVATAR_SIZE]
            exec = response[SET_AVATAR]["exec"]
            self.server.send_handler(
                content="STATUS OK; CODE 200",
                json_dumps=True
            )
            self.server.recv_size = int(size + 10)
            avatar = self.server.recv_handler(
                json_loads=False, decoding=False)
            self.server.recv_size = 1024
            self.server.send_handler(
                content="SET-AVATAR OK; CODE 200",
                json_dumps=True, encoding=True
            )

        with open(f"../server_responses/{username}{self.count}{exec}", "wb") as file:
            file.write(avatar)
            if not returned:
                self.select_path(
                    f"../server_responses/{username}{self.count}{exec}",
                    filemanager=False)
            else:
                # self.usericon = f"../server_downloads/username{exec}"
                return f"../server_responses/{username}{self.count}{exec}"

    def get_sing_up(self):
        self.screen_manager.transition.direction = 'left'
        self.change_screen('singup_screen')


    def get_sing_in(self):
        self.screen_manager.transition.direction = 'right'
        self.change_screen('singin_screen')


    def get_main_screen(self):
        self.screen_manager.transition.direction = 'right'
        self.change_screen('main_screen')


    def data_accaunt(self, *args):
        if len(args[0]) > 9:
            self.screen_manager.get_screen('main_screen').\
                ids.usernamelabel.pos_hint = {"center_x": 0.29, "center_y": 1.5}

        self.screen_manager.get_screen('main_screen').\
            ids.usernamelabel.text = args[0]

        for widget, id in self.handler_userwidget(args[1]):
            self.screen_manager.get_screen('main_screen').\
                ids.listusers.add_widget(widget)

            self.ids[widget.text] = id

    def change_screen(self, name):
        self.screen_manager.current = name

    @connection_check
    def send_message(self, chatname, message=None, auto_login=True):
        if not message:
            message = self.screen_manager.get_screen(chatname).\
                ids.sendmessage_textfield.text

        if message:
            size, halign = fix(message)
            request = {
                MESSAGE_DATA: {
                    "Message": message,
                    "Recipient": chatname[5:]
                }
            }
            self.server_for_sendmes.send_handler(
                content=request, json_dumps=True)

            message_widget = Message(radius=(23, 23, 0, 23))
            message_widget.text = message
            message_widget.halign = halign
            message_widget.pos_hint = {"right": .98}
            message_widget.size_hint_x = size

            self.screen_manager.get_screen(chatname).\
                ids.message_list.add_widget(message_widget)

            self.screen_manager.get_screen(chatname).\
                ids.sendmessage_textfield.text = ''

            username = chatname.split('|')[1]
            self.ids[username].text = f"Вы: {message}"

    def response_message(self, message, chatname):
        if message:
            size, halign = fix(message)

            message_widget = Message(radius=(23, 23, 23, 0))
            message_widget.text = message
            message_widget.halign = halign
            message_widget.pos_hint = {"x": .02}
            message_widget.size_hint_x = size

            self.screen_manager.get_screen(chatname).\
                ids.message_list.add_widget(message_widget)

            username = chatname.split('|')[1]
            self.ids[username].text = f"{username}: {message}"


    def handler_message(self, instance):

        if self.message and self.chat:
            self.lock = True
            try:
                self.response_message(self.message, "chat|" + self.chat)
            except ScreenManagerException:
                self.append_chat_screen(self.chat)
                self.server.send_handler({SEARCH_DATA: self.chat})
                if self.server.recv_handler() != "user_is":
                    self.add_widget(
                        appended_user=self.chat,
                        instance=False
                    )
                self.response_message(self.message, "chat|" + self.chat)

            self.message = ''; self.chat = ''
            self.lock = False

        if self.list_messages:
            self.lock = True
            for message_data in self.list_messages:
                if MESSAGE_DATA in message_data:
                    messages = message_data[MESSAGE_DATA]["Message"]
                    chat = message_data[MESSAGE_DATA]["Chat"]
                    try:
                        for message in messages:
                            self.response_message(message, "chat|" + chat)
                    except ScreenManagerException:
                        self.append_chat_screen(chat)
                        self.server.send_handler({SEARCH_DATA: chat})
                        if self.server.recv_handler() != "user_is":
                            self.add_widget(
                                appended_user=chat,
                                instance=False
                            )
                        for message in messages:
                            self.response_message(message, "chat|" + chat)

            self.list_messages = ''
            self.lock = False

    def append_chat_screen(self, username):
        if username not in self.loads:
            self.screen_manager.add_widget(
                ChatScreen(
                    username=username,
                    press_leftboldiconbutton=self.get_main_screen,
                    press_sendiconbutton=self.send_message
                )
            )
            self.loads.append(username)

    @connection_check
    def control_message_recv(self):
        try:
            while True:
                if not self.lock:
                    response = self.server_for_sendmes.recv_handler(json_loads=True)
                    if response and MESSAGE_DATA in response:
                        self.message = response[MESSAGE_DATA]["Message"]
                        self.chat = response[MESSAGE_DATA]["Chat"]
                    elif response and LIST_MESSAGE_DATA in response:
                        self.list_messages = response[LIST_MESSAGE_DATA]

        except ConnectionRecovery:
            pass

    @connection_check
    def search_user(self, auto_login=True):
        search_text = self.screen_manager.\
            get_screen('main_screen').ids.searchtextfieldr.text

        if not search_text: return
        self.server.send_handler(
            content={SEARCH_DATA: search_text},
            json_dumps=True
        )
        response = self.server.recv_handler()

        match response:
            case True:
                self.dialog = MDDialog(
                    title='Messenger',
                    text=f'Вы хотите добавить пользователя {search_text}?',
                    buttons=[MDFlatButton(text='Да', on_release=(
                                 lambda ins: self.add_widget(search_text))),
                             MDFlatButton(text='Нет', on_release=(
                                 lambda ins: self.dialog.dismiss()))]
                )
                self.dialog.open()

            case 'user_is':
                self.dialog = MDDialog(
                    title='Messenger',
                    text=f'Пользователь {search_text} уже добавлен!',
                    buttons=[MDFlatButton(
                        text='Ок', on_release=lambda ins: self.dialog.dismiss())])
                self.dialog.open()

            case False:
                self.dialog = MDDialog(
                    title='Messenger',
                    text=f'Пользователя {search_text} не существует!',
                    buttons=[MDFlatButton(
                        text='Ок', on_release=lambda ins: self.dialog.dismiss())])
                self.dialog.open()

            case _: pass

    def add_widget(self, appended_user, instance=True):
        if not self.server.send_handler(
            {APPEND_USER: {"appended_user": appended_user}}):
            return

        if instance: self.dialog.dismiss()
        response = self.server.recv_handler()
        if response and "UserWidget" in response:
            response_data = response["UserWidget"]
            username = response_data["Username"]
            message_text = response_data["Message_text"]

            for widget, id in self.handler_userwidget(
                    f"User_widget:{username}:Best messenget\n"):

                self.screen_manager.get_screen('main_screen'). \
                    ids.listusers.add_widget(widget)

                self.ids[widget.text] = id


    def set_config(self):

        with open('../assets/icon/icon.config', 'r') as icon_config:
            config = icon_config.read()
            if config != '':
                config = config.split('|')

                match config[0]:
                    case 'path':
                        path = config[1]
                        self.screen_manager.get_screen('main_screen').\
                            ids.avatarimage.source = path

    def change_icon(self, send_server=False):
        """
        Создаем экземпляр класса MDFileManaget
        Определяем начальную директорию, которая
        откроется в filemanager-е и открываем filemanager
        """
        if not self.manager_open:
            self.filemanager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=lambda path: self.select_path(
                    path=path, auto_login=False, send_avatar=send_server)
            )
            if os.path.isdir("C:%s\OneDrive\\Рабочий стол\\Изображения" % os.environ["HOMEPATH"]):
                path = "C:%s\OneDrive\\Рабочий стол\\Изображения" % os.environ["HOMEPATH"]
            elif os.path.isdir("C:%s\\Изображения" % os.environ["HOMEPATH"]):
                path = "C:%s\\Изображения" % os.environ["HOMEPATH"]
            else:
                path = "C:\\"

            self.filemanager.show(path)

        self.manager_open = True


    def exit_manager(self, *args):
        """
        Закрываем filemanager и удаляем объект.
        """
        self.filemanager.close()
        self.manager_open = False
        del self.filemanager

    @connection_check
    def send_avatar_server(self, auto_login=True):
        """
        Метод позволяет отправить выбранную
        аватарку на сервер для дальнейшего сохранения.
        """
        self.server.send_handler(
            content={SET_AVATAR: {AVATAR_SIZE: self.avatar_size, "exec": self.exec}},
            json_dumps=True,
            encoding=True
        )
        if self.server.recv_handler() == "STATUS OK; CODE 200":
            self.server.send_handler(
                content=self.avatar,
                encoding=False,
                json_dumps=False
            )
            if self.server.recv_handler() != "SET-AVATAR OK; CODE 200":
                self.dialog = MDDialog(
                    title='Messenger',
                    text=f'Не удалось установить аватарку!',
                    buttons=[
                        MDFlatButton(
                            text='Ок',
                            on_release=lambda instance: self.dialog.dismiss()),
                    ]
                )
                self.dialog.open()
                self.avatar_size = ''
                self.avatar = ''
                self.exec = ''

                return False

            self.avatar_size = ''
            self.avatar = ''
            self.exec = ''

            return True

    def select_path(self, path, filemanager=True,
                    auto_login=False, send_avatar=False):

        self.set_avatar = True
        exts = ('.png', '.jpg')
        if os.path.isfile(path) and os.path.splitext(path)[-1] in exts:
            with open(path, "rb") as avatar_bytes:
                self.avatar = avatar_bytes.read()
                self.avatar_size = os.path.getsize(path)
                self.exec = os.path.splitext(path)[-1]
                if send_avatar:
                    self.send_avatar_server(auto_login=True)
        try:
            self.screen_manager.get_screen('singup_screen').\
                ids.avatartimage.source = path
        except ScreenManagerException: pass
        self.screen_manager.get_screen('main_screen').\
            ids.avatarimage.source = path

        self.copy_file(path, '../assets/icon')
        if filemanager: self.exit_manager()


    def copy_file(self, path_from, path_to, onefile=True):
        """
        Метод позволяет копировать файл из одной
        директории в другю.
        В зависимости от аргумента onefile мы будем
        отчищать директорию paht_to, елси onfile=True,
        елси onfile=False директория paht_to останется
        в исходном состоянии.
        """

        if onefile:
            for path in os.listdir(f"../assets/{path_to}"):
                if (
                    path != os.path.basename(path_to) and
                    os.path.splitext(path)[-1] != '.config'
                ):
                    try: os.remove(f"./{path_to}/{path}")
                    except FileNotFoundError: pass
        with (
            open(path_from, 'rb') as file_read,
            open(f"{path_to}/{os.path.basename(path_from)}", 'wb') as file_write
        ):
            file_write.write(file_read.read())

    @connection_check
    def remove_user(self, instance=None, auto_login=False):
        """
        Метод отвечает за удаление пользователей
        из друзей.
        """

        def get_remove(_instance):
            """
            Функция отправляет запрос на сервер
            для удаления пользователя, если ответ
            равет "STATUS: OK; CODE: 200" тогда пользователь
            будет успешно удален! Иначе выведется сообщение
            об ошибке!
            """
            username = instance.parent.parent.text
            self.server.send_handler(
                {REMOVE_USER: {"Username": username}})

            if self.server.recv_handler() == "STATUS: OK; CODE: 200":
                self.screen_manager.get_screen('main_screen'). \
                    ids.listusers.remove_widget(
                    instance.parent.parent
                )

                try:
                    self.screen_manager.remove_widget(
                        self.screen_manager.get_screen(f"chat|{username}"))
                    try: self.loads.remove(username)
                    except ValueError: pass

                except ScreenManagerException: pass
                self.ids.pop(username)
                self.dialog_one.dismiss()

            else:
                self.dialog_one.dismiss()
                self.dialog_two = MDDialog(
                    title='Messenger',
                    text=f'Произошла ошибка на сервере!',
                    buttons=[
                        MDFlatButton(
                            text='Ок',
                            on_release=lambda instance: self.dialog_two.dismiss()),
                    ]
                )
                self.dialog_two.open()


        self.dialog_one = MDDialog(
            title='Messenger',
            text=f'Вы действительно хотите удалть позльзователя {instance.parent.parent.text}?',
            buttons=[
                MDFlatButton(text='Да', on_release=get_remove),
                MDFlatButton(text='Нет',
                             on_release=lambda instance: self.dialog_one.dismiss())
            ]
        )
        self.dialog_one.open()

    def on_stop(self):
        close_data = {CLOSE_CONNECTION: True}
        if (
            self.server and self.server_for_sendmes and
            self.server.connection_ and self.server_for_sendmes.connection_
        ):
            self.server.send_handler(
                content=close_data, json_dumps=True)
            self.server_for_sendmes.send_handler(
                content=close_data, json_dumps=True)

        for file in os.listdir("../server_downloads"):
            os.remove("../server_responses/" + file)

        sys.exit()


if __name__ == '__main__':
    MessengerApp().run()

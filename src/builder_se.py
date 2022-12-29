from mywidget import MyWidget
from mytypes import *


class Builder_new(MyWidget):

    def handler_userwidget(self, response):
        if not response: return ()
        commands = response.split('\n')

        for command in commands:
            data_widget = command.split(':')

            match data_widget[0]:
                case 'User_widget':
                    username, secondary_text = data_widget[1:] # icon
                    geticon_json = {GET_USERICON: {"username": username}}
                    self.server.send_handler(
                        content=geticon_json,
                        json_dumps=True, encoding=True)

                    yield self.UserAvatarListItem(
                        username, secondary_text,
                        self.accepticon(username=username, auto_login=True, returned=True)
                    ) # self.usericon

                case 'Message_widget':
                    pass

    def _message_widget_handler(self):
        pass


class Builder_se:
    __slots__ = ('screen_manager', 'change_screen', 'send_message',
                 'response_message', 'file', 'text', 'lines')

    def __init__(self, screen_manager, change_screen, send_message=None,
                 response_message=None, file=None, text=None):

        self.screen_manager = screen_manager
        self.change_screen = change_screen

        if send_message and response_message:
            self.send_message = send_message
            self.response_message = response_message
            # self.username = username

        if file != None and text == None:
            with open(file, 'r') as file:
                lines = file.readlines()
                lines = tuple(map(self.striping, lines))
        elif text != None and file == None:
            self.lines = text.split('\n')

        self.run()

    def handler_lines_userwidget(self, lines: list | tuple):
        usernames = []
        for line in lines:
            line = line.strip()
            tuple_ = self.user_widget_handler(line)
            if tuple_ != None:
                username, secondary_text, icon = tuple_
            if username not in usernames:
                widget = MyWidget(self.screen_manager, self.change_screen)._TwoLineAvatarListItem_(
                                username=username, secondary_text=secondary_text, icon=icon)
                usernames.append(username)
                yield widget
        else:
            del usernames

    def habdler_lines_message_widget(self, lines: list | tuple):
        for line in lines:
            line = line.strip()
            method, message = self.message_widget_handler(line)
            if method == 'res':
                self.response_message(message, f'chat_{self.username}', )
            if method == 'sen':
                self.send_message(f'chat_{self.username}', message)

    def user_widget_handler(self, line):
        try:
            widget_name, username, secondary_text, icon = line.split(":")
            return username, secondary_text, icon
        except ValueError:
            pass

    def message_widget_handler(self, line):
        return line.split(':')

    def striping(self, line: list | tuple):
        return line.strip()

    def run(self):
        if self.lines[0] == "@User_widget":
            for widget in self.handler_lines_userwidget(self.lines[1:]):
                self.screen_manager.get_screen('main').listusers.add_widget(widget)
        elif self.lines[0] == "@Message_widget":
            self.habdler_lines_message_widget(self.lines[1:])
from kivymd.uix.screen import MDScreen
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton



class MyFloatLayoutOne(MDFloatLayout):

    def __init__(self, **kwargs):
        MDFloatLayout.__init__(self, **kwargs)

        self.size_hint = [0.8, 0.3]
        self.pos_hint = {"center_x": 0.5, "center_y": 0.87}


class MyFloatLayoutTwo(MDFloatLayout):

    def __init__(self, **kwargs):
        MDFloatLayout.__init__(self, **kwargs)

        self.size_hint = [1, 1]


class MessengerLabel(MDLabel):

    def __init__(self, **kwargs):
        MDLabel.__init__(self, **kwargs)

        self.text = "Messenger"
        self.text_color = "blue"
        self.font_name = "../assets/font/mon-amour-one-medium.ttf"
        self.font_size = 53
        self.pos_hint = {"center_x": 0.5, "center_y": 0.3}
        self.size_hint = (1, None)
        self.halign = "center"


class LoginTextField(MDTextField):

    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)

        self.icon_right = "account"
        self.size_hint_x = None
        self.width = "320dp"
        self.mode = "fill"
        self.fill_color_normal = (1, 1, 1, 0.1)
        self.fill_color_focus = (1, 1, 1, 0.3)
        self.hint_text = "Login"
        self.hint_text_color_focus = "black"
        self.text_color_focus = "black"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        self.font_size = "18sp"


class PasswordTextField(MDTextField):

    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)

        self.size_hint_x = None
        self.width = "320dp"
        self.mode = "fill"
        self.fill_color_normal = (1, 1, 1, 0.1)
        self.fill_color_focus = (1, 1, 1, 0.3)
        self.hint_text = "Password"
        self.hint_text_color_focus = "black"
        self.text_color_focus = "black"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.45}
        self.password = True
        self.font_size = "18sp"

    def password_visibility_control(self):
        self.password = (
            False if self.password is True else True)


class IconButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = "eye-off"
        self.theme_text_color = "Hint"
        self.pos_hint = {"center_x": 0.73, "center_y": 0.45}


class LoginButton(MDFillRoundFlatButton):

    def __init__(self, **kwargs):
        MDFillRoundFlatButton.__init__(self, **kwargs)

        self.text = "Login"
        self.pos = (190, 130)
        self.size_hint_y = 0.1
        self.size_hint_x = 0.35
        self.md_bg_color = (1, 1, 1, 0.1)


class SingUpButton(MDFillRoundFlatButton):

    def __init__(self, **kwargs):
        MDFillRoundFlatButton.__init__(self, **kwargs)

        self.text = "Sing up"
        self.pos = (190, 50)
        self.size_hint_y = 0.1
        self.size_hint_x = 0.35
        self.md_bg_color = (1, 1, 1, 0.1)


class MyRelativeLayout(MDRelativeLayout):
    pass


class SingInScreen(MDScreen):

    def __init__(self, **kwargs):
        self.name = "singin_screen"

        keys = []
        for key, value in kwargs.items():
            if key == "press_button_login":
                self.press_button_login = value
                keys.append(key)
            elif key == "press_button_singup":
                self.press_button_singup = value
                keys.append(key)
        else:
            for key in keys:
                kwargs.pop(key)
            del keys

        MDScreen.__init__(self, **kwargs)

        self.add_widget(FitImage(source="../assets/images/Fitimage.png"))
        self.append_widget()

    def append_widget(self):
        # creating class instances
        _MyRelativeLayout = MyRelativeLayout()
        _MyFloatLayoutOne = MyFloatLayoutOne()
        _MyFloatLayoutTwo = MyFloatLayoutTwo()

        password_text_field = PasswordTextField()
        login_text_field = LoginTextField()
        singup_button = SingUpButton()
        login_button = LoginButton()
        icon_button = IconButton()

        # pressure tracking
        login_button.on_release = lambda: \
            self.press_button_login(auto_login=False)
        singup_button.on_release = self.press_button_singup
        icon_button.on_release = password_text_field.password_visibility_control

        # append in ids
        self.ids["password_text_field"] = password_text_field
        self.ids["login_text_field"] = login_text_field

        # append in widget
        _MyFloatLayoutOne.add_widget(MessengerLabel())
        _MyRelativeLayout.add_widget(password_text_field)
        _MyRelativeLayout.add_widget(icon_button)
        _MyFloatLayoutTwo.add_widget(login_text_field)
        _MyFloatLayoutTwo.add_widget(_MyRelativeLayout)
        _MyFloatLayoutTwo.add_widget(login_button)
        _MyFloatLayoutTwo.add_widget(singup_button)

        # append in screen
        self.add_widget(_MyFloatLayoutOne)
        self.add_widget(_MyFloatLayoutTwo)
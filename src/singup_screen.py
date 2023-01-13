from kivymd.uix.screen import MDScreen
from kivymd.uix.fitimage import FitImage
from kivymd.uix.textfield import MDTextField
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton



class LeftBoldIconButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = "arrow-left-bold-circle"
        self.pos_hint = {"center_x": 0.07, "center_y": 0.90}
        self.icon_size = "60sp"


class EyeOffIconButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = "eye-off"
        self.pos_hint = {"center_x": 0.73, "center_y": 0.42}
        self.theme_text_color = "Hint"


class UsernameTextField(MDTextField):

    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)

        self.icon_right = "account"
        self.size_hint_x = None
        self.width = "320dp"
        self.mode = "fill"
        self.fill_color_normal = (1, 1, 1, 0.1)
        self.fill_color_focus = (1, 1, 1, 0.3)
        self.hint_text = "Username"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.66}
        self.font_size = "18sp"
        self.hint_text_color_focus = "black"
        self.text_color_focus = "black"


class SurnameTextField(MDTextField):

    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)

        self.icon_right = "account"
        self.size_hint_x = None
        self.width = "320dp"
        self.mode = "fill"
        self.fill_color_normal = (1, 1, 1, 0.1)
        self.fill_color_focus = (1, 1, 1, 0.3)
        self.hint_text = "Surname"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.54}
        self.font_size = "18sp"
        self.hint_text_color_focus = "black"
        self.text_color_focus = "black"


class PasswordTextField(MDTextField):

    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)

        self.size_hint_x = None
        self.width = "320dp"
        self.mode = "fill"
        self.fill_color_normal = (1, 1, 1, 0.1)
        self.fill_color_focus = (1, 1, 1, 0.3)
        self.hint_text = "Password"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.42}
        self.password = True
        self.font_size = "18sp"
        self.hint_text_color_focus = "black"
        self.text_color_focus = "black"

    def password_visibility_control(self):
        self.password = (
            False if self.password is True else True)


class AvatarImage(FitImage):

    def __init__(self, **kwargs):
        FitImage.__init__(self, **kwargs)

        self.source = "../assets/images/user.png"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.85}
        self.size_hint = 0.19, 0.19
        self.radius = (55, 55, 55, 55)


class SelectAvatarImage(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, kwargs)

        self.icon_size = "110sp"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.85}


class RegistrationButton(MDFillRoundFlatButton):

    def __init__(self, **kwargs):
        MDFillRoundFlatButton.__init__(self, **kwargs)

        self.text = "Зарегестрироваться"
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.1}
        self.size_hint_y = 0.1
        self.size_hint_x = 0.35
        self.md_bg_color = 1, 1, 1, 0.1


class SingUpScreen(MDScreen):

    def __init__(self, **kwargs):
        self.name = "singup_screen"

        keys = []
        for key, value in kwargs.items():
            if key == "press_select_photo":
                self.press_select_photo = value
                keys.append(key)
            elif key == "press_leftboldiconbutton":
                self.press_leftboldiconbutton = value
                keys.append(key)
            elif key == "press_regisrationbutton":
                self.press_regisrationbutton = value
                keys.append(key)
        else:
            for key in keys:
                kwargs.pop(key)

        MDScreen.__init__(self, **kwargs)

        self.add_widget(FitImage(source="../assets/Images/Fitimage.png"))
        self.append_widget()

    def append_widget(self):
        leftboldiconbutton = LeftBoldIconButton()
        usernametextfield = UsernameTextField()
        surnametextfield = SurnameTextField()
        passwrodtextfield = PasswordTextField()
        eyeofficonbutton = EyeOffIconButton()
        regisrationbutton = RegistrationButton()
        selectavatarimage = SelectAvatarImage()
        avatarimage = AvatarImage()

        leftboldiconbutton.on_release = self.press_leftboldiconbutton
        regisrationbutton.on_release = lambda: self.press_regisrationbutton(auto_login=False)
        selectavatarimage.on_release = self.press_select_photo
        eyeofficonbutton.on_release = passwrodtextfield.password_visibility_control

        relativelayout = MDRelativeLayout()
        relativelayout.add_widget(passwrodtextfield)
        relativelayout.add_widget(eyeofficonbutton)


        self.ids["usernametextfield"] = usernametextfield
        self.ids["surnametextfield"] = surnametextfield
        self.ids["passwrodtextfield"] = passwrodtextfield
        self.ids["avatartimage"] = avatarimage

        self.add_widget(leftboldiconbutton)
        self.add_widget(usernametextfield)
        self.add_widget(surnametextfield)
        self.add_widget(relativelayout)
        self.add_widget(selectavatarimage)
        self.add_widget(avatarimage)
        self.add_widget(regisrationbutton)

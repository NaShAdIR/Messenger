from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.graphics import Color
from kivy.lang import Builder


def Message(radius: tuple | list):
    message_widget = """
MDLabel:
    size_hint_y: None
    height: self.texture_size[1]
    padding: 12, 10
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    
    canvas.before:
        Color:
            rgba: (1, 1, 1, 0.1)
        RoundedRectangle:
            size: self.width, self.height
            pos: self.pos
            radius: %s
    """ % str(radius)

    return Builder.load_string(message_widget)


class FloatLayoutOne(MDFloatLayout):

    def __init__(self, **kwargs):
        MDFloatLayout.__init__(self, **kwargs)


class FloatLayoutTwo(MDFloatLayout):

    def __init__(self, **kwargs):
        MDFloatLayout.__init__(self, **kwargs)

        self.md_bg_color = (0.117, 0.190, 0.218, 0.5)
        self.size_hint_y = 0.11
        self.pos_hint = {"center_y": 0.95}


class FloatLayoutFour(MDFloatLayout):

    def __init__(self, **kwargs):
        MDFloatLayout.__init__(self, **kwargs)


class LeftBoldIconButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = "arrow-left-bold-circle"
        self.pos_hint = {"center_x": 0.07, "center_y": 0.5}
        self.icon_size = "60sp"


class UsernameLabel(MDLabel):

    def __init__(self, **kwargs):
        MDLabel.__init__(self, **kwargs)

        self.text = "You hack me!!!"
        self.pos_hint = {"center_y": 0.5}
        self.halign = "center"
        self.font_size = "25sp"
        self.theme_text_color = "Custom"


class ScrollView(MDScrollView):

    def __init__(self, **kwargs):
        MDScrollView.__init__(self, **kwargs)

        self.size_hint_y = 0.7
        self.pos_hint = {'x': 0, 'y': 0.18}
        self.do_scroll_x = False
        self.do_scroll_y = True


class BoxLayout(MDBoxLayout):

    def __init__(self, **kwargs):
        MDBoxLayout.__init__(self, **kwargs)

        self.orientation = "vertical"
        self.size = (600, 600)
        self.size_hint_y = None
        self.pos_hint = {'top': 10}
        self.cols = 1
        self.spacing = 5
        self.adaptive_height = True


class SendMessageTextField(MDTextField):

    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)

        self.mode = "fill"
        self.multiline = True
        self.max_height = "120dp"
        self.size_hint = .8, None
        self.pos_hint = {"center_x": 0.45, "center_y": 1}
        self.font_size = "18sp"
        self.height = self.minimum_height
        self.cursor_width = "2sp"
        self.fill_color_normal = (0.9, 0.9, 0.9, 0.2)
        self.fill_color_focus = (0, 0, 0, 0.1)
        self.padding = 15


class SendMessageIconButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = 'send'
        self.pos_hint = {"center_x": 0.93, "center_y": 1}
        self.user_font_size = "18sp"
        self.theme_text_color = "Custom"
        self.text_color = (1, 1, 1, 1)
        self.md_bg_color = (1, 1, 1, 0.1)


class ChatScreen(MDScreen):

    def __init__(self, **kwargs):

        keys = []
        for key, value in kwargs.items():
            if key == "username":
                self.name = f"chat|{value}"
                self.username = value
                keys.append(key)
            elif key == "press_leftboldiconbutton":
                self.press_leftboldiconbutton = value
                keys.append(key)
            elif key == "press_sendiconbutton":
                self.press_sendiconbutton = value
                keys.append(key)
        else:
            for key in keys:
                kwargs.pop(key)

        MDScreen.__init__(self, **kwargs)
        self.append_widget()

    def append_widget(self):
        floatlayoutone = FloatLayoutOne()
        floatlayouttwo = FloatLayoutTwo()
        floatlayoutthree = MDFloatLayout(size_hint_y=0.13)
        floatlayoutfour = MDFloatLayout()
        leftboldiconbutton = LeftBoldIconButton()
        usernamelabel = UsernameLabel()
        scrollview = ScrollView()
        boxlayout = BoxLayout()
        sendtextfield = SendMessageTextField()
        sendiconbutton = SendMessageIconButton()

        usernamelabel.text = self.username
        leftboldiconbutton.on_release = self.press_leftboldiconbutton
        sendiconbutton.on_release = lambda: \
            self.press_sendiconbutton(
                chatname=self.name, message=sendtextfield.text,
                auto_login=True
            )
        scrollview.scroll_y = 0

        floatlayoutone.add_widget(FitImage(source="../assets/Images/Fitimage.png"))
        floatlayouttwo.add_widget(leftboldiconbutton)
        floatlayouttwo.add_widget(usernamelabel)
        floatlayoutone.add_widget(floatlayouttwo)
        scrollview.add_widget(boxlayout)
        floatlayoutone.add_widget(scrollview)
        floatlayoutfour.add_widget(sendtextfield)
        floatlayoutthree.add_widget(floatlayoutfour)
        floatlayoutthree.add_widget(sendiconbutton)
        floatlayoutone.add_widget(floatlayoutthree)

        self.ids["sendmessage_textfield"] = sendtextfield
        self.ids["message_list"] = boxlayout

        self.add_widget(floatlayoutone)
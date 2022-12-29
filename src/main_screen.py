from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.fitimage import FitImage
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.navigationdrawer import (
                            MDNavigationLayout,
                            MDNavigationDrawer,
                            MDNavigationDrawerItem)


class ScrollView(MDScrollView):

    def __init__(self, **kwargs):
        MDScrollView.__init__(self, **kwargs)

        self.md_bg_color = (1, 1, 1, 0.3)
        self.scroll_timeout = 100
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.size_hint_y = 0.8


class IconButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = "menu"
        self.pos_hint = {"center_x": .05, "center_y": .5}


class NavigationDrawer(MDNavigationDrawer):

    def __init__(self, **kwargs):
        MDNavigationDrawer.__init__(self, **kwargs)

        self.type = "modal"
        self.anchor = "left"
        self.scrim_color = 0, 0, 0, 1
        self.md_bg_color = 1, 1, .8


class SearchTextFieldRect(MDTextFieldRect):

    def __init__(self, **kwargs):
        MDTextFieldRect.__init__(self, **kwargs)

        self.hint_text = 'Search'
        self.mode = "rectangle"
        self.height = "36dp"
        self.size_hint = .8, None
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.background_color = "white"
        # max_text_length: 5


class SelectPhotoButton(MDIconButton):

    def __init__(self, **kwargs):
        MDIconButton.__init__(self, **kwargs)

        self.icon = "camera"
        self.pos_hint = {"center_x": .85, "center_y": 1.4}
        self.size = ("100dp", "100dp")
        self.size_hint = (None, None)
        self.radius = (50, 50, 50, 50)
        self.md_bg_color = (1, 1, .8)


class UsernameLabel(MDLabel):

    def __init__(self, **kwargs):
        MDLabel.__init__(self, **kwargs)

        self.font_size = "24sp"
        self.theme_text_color = "Custom"
        self.text_color = "white"
        self.halign = "center"
        self.size_hint_x = 1
        self.size_hint_y = 0.1
        self.pos_hint = {"center_x": 0.125, "center_y": 1.5}


class AvatarImage(FitImage):

    def __init__(self, **kwargs):
        FitImage.__init__(self, **kwargs)

        self.source = "../assets/images/user.png"
        self.size_hint = [1.105, .8]
        self.pos_hint = {"center_x": .490, "center_y": 1.8}


class NavigationDrawerItemOne(MDNavigationDrawerItem):

    def __init__(self, **kwargs):
        MDNavigationDrawerItem.__init__(self, **kwargs)

        self.icon = "gmail"
        self.right_text = "+99"
        # self.md_bg_color = (1, 1, .93)
        # self.text_right_color = "#4a4939"
        self.text = "Requests"
        self.pos_hint = {"center_x": .49, "center_y": .8}


class NavigationDrawerItemTwo(MDNavigationDrawerItem):

    def __init__(self, **kwargs):
        MDNavigationDrawerItem.__init__(self, **kwargs)

        self.icon = "cog"
        self.md_bg_color = (1, 1, .93)
        self.text = "Settings"
        self.text_right_color = "#4a4939"
        self.pos_hint = {"center_x": .49, "center_y": .59}


class MainScreen(MDScreen):

    def __init__(self, **kwargs):
        self.name = "main_screen"

        keys = []
        for key, value in kwargs.items():
            if key == 'press_menu_button':
                self.press_menu_button = value
                keys.append(key)
            elif key == 'press_search_button':
                self.press_search_button = value
                keys.append(key)
            elif key == 'press_select_photo':
                self.press_select_photo = value
                keys.append(key)
        else:
            for key in keys:
                kwargs.pop(key)
            del keys

        MDScreen.__init__(self, **kwargs)
        fl = MDFloatLayout(
                size_hint=(1, 0.1),
                md_bg_color=(0.5, 0.5, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.05}
        )
        fl.add_widget(MDLabel(
                text="Official messenger from Seyran",
                halign="center"
            )
        )
        self.add_widget(fl)
        self.append_widget()


    def append_widget(self):
        # creating class instances
        md_floatlayout_1 = MDFloatLayout()
        md_floatlayout_2 = MDFloatLayout(
            pos_hint={"center_x": .5, "center_y": .95},
            md_bg_color=(0.5, 0.5, 1),
            size_hint=[1, .1]
        )
        md_floatlayout_3 = MDFloatLayout(
            pos_hint={"center_x": .5, "center_y": .2},
            size_hint=[1, 0.5]
        )
        md_floatlayout_4 = MDFloatLayout(
            pos_hint={"center_x": .49, "center_y": .8}
        )
        icon_button_search = MDIconButton(
            pos_hint={"center_x": .95, "center_y": .5},
            icon="account-search-outline"
        )
        selectphotobutton = SelectPhotoButton()
        navigationlayout = MDNavigationLayout()
        textfieldrect = SearchTextFieldRect()
        navigationdrawer = NavigationDrawer()
        icon_button_menu = IconButton()
        usernamelabel = UsernameLabel()
        md_boxlayout = MDBoxLayout(orientation="vertical")
        avatarimage = AvatarImage()
        scroll_view = ScrollView()
        md_list = MDList()

        # append in widget
        scroll_view.add_widget(md_list)
        md_floatlayout_2.add_widget(icon_button_menu)
        md_floatlayout_2.add_widget(textfieldrect)
        md_floatlayout_2.add_widget(icon_button_search)
        md_floatlayout_3.add_widget(avatarimage)
        md_floatlayout_3.add_widget(selectphotobutton)
        md_floatlayout_3.add_widget(usernamelabel)
        md_floatlayout_3.add_widget(
            MDFillRoundFlatIconButton(
                text="Settings",
                icon="cog",
                icon_size="24sp",
                font_size="18sp",
                md_bg_color=(.5, 1, .5),
                text_color="black",
                icon_color="black",
                pos_hint={"center_x": 0.5, "center_y": .5},
                size_hint=(1, .2)
            )
        )
        md_floatlayout_3.add_widget(
            MDLabel(
                text="Hello everyone, my name is Seyran and I developed this shitty messenger!",
                font_size="18sp",
                pos_hint={"center_x": 0.5, "center_y": 1}
            )
        )
        navigationdrawer.add_widget(md_floatlayout_3)
        navigationlayout.add_widget(navigationdrawer)
        md_floatlayout_1.add_widget(scroll_view)
        md_floatlayout_1.add_widget(md_floatlayout_2)
        md_floatlayout_1.add_widget(navigationlayout)

        # pressure tracking
        icon_button_menu.on_release = lambda: navigationdrawer.set_state('open')
        icon_button_search.on_release = lambda: \
            self.press_search_button(auto_login=True)
        selectphotobutton.on_release = lambda: \
            self.press_select_photo(send_server=True)

        # append in ids
        self.ids['listusers'] = md_list
        self.ids['searchtextfieldr'] = textfieldrect
        self.ids['avatarimage'] = avatarimage
        self.ids['selectphotobutton'] = selectphotobutton
        self.ids['usernamelabel'] = usernamelabel

        # append in screen
        self.add_widget(md_floatlayout_1)


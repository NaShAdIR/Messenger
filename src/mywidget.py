from kivy.uix.button import ButtonBehavior
from kivymd.uix.fitimage import FitImage
from kivymd.uix.list import (
            IconLeftWidget, IconRightWidget,
            TwoLineAvatarIconListItem
)


class RoundIcon(ButtonBehavior, FitImage):
    pass


class MyWidget:
    __slots__ = ()
    loads = []

    def UserAvatarListItem(self, username, secondary_text, icon):
        icon_lift = IconLeftWidget()
        icon_right = IconRightWidget(
            icon="trash-can",
            on_release=lambda instance: self.remove_user(
                instance=instance, auto_login=True)
        )
        icon_lift.add_widget(
            RoundIcon(
                source=icon,
                size=("55dp", "55dp"),
                size_hint=(None, None),
                radius=(20, 20, 20, 20)
            )
        )
        widget = TwoLineAvatarIconListItem(
            text=username,
            secondary_text=secondary_text,
            on_release=(lambda instance: self.get_chat(username))
        )
        widget.add_widget(icon_lift)
        widget.add_widget(icon_right)

        return widget, widget.ids["_lbl_secondary"]

    def get_chat(self, username):
        self.append_chat_screen(username)
        self.screen_manager.transition.direction = 'left'
        self.change_screen(f'chat|{username}')

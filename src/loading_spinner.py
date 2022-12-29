from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class LoadingWidget(MDDialog):

    def __init__(self, **kwargs):
        MDDialog.__init__(self, **kwargs)

        self.size_hint_x = 0.4
        # self.md_bg_color = (0.2, 0.2, 0.2)

        boxlayout = MDBoxLayout(spacing=30)
        floatlayout = MDFloatLayout(size_hint_x=0.4)
        floatlayout.add_widget(
            MDSpinner(
                size_hint=(None, None),
                pos_hint={"center_x": .7, "center_y": .5},
                size=(40, 40),
                active=True
            )
        )
        boxlayout.add_widget(floatlayout)
        boxlayout.add_widget(
            MDLabel(
                text="Загрузка...",
                text_color=(1, 1, 1),
                halign="left"
            )
        )

        self.add_widget(boxlayout)

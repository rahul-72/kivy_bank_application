from kivy.app import App
from kivy.lang import Builder

KV = """

#:import NoTransition kivy.uix.screenmanager.NoTransition

BoxLayout:
    orientation: "vertical"
    Label:
        text: "top"
    ScreenManager:
        id: sm
        transition: NoTransition()
        Screen:
            name: "screen1"
            Button:
                text: "screen 2"
                on_release: sm.current = "screen2"
        Screen:
            name: "screen2"
            Button:
                text: "screen 1"
                on_release: sm.current = "screen1"
    Label:
        text: "bottom"
"""

class TestApp(App):
    def build(self):
        return Builder.load_string(KV)

TestApp().run()
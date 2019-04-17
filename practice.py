from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class MyPracticeApp(App):
    def build(self):
        return Debit()

class Debit(Widget):
    def debit(self):
        print("hi")
        Hello()

class Hello:
    print("Hello world")

if __name__ == "__main__":
    MyPracticeApp().run()
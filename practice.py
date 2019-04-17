from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown

class MyPracticeApp(App):
    def build(self):
        return Debit()

class Debit(Widget):
    def debit(self):
        Hello()


class Hello:
    print("Hello")



if __name__ == "__main__":
    MyPracticeApp().run()
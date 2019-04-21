from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen,ScreenManager


data = None

def hi():
    global data
    data = ('harry', 26)

class MyPracticeApp(App):
    def build(self):
        return Menu()

class Menu(ScreenManager):
    pass

class Debit(Screen):
    def btn(self):
        hi()
        print(data)
        self.manager.current='credit'

class Credit(Screen):
    data_cls = ObjectProperty(None)
    data_cls = data


if __name__ == "__main__":
    MyPracticeApp().run()
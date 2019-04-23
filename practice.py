from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory

class MyPracticeApp(App):
    def build(self):
        return Hello()


class Hello(BoxLayout):
    text_input = ObjectProperty('hi')
    pass

class Mypopup(Popup):
    mytext_input = ObjectProperty('hello')
    def btn(self):
        self.mytext_input = 'qwerty'
        Hello.text_input = self.mytext_input
        print(Hello.text_input)
        self.dismiss()

Factory.register('Hello', cls=Hello)
Factory.register('Mypopup', cls=Mypopup)



if __name__ == "__main__":
    MyPracticeApp().run()
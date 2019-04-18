from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class MyPracticeApp(App):
    def build(self):
        return Menu()

class Menu(Widget):
    def debit(self):
        if self.ids['username'].text == 'hello':
            pass
        else:
            error = "Username Does Not Exist....."
            Popup(title='warning', content=Label(text=error), size=(300, 200), size_hint=(None, None)).open()



if __name__ == "__main__":
    MyPracticeApp().run()
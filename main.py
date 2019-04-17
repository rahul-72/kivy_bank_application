from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import sqlite3 as sql
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""

# creating functions for sqlite3 database.
# creating 3 global variables so that we can use them in functions like debit, credit etc.
db = None
cursor = None
data = None
"""After the execution of db_execute_fetch function the value of data will be:

data= ('rahul123',
 'rahul',
 'charan',
 33000,
 '11100011100',
 'rahul456',
 'charan7rahul@gmail.com',
 2147483647)  

 means data will be in tuple form.
 """


def db_connection():
    global db, cursor
    db = sql.connect("data/bank.db") # Connecting to database if it exits otherwise it will create it.
    cursor = db.cursor()
    # exception handling -->>
    try:
        cursor.execute("create table xyz(username varchar(50) not null primary key, first_name varchar(50) not null, last_name varchar(50) not null, balance int(50) not null, account_number varchar(50) not null, password varchar(50) not null, email varchar(50) not null, phone_number int(50) not null) ")
        cursor.execute("insert into xyz values('rahul123', 'Rahul', 'Charan', 20000, 11100011101, 'rahul456', 'charan7rahul@gmail.com', 7296925650)")
        db.commit()
    except Exception as e:
        pass
    except sql.OperationalError as e:
        pass


def db_execute_fetch(cmd):
    """database ---->>>>> program"""
    global data
    cursor.execute(cmd)
    db.commit()
    data = cursor.fetchone()


def db_execute_insert(cmd):
    """database <<<<<<<-------- program"""
    cursor.execute(cmd)
    db.commit()


def db_close():
    global db, cursor, data
    cursor.close()
    db.close()
    db = None
    cursor = None
    data = None



"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""
class MyApp(App):
    def build(self):
        return WindowManager()

class WindowManager(ScreenManager):
    pass

"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""

class MainMenu(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def check(self):
        db_connection()
        cmd = f"select * from xyz where username='{self.username.text}'"
        db_execute_fetch(cmd)
        print(data)
        if data:
            if self.password.text == data[5]:
                self.manager.current = 'login'

        else:
            error = "Username Does Not Exist....."
            Popup(title='warning', content=Label(text=error), size=(300,200), size_hint=(None,None)).open()



"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""
class Login(Screen):
    pass


class Debit(Screen):
    amount = ObjectProperty(None)
    """amount = int(str(amount))
    def amount_check(self):
        if amount > data[3]:
            self.p = Popup(text='Warning', content=Label(text='You Do Not Have Sufficient Amount.....'), size_hint=(None,None), size=(400,400))
            self.p.open()

        else:"""
    pass




"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""

if __name__ == "__main__":
    MyApp().run()
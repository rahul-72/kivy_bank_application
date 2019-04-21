from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
import sqlite3 as sql
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ListProperty, ObjectProperty
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
# Declaring global username and password...
username = ''
password = ''

"""********************************************************************************************************"""
class MainMenu(Screen):


    def check(self):
        global username, password
        db_connection()

        cmd = f"select * from xyz where username='{self.username.text}'"
        db_execute_fetch(cmd)
        print(data)


        if data:
            if self.password.text == data[5]:
                username = self.username.text
                password = self.password.text

                self.manager.current = 'login'

            else:
                error = "Invalid Password....."
                Popup(title='warning', content=Label(text=error), size=(300, 200), size_hint=(None, None)).open()


        else:
            error = "Username Does Not Exist....."
            Popup(title='warning', content=Label(text=error), size=(300,200), size_hint=(None,None)).open()



"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""
class Login(Screen):
    data_cls = ObjectProperty()
    data_cls = data


    def update_debit(self):
        if self.ids['amount_debit'].text.isdigit():
            self.amount = int(self.ids['amount_debit'].text)
            if self.amount > data[3]:
                print("hiii")
                print(self.data_cls)
                print(data)

                Popup(title='Warning', content=Label(text='You Do Not Have Sufficient Amount.....'), size=(400, 400),
                      size_hint=(None, None)).open()
                self.ids['amount_debit'].text = ''


            else:
                new_amount = data[3] - self.amount
                cmd1 = f"update xyz set balance='{new_amount}' where username='{username}' "
                db_execute_insert(cmd1)

                Popup(title='Warning', content=Label(text=f'****Rs {self.amount} is Debitted \n Successfully From Your Account****'), size=(400, 400),
                      size_hint=(None, None)).open()
                self.ids['amount_debit'].text = ''

        else:
            Popup(title='Warning', content=Label(text='Please Enter Only Numerical Digit.....'), size=(400, 400),
                  size_hint=(None, None)).open()


        """*******************************************************************************************************"""

    def update_credit(self):
        if self.ids['amount_credit'].text.isdigit():
            self.amount = int(self.ids['amount_credit'].text)

            new_amount = data[3] + self.amount
            cmd1 = f"update xyz set balance='{new_amount}' where username='{username}' "
            db_execute_insert(cmd1)

            Popup(title='Warning', content=Label(text='****Your Amount is Updated Successfuly****'),
                  size=(400, 400),
                  size_hint=(None, None)).open()
            self.ids['amount_credit'].text = ''

        else:
            Popup(title='Warning', content=Label(text='Please Enter Only Numerical Digit.....'), size=(400, 400),
                  size_hint=(None, None)).open()

    """**************************************************************************************"""
    def btn_name(self,value):
        if value == 'name':
            return MyPopup_name().open()
        elif value == 'password':
            pass

"""****************************************************************************************************************"""

class MyPopup_name(Popup):

    def btn(self):
        if self.ids['new_first_name'].text:
            cmd1 = f"update xyz set first_name='{self.ids['new_first_name'].text}' where username='{username}'"
            db_execute_fetch(cmd1)

            cmd2 = f"update xyz set last_name='{self.ids['new_last_name'].text}' where username='{username}'"
            db_execute_fetch(cmd2)

            Popup(title='Update', content=Label(text='First and Last Name are\n updated Successfully....'), size=(300, 300),
                  size_hint=(None, None)).open()
            self.ids['new_first_name'].text = ''
            self.ids['new_last_name'].text = ''


        else:
            Popup(title='Warning', content=Label(text='First Name is Mandatory....'), size=(200, 200),
                size_hint=(None, None)).open()

class MyPopup_password(Popup):
    pass

class MyPopup_email(Popup):
    pass

class MyPopup_phone_number(Popup):
    pass

"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""

if __name__ == "__main__":
    MyApp().run()
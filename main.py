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
from random import randint

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
    title = "XYZ Bank"
    icon = 'static/icons/5.ico'
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
                self.username.text = ''
                self.password.text = ''
                Login.data_cls = data

                self.manager.current = 'login'

            else:
                error = "Invalid Password....."
                Popup(title='warning', content=Label(text=error), size=(300, 200), size_hint=(None, None)).open()


        else:
            error = "Username Does Not Exist....."
            Popup(title='warning', content=Label(text=error), size=(300,200), size_hint=(None,None)).open()



"""XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"""
class Login(Screen):
    data_cls = ObjectProperty((1,2,3,4,5,6,7,8))


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


    def logout(self):
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

class Signup(Screen):
    def signup(self):
        if self.ids['username'].text:
            if self.ids['first_name'].text:
                if self.ids['password'].text:
                    if self.ids['email'].text:
                        if self.ids['phone_number'].text:
                            cmd = f"select * from xyz where username='{self.ids['username'].text}'"
                            db_connection()
                            db_execute_fetch(cmd)

                            if not data:
                                if self.ids['password'].text== self.ids['verify_password'].text:

                                    while True:
                                        q, w, e, r, t, y, u, i, o, p, l = map(str, [randint(0, 9) for i in range(11)])
                                        """Assigning 11 random number to update
                                        account-number in database."""
                                        a = q + w + e + r + t + y + u + i + o + p + l

                                        cmd1 = "select * from xyz where account_number='{a}'"
                                        # Here I am not database' functions which I created above.
                                        cursor.execute(cmd1)
                                        data1 = cursor.fetchall()
                                        if data1:
                                            """checking whether a randomly generated account number is already
                                            in bank database or not."""
                                            continue
                                        else:
                                            break



                                    if len(self.ids['phone_number'].text) == 10:
                                        try:

                                            int_phone_number = int(self.ids['phone_number'].text)
                                            cmd2 = f"insert into xyz values('{ self.ids['username'].text}','{ self.ids['first_name'].text}','{self.ids['last_name'].text}',0,'{a}','{ self.ids['password'].text}','{self.ids['email'].text}','{int_phone_number}')"
                                            db_execute_insert(cmd2)
                                            db_close()

                                            self.name = self.ids['first_name'].text.title() + ''+ self.ids['last_name'].text.title()

                                            Popup(title='Warning',
                                                  content=Label(text=f'Hello {self.name}...\nAccount Is Successfully Created With Initial Balance Of  Rs 0  \n...Your Account Number is -->> {a}..........\n Enjoy The Services Of XYZ Bank....Have A Nice Day...'),
                                                  size=(700, 400),
                                                  size_hint=(None, None)).open()

                                            self.ids['username'].text = ''
                                            self.ids['first_name'].text = ''
                                            self.ids['last_name'].text = ''
                                            self.ids['password'].text = ''
                                            self.ids['verify_password'].text = ''
                                            self.ids['email'].text = ''
                                            self.ids['phone_number'].text = ''

                                            self.manager.current = 'mainmenu'

                                        except Exception as e:
                                            print(e)
                                            Popup(title='Warning',
                                                  content=Label(text='Enter Only Digits in Phone  number..'),
                                                  size=(400, 200),
                                                  size_hint=(None, None)).open()

                                            self.ids['password'].text = ''
                                            self.ids['verify_password'].text = ''




                                    else:
                                        Popup(title='Warning', content=Label(text='Enter Only 10 Digits Phone Number..'),
                                              size=(400, 200),
                                              size_hint=(None, None)).open()

                                else:
                                    Popup(title='Warning', content=Label(text='Password Verification is Failed...'),
                                          size=(400, 200),
                                          size_hint=(None, None)).open()

                            else:
                                Popup(title='Warning', content=Label(text='UserName has already been taken.\n Please Choose Another UserName..'),
                                      size=(500, 200),
                                      size_hint=(None, None)).open()


                        else:
                            Popup(title='Warning', content=Label(text='Phone Number is Mandatory....'), size=(400, 200),
                                  size_hint=(None, None)).open()

                    else:
                        Popup(title='Warning', content=Label(text='Email is Mandatory....'), size=(400, 200),
                              size_hint=(None, None)).open()

                else:
                    Popup(title='Warning', content=Label(text='Password is Mandatory....'), size=(400, 200),
                          size_hint=(None, None)).open()

            else:
                Popup(title='Warning', content=Label(text='First Name is Mandatory....'), size=(400, 200),
                      size_hint=(None, None)).open()

        else:
            Popup(title='Warning', content=Label(text='Username is Mandatory....'), size=(400, 200),
                  size_hint=(None, None)).open()

"""================================================================================================================"""
if __name__ == "__main__":
    MyApp().run()
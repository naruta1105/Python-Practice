from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from image.hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self) :
        self.manager.current = "sign_up_screen"

    def login(self,uname, pword) :
        with open("users.json") as file :
            users = json.load(file)
        
        if uname in users.keys():
            if users[uname]['password'] == pword :
                self.manager.current = "login_success_screen"
            else :
                self.ids.login_wrong.text = "Wrong password"
        else :
            self.ids.login_wrong.text = "User not exist"


class SignUpScreen(Screen):
    def add_user(self, uname, pword) :
        with open("users.json") as file :
            users = json.load(file)

        users[uname] = {'username':uname, 'password':pword, 
            'created': datetime.now().strftime("%y-%m-%d %H:%M:%S.%f")}

        with open("users.json","w") as file :
            json.dump(users, file)
        
        self.manager.current = "sign_up_success_screen"

class SignUpSuccessScreen(Screen):
    def go_to_login(self):
        # change direction when change page to 'right', default is left
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
        
class LoginSuccessScreen(Screen):
    def log_out(self):
        # change direction when change page to 'right', default is left
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    
    def got_quote(self,emo):
        emo = emo.lower()
        available_emos = glob.glob("quotes/*txt")
        available_emos = [Path(filename).stem for filename in available_emos]
        
        if emo in available_emos :
            with open(f"quotes/{emo}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else :
            self.ids.quote.text = "Try another one (ex: happy, sad...)"
class ImageButton(ButtonBehavior, HoverBehavior, Image ) :
    # ButtonBehavior nên đặt lên đầu để cho on_press thưc thi được
    pass
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__" :
    MainApp().run()
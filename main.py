import datetime
import tkinter as tk
from PIL import Image, ImageTk 
import subprocess
import util
import cv2
import os.path

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100") 
        background_image = Image.open("/Users/Cherry/Desktop/Face recognition attendance system/bg_photo/pexels-laura-tancredi-7078620.jpg")  
        background_photo = ImageTk.PhotoImage(background_image)
        
        background_label = tk.Label(self.main_window, image=background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_photo
        
        heading_label = tk.Label(self.main_window, text="Lorem Ipsum Ltd. Attendance System", font=("Helvetica", 30), foreground="black")
        heading_label.place(x=350, y=520)

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'blue', self.login)
        self.login_button_main_window.place(x=750, y=300)
        self.main_window.update_idletasks()

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'red', self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
          os.mkdir(self.db_dir)
          
        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        def process_webcam():
            ret, frame = self.cap.read()

            self.most_recent_capture_arr = frame

            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

            self.most_recent_capture_pil = Image.fromarray(img_)

            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            label.after(20, process_webcam)

        process_webcam()

    def login(self):
      
        unknown_img_path = './.tmp.jpg'
        
        cv2.imwrite(unknown_img_path,self.most_recent_capture_arr)
        
        output = str(subprocess.check_output(['face_recognition',self.db_dir,unknown_img_path]))
        name = output.split(',')[1][:-3]
        
        if name in ['unknown_person','no_person_found']:
          util.msg_box('Ups...','Unknown user. Please register new user or try again.')
          
        else:
          util.msg_box('Welcome back!','Welcome,{}'.format(name))
          with open(self.log_path,'a') as f:
            f.write('{},{}\n'.format(name,datetime.datetime.now()))
            f.close()
        os.remove(unknown_img_path)
        
        
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)
        
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)
        
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        
        self.add_image_to_label(self.capture_label)
        
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750,y=150)
        
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750,y=70)
        
    def try_again_register_new_user(self):
      self.register_new_user_window.destroy()
        
    def add_image_to_label(self,label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()
        
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0,"end-1c")
        cv2.imwrite(os.path.join(self.db_dir,'{}.jpg'.format(name)),self.register_new_user_capture)
        
        util.msg_box('Success!','User was registered successfully !')
        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()

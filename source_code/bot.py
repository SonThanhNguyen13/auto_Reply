import tkinter as tk
from tkinter import messagebox
import multiprocessing
from fbchat import Client
from fbchat.models import *

# make a list of ids to avoid being spam
list_id = []


class Bot(Client):
    def onMessage(
        self, message_object, author_id, thread_id, thread_type, **kwargs):
        if author_id != self.uid and author_id not in list_id:
            list_id.append(author_id)
            self.send(Message(
                text='Auto message: {}'.format(inp_tx)),
                thread_id=author_id,
                thread_type=ThreadType.USER
                )
            self.send(
                Message(sticker=Sticker(inp_st)),
                thread_id=author_id,
                thread_type=ThreadType.USER
                )


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.master.title('Facebook auto reply message')
        self.pack(fill='both', expand=1)
        self.label = tk.Label(text='Login', fg='red')
        self.label.place(x=130, y=35)

        self.o_username = tk.Entry()
        self.o_username.place(x=100, y=70)
        self.o_username.bind('<Key-Return>', self.login)

        self.o_pw = tk.Entry(show='*')
        self.o_pw.place(x=100, y=100)
        self.o_pw.bind('<Key-Return>', self.login)

        us_lb = tk.Label(text='Username', fg='black')
        us_lb.place(x=20, y=70)

        pw_lb = tk.Label(text='Password', fg='black')
        pw_lb.place(x=20, y=100)

        sl_lb = tk.Label(text='Message', fg='black')
        sl_lb.place(x=20, y=180)

        self.inp_text = tk.Entry()
        self.inp_text.place(x=100, y=180)
        self.inp_text.bind('<Key-Return>', self.login)

        self.t_lb = tk.Label(text='Message', fg='blue')
        self.t_lb.place(x=120, y=150)

        self.o_sticker = tk.Entry()
        self.o_sticker.place(x=100, y=210)
        self.o_sticker.bind('<Key-Return>', self.login)

        self.sticker_lb = tk.Label(text='Sticker id')
        self.sticker_lb.place(x=20, y=210)

        input_button = tk.Button(
            self,
            text='Login & Run',
            fg='blue',
            command=self.login
            )
        input_button.place(x=30, y=250)

        self.stop_button = tk.Button(
            self,
            text='Stop!!!',
            fg='red',
            command=self.stop
        )
        self.stop_button.place(x=190, y=250)

    def stop(self):
        try:
            if self.lis.is_alive() is True:
                self.lis.terminate()
                messagebox.showinfo('', 'Listening stopped')
                self.o_pw.delete(0, 'end')
        except AttributeError:
            pass

    def login(self, event=None):
        try:
            if self.lis.is_alive() is True:
                pass
        except AttributeError:
            id = self.o_username.get()
            pw = self.o_pw.get()
            if id is '' or pw is '':
                messagebox.showerror('', 'Email or password not set')
                return
            else:
                try:
                    global inp_tx
                    inp_tx = self.inp_text.get()
                    global inp_st
                    inp_st = self.o_sticker.get()
                    bot = Bot(id, pw)
                    messagebox.showinfo(' ', 'Success, start listening')
                    self.o_pw.delete(0, 'end')
                    self.lis = multiprocessing.Process(target=bot.listen)
                    self.lis.start()
                except FBchatUserError:
                    messagebox.showerror('', 'Invalid username or password')
                    self.o_pw.delete(0, 'end')


def main():
    root = tk.Tk()
    app = Application(master=root)
    root.geometry('300x300')
    app.mainloop()


if __name__ == '__main__':
    main()

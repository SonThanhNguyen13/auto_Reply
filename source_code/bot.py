from tkinter import *
from fbchat import Client
from fbchat.models import *
from tkinter import messagebox

# make a list of ids to avoid being spam
list_id = []


class Bot(Client):
    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
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


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.master.title('Facebook auto reply message')
        self.pack(fill='both', expand=1)
        
        self.label = Label(text='Login', fg='red')
        self.label.place(x=130, y=35)
        
        self.username = StringVar()
        self.o_username = Entry()
        self.o_username.place(x=100, y=70)
        self.o_username.bind('<Key-Return>', self.login)
        
        self.o_pw = Entry(show='*')
        self.o_pw.place(x=100, y=100)
        self.o_pw.bind('<Key-Return>', self.login)
        
        us_lb = Label(text='Username', fg='black')
        us_lb.place(x=20, y=70)
        
        pw_lb = Label(text='Password', fg='black')
        pw_lb.place(x=20, y=100)
        
        sl_lb = Label(text='Message', fg='black')
        sl_lb.place(x=20, y=180)
        
        self.inp_text = Entry()
        self.inp_text.place(x=100, y=180)
        self.inp_text.bind('<Key-Return>', self.login)

        self.t_lb = Label(text='Message', fg='blue')
        self.t_lb.place(x=120, y=150)

        self.o_sticker = Entry()
        self.o_sticker.place(x=100, y=210)
        self.o_sticker.bind('<Key-Return>', self.login)

        self.sticker_lb = Label(text='Sticker id')
        self.sticker_lb.place(x=20, y=210)

        input_button = Button(
            self,
            text='Login & Run',
            fg='blue',
            command=self.login
            )
        input_button.place(x=100, y=250)

    def login(self, event=None):
        try:
            id = self.o_username.get()
            pw = self.o_pw.get()
            global inp_tx
            inp_tx = self.inp_text.get()
            global inp_st
            inp_st = self.o_sticker.get()
            bot = Bot(id, pw)
        except Exception:
            messagebox.showerror(' ','Invalid Username or Password')
            return self.create_widgets()
        else:
            messagebox.showinfo(' ', 'Success, start listening')
            self.master.destroy()
            bot.listen()


def main():
    root = Tk()
    app = Application(master=root)
    root.geometry('300x300')
    app.mainloop()


if __name__ == '__main__':
    main()

import json
import os
import tkinter.font as font
from os import system
from sys import exit as end
from threading import Thread
from tkinter import *
from tkinter import messagebox

from flask import Flask, request

app = Flask(__name__)

# if user has the keyboard module installed
has_keyboard = True

try:
    import keyboard
except (ModuleNotFoundError, ImportError):
    # user doesn't have keyboard module installed
    dummy = Tk()
    dummy.withdraw()
    messagebox.showwarning(
        "Missing Module: keyboard",
        'Your system is missing the module "keyboard" for this program to work correctly.\n\nPlease click OK to install the "keyboard" module automatically.\nIn case this fails, the keyboard will still open in a non functional state',
    )
    kbmodulestatus = system("python -m pip install keyboard")
    if kbmodulestatus != 0:
        messagebox.showerror(
            "Error",
            'Couldn\'t install "keyboard" module automatically. Please try again manually in command prompt using command:\n\npip install keyboard',
        )
        dummy.destroy()
        has_keyboard = False
    else:
        import keyboard

        dummy.destroy()
        has_keyboard = True


class VirtualKeyboard:

    def __init__(self, master=Tk()):
        # Main Window
        self.master = master
        self.master.overrideredirect(True)
        self.spl_key_pressed = False
        # Colors
        self.lightgray = "#CCCCCC"
        self.gray = "#767676"
        self.darkred = "#591717"
        self.red = "#822626"
        self.darkpurple = "#7151c4"
        self.purple = "#9369ff"
        self.darkblue = "#386cba"
        self.blue = "#488bf0"
        self.darkyellow = "#bfb967"
        self.yellow = "#ebe481"
        self.white = "#ffffff"
        self.black = "#000000"

        self.master.configure(bg=self.white)
        self.unmap_bind = self.master.bind("<Unmap>", lambda e: [self.rel_shifts()])

        # makes sure shift/ctrl/alt/win keys aren't pressed down after keyboard closed
        self.master.protocol("WM_DELETE_WINDOW", lambda: [self.master.destroy(), end()])

        self.user_scr_width = int(self.master.winfo_screenwidth())
        self.user_scr_height = int(self.master.winfo_screenheight())

        self.trans_value = 0.9
        self.master.attributes("-alpha", self.trans_value)
        self.master.attributes("-topmost", True)

        w = int(0.63 * self.user_scr_width)
        h = int(0.37 * self.user_scr_height)

        # open keyboard in medium size by default (not resizable)
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs) - (h)

        # set the dimensions of the screen
        # and where it is placed

        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.resizable(True, True)

        # Define only the letters A-Z and numbers 0-9
        self.row1keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        self.row2keys = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]

        self.row3keys = ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ñ"]

        self.row4keys = ["z", "x", "c", "v", "b", "n", "m", "backspace"]

        self.row5keys = ["shift", "spacebar", "enter"]

        # buttons for each row
        self.row1buttons = []
        self.row2buttons = []
        self.row3buttons = []
        self.row4buttons = []
        self.row5buttons = []

        # efficiency i guess?
        appendrow1 = self.row1buttons.append
        appendrow2 = self.row2buttons.append
        appendrow3 = self.row3buttons.append
        appendrow4 = self.row4buttons.append
        appendrow5 = self.row5buttons.append

        # prevents frames having inconsistent relative dimensions
        self.master.columnconfigure(0, weight=1)
        for i in range(5):
            self.master.rowconfigure(i, pad=1, weight=1)

        # Create fonts according to screen resolution
        if self.user_scr_width < 1600:
            self.keyfont = font.Font(family="Calibri", size=14, weight="bold")
        else:
            self.keyfont = font.Font(family="Calibri", size=18, weight="bold")

        # Create frames and buttons for each row
        configs = dict(row=0, sticky="NSEW", padx=10)
        # ROW 1

        alphanum_keys_style = dict(
            bg=self.lightgray,
            fg=self.black,
            activebackground=self.gray,
            activeforeground=self.white,
            relief=GROOVE,
            borderwidth=2,
            width=5,
        )
        keyframe1 = Frame(self.master, height=1)
        keyframe1.rowconfigure(0, weight=1)
        for key in self.row1keys:
            ind = self.row1keys.index(key)
            keyframe1.columnconfigure(ind, weight=1)
            appendrow1(
                Button(
                    keyframe1,
                    font=self.keyfont,
                    text=key.title(),
                    **alphanum_keys_style
                )
            )
            self.row1buttons[ind].grid(column=ind, **configs)

        # ROW 2
        keyframe2 = Frame(self.master, height=1)
        keyframe2.rowconfigure(0, weight=1)
        for key in self.row2keys:
            ind = self.row2keys.index(key)
            keyframe2.columnconfigure(ind, weight=1)
            appendrow2(
                Button(
                    keyframe2,
                    font=self.keyfont,
                    text=key.title(),
                    **alphanum_keys_style
                )
            )
            self.row2buttons[ind].grid(column=ind, **configs)

        # ROW 3
        keyframe3 = Frame(self.master, height=1)
        keyframe3.rowconfigure(0, weight=1)
        for key in self.row3keys:
            ind = self.row3keys.index(key)
            keyframe3.columnconfigure(ind, weight=1)
            appendrow3(
                Button(
                    keyframe3,
                    font=self.keyfont,
                    text=key.title(),
                    **alphanum_keys_style
                )
            )
            self.row3buttons[ind].grid(column=ind, **configs)

        # ROW 4
        keyframe4 = Frame(self.master, height=1)
        keyframe4.rowconfigure(0, weight=1)
        for key in self.row4keys:
            title = key.title()
            ind = self.row4keys.index(key)
            keyframe4.columnconfigure(ind, weight=1)
            if title == "Backspace":
                title = "←\nBorrar"
                bg = self.gray
                fg = self.white
                keyfont = font.Font(family="Calibri", size=14, weight="bold")
                width = 28
                button_style = dict(font=keyfont, text=title, bg=bg, fg=fg, width=width)
            else:
                button_style = dict(
                    font=self.keyfont, text=key.title(), **alphanum_keys_style
                )

            appendrow4(Button(keyframe4, **button_style))

            self.row4buttons[ind].grid(column=ind, **configs)

        keyframe5 = Frame(self.master, height=1)
        keyframe5.rowconfigure(0, weight=1)
        for key in self.row5keys:
            title = key.title()
            bg = self.white
            ind = self.row5keys.index(key)
            keyframe5.columnconfigure(ind, weight=1)
            width = 10
            fg = self.black
            if title == "Spacebar":
                title = "Espacio"
                width = 56
                bg = self.gray
                fg = self.white
            elif title == "Enter":
                title = "Intro"
                bg = self.gray
                fg = self.white
            elif title == "Shift":
                title = "Shift ↑"
                bg = self.gray
                fg = self.white
            appendrow5(
                Button(
                    keyframe5,
                    font=self.keyfont,
                    bg=bg,
                    fg=fg,
                    activebackground=self.gray,
                    activeforeground=self.lightgray,
                    width=width,
                    relief=GROOVE,
                    text=title,
                )
            )
            configs["padx"] = 5
            self.row5buttons[ind].grid(column=ind, **configs)

        # Adding frames to the main window
        padding_and_stick = dict(padx=10, pady=2, sticky="NSEW")
        keyframe1.grid(row=0, **padding_and_stick)
        keyframe2.grid(row=1, **padding_and_stick)
        keyframe3.grid(row=2, **padding_and_stick)
        keyframe4.grid(row=3, **padding_and_stick)
        keyframe5.grid(row=4, **padding_and_stick)

    def donothing(self):
        pass

    def vupdownkey(self, event, y, a):
        self.master.after(80, self.donothing())

        if y == "shift":
            if self.row5buttons[0].cget("relief") == SUNKEN:
                self.rel_shifts()
            else:
                self.prs_shifts()
        if a == "L":
            self.spl_key_pressed = False
        elif a == "R":
            self.spl_key_pressed = True

    # release shift keys
    def rel_shifts(self):
        """
        Release the shift button
        """
        keyboard.release("shift")

        self.row5buttons[0].config(
            relief=RAISED,
            bg=self.gray,
            activebackground=self.gray,
            activeforeground="#bababa",
            fg="white",
        )

    def prs_shifts(self):
        """
        Keep the shift pressed
        """
        keyboard.press("shift")

        self.row5buttons[0].config(
            relief=SUNKEN,
            activebackground=self.gray,
            bg=self.gray,
            fg="#bababa",
            activeforeground="white",
        )

    def start(self):
        """
        Start the keyboard
        """
        self.master.mainloop()

    def engine(self):
        """
        Add functionality to keyboard
        """
        self.master.protocol(
            "WM_DELETE_WINDOW",
            lambda: [keyboard.release("shift"), self.master.destroy(), end()],
        )

        for key in self.row1keys:
            ind = self.row1keys.index(key)
            self.row1buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row2keys:
            ind = self.row2keys.index(key)
            self.row2buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row3keys:
            ind = self.row3keys.index(key)
            self.row3buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row4keys:
            ind = self.row4keys.index(key)
            self.row4buttons[ind].config(command=lambda x=key: self.vpresskey(x))

        for key in self.row5keys:
            ind = self.row5keys.index(key)
            if key.title() == "Shift":
                self.row5buttons[ind].config(
                    command=lambda: self.vupdownkey(
                        event="<Button-1>", y="shift", a="R"
                    )
                )
                self.row5buttons[ind].bind(
                    "<Button-3>",
                    lambda event="<Button-3>", y="shift", a="L": self.vupdownkey(
                        event, y, a
                    ),
                )
            else:
                self.row5buttons[ind].config(command=lambda x=key: self.vpresskey(x))
        self.master.withdraw()

    def vpresskey(self, x):
        """
        Function to press and release keys

        Parameters:
            x: string that represent a character mapped in the keyboard
        """
        if not self.spl_key_pressed or x in ("1234567890"):
            self.rel_shifts()
        self.master.unbind("<Unmap>", self.unmap_bind)
        self.master.withdraw()
        self.master.after(1, keyboard.send(x))
        self.master.after(0, self.master.wm_deiconify())
        self.unmap_bind = self.master.bind("<Unmap>", lambda e: [self.rel_shifts()])

    def resize(self, w, h):
        """
        Fuction that allows resizing through API calls
        """
        # open keyboard in medium size by default (not resizable)
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs) - (h)

        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.master.resizable(True, True)

    def show(self):
        """
        Shows the keyboard through API calls.
        """
        self.master.deiconify()  # Muestra el teclado

    def hide(self):
        """
        Hide the keyboard through API calls.
        """
        self.master.withdraw()  # Oculta el teclado

    def set_transparency(self, value):
        """
        Set th keyboard transparency through API calls.
        """
        self.master.withdraw()
        self.trans_value = value
        self.master.attributes("-alpha", self.trans_value)
        self.master.wm_deiconify()

    @app.route("/keyboard", methods=["POST"])
    def keyboard_action():
        """
        Manage actions

        Requests ex:
            ** check documentation
        """
        action = request.json.get("action")
        if action == "show":
            keyboard1.show()
        elif action == "hide":
            keyboard1.hide()
        elif action == "resize":
            w = int(request.json.get("width"))
            h = int(request.json.get("height"))
            keyboard1.resize(w, h)
        elif action == "set_transparency":
            value = float(request.json.get("value"))
            keyboard1.set_transparency(value)
        elif action == "quit":
            os._exit(0)
        return json.dumps({"status": "success"}), 200

    @app.route("/keyboard/presskey", methods=["POST"])
    def press_button():
        content = request.json.get("content")
        for char in content:
            keyboard1.vpresskey(char)
        return json.dumps({"status": "success"}), 200


def run_flask():
    app.run(host="0.0.0.0", port=5000)  # Ejecuta Flask en otro hilo


if __name__ == "__main__":
    keyboard1 = VirtualKeyboard()
    if has_keyboard:
        keyboard1.engine()

    # Ejecuta Flask en un hilo separado
    Thread(target=run_flask).start()

    # Muestra el teclado
    keyboard1.start()

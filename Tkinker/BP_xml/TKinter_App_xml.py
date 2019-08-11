

import tkinter as tk
from tkinter import ttk
# import matplotlib
# from matplotlib import style
import os
from settings import Settings
from file_management import SaveOutputToCsv
from xml_loop import ParsingXml


LARGE_FONT = ("Verdana", 15, "bold")
# style.use("ggplot")
Label_dispaly = "This application is retreving information regarding:\n processes, objects and variables."


class xmlPages (tk.Tk):
    """ The main class is inheriting from tk.TK class  """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__ (self, *args, **kwargs)
        """  """
        self.app_data = {
            "file_path": tk.StringVar(),
            "process_subprocess_list": [],
            "save_file_path": "",

        }

        # Set window title
        tk.Tk.wm_title(self, "Manipulation Tool v 1.0")
        # Set geomatry
        self.set_geometry()

        # create container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background="#bdb5bf")

        # frame = StartPage(container, self)
        # self.frames[StartPage]=frame

        self.show_frame(StartPage)
        print(self.frames)

    def show_frame(self, count):
        """ Show TKinter frame"""
        frame = self.frames[count]
        frame.tkraise()

    def set_geometry(self):
        """ Set TKinter window in the middle of the screen """
        settings = Settings()

        x_coordinate = ((int(self.winfo_screenwidth()) / 2)
                        - (int(settings.width_of_window) / 2))
        y_coordiante = ((int(self.winfo_screenheight()) / 2)
                        - (int(settings.height_of_window) / 2))

        print(
            "%dx%d+%d+%d" % (
                settings.width_of_window,
                settings.height_of_window,
                x_coordinate, y_coordiante
            )
        )
        self.geometry(
            "%dx%d+%d+%d" % (
                settings.width_of_window,
                settings.height_of_window,
                x_coordinate, y_coordiante
            )
        )
        # self.geometry(f"{self.height_of_window}x{self.width_of_window}+{str(x_coordinate)}+{str(y_coordiante)}")

    def open_file_and_parse_xml(self):

        file_path = SaveOutputToCsv.open_file_dialog_box()


        # Assign file path to app_data dic\
        self.app_data["file_path"] = file_path

        self.app_data["process_subprocess_list"] = ParsingXml.parse_bp_releases(file_path)

        # Display page one frame
        self.show_frame(PageOne)

    def save_path_cont(self):

        output_file = SaveOutputToCsv(self.app_data["process_subprocess_list"])

        output_file.save_path_cont()

        output_file.create_csv()

        # display frame Page two
        self.show_frame(PageTwo)


class StartPage (tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         text=Label_dispaly,
                         bg="grey",
                         font=LARGE_FONT,
                         width="330",
                         height="2",
                         fg="white",
                         relief="groove",
                         anchor="center")

        label.pack()
        tk.Label(self, background="#bdb5bf").pack()
        ttk.Label(self, background="#bdb5bf").pack()
        button1 = tk.Button (
            self,
            text="Open file",
            width="33",
            height="2",
            command=lambda: controller.open_file_and_parse_xml()
        )
        button1.pack()


class PageOne (tk.Frame):
    """ First page class """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Successful load!!\nChoose the save files location.",
                         font=LARGE_FONT,
                         bg="grey",
                         width="330",
                         height="2",
                         fg="white",
                         relief="groove",
                         anchor="center")

        label.pack(pady=10, padx=10)
        tk.Label(self, background="#bdb5bf").pack()
        ttk.Label(self, background="#bdb5bf").pack()

        button1 = tk.Button(
            self,
            text="Save",
            width="33",
            height="2",
            command=lambda: controller.save_path_cont()
        )
        button1.pack()


class PageTwo (tk.Frame):
    """ Second page class """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, background="#bdb5bf").pack()
        ttk.Label(self, background="#bdb5bf").pack()
        tk.Label(self, background="#bdb5bf").pack()

        label = tk.Label(self, text="File created!!!",
                         font=LARGE_FONT,
                         bg="grey",
                         width="330",
                         height="2",
                         fg="white",
                         relief="groove",
                         anchor="center")

        label.pack(pady=10, padx=10)


app = xmlPages()

app.mainloop()

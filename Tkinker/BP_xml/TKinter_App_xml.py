from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
# import matplotlib
# from matplotlib import style
import os

import csv
from xml_loop import ParsingXml


LARGE_FONT = ("Verdana", 15, "bold")
# style.use("ggplot")
Label_dispaly = "This application is retreving information regarding:\n processes, objects and variables."


class xmlPages (tk.Tk):
    """ The main class is inheriting from tk.TK class  """
    # Class variable
    width_of_window = 600
    height_of_window = 200

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__ (self, *args, **kwargs)
        """  """
        self.app_data = {
            "file_path": tk.StringVar(),
            "process_subprocess_list": [],
            "save_file_path": "",
            "csv_file_header": ['process_name', 'subsheet_name', 'stage_type',
                                'user_action_name',
                                'BP_action_name', 'object_typ',
                                'input_name', 'input_type', 'input_store_in', 'input_desc',
                                'output_name', 'output_type', 'output_store_in', 'output_desc',
                                'variable_name', 'variable_type',
                                'exception_name', 'exception_type', 'exception_details'
                                ]
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
        x_coordinate = ((int(self.winfo_screenwidth()) / 2)
                        - (int(self.width_of_window) / 2))
        y_coordiante = ((int(self.winfo_screenheight()) / 2)
                        - (int(self.height_of_window) / 2))

        print(
            "%dx%d+%d+%d" % (
                self.width_of_window,
                self.height_of_window,
                x_coordinate, y_coordiante
            )
        )
        self.geometry(
            "%dx%d+%d+%d" % (
                self.width_of_window,
                self.height_of_window,
                x_coordinate, y_coordiante
            )
        )
        # self.geometry(f"{self.height_of_window}x{self.width_of_window}+{str(x_coordinate)}+{str(y_coordiante)}")

    def open_file(self):
        file_path = filedialog.askopenfilename(initialdir="/",
                                                   title="Select file",
                                                   filetypes=(
                                                   ("bprelease files", "*.bprelease"),
                                                   ("all files", "*.*")))
        if file_path == "":
            msg_box = messagebox.askquestion("No path selected",
                                             "Are you sure you do not want to choose any path ?",
                                             icon="warning")
            if msg_box == "yes":
                exit()
            else:
                messagebox.showinfo("return", "You will now return to the application screen")
                self.open_file()
        # Assign file path to app_data dic
        self.app_data["file_path"] = self.filepath
        # Display page one frame
        self.show_frame(PageOne)

    def create_csv(self, path, list_header, list_to_save):
        # writing to csv file

        with open(path, 'w', newline='') as csv_file:
            # creating a csv dict writer object
            writer = csv.DictWriter(csv_file, fieldnames=list_header)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            writer.writerows (list_to_save)

    def save_path_cont(self):
        save_file_path = filedialog.asksaveasfilename(initialdir="/",
                                                      title="Select file",
                                                      filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if save_file_path[-4:] == ".csv":
            self.app_data["save_file_path"] = save_file_path
            print(self.app_data["save_file_path"])
            self.parse_bprelease_main(self.app_data["file_path"])
        elif save_file_path == "":
            msg_box = messagebox.askquestion("No path selected",
                                             "Are you sure you do not want to choose any path ?",
                                             icon="warning")
            if msg_box == "yes":
                exit()
            else:
                messagebox.showinfo("return", "You will now return to the application screen")
                self.save_path_cont()
        else:
            # Add extension to the end of file
            self.app_data["save_file_path"] = save_file_path + ".csv"
            self.parse_bprelease_main(self.app_data["file_path"])

        # print
        print(self.app_data["process_subprocess_list"])
        # Create csv file
        self.create_csv(self.app_data["save_file_path"],
                        self.app_data["csv_file_header"],
                        self.app_data["process_subprocess_list"])
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
            command=lambda: controller.open_file()
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

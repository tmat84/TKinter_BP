from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
# import matplotlib
# from matplotlib import style
import os
import xml.etree.ElementTree as ET
import csv

LARGE_FONT= ("Verdana",15,"bold")
# style.use("ggplot")
Label_dispaly = "This application is retreving information regarding:\n processes, objects and variables."


class xmlPages(tk.Tk):
    """ Main class  """
    # Class variable
    width_of_window = 600
    height_of_window = 200

    def __init__(self, *args,**kwargs):
        tk.Tk.__init__(self, *args,**kwargs)
        """  """
        self.app_data ={
            "file_path":tk.StringVar(),
            "process_subprocess_list":[],
            "save_file_path":"",
            "csv_file_header":['process_name','subsheet_name', 'stage_type',
                'user_action_name',
                'BP_action_name', 'object_typ',
                'input_name','input_type','input_store_in','input_desc',
                'output_name','output_type','output_store_in','output_desc',
                'variable_name', 'variable_type',
                'exception_name','exception_type','exception_details'
                ]
            }

        #Set window title
        tk.Tk.wm_title(self,"Manipulation Tool v 1.0")
        #Set geomatry
        self.set_geometry()



        #create container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne,PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid (row=0, column=0, sticky="nsew")
            frame.configure(background="#bdb5bf")

        # frame = StartPage(container, self)
        # self.frames[StartPage]=frame

        self.show_frame(StartPage)
        print(self.frames)

    def show_frame(self, count):
        """ show TKinter frame"""
        frame =  self.frames[count]
        frame.tkraise()

    def set_geometry(self):
        """ Set TKinter window in the middle of the screen """
        x_coordinate = ((int(self.winfo_screenwidth())/2)
                        - (int(self.width_of_window)/2))
        y_coordiante = ((int(self.winfo_screenheight())/2)
                        - (int(self.height_of_window)/2))

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
        #self.geometry(f"{self.height_of_window}x{self.width_of_window}+{str(x_coordinate)}+{str(y_coordiante)}")

    def open_file(self):
        self.filepath = filedialog.askopenfilename(initialdir = "/",
            title = "Select file",
            filetypes = (("bprelease files","*.bprelease"),("all files","*.*")))
        if self.filepath == "":
            msg_Box = messagebox.askquestion ("No path selected","Are you sure you do not want to choose any path ?", icon = "warning")
            if msg_Box == "yes":
                exit()
            else:
                messagebox.showinfo("return","You will now return to the application screen")
                self.open_file()
        #Assign filepath to app_data dic
        self.app_data["file_path"] = self.filepath
        # Display pageone frame
        self.show_frame(PageOne)

    def create_csv(self,path,list_header,list_to_save):
        # writing to csv file

        with open(path, 'w',newline='') as csvfile:

        # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames = list_header)

        # writing headers (field names)
            writer.writeheader()

        # writing data rows
            writer.writerows(list_to_save)


    def save_path_cont(self):
        self.save_filepath = filedialog.asksaveasfilename(initialdir = "/",
            title = "Select file",
            filetypes = (("csv files","*.csv"),("all files","*.*")))
        if self.save_filepath[-4:]==".csv":
            self.app_data["save_file_path"] = self.save_filepath
            print(self.app_data["save_file_path"])
            self.parse_bprelease_main(self.app_data["file_path"])
        elif self.save_filepath == "":
            msg_Box = messagebox.askquestion ("No path selected","Are you sure you do not want to choose any path ?", icon = "warning")
            if msg_Box == "yes":
                exit()
            else:
                messagebox.showinfo("return","You will now return to the application screen")
                self.save_path_cont()
        else:
            #Add extenstion to the end of file
            self.app_data["save_file_path"] = self.save_filepath +".csv"
            self.parse_bprelease_main(self.app_data["file_path"])

        #print
        print(self.app_data["process_subprocess_list"])
         #Create csv file
        self.create_csv(self.app_data["save_file_path"],
            self.app_data["csv_file_header"],
            self.app_data["process_subprocess_list"])
        #dsiaply frame Pagetwo
        self.show_frame(PageTwo)

    def parse_bprelease_main(self,full_path):
        tree = ET.parse(full_path)

        root=tree.getroot()



        temp_list_output = []

        for process in root.iter("{http://www.blueprism.co.uk/product/process}process"):
            #print(process.tag,process.attrib)
            process_name = process.attrib["name"]


            subsheet_dic = dict()

            for subsheet in root.findall(".//{http://www.blueprism.co.uk/product/process}subsheet"):
                for child in subsheet:
                    if (child.tag == "{http://www.blueprism.co.uk/product/process}name"):
                        subsheet_dic.update({subsheet.attrib['subsheetid']:child.text})

            for action in root.findall(".//{http://www.blueprism.co.uk/product/process}stage"):

                # Stage with attribute Data in type are data item
                # Stage with attribute SubSheetInfo in type are subpage
                if action.attrib['type'] == 'Action':
                    #create dictonary

                    object_BP = {
                            'process_name':"",
                            'subsheet_name':"",
                            'BP_action_name':"",
                            'object_typ':"",
                        }

                    object_BP["process_name"] = process_name

                    inputs_BP ={}
                    outputs_BP ={}

                    #set action name
                    action_name = action.attrib['name']

                    for res in action:
                        if (res.tag == '{http://www.blueprism.co.uk/product/process}resource'):
                            object_BP["BP_action_name"] = res.attrib["action"]
                            object_BP["object_typ"] = res.attrib["object"]

                    for child in action:

                        if 'stage_type' and "user_action_name" in object_BP.keys():
                            pass

                        else:
                            object_BP['stage_type'] = "action"
                            object_BP["user_action_name"] = action_name



                        if (child.tag == '{http://www.blueprism.co.uk/product/process}subsheetid'):
                            object_BP["subsheet_name"]=subsheet_dic[child.text]

                        elif child.tag == '{http://www.blueprism.co.uk/product/process}inputs':

                            for index,subchild in enumerate(child):

                                if index == 0:
                                    object_BP["input_name"] = subchild.attrib["name"]
                                    object_BP["input_type"] = subchild.attrib["type"]
                                    object_BP["input_store_in"] = subchild.get("expr")
                                    object_BP["input_desc"] = subchild.get("narrative")
                                    temp_list_output.append(object_BP)
                                    object_BP = object_BP.copy()
                                    object_BP["input_name"] = ""
                                    object_BP["input_type"] = ""
                                    object_BP["input_store_in"] = ""
                                    object_BP["input_desc"] = ""

                                else:
                                    inputs_BP["input_name"+str(index)] = subchild.attrib["name"]
                                    inputs_BP["input_type"+str(index)] = subchild.attrib["type"]
                                    inputs_BP["input_store_in"+str(index)] = subchild.get("expr")
                                    inputs_BP["input_desc"+str(index)] = subchild.get("narrative")

                        elif child.tag == '{http://www.blueprism.co.uk/product/process}outputs':
                            for index,subchild in enumerate(child):
                                if index == 0:
                                    object_BP["output_name"] = subchild.get("name")
                                    object_BP["output_type"] = subchild.attrib["type"]
                                    object_BP["output_store_in"] = subchild.get("stage")
                                    object_BP["output_desc"] = subchild.get("narrative")
                                    temp_list_output.append(object_BP)
                                    object_BP = object_BP.copy()
                                    object_BP["output_name"] = ""
                                    object_BP["output_type"] = ""
                                    object_BP["output_store_in"] = ""
                                    object_BP["output_desc"] = ""

                                else:
                                    outputs_BP["output_name"+str(index)] = subchild.attrib["name"]
                                    outputs_BP["output_type"+str(index)] = subchild.attrib["type"]
                                    outputs_BP["output_store_in"+str(index)] = subchild.get("stage")
                                    outputs_BP["output_desc"+str(index)] = subchild.get("narrative")



                        if inputs_BP:

                            index = 0

                            for key,value in inputs_BP.items():
                                if key.startswith("input_name"):
                                    object_BP["input_name"] = value
                                elif key.startswith("input_type"):
                                    object_BP["input_type"] = value
                                elif key.startswith("input_store_in"):
                                    object_BP["input_store_in"] = value
                                elif key.startswith("input_desc"):
                                    object_BP["input_desc"] = value
                                index+=1
                                if index%4 == 0 and index is not 0:
                                    temp_dict = object_BP.copy()
                                    object_BP["input_name"] = ""
                                    object_BP["input_type"] = ""
                                    object_BP["input_store_in"] = ""
                                    object_BP["input_desc"] = ""
                                    temp_list_output.append (temp_dict)
                        inputs_BP.clear()

                        if outputs_BP:
                            index = 0
                            for key,value in outputs_BP.items():
                                if key.startswith("output_name"):
                                    object_BP["output_name"] = value
                                elif key.startswith("output_type"):
                                    object_BP["output_type"] = value
                                elif key.startswith("output_store_in"):
                                    object_BP["output_store_in"] = value
                                elif key.startswith("output_desc"):
                                    object_BP["output_desc"] = value
                                index+=1
                                if index%4 == 0 and index is not 0:
                                    temp_dict = object_BP.copy()
                                    object_BP["output_name"] = ""
                                    object_BP["output_type"] = ""
                                    object_BP["output_store_in"] = ""
                                    object_BP["output_desc"] = ""
                                    temp_list_output.append (temp_dict)
                        outputs_BP.clear()

                # elif (action.attrib['type'] == 'Data' or
                #         action.attrib['type'] == 'Collection') :
                #     #variables

                #     dic_varaibles = {
                #         'process_name':"",
                #         'subsheet_name':"",
                #         'stage_type':"",
                #         'variable_name':"",
                #         'variable_type':""
                #         }

                #     dic_varaibles["process_name"] = process_name

                #     if action.attrib['type'] == 'Data':
                #         dic_varaibles['stage_type'] = "data item"
                #     elif action.attrib['type'] == 'Collection':
                #         dic_varaibles['stage_type'] = "collection"

                #     dic_varaibles['variable_name'] = action.attrib["name"]


                #     for child in action:

                #         if child.tag == ('{http://www.blueprism.co.uk/product/process}subsheetid' and
                #                 len(child.text)>0):
                #             dic_varaibles["subsheet_name"] = subsheet_dic[child.text]
                #         elif child.tag == '{http://www.blueprism.co.uk/product/process}datatype':
                #             dic_varaibles['variable_type'] = child.text

                #     temp_list_output.append(dic_varaibles)
                elif action.attrib['type'] == 'Exception':

                    dic_exception ={
                        'process_name':"",
                        'subsheet_name':"",
                        'stage_type':"",
                        'exception_name':"",
                        'exception_type':"",
                        'exception_details':""
                        }

                    dic_exception["process_name"] = process_name
                    dic_exception["stage_type"] = "Exception"

                    dic_exception['exception_name'] = action.attrib["name"]

                    for child in action:
                        if child.tag == ('{http://www.blueprism.co.uk/product/process}subsheetid'):
                            dic_exception["subsheet_name"] = subsheet_dic[child.text]
                        elif child.tag == "{http://www.blueprism.co.uk/product/process}exception":
                            dic_exception["exception_type"] = child.get("type")
                            dic_exception["exception_details"] = child.get("detail")
                    temp_list_output.append(dic_exception)


        # Assign list to class attribute dict app_data
        self.app_data["process_subprocess_list"] = temp_list_output

class StartPage(tk.Frame):


    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller


        label = tk.Label(self,
             text=Label_dispaly,
             bg="grey",
             font=LARGE_FONT,
             width="330",
             height = "2",
             fg="white",
             relief="groove",
             anchor="center"
             )

        label.pack()
        tk.Label(self,background="#bdb5bf").pack()
        ttk.Label(self,background="#bdb5bf").pack()
        button1 = tk.Button(
            self,
            text="Open file",
            width="33",
            height = "2",
            command=lambda: controller.open_file()
            )
        button1.pack()



class PageOne(tk.Frame):
    """ First page class """
    def __init__(self,parent, controller):

        tk.Frame.__init__(self,parent)


        label = tk.Label(self, text="Successful load!!\nChoose the save files location.",
                        font=LARGE_FONT,
                        bg="grey",
                        width="330",
                        height = "2",
                        fg="white",
                        relief="groove",
                        anchor="center")

        label.pack(pady=10,padx=10)
        tk.Label(self,background="#bdb5bf").pack()
        ttk.Label(self,background="#bdb5bf").pack()

        button1 = tk.Button(
            self,
            text="Save",
            width="33",
            height = "2",
            command=lambda: controller.save_path_cont()
            )
        button1.pack()

class PageTwo(tk.Frame):
    """ Second page class """
    def __init__(self,parent, controller):

        tk.Frame.__init__(self,parent)

        tk.Label(self,background="#bdb5bf").pack()
        ttk.Label(self,background="#bdb5bf").pack()
        tk.Label(self,background="#bdb5bf").pack()


        label = tk.Label(self, text="File created!!!",
                        font=LARGE_FONT,
                        bg="grey",
                        width="330",
                        height = "2",
                        fg="white",
                        relief="groove",
                        anchor="center")

        label.pack(pady=10,padx=10)


app = xmlPages()

app.mainloop()


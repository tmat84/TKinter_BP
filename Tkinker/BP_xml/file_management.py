import csv
import os
from tkinter import filedialog
from tkinter import messagebox


def open_file_dialog_box():
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
            exit ()
        else:
            messagebox.showinfo("return", "You will now return to the application screen")
            open_file_dialog_box()
    return file_path


class SaveOutputToCsv:
    def __init__(self, list_to_save):
        self.list_header = ['process_name', 'subsheet_name', 'stage_type',
                            'user_action_name',
                            'BP_action_name', 'object_typ',
                            'input_name', 'input_type', 'input_store_in', 'input_desc',
                            'output_name', 'output_type', 'output_store_in', 'output_desc',
                            'variable_name', 'variable_type',
                            'exception_name', 'exception_type', 'exception_details'
                            ]
        self.list_to_save = list_to_save
        self.path_to_save = ""

    def save_path_cont(self):
        save_file_path = filedialog.asksaveasfilename(initialdir="/",
                                                      title="Select file",
                                                      filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if save_file_path[-4:] == ".csv":
            self.path_to_save = save_file_path
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
            self.path_to_save = save_file_path + ".csv"

    def create_csv(self):
        # writing to csv file

        try:

            with open(self.path_to_save, 'w', newline='') as csv_file:
                # creating a csv dict writer object
                writer = csv.DictWriter(csv_file, fieldnames=self.list_header)

                # writing headers (field names)
                writer.writeheader()

                # writing data rows
                writer.writerows(self.list_to_save)

        except OSError:
            msg = "File " + os.path.basename(self.path_to_save) + "is currently opened"
            print(msg)
            # Handling unexpected exceptions, by showing the associated error message
        except Exception as object_exception:
            print(f"Unexpected error: {object_exception}")






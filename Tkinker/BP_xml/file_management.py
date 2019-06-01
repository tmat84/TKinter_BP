import csv
import os
from tkinter import filedialog
from tkinter import messagebox


class SaveOutputToCsv:
    def __init__(self, path, list_header, list_to_save):
        self.path = path
        self.list_header = list_header
        self.list_to_save = list_to_save

    def open_file_dialog_box(self):
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
                self.open_file_dialog_box()
        return file_path

    def create_csv(self):
        # writing to csv file

        try:

            with open(self.path, 'w', newline='') as csv_file:
                # creating a csv dict writer object
                writer = csv.DictWriter(csv_file, fieldnames=self.list_header)

                # writing headers (field names)
                writer.writeheader()

                # writing data rows
                writer.writerows(self.list_to_save)

        except OSError:
            msg = "File " + os.path.basename(self.path) + "is currently opened"
            print(msg)
            # Handling unexpected exceptions, by showing the associated error message
        except Exception as object_exception:
            print(f"Unexpected error: {object_exception}")






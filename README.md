
# Retrieving Data from Blue Prism packages using TKinter and xml.etree.ElementTree

The application has a really simple interface, which is only one button on each window :)

1. After clicking the **Open file** button the method **open_file_and_parse_xml()** is being invoked.
    1.  In the begining the filedialog box appears.Thanks to **open_file_dialog_box()**, The method returns the file path.
    The file need to have n extension **.bprelease**.
    1. Next, the **ParsingXml.parse_bp_releases** method is invoked. 
    The method stores the output in a dictionary app_data under key **process_subprocess_list**
    1. After the method is executed a new frame **show_frame(PageOne)** is displayed 
1. The new window appears with **Save** button.
    1. After clikcing the button the new instance of class **SaveOutputToCsv** is created 
    and  assign this object to the local variable **output_file**
    1. Next, run the **save_path_cont** method which returns the **save_file_path** where the output file will be saved.
    1. Finally, run the **create_csv** method. The csv file is created under desire path.
    
The output file is consisting of fields: 

Fields |
------------ |
ID |
process_name |
subsheet_name |
stage_type |
user_action_name |
BP_action_name |
object_typ |
input_name |
input_type |
input_store_in |
input_desc |
output_name |
output_type |
output_store_in |
output_desc |
variable_name |	
variable_type	|
exception_name |	
exception_type |	
exception_details |







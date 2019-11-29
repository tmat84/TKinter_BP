import xml.etree.ElementTree as ET


class ParsingXml:
    """ Class for parsing Blue Prism xml """

    @staticmethod
    def parse_bp_releases(full_path):
        tree = ET.parse(full_path)
        # Add settings file Move some logic to file_management

        root = tree.getroot()

        temp_list_output = []
        #
        blue_prism_path_xml = "{http://www.blueprism.co.uk/product/process}"

        for process in root.iter(blue_prism_path_xml+"process"):
            # print(process.tag,process.attrib)
            process_name = process.attrib["name"]

            sub_sheet_dic = dict()
            # Loop through {http://www.blueprism.co.uk/product/process}subsheetid
            for sub_sheet in root.findall(".//"+blue_prism_path_xml+"subsheet"):
                for child in sub_sheet:
                    if child.tag == blue_prism_path_xml+"name":
                        # Update dictionary sub_sheet_dic with the specific key-value pairs
                        sub_sheet_dic.update({sub_sheet.attrib['subsheetid']: child.text})

            for action in root.findall(".//"+blue_prism_path_xml+"stage"):

                # Stage with attribute Data in type are data item
                # Stage with attribute SubSheetInfo in type are subpage
                if action.attrib['type'] == 'Action':
                    # create dictionary

                    blue_prism_object_details = dict(process_name="",
                                                     subsheet_name="",
                                                     BP_action_name="",
                                                     object_typ="")

                    blue_prism_object_details["process_name"] = process_name

                    blue_prism_action_inputs_variables = {}
                    blue_prism_action_outputs_variables = {}

                    # set action name
                    action_name = action.attrib['name']

                    for res in action:
                        if res.tag == blue_prism_path_xml+'resource':
                            blue_prism_object_details["BP_action_name"] = res.attrib["action"]
                            blue_prism_object_details["object_typ"] = res.attrib["object"]

                    for child in action:

                        if 'stage_type' and "user_action_name" in blue_prism_object_details.keys():
                            pass

                        else:
                            blue_prism_object_details['stage_type'] = "action"
                            blue_prism_object_details["user_action_name"] = action_name

                        if child.tag == blue_prism_path_xml+'subsheetid':
                            blue_prism_object_details["subsheet_name"] = sub_sheet_dic[child.text]

                        elif child.tag == blue_prism_path_xml+'inputs':

                            for index, sub_child in enumerate(child):

                                if index == 0:
                                    blue_prism_object_details["input_name"] = sub_child.attrib["name"]
                                    blue_prism_object_details["input_type"] = sub_child.attrib["type"]
                                    blue_prism_object_details["input_store_in"] = sub_child.get("expr")
                                    blue_prism_object_details["input_desc"] = sub_child.get("narrative")
                                    temp_list_output.append(blue_prism_object_details)
                                    blue_prism_object_details = blue_prism_object_details.copy()
                                    blue_prism_object_details["input_name"] = ""
                                    blue_prism_object_details["input_type"] = ""
                                    blue_prism_object_details["input_store_in"] = ""
                                    blue_prism_object_details["input_desc"] = ""

                                else:
                                    blue_prism_action_inputs_variables["input_name" + str(index)] = sub_child.attrib["name"]
                                    blue_prism_action_inputs_variables["input_type" + str(index)] = sub_child.attrib["type"]
                                    blue_prism_action_inputs_variables["input_store_in" + str(index)] = sub_child.get("expr")
                                    blue_prism_action_inputs_variables["input_desc" + str(index)] = sub_child.get("narrative")

                        elif child.tag == blue_prism_path_xml+'outputs':
                            for index, sub_child in enumerate(child):
                                if index == 0:
                                    blue_prism_object_details["output_name"] = sub_child.get("name")
                                    blue_prism_object_details["output_type"] = sub_child.attrib["type"]
                                    blue_prism_object_details["output_store_in"] = sub_child.get("stage")
                                    blue_prism_object_details["output_desc"] = sub_child.get("narrative")
                                    temp_list_output.append(blue_prism_object_details)
                                    blue_prism_object_details = blue_prism_object_details.copy()
                                    blue_prism_object_details["output_name"] = ""
                                    blue_prism_object_details["output_type"] = ""
                                    blue_prism_object_details["output_store_in"] = ""
                                    blue_prism_object_details["output_desc"] = ""

                                else:
                                    blue_prism_action_outputs_variables["output_name" + str(index)] = sub_child.attrib["name"]
                                    blue_prism_action_outputs_variables["output_type" + str(index)] = sub_child.attrib["type"]
                                    blue_prism_action_outputs_variables["output_store_in" + str(index)] = sub_child.get("stage")
                                    blue_prism_action_outputs_variables["output_desc" + str(index)] = sub_child.get("narrative")

                        if blue_prism_action_inputs_variables:

                            index = 0

                            for key, value in blue_prism_action_inputs_variables.items():
                                if key.startswith("input_name"):
                                    blue_prism_object_details["input_name"] = value
                                elif key.startswith("input_type"):
                                    blue_prism_object_details["input_type"] = value
                                elif key.startswith("input_store_in"):
                                    blue_prism_object_details["input_store_in"] = value
                                elif key.startswith("input_desc"):
                                    blue_prism_object_details["input_desc"] = value
                                index += 1
                                if index % 4 == 0 and index is not 0:
                                    temp_dict = blue_prism_object_details.copy()
                                    blue_prism_object_details["input_name"] = ""
                                    blue_prism_object_details["input_type"] = ""
                                    blue_prism_object_details["input_store_in"] = ""
                                    blue_prism_object_details["input_desc"] = ""
                                    temp_list_output.append(temp_dict)
                        blue_prism_action_inputs_variables.clear()

                        if blue_prism_action_outputs_variables:
                            index = 0
                            for key, value in blue_prism_action_outputs_variables.items():
                                if key.startswith("output_name"):
                                    blue_prism_object_details["output_name"] = value
                                elif key.startswith("output_type"):
                                    blue_prism_object_details["output_type"] = value
                                elif key.startswith("output_store_in"):
                                    blue_prism_object_details["output_store_in"] = value
                                elif key.startswith("output_desc"):
                                    blue_prism_object_details["output_desc"] = value
                                index += 1
                                if index % 4 == 0 and index is not 0:
                                    temp_dict = blue_prism_object_details.copy()
                                    blue_prism_object_details["output_name"] = ""
                                    blue_prism_object_details["output_type"] = ""
                                    blue_prism_object_details["output_store_in"] = ""
                                    blue_prism_object_details["output_desc"] = ""
                                    temp_list_output.append(temp_dict)
                        blue_prism_action_outputs_variables.clear()

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
                #             dic_varaibles["subsheet_name"] = sub_sheet_dic[child.text]
                #         elif child.tag == '{http://www.blueprism.co.uk/product/process}datatype':
                #             dic_varaibles['variable_type'] = child.text

                #     temp_list_output.append(dic_varaibles)
                elif action.attrib['type'] == 'Exception':

                    dic_exception = dict(process_name="",
                                         subsheet_name="",
                                         stage_type="",
                                         exception_name="",
                                         exception_type="",
                                         exception_details="")
                    dic_exception["process_name"]= process_name
                    dic_exception["stage_type"] = "Exception"
                    dic_exception['exception_name'] = action.attrib["name"]

                    for child in action:
                        if child.tag == blue_prism_path_xml+'subsheetid':
                            dic_exception["subsheet_name"] = sub_sheet_dic[child.text]
                        elif child.tag == blue_prism_path_xml+"exception":
                            dic_exception["exception_type"] = child.get("type")
                            dic_exception["exception_details"] = child.get("detail")
                    temp_list_output.append (dic_exception)

        # Assign list to class attribute dict app_data
        return temp_list_output



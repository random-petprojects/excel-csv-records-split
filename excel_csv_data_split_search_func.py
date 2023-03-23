# Importing all the necessary packages
import PySimpleGUI as sg
import datetime
import pandas as pd
import os
import logging
# import keyword
# keywords = keyword.kwlist

logging.basicConfig(filename="file_split_log.txt",level=logging.DEBUG,format="%(asctime)s-%(levelname)s-%(message)s")
# logging.disable(logging.CRITICAL)
# Script start time
search_list = []
search_set = set()
logging.info("Program Execution - started")
start_time = datetime.datetime.now()

form = sg.FlexForm('File split script')


layout = [
            [sg.Text('Please upload file & enter the remaining details and click "submit" button to execute the script')],
            [sg.Text('Input File', size=(10, 1), auto_size_text=False, justification='left')],
            [sg.InputText('Please upload either the CSV/XLSX input file'), sg.FileBrowse(key="-Input_Values-")],
            [sg.Text('Output File', size=(10, 1), auto_size_text=False, justification='left')],
            [sg.InputText('Please choose the output folder'), sg.FolderBrowse(key="-Output_Values-")],
            [sg.Text('No of records per file'), sg.InputText(key = '-no_of_records-'), sg.Text('in multiples of 1000')],
            [sg.Text(' ',size=(5, 1))],
            [sg.InputText('',key = '-Search_Box-', enable_events=True),sg.Button('Merge_Search_Fields_And_Listbox_Selected_Fields')],
            [sg.Text('Select the Required columns')],
            [sg.Listbox(values = (),select_mode= 'multiple', size=(30, 30), key='-ListBox-', enable_events=True),  sg.Button("Populate Columns"), sg.Text('Double click the button',font=('Arial', 13, 'bold')) ],
            [sg.Submit(), sg.Cancel()]
         ]

window = form.Layout(layout)
event, values = window.read()

while True:
    event, values = window.read()
    print(event, values)
    file_path = values[0]

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if int(values["-no_of_records-"]) % 1000 != 0: # no od rec = 65 ValueError: invalid literal for int() with base 10: ''
        window['-no_of_records-']('')
        logging.error("No of records per file should be in multiple of 1000, Please re-enter the value")
        sg.Popup('No of records per file should be in multiple of 1000, Please re-enter the value', keep_on_top=True)
        raise ValueError("No of records per file should be in multiple of 1000, i.e 1000, 2000, 3000, 6000, 10000 etc..., Please re-run the script with valid value")

    if event == 'Submit':
        break

    if event == 'Populate Columns':
        try:
            file_type = file_path.split(".")[1]
        except IndexError:
            print("Please choose the input file")
            logging.error("User didn't choosed input file")
            raise IndexError("Please choose the input file - By clicking on 'Browse' button")
        print(file_type)
        if file_type == "xlsx":
            df_full_content = pd.read_excel(file_path)
        elif file_type == "csv":
            df_full_content = pd.read_csv(file_path, encoding = "ISO-8859-1")
        else:
            print("Only CSV/XLSX format files can be processed, Please upload correct file types")
            logging.error("User uploaded file of different format other than CSV/XLSX")

        column_names = list(df_full_content.columns)
        total_records = df_full_content.shape[0]
        print(f"total_records: {total_records}")
        logging.info(f"Total Records in Input file: {total_records}")

        window.Element('-ListBox-').update(values= column_names)

    if event == '-Search_Box-':
        text = values['-Search_Box-']
        print(text)
        # if text:
        #     search_list = [item for item in keywords if item.startswith(text)]
        if text in column_names:
            print(f"search box columns: {column_names}")
            # search_list.append(text)
            search_set.add(text)

        # print(f"search_list: {search_list}")
        print(f"search_set:{search_set}")

        # window.Element('-ListBox-').update(values= search_list)
        window.Element('-ListBox-').update(values=search_set)



    if event == 'Merge_Search_Fields_And_Listbox_Selected_Fields':
        # window.Element('-ListBox-').update(values= search_set + "Add the listbox active fields- add 1 by 1 to list and add here")
        window.Element('-ListBox-').update(values= list(search_set))


print(f"event : {event}")
print(f"values: {values}")
print(values["-Input_Values-"])
output_folder = values["-Output_Values-"]
print(f"output folder: {output_folder}")

if len(values["-ListBox-"]) == 0:
    values["-ListBox-"] = column_names

print("==" * 10)

if event == "Cancel":
    print("User explicitly Aborted the UI Screen")

file_path = values["-Input_Values-"]
original_file_name = values["-Input_Values-"].split("/")[-1].split('.')[0]
logging.info(f"Input file path: {file_path}")
logging.info(f"Output folder path: {output_folder}")
records_per_file = int(values["-no_of_records-"])
logging.info(f"no. of records per file: {records_per_file}")
columns = values["-ListBox-"]
print(f"Final Columns list : {columns}")
logging.info(f"selected columns: {columns}")

df_full_content = df_full_content[columns]

total_records = df_full_content.shape[0]
print(f"total_records: {total_records}")

for record_no in range(0,total_records,records_per_file):
    print(f"record_no: {record_no}")
    end_pos = record_no + records_per_file

    df_splitted = df_full_content.iloc[record_no:end_pos,:]
    new_file_name = original_file_name + "_" + str(record_no + 1) + "-" + str(end_pos) + "." + file_type
    print(f"output file path: {output_folder + '/' +  new_file_name}")

    if file_type == "xlsx":
        df_splitted.to_excel(os.path.join(output_folder,new_file_name))
        # df_splitted.to_excel(output_folder + "/" + new_file_name)
    else:
        df_splitted.to_csv(os.path.join(output_folder, new_file_name))
        # df_splitted.to_csv( output_folder + "/" + new_file_name)

end_time = datetime.datetime.now()
print(f"executed_duration: {end_time - start_time}" + " (m)seconds")
logging.debug("=********** End of the script **********=")
print("Files Generated successful")














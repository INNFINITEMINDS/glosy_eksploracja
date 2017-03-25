#LIBRARY IMPORT
import pandas as pd
import easygui

#DEFINING CONSTANTS
activities = ["bieganie","brzuszki","chodzenie","jedzenie","komputer","lezenie","pisanie","przysiady","siedzenie","stanie","upadek"]
number_of_subjects = 6;
dataframe_collection = {} #all dataframes representing activities will be stored in dataframe_collection

#CHOOSING MEASUREMENT DIRECTORY
measurement_directory = (easygui.diropenbox()) #you have to choose a path to your measurement catalogue
print('Your directory of measurements is:'); print(measurement_directory)

#READING DATA
for activity in activities:
    subfolder = measurement_directory + "\\" + activity
    for msr_counter in range(1,number_of_subjects + 1):
        path = subfolder + "\\" + str(msr_counter) + "_" + activity + ".csv"
        variable_name = str(msr_counter) + "_" + activity
        dataframe_collection[variable_name] = pd.read_csv(path,
                                    names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'])

#PRINTING EXAMPLE VALUES
print(dataframe_collection.keys()) #these are the keys to your data
print(dataframe_collection['1_pisanie']) #to obtain some data you only have to use a specific key
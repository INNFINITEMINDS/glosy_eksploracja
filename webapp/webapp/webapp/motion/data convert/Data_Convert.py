#LIBRARY IMPORT
import pandas as pd
import numpy as np
import easygui
from decimal import Decimal


#DEFINING CONSTANTS
#activities = ["bieganie","brzuszki","chodzenie","jedzenie","komputer","lezenie","pisanie","przysiady","siedzenie","stanie","upadek"]
activities = ["bieganie", "lezenie"]
number_of_subjects = 6;
dataframe_collection = {} #all dataframes representing activities will be stored in dataframe_collection

#CHOOSING MEASUREMENT DIRECTORY
measurement_directory = (easygui.diropenbox()) #you have to choose a path to your measurement catalogue
print('Your directory of measurements is:'); print(measurement_directory)

#READING DATA
for activity in activities:
    subfolder = measurement_directory + "/" + activity
    # Pliki do zapisu muszą być puste! Jesli plików w danym folderze nie będzie to zostaną automatycznie utworzone
    writePathActivitiesLabels = measurement_directory + "/activities_leabels.csv"
    writePathDataFeatures = measurement_directory + "/data_features.csv"

    #ustawianie label'ki aktywnosci jako indeksu tabeli aktywności (dlatego tez numerują sie od 0)
    ActivityLabel = (activities.index(activity))

    for msr_counter in range(1,number_of_subjects + 1):
        path = subfolder + "/" + str(msr_counter) + "_" + activity + ".csv"
        print(path)
        variable_name = str(msr_counter) + "_" + activity
        #czytanie tylko interesujących nas kolumn
        DataX = pd.read_csv(path,
                            names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'],
                            usecols=[1])

        DataY = pd.read_csv(path,
                            names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'],
                            usecols=[2])

        DataZ = pd.read_csv(path,
                            names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'],
                            usecols=[3])

        frame_lenght = 30; #USTALANIE SZEROKOŚCI OKNA
        data_lenght =len(DataX.index);
        frames_count = np.math.floor(data_lenght/frame_lenght);
        bottom_sample =0;
        top_sample = frame_lenght;

        DataLabel = pd.Series([ActivityLabel] * frame_lenght * frames_count)
        with open(writePathActivitiesLabels, 'a') as destinationFile:
            DataLabel.to_csv(destinationFile, header=False, index=False, sep=' ')
        print("Labels for current file added to output file")

        for step in range(0, frames_count):
            bottom_sample += frame_lenght;
            top_sample += frame_lenght;
            frameX = DataX[bottom_sample:top_sample];
            frameY = DataY[bottom_sample:top_sample];
            frameZ = DataZ[bottom_sample:top_sample];

            # print("mean")
            meanX = pd.concat([frameX.mean()] * frame_lenght)
            meanY = pd.concat([frameY.mean()] * frame_lenght)
            meanZ = pd.concat([frameZ.mean()] * frame_lenght)
            # print("max")
            maxX = pd.concat([frameX.max()] * frame_lenght)
            maxY = pd.concat([frameY.max()] * frame_lenght)
            maxZ = pd.concat([frameZ.max()] * frame_lenght)
            # print("min")
            minX = pd.concat([frameX.min()] * frame_lenght)
            minY = pd.concat([frameY.min()] * frame_lenght)
            minZ = pd.concat([frameZ.min()] * frame_lenght)
            # print("power")
            powerX = pd.concat([frameX.pow(2).sum()] * frame_lenght)
            powerY = pd.concat([frameY.pow(2).sum()] * frame_lenght)
            powerZ = pd.concat([frameZ.pow(2).sum()] * frame_lenght)
            # print("std")
            stdX = pd.concat([frameX.std()] * frame_lenght)
            stdY = pd.concat([frameY.std()] * frame_lenght)
            stdZ = pd.concat([frameZ.std()] * frame_lenght)

            DataFeatures = pd.DataFrame({'meanX': meanX.values,
                                         'meanY': meanY.values,
                                         'meanZ': meanZ.values,
                                         'maxX': maxX.values,
                                         'maxY': maxY.values,
                                         'maxZ': maxZ.values,
                                         'minX': minX.values,
                                         'minY': minY.values,
                                         'minZ': minZ.values,
                                         'powerX': powerX.values,
                                         'powerY': powerY.values,
                                         'powerZ': powerZ.values,
                                         'stdX': stdX.values,
                                         'stdY': stdY.values,
                                         'stdZ': stdZ.values,
                                         }).round(3)

            with open(writePathDataFeatures, 'a') as destinationFile:
                DataFeatures.to_csv(destinationFile, header=False, index=False, sep=' ')


        #   Kolejność kolumn w pliku
        #   maxX maxY maxZ meanX meanY meanZ minX minY minZ powerX powerY powerZ stdX stdY stdZ

        print("DataFeatures for current file added to output file")
print("Done")

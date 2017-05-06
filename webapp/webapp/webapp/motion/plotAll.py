import pandas as pd
import matplotlib.pyplot as plt
import os

measurement_directory = "measurements"

for root, dirs, files in os.walk(measurement_directory):
    for file in files:
        if file.endswith(".csv"):
            print("Processing file: " + file + "...", end="\t")
            dataframe = pd.read_csv(os.path.join(root, file),
                                    names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'])

            print("Saving figure...", end="\t")
            accel_only = dataframe[['Time', 'Acc X', 'Acc Y', 'Acc Z']]
            plot = accel_only.plot(title=file.split(".")[0])
            plot.figure.savefig(measurement_directory + "\\_photos\\" + file.split(".")[0])
            plt.close('all')

            print("\t Done!")

print("\n")

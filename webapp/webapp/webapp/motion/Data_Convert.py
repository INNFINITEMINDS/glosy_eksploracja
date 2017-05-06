import pandas as pd
import numpy as np


class TraitExtractor(object):
    activities = ["bieganie", "brzuszki", "chodzenie", "jedzenie", "komputer", "lezenie",
                  "pisanie", "przysiady", "siedzenie", "stanie", "upadek"]
    number_of_subjects = 6
    dataframe_collection = {}  # all dataframes representing activities will be stored in dataframe_collection

    traits = []
    labels = []
    test_traits = []

    def __init__(self, measurement_directory, test_file):
        self.measurement_directory = measurement_directory
        self.test_file = test_file
        self.extract_traits()
        self.extract_traits_from_file()

    def get_traits(self):
        return self.traits

    def get_test_traits(self):
        return self.test_traits

    def get_labels(self):
        return np.array(self.labels)

    def extract_traits(self):
        for activity in self.activities:
            subfolder = self.measurement_directory + "/" + activity

            # ustawianie label'ki aktywnosci jako indeksu tabeli aktywności (dlatego tez numerują sie od 0)
            ActivityLabel = (self.activities.index(activity))

            for msr_counter in range(1, self.number_of_subjects):
                path = subfolder + "/" + str(msr_counter) + "_" + activity + ".csv"
                # czytanie tylko interesujących nas kolumn
                DataAll = pd.read_csv(path,
                                      names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'],
                                      usecols=[1, 2, 3])

                DataX = DataAll[[0]]
                DataY = DataAll[[1]]
                DataZ = DataAll[[2]]

                frame_length = 250
                data_length = len(DataX.index)
                frames_count = np.math.floor(data_length / frame_length) - 1
                bottom_sample = 0
                top_sample = frame_length

                data_labels = [ActivityLabel] * frames_count

                self.labels.extend(data_labels)


                for step in range(0, frames_count):
                    bottom_sample += frame_length
                    top_sample += frame_length
                    frameX = DataX[bottom_sample:top_sample]
                    frameY = DataY[bottom_sample:top_sample]
                    frameZ = DataZ[bottom_sample:top_sample]

                    data_features = self.calculate_traits(frameX, frameY, frameZ, frame_length)

                    self.traits.append(data_features)




                # Kolejność kolumn w pliku
                #   maxX maxY maxZ meanX meanY meanZ minX minY minZ powerX powerY powerZ stdX stdY stdZ

    def extract_traits_from_file(self):
                DataAll = pd.read_csv(self.test_file,
                                      names=['Time', 'Acc X', 'Acc Y', 'Acc Z', 'Light Meter', 'Button Status', 'Temp'],
                                      usecols=[1, 2, 3])

                DataX = DataAll[[0]]
                DataY = DataAll[[1]]
                DataZ = DataAll[[2]]

                frame_length = 250
                data_length = len(DataX.index)
                frames_count = np.math.floor(data_length / frame_length) - 1
                bottom_sample = 0
                top_sample = frame_length



                for step in range(0, frames_count):
                    bottom_sample += frame_length
                    top_sample += frame_length
                    frameX = DataX[bottom_sample:top_sample]
                    frameY = DataY[bottom_sample:top_sample]
                    frameZ = DataZ[bottom_sample:top_sample]

                    data_features = self.calculate_traits(frameX, frameY, frameZ, frame_length)

                    self.test_traits.append(data_features)

    def calculate_traits(self, frameX, frameY, frameZ, frame_length):
        # print("mean")
        #meanX = frameX.values.mean()
        #meanY = frameY.values.mean()
        #meanZ = frameZ.values.mean()
        # # print("power")
        #powerX = frameX.pow(2).sum() / frame_length
        #powerY = frameY.pow(2).sum() / frame_length
        #powerZ = frameZ.pow(2).sum() / frame_length


        # # print("std")
        stdX = frameX.values.std()
        stdY = frameY.values.std()
        stdZ = frameZ.values.std()

        # print("FFT Power")
        fftPowerX = np.sum(np.abs(np.fft.fft(frameX)) ** 2) / frame_length
        fftPowerY = np.sum(np.abs(np.fft.fft(frameY)) ** 2) / frame_length
        fftPowerZ = np.sum(np.abs(np.fft.fft(frameZ)) ** 2) / frame_length

        # print("Cepstrum Power")
        cepsPowerX = np.sum(np.abs(np.fft.ifft(np.log(np.abs(np.fft.fft(frameX))))) ** 2) / frame_length
        cepsPowerY = np.sum(np.abs(np.fft.ifft(np.log(np.abs(np.fft.fft(frameY))))) ** 2) / frame_length
        cepsPowerZ = np.sum(np.abs(np.fft.ifft(np.log(np.abs(np.fft.fft(frameZ))))) ** 2) / frame_length

        return np.array([
            #meanX, meanY, meanZ,
            #powerX, powerY, powerZ,
            stdX, stdY, stdZ,
            fftPowerX, fftPowerY, fftPowerZ,
            cepsPowerX, cepsPowerY, cepsPowerZ
])
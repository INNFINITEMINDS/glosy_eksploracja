
# Thanks to Zhao Yu for converting the .ipynb notebook to
# this simplified Python script that I edited a little.

# Note that the dataset must be already downloaded for this script to work, do:
#     $ cd data/
#     $ python download_dataset.py

import numpy as np
from sklearn import svm


# Load "X" ( training and testing inputs)
def load_X(X_signals_paths):
    X_signals = []

    for signal_type_path in X_signals_paths:

        file = open(signal_type_path, 'r')

        # Read dataset from disk, dealing with text files' syntax
        X_signals.append(
            [np.array(serie, dtype=np.float32) for serie in [
                row.replace('  ', ' ').strip().split(' ') for row in file
            ]]
        )
        file.close()

    return np.transpose(np.array(X_signals) )#, (1, 2, 0))


# Load "y" (training and testing outputs)

def load_y(y_path):
    file = open(y_path, 'r')
    # Read dataset from disk, dealing with text file's syntax
    y_ = np.array(
        [elem for elem in [
            row.replace('  ', ' ').strip().split(' ') for row in file
        ]],
        dtype=np.int32
    )
    file.close()
    return y_

if __name__ == "__main__":

    #-----------------------------
    # step1: load and prepare data
    #-----------------------------
    # Those are separate normalised input features for the neural network

    DATA_PATH = "data/"
    DATASET_PATH = DATA_PATH + "UCI HAR Dataset/"
    print("\n" + "Dataset is now located at: " + DATASET_PATH)
    TRAIN = "train/"
    TEST = "test/"

X_train_signals_paths=[DATASET_PATH + TRAIN + "X_train.txt"]
X_test_signals_paths=[DATASET_PATH + TEST + "X_test.txt"]
print(X_train_signals_paths)
X_train = load_X(X_train_signals_paths)
X_test = load_X(X_test_signals_paths)

# Input Data

y_train_path = DATASET_PATH + TRAIN + "y_train.txt"
y_test_path = DATASET_PATH + TEST + "y_test.txt"

y_train = load_y(y_train_path)
y_test = load_y(y_test_path)

# Some debugging info

print ("Begin training")

# Support Vector Machine

X_train =X_train[:,:,0]                      #select training data from array
X_train=np.transpose(X_train)                #transpose training array
y = np.ravel(y_train)                        #return contiguous array
clf = svm.SVC(kernel='rbf', C=1,gamma=1)     #Support Vectorm Machine with proper parameters
clf.fit(X_train, y)                          #training of SVM
print ("Learning Finished!")

print ("Begin testing")
X_test=X_test[:,:,0]                         #select testing data from array
X_test=np.transpose(X_test)                  #transpose training array
A=clf.predict(X_test)                        #predict labels of testing parameters
print ("Testing Finished!")
np.savetxt('test.out', A, delimiter='\n')

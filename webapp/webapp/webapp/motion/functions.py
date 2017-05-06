
import numpy as np
from sklearn import svm
from Data_Convert import TraitExtractor


def use_svm(train_samples, train_labels, test_samples):
    # data preparing
    train_labels = np.ravel(train_labels)

    # learning
    clf = svm.SVC(decision_function_shape='ovo', kernel='poly', gamma='auto')
    clf.fit(train_samples, train_labels)

    # testing
    result = clf.predict(test_samples)
    return result


def calculate_accuracy(result_labels, test_labels):
    return (np.array(result_labels) == np.array(test_labels)).sum()/result_labels.size*100


def classify_sample(test_file):

    # choose measurement directory
    measurement_directory = "./measurements"

    traits_provider = TraitExtractor(measurement_directory, test_file)

    # prepare training data
    train_activities = traits_provider.get_traits()
    training_labels = traits_provider.get_labels()

    # prepare testing data
    test_activities = traits_provider.get_test_traits()

    # classification
    train_activities = np.squeeze(train_activities)
    training_labels = np.squeeze(training_labels)
    test_activities = np.squeeze(test_activities)

    results = use_svm(train_activities, training_labels, test_activities)

    return results

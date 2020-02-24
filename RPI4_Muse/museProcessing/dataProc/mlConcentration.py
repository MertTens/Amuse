import csv
import glob
import os

import numpy as np
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.neighbors import KNeighborsClassifier

"""
Classifies our EEG data as concentrated or not.
"""


class classifier:
    """
    A KNN classifier that reads EEG data from a CSV
    """

    def __init__(self, test_size=0.20, row_merges=5, n_neighbors=3, k_folds=5):
        # Assert our parameters
        assert (0 < test_size < 1.0)
        assert (0 < row_merges)
        assert (0 < n_neighbors)
        assert (0 < k_folds)

        self.test_size = test_size
        self.row_merges = row_merges
        self.n_neighbors = n_neighbors
        self.k_folds = k_folds
        self.X = None
        self.y = None
        self.classifier = None

    def train(self, print_accuracy=True):
        """
        Trains the model.

        :param print_accuracy: Whether to print the accuracy
        :type print_accuracy: bool
        """
        # Load in the data
        concentrated_data, distracted_data = self.load_data()

        # Do feature extraction
        #  1. Average all row_merges number of rows together
        concentrated_data = self.avg(concentrated_data, self.row_merges)
        distracted_data = self.avg(distracted_data, self.row_merges)

        #  2. Remove the timestamp column
        concentrated_data = np.delete(concentrated_data, 0, 1)
        distracted_data = np.delete(distracted_data, 0, 1)

        # Merge the arrays and seperate the labels
        full_dataset = np.vstack((concentrated_data, distracted_data))
        self.X = full_dataset[:, :-1]
        self.y = full_dataset[:, -1]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                            test_size=self.test_size)

        # Train using KNN
        self.classifier = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        self.classifier.fit(X_train, y_train)

        # Test using the classifier
        if print_accuracy:
            accuracy = self.classifier.score(X_test, y_test)
            print("Naïve Accuracy: " + str(accuracy))

    def cross_validate(self, k_folds=None):
        """
        Cross validates.

        :param k_folds: the number of folds
        :type k_folds: int
        :return: The scores
        :rtype: dict
        """
        # Cross Validate
        if k_folds is None:
            k_folds = self.k_folds

        scores = cross_validate(classifier, self.X, self.y, cv=k_folds)
        return scores

    def load_data(self, labelled=True):
        """
        Returns the cleaned and labelled EEG data as two matrices, one for concentrated and one for meditated.

        :return: concentrated_list, distracted_list
        :rtype: (np array, np array)
        """
        concentrated = []
        distracted = []

        os.chdir("./data/labeledData/")
        csv_files = glob.glob("*.csv")

        for filename in csv_files:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)

                if "distracted" in filename:
                    distracted.extend(data[1:])

                elif "meditated" in filename:
                    concentrated.extend(data[1:])
                else:
                    print(filename + "was not parsed.")
                    continue

        concentrated = np.array(concentrated, dtype=float)
        distracted = np.array(distracted, dtype=float)

        if labelled:
            concentrated = np.hstack((concentrated, np.ones((len(concentrated), 1))))
            distracted = np.hstack((distracted, np.zeros((len(distracted), 1))))

        return concentrated, distracted

    # From: https://stackoverflow.com/questions/30379311/fast-way-to-take-average-of-every-n-rows-in-a-npy-array
    def avg(self, myArray, N=2):
        """
        Averages every N rows from myArray together.
        """
        cum = np.cumsum(myArray, 0)
        result = cum[N - 1::N] / float(N)
        result[1:] = result[1:] - result[:-1]

        remainder = myArray.shape[0] % N
        if remainder != 0:
            if remainder < myArray.shape[0]:
                lastAvg = (cum[-1] - cum[-1 - remainder]) / float(remainder)

            else:
                lastAvg = cum[-1] / float(remainder)
            result = np.vstack([result, lastAvg])

        return result

    def predict(self, X):
        """
        Predicts X.
        """
        return self.classifier.predict(X)


if __name__ == "__main__":
    classifier = classifier()
    classifier.train()

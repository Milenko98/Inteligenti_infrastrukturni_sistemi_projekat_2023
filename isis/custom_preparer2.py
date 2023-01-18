import numpy
from sklearn.preprocessing import MinMaxScaler


class CustomPreparer2:
    def __init__(self, dataframe):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.datasetOrig = dataframe.values
        self.datasetOrig = self.datasetOrig.astype('float32')

    def prepare_for_training(self):
        dataset = self.scaler.fit_transform(self.datasetOrig)
        look_back = 11
        testX = self.create_dataset(dataset, look_back)
        testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        self.testX = testX
        return testX.copy()

    def inverse_transform(self, testPredict):
        testPredict = numpy.reshape(testPredict, (testPredict.shape[0], testPredict.shape[1]))
        self.testX = numpy.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))
        testXAndPredict = numpy.concatenate((self.testX, testPredict), axis=1)
        testXAndPredict = self.scaler.inverse_transform(testXAndPredict)
        testPredict = testXAndPredict
        return testPredict

    def create_dataset(self, dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset)):
            a = dataset[i, 0:look_back-1]
            dataX.append(a)
        return numpy.array(dataX)

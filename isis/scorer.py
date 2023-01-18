import numpy


class Scorer:
    def get_score(self, trainY, trainPredict, testY, testPredict):
        trainScore = numpy.mean(numpy.abs((trainY - trainPredict) / trainY))*100
        testScore = numpy.mean(numpy.abs((testY - testPredict) / testY))*100
        return trainScore, testScore

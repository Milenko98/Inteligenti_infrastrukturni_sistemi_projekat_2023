from datetime import datetime

import numpy
import pandas

import create_db


def parseWeatherData(dataframe):
    dataframe.replace({numpy.inf: numpy.nan, -numpy.inf: numpy.nan}, inplace=True)
    dataframe.interpolate(method='linear', limit_direction='forward', inplace=True)
    dataframe = dataframe.fillna(0.0)
    dataframe.replace(numpy.nan, 0, inplace=True)
    dataframe.interpolate()
    dataframe['temp'] = numpy.where(dataframe['temp'] > 100, 100, dataframe['temp'])
    dataframe['temp'] = numpy.where(dataframe['temp'] < -100, -100, dataframe['temp'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == '', 'Clear', dataframe['conditions'])
    dataframe['datetime'] = numpy.where(dataframe['datetime'] == '', '2022-01-01', dataframe['datetime'])
    dataframe['datetime'] = dataframe['datetime'].apply(
        lambda xx: datetime.strptime(xx, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Clear', '0',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Partially cloudy', '1',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Overcast', '2',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Snow, Overcast', '3',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Snow, Partially cloudy', '4',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Rain, Overcast', '5',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Rain, Partially cloudy', '6',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Rain, Partially cloudy', '7',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Rain, Partially cloudy', '8',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Rain', '9',
                                          dataframe['conditions'])
    dataframe['conditions'] = numpy.where(dataframe['conditions'] == 'Snow', '10',
                                          dataframe['conditions'])
    dataframe['temp'] = dataframe['temp'].round(decimals=2)
    dataframe['feelslike'] = dataframe['feelslike'].round(decimals=2)
    dataframe['dew'] = dataframe['dew'].round(decimals=2)
    dataframe['humidity'] = dataframe['humidity'].round(decimals=2)
    dataframe['precip'] = dataframe['precip'].round(decimals=2)
    dataframe['precipprob'] = dataframe['precipprob'].round(decimals=2)
    dataframe['preciptype'] = dataframe['preciptype'].round(decimals=2)
    dataframe['snow'] = dataframe['snow'].round(decimals=2)
    dataframe['snowdepth'] = dataframe['snowdepth'].round(decimals=2)
    dataframe['windgust'] = dataframe['windgust'].round(decimals=2)
    dataframe['windspeed'] = dataframe['windspeed'].round(decimals=2)
    dataframe['winddir'] = dataframe['winddir'].round(decimals=2)
    dataframe['sealevelpressure'] = dataframe['sealevelpressure'].round(decimals=2)
    dataframe['cloudcover'] = dataframe['cloudcover'].round(decimals=2)
    dataframe['visibility'] = dataframe['visibility'].round(decimals=2)
    dataframe['solarradiation'] = dataframe['solarradiation'].round(decimals=2)
    dataframe['solarenergy'] = dataframe['solarenergy'].round(decimals=2)
    dataframe['uvindex'] = dataframe['uvindex'].round(decimals=2)
    dataframe['severerisk'] = dataframe['severerisk'].round(decimals=2)
    return dataframe


def parseLoadData(dataframe):
    dataframe = dataframe[dataframe['name'] == 'N.Y.C.']
    dataframe = dataframe.loc[dataframe['datetime'].str.contains(":00:00", case=False)]
    dataframe.replace({numpy.inf: numpy.nan, -numpy.inf: numpy.nan}, inplace=True)
    dataframe.interpolate(method='linear', limit_direction='forward', inplace=True)
    dataframe = dataframe.fillna(0.0)
    dataframe.replace(numpy.nan, 0, inplace=True)
    dataframe.interpolate()
    dataframe['datetime'] = dataframe['datetime'].apply(
        lambda xx: datetime.strptime(xx, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
    return dataframe


def chooseDataForTraining(start, end):
    sql_weather_data_query = pandas.read_sql('SELECT * FROM Weather_data', create_db.conn)
    weatherDf = pandas.DataFrame(sql_weather_data_query)

    sql_load_data_query = pandas.read_sql('SELECT * FROM Load_data', create_db.conn)
    loadDf = pandas.DataFrame(sql_load_data_query)

    finalDf = pandas.merge(weatherDf, loadDf, on='datetime')
    finalDf.drop('name_y', axis=1, inplace=True)
    finalDf.columns = finalDf.columns.str.replace('name_x', 'name')

    mask = (finalDf['datetime'] >= start) & (finalDf['datetime'] <= end)
    finalDf = finalDf.loc[mask]

    forTrainingDf = finalDf.filter(
        ['temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover',
         'conditions', 'load'], axis=1)
    return forTrainingDf

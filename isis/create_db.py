import numpy
import pandas as pd
import pyodbc

import warnings

warnings.filterwarnings('ignore')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-DAAHICE\SQLEXPRESS;'
                      'Database=DB;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


def createdb():
    cursor.execute('''CREATE TABLE Weather_data (name nvarchar(50) null, datetime nvarchar(50) null, temp float null, feelslike float null, dew float null, humidity float null, precip float null, precipprob float null, preciptype float null, snow float null, snowdepth float null, windgust float null, windspeed float null, winddir float null,
    sealevelpressure float null, cloudcover float null, visibility float null, solarradiation float null, solarenergy float null, uvindex float null, severrisk float null, conditions nvarchar(50) null)''')
    conn.commit()

def createOdbranadb():
    cursor.execute('''CREATE TABLE Odbrana_Weather_data (name nvarchar(50) null, datetime nvarchar(50) null, temp float null, feelslike float null, dew float null, humidity float null, precip float null, precipprob float null, preciptype float null, snow float null, snowdepth float null, windgust float null, windspeed float null, winddir float null,
    sealevelpressure float null, cloudcover float null, visibility float null, solarradiation float null, solarenergy float null, uvindex float null, severrisk float null, conditions nvarchar(50) null)''')
    conn.commit()

def createLoadDb():
    cursor.execute('''CREATE TABLE Load_data (datetime nvarchar(50) null, name nvarchar(50) null, load float null)''')
    conn.commit()

# def get():
#     sql_query = pd.read_sql_query('''
#                                    SELECT
#                                    *
#                                    FROM Weather_data
#                                    ''', conn)
#
#     dataframe = pd.DataFrame(sql_query)
#     dataframe.replace({numpy.inf: numpy.nan, -numpy.inf: numpy.nan}, inplace=True)
#     dataframe.interpolate(method='linear', limit_direction='forward', inplace=True)
#     dataframe = dataframe.fillna(0.0)
#     dataframe.replace(numpy.nan, 0, inplace=True)
#     dataframe.interpolate()
#     dataframe.to_csv('proba.csv')
#
#
# get()

#createOdbranadb()

from tkcalendar import Calendar
from datetime import datetime, date
from tkinter import *
from tkinter import filedialog
import create_db
import pandas
import parse_data
from ann_regression import AnnRegression
from custom_preparer import CustomPreparer
from custom_preparer2 import CustomPreparer2
from scorer import Scorer

win = Tk()
fileNames = []
dataframes = []

win.title('consumption estimation app')

width = 1200  # Width
height = 700  # Height
chosenStart = ''
chosenEnd = ''

screen_width = win.winfo_screenwidth()  # Width of the screen
screen_height = win.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

win.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Holidays in US
holidays = [['Monday', '2018-01-01', "New Year's Day", 1], ['Monday', '2018-01-15', "M L King Day"],
            ['Wednesday', '2018-02-14', "Valentine's Day"], ['Monday', '2018-02-19', "President's Day"],
            ['Friday', '2018-03-30', "Good Friday"], ['Sunday', '2018-04-01', "Easter Sunday"],
            ['Sunday', '2018-05-13', "Mother's Day"], ['Monday', '2018-05-28', "Memorial Day"],
            ['Wednesday', '2018-07-04', "Independence Day"], ['Sunday', '2018-06-17', "Father's Day"],
            ['Monday', '2018-09-03', "Labor Day"], ['Monday', '2018-10-08', "Columbus Day"],
            ['Wednesday', '2018-10-31', "Halloween"], ['Sunday', '2018-11-11', "Veterans Day"],
            ['Thursday', '2018-11-22', "Thanksgiving Day"], ['Tuesday', '2018-12-25', "Christmas"],

            ['Tuesday', '2019-01-01', "New Year's Day"], ['Monday', '2019-01-21', "M L King Day"],
            ['Thursday', '2019-02-14', "Valentine's Day"], ['Monday', '2019-02-18', "President's Day"],
            ['Friday', '2019-04-19', "Good Friday"], ['Sunday', '2019-04-21', "Easter Sunday"],
            ['Sunday', '2019-05-12', "Mother's Day"], ['Monday', '2019-05-27', "Memorial Day"],
            ['Thursday', '2019-07-04', "Independence Day"], ['Sunday', '2019-06-16', "Father's Day"],
            ['Monday', '2019-09-02', "Labor Day"], ['Monday', '2019-10-14', "Columbus Day"],
            ['Thursday', '2019-10-31', "Halloween"], ['Monday', '2019-11-11', "Veterans Day"],
            ['Thursday', '2019-11-28', "Thanksgiving Day"], ['Wednesday', '2019-12-25', "Christmas"],

            ['Wednesday', '2020-01-01', "New Year's Day"], ['Monday', '2020-01-20', "M L King Day"],
            ['Friday', '2020-02-14', "Valentine's Day"], ['Monday', '2020-02-17', "President's Day"],
            ['Friday', '2020-04-10', "Good Friday"], ['Sunday', '2020-04-12', "Easter Sunday"],
            ['Sunday', '2020-05-10', "Mother's Day"], ['Monday', '2020-05-25', "Memorial Day"],
            ['Saturday', '2020-07-04', "Independence Day"], ['Sunday', '2020-06-21', "Father's Day"],
            ['Friday', '2020-07-03', "Independence Day Holiday"],
            ['Monday', '2020-09-07', "Labor Day"], ['Monday', '2020-10-12', "Columbus Day"],
            ['Saturday', '2020-10-31', "Halloween"], ['Wednesday', '2020-11-11', "Veterans Day"],
            ['Thursday', '2020-11-26', "Thanksgiving Day"], ['Friday', '2020-12-25', "Christmas"],

            ['Wednesday', '2021-01-01', "New Year's Day"], ['Monday', '2021-01-20', "M L King Day"],
            ['Friday', '2021-02-14', "Valentine's Day"], ['Monday', '2021-02-17', "President's Day"],
            ['Friday', '2021-04-10', "Good Friday"], ['Sunday', '2021-04-12', "Easter Sunday"],
            ['Sunday', '2021-05-10', "Mother's Day"], ['Monday', '2021-05-25', "Memorial Day"],
            ['Saturday', '2021-07-04', "Independence Day"], ['Sunday', '2021-06-21', "Father's Day"],
            ['Friday', '2021-07-03', "Independence Day Holiday"],
            ['Monday', '2021-09-07', "Labor Day"], ['Monday', '2021-10-12', "Columbus Day"],
            ['Saturday', '2021-10-31', "Halloween"], ['Wednesday', '2021-11-11', "Veterans Day"],
            ['Thursday', '2021-11-26', "Thanksgiving Day"], ['Friday', '2021-12-25', "Christmas"],
            ]

# Create the pandas DataFrame
holidaysDf = pandas.DataFrame(holidays, columns=['Day', 'Date', 'Holiday', 'Rang'])


def insertWeatherDataIntoDB():
    try:
        if len(dataframes) >= 1:
            for dataframe in dataframes:
                dataframe = parse_data.parseWeatherData(dataframe)
                for row in dataframe.itertuples():
                    create_db.cursor.execute('''
                                            INSERT INTO Odbrana_Weather_data (name, datetime, temp, feelslike, dew, humidity, precip, precipprob, preciptype, snow, snowdepth,
                                            windgust, windspeed, winddir, sealevelpressure, cloudcover, visibility, solarradiation, solarenergy, uvindex, severrisk, conditions)
                                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                            ''',
                                             row.name,
                                             row.datetime,
                                             row.temp,
                                             row.feelslike,
                                             row.dew,
                                             row.humidity,
                                             row.precip,
                                             row.precipprob,
                                             row.preciptype,
                                             row.snow,
                                             row.snowdepth,
                                             row.windgust,
                                             row.windspeed,
                                             row.winddir,
                                             row.sealevelpressure,
                                             row.cloudcover,
                                             row.visibility,
                                             row.solarradiation,
                                             row.solarenergy,
                                             row.uvindex,
                                             row.severerisk,
                                             row.conditions if row.conditions != '' else 'Clear'
                                             )
                create_db.conn.commit()

            insertedLabel.configure(text='Csv files successfully inserted into database.', fg='green')
            insertedLabel.grid(column=0, row=4, sticky='EW', columnspan=2)
    except:
        insertedLabel.configure(text='Csv files did not successfully inserted into database.', fg='red')
        insertedLabel.grid(column=0, row=4, sticky='EW', columnspan=2)


# def insertLoadIntoDB():
#     try:
#         if len(dataframes) >= 1:
#             for dataframe in dataframes:
#                 dataframe = parse_data.parseLoadData(dataframe)
#                 for row in dataframe.itertuples():
#                     create_db.cursor.execute('''
#                                         INSERT INTO Load_data (datetime, name, load)
#                                         VALUES (?,?,?)
#                                         ''',
#                                              row.datetime,
#                                              row.name,
#                                              row.load
#                                              )
#         create_db.conn.commit()
#         insertedLabel.configure(text='Csv load files successfully inserted into database.', fg='green')
#         insertedLabel.pack(fill='x')
#     except:
#         insertedLabel.configure(text='Csv load files did not successfully inserted into database.', fg='red')
#         insertedLabel.pack(fill='x')


def browseFiles():
    global fileNames
    global dataframes
    filenames = filedialog.askopenfilenames(initialdir="/",
                                            title="Select a File",
                                            filetypes=(("Text files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
    if len(filenames) >= 1:
        for i in filenames:
            listOfChosenFiles.insert(END, i)
            fileNames.append(i)
            data = pandas.read_csv(i)
            dataframe = pandas.DataFrame(data)
            dataframe.columns = dataframe.columns.str.replace('Time Stamp', 'datetime')
            dataframe.columns = dataframe.columns.str.replace('Name', 'name')
            dataframe.columns = dataframe.columns.str.replace('Load', 'load')
            dataframes.append(dataframe)


def deleteFiles():
    listOfChosenFiles.delete(0, END)


def predict():
    sql_odbrana_weather_data_query = pandas.read_sql('SELECT * FROM Odbrana_Weather_data', create_db.conn)
    odbrana_weatherdf = pandas.DataFrame(sql_odbrana_weather_data_query)

    mask = (odbrana_weatherdf['datetime'] >= chosenStart) & (odbrana_weatherdf['datetime'] <= chosenEnd)
    finaldf = odbrana_weatherdf.loc[mask]

    forOdbranadf = finaldf.filter(
        ['temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover',
         'conditions', 'visibility'], axis=1)
    withdate = finaldf.filter(['datetime'])

    preparer = CustomPreparer2(forOdbranadf)
    testX = preparer.prepare_for_training()

    # make predictions
    ann_regression = AnnRegression()
    testPredict = ann_regression.get_predictOdbrana(testX)

    # invert predictions
    testPredict = preparer.inverse_transform(testPredict)
    temp = pandas.DataFrame(testPredict)
    temp.columns = ['temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed', 'winddir', 'sealevelpressure',
                    'cloudcover', 'conditions', 'predicted_load']
    # temp = temp.filter(['predicted_load'])
    loadList = temp['predicted_load'].values.tolist()
    dates = withdate['datetime'].values.tolist()
    prazna_lista = []
    for i in range(len(dates)):
        prazna_lista.append((dates[i], loadList[i]))
    nesto = pandas.DataFrame(prazna_lista)
    nesto.columns = ['datetime', 'predicted_load']
    nesto.to_csv('ajoj.csv')
    #temp.to_csv('ajoj.csv')
    successPredictLabel.configure(text='Prediction was successfully executed!', fg='green')
    #temp['datetime'] = withdate['datetime']
    # frames = [withdate, temp]
    # df1 = pandas.DataFrame()
    # result = pandas.merge(frames, axis=0)
    #result = result.append(temp)
    # merged = withdate.append(temp)
    # temp.columns = ['temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover', 'conditions', 'predicted_load']
    # print(result)
    #result.to_csv('ajoj.csv')
    # merged.columns = ['datetime', 'temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed', 'winddir', 'sealevelpressure', 'cloudcover', 'conditions', 'predicted_load']
    # odbrana = merged.filter(['datetime', 'predicted_load'])
    # odbrana.to_csv('auu.csv')
    # print(testPredict)


def printDates():
    global fromm, to, chosenStart, chosenEnd
    firstdate = cal.get_date() + ' ' + fromm.get() + ':00'
    seconddate = cal2.get_date() + ' ' + to.get() + ':00'

    firstdate2 = datetime.strptime(firstdate, '%m/%d/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    seconddate2 = datetime.strptime(seconddate, '%m/%d/%y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    chosenStart = firstdate2
    chosenEnd = seconddate2

    ispis.configure(text=firstdate2 + ' - ' + seconddate2)


def train():
    forTrainingDf = parse_data.chooseDataForTraining(chosenStart, chosenEnd)
    preparer = CustomPreparer(forTrainingDf, 11, 0.85)
    trainX, trainY, testX, testY = preparer.prepare_for_training()

    # make predictions
    ann_regression = AnnRegression()
    trainPredict, testPredict = ann_regression.compile_fit_predict(trainX, trainY, testX)

    # invert predictions
    trainPredict, trainY, testPredict, testY = preparer.inverse_transform(trainPredict, testPredict)

    # calculate root mean squared error
    scorer = Scorer()
    trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
    greskaLabel.configure(text='Training has successfully finished!', fg='green')


chooseFilesBtn = Button(win, text='Choose .csv files', fg='green', command=browseFiles)
chooseFilesBtn.grid(column=0, row=0, sticky='EW', columnspan=1)

deleteChosenFilesBtn = Button(win, text='Delete chosen files', fg='red', command=deleteFiles)
deleteChosenFilesBtn.grid(column=1, row=0, sticky='EW', columnspan=1)

listOfChosenFiles = Listbox(win, font='Helvetica 15 bold', bg="white")
listOfChosenFiles.grid(column=0, row=2, sticky='EW', columnspan=2)

insertWeatherDataIntoDbBtn = Button(win, text='Insert weather data', fg='green', command=insertWeatherDataIntoDB)
insertWeatherDataIntoDbBtn.grid(column=0, row=3, sticky='EW', columnspan=2, pady=10)

# insertLoadIntoDbBtn = Button(win, text='Insert load into database', fg='green', command=insertLoadIntoDB)
# insertLoadIntoDbBtn.grid(column=0, row=4, sticky='EW', columnspan=2, pady=10)

insertedLabel = Label(win, text='')

dateNow = date.today()

cal = Calendar(win, selectmode='day',
               year=dateNow.year, month=dateNow.month,
               day=dateNow.day)

cal.grid(column=0, row=5)

cal2 = Calendar(win, selectmode='day',
                year=dateNow.year, month=dateNow.month,
                day=dateNow.day)
cal2.grid(column=1, row=5, padx=20)

fromm = Entry(win)
fromm.grid(column=0, row=6, pady=20)

to = Entry(win)
to.grid(column=1, row=6, pady=20)

confirm = Button(win, text='Confirm', command=printDates, width=50)
confirm.grid(column=0, row=7, sticky='EW', pady=5, columnspan=2)

izabrandatum = Label(win, text='Chosen date')
izabrandatum.grid(column=0, row=8, sticky='EW', pady=5, columnspan=2)

ispis = Label(win, borderwidth=1, relief='solid')
ispis.grid(column=0, row=9, sticky='EW', columnspan=2)

trainBtn = Button(win, text='Train', command=train, width=100)
trainBtn.grid(column=3, row=0, sticky='EW', pady=5, padx=5)

greskaLabel = Label(win, borderwidth=1, relief='solid')
greskaLabel.grid(column=3, row=1, sticky='EW', pady=5, padx=5)

predictBtn = Button(win, text='Predict', command=predict, width=100)
predictBtn.grid(column=3, row=2, sticky='N', pady=5, padx=5)

successPredictLabel = Label(win, borderwidth=1, relief='solid')
successPredictLabel.grid(column=3, row=2, sticky='EW', pady=5, padx=5)

win.mainloop()

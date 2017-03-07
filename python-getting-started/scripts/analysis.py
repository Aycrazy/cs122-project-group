from datetime import date, timedelta
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

startdate = date(int("2010"), int("01"), int("02"))
dt = []
while startdate < date(int("2010"), int("04"), int("10")):
    dt.append(startdate)
    startdate += timedelta(days=1)

scores = [np.random.normal(0, 1) for i in range(len(dt))]
findata = [random.uniform(100, 300) for i in range(len(dt))]

d = {'scores': pd.Series(scores),
     'findata': pd.Series(findata),
     'time': pd.Series(dt)}




df = pd.DataFrame(d)

df = df.set_index(pd.to_datetime(dt))

#Descriptive Statistics

df.describe()
 
# Correlation for the time period

df.scores.corr(df.findata)


# Scatter

def scatter_plot(data):
    '''
    '''
    colors = np.random.rand(len(dt))
    area = np.pi * (15 * np.random.rand(len(dt)))**2  # 0 to 15 point radii
    plt.figure()
    plt.scatter(data.findata, data.scores, s=area, c=colors, alpha=0.5)
    plt.grid(True)
    return plt.show()


# Histograms

def histo_plot(data):
    '''
    '''
    plt.figure()

    return plt.show()



# Time Series

def time_series(data):
    '''
    '''

    fig, ax = plt.subplots()

    with pd.plot_params.use('x_compat', True):

        data.scores.plot(color = 'b')

        data.findata.plot(secondary_y = True, style='g')

        labels = ax.get_xticklabels()

        plt.setp(labels, rotation=30, fontsize=10)
   
        plt.grid()

    return plt.show()
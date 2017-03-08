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

scores_text = [np.random.normal(0, 1) for i in range(len(dt))]
scores_title = [np.random.normal(0, 1) for i in range(len(dt))]
findata = [random.uniform(100, 300) for i in range(len(dt))]

def create_df(date,scores_text,scores_title,findata):

    d = {'scores_text': pd.Series(scores_text),
         'scores_title': pd.Series(scores_title),
         'findata': pd.Series(findata),
         'time': pd.Series(dt)}

    df = pd.DataFrame(d)

    df = df.set_index(pd.to_datetime(dt))

    return df

def describe(df):
    #Descriptive Statistics

    df.describe()
     
    # Correlation for the time period

    df.scores_text.corr(df.findata)

    df.scores_title.corr(df.findata)

    
# Scatter

def scatter_plot(data, save_to = None):
    '''
    Computes the scatter plot for sentiment scores_text
    and financial data for a specified time period
    Inputs:
            Pandas DataFrame
            Filename, default value None
    Returns:
            It can only show the plot or save a 
            file with the plot
    '''
    colors = np.random.rand(len(dt))
    area = np.pi * (15 * np.array([0.6]
    *len(dt)))**2  # 0 to 15 point radii
    f = plt.figure()
    plt.scatter(data.findata, data.scores_text, s=area, c=colors, alpha=0.5)
    plt.grid(True)

    if save_to == None:

        plt.show()

    else:
        f.savefig(save_to)


# Text vs. title nltk scores 

def scatter_plot_comparison(data, save_to = None):
    '''
    Computes the scatter plot for sentiment scores_text
    and financial data for a specified time period
    Inputs:
            Pandas DataFrame
            Filename, default value None
    Returns:
            It can only show the plot or save a 
            file with the plot
    '''
    colors = np.random.rand(len(dt))
    area = np.pi * (15 * np.array([0.6]*len(dt)))**2  # 0 to 15 point radii
    plt.scatter(data.scores_title, data.scores_text, s=area, c=colors, alpha=0.5)

    x = np.array(data.scores_text)
    y = np.array(data.scores_title)

    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, '-')
    plt.grid(True)

    if save_to == None:

        plt.show()

    else:
        plt.savefig(save_to)




# Histograms

def histo_plot(data, save_to = None):
    '''
    Computes the histograms for sentiment scores_text
    and financial data for a specified time period
    Inputs:
            Pandas DataFrame
            Filename, default value None
    Returns:
            It can only show the plot or save a 
            file with the plot
    '''
    data.hist(layout=(1,3)) 

    if save_to == None:

        plt.show()

    else:
        plt.savefig(save_to)



# Time Series

def time_series(data, save_to = None):
    '''
    Plots sentiment scores_text and financial data for
    a specified time period
    
    Inputs:
            Pandas DataFrame
            Filename, default value None
    Returns:
            It can only show the plot or save a 
            file with the plot
    '''

    f, ax = plt.subplots()

    with pd.plot_params.use('x_compat', True):

        data.scores_text.plot(color = 'b')

        data.findata.plot(secondary_y = True, style='g')

        labels = ax.get_xticklabels()

        plt.setp(labels, rotation=30, fontsize=10)
   
        plt.grid()

    if save_to == None:

        plt.show()

    else:
        f.savefig(save_to)


def get_plots(data, save_to = None):

    # Inputs for scatter plots
    colors = np.random.rand(len(dt))
    area = np.pi * (15 * np.array([0.6]*len(dt)))**2  # 0 to 15 point radii
    plt.scatter(data.scores_title, data.scores_text, s=area, c=colors, alpha=0.5)
    # Linear fit for nltk comparison scores
    x = np.array(data.scores_text)
    y = np.array(data.scores_title)
    m, b = np.polyfit(x, y, 1)
    # Fontsize
    num = 12
    # Number of bins for nltk histograms
    bins = np.linspace(-3, 3, 100)

    #Create subplots
    f, axarr = plt.subplots(2, 2)

    axarr[0,0].scatter(data.findata, data.scores_text, s=area, c=colors, alpha=0.5)
    axarr[0,0].grid()
    axarr[0,0].set_title('Scatter plot financial data vs. nltk text', fontsize = num)
    axarr[0,1].scatter(data.scores_title, data.scores_text, s=area, c=colors, alpha=0.5)
    axarr[0,1].plot(x, m*x + b, '-')
    axarr[0,1].grid()
    axarr[0,1].set_title('Scatter plot nltk title vs. text', fontsize = num)
    axarr[1,0].hist(data.scores_title, bins, alpha=0.5, label= "title")
    axarr[1,0].hist(data.scores_text, bins, alpha=0.5, label= "text")
    axarr[1,0].legend(loc='upper right')
    axarr[1,0].grid()
    axarr[1,0].set_title('Nltk Histograms title vs. text', fontsize = num)
    axarr[1,1].plot(data.scores_text)
    ax2 = axarr[1,1].twinx()
    ax2.plot(data.findata, color="g")
    axarr[1,1].grid()
    axarr[1,1].set_title('Time series financial data vs. nltk text', fontsize = num)
    f.tight_layout()



    if save_to == None:

        f.show()

    else:
        f.savefig(save_to)


 
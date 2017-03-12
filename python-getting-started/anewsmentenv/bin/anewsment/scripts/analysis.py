from datetime import date, timedelta
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib
import django

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#from io import BytesIO
from PIL import Image
from time import sleep
from random import randint

import numpy as np
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import django
#from PIL import image

startdate = date(int("2010"), int("01"), int("02"))
dt = []
while startdate < date(int("2010"), int("04"), int("10")):
    dt.append(startdate)
    startdate += timedelta(days=1)

#findata = [random.uniform(100, 300) for i in range(len(dt))]

def create_df(date,scores_text,scores_title,findata):
    
    f = {'findata': pd.Series(findata)}

    d = {'scores_text': pd.Series(scores_text),
         'scores_title': pd.Series(scores_title),
         'date': pd.Series(date)}

    df = pd.DataFrame(d)
    print(df.shape[0], 'I was this big')
    print(df)
    df2 = pd.DataFrame(f)

    df = df.set_index(pd.to_datetime(date))
    

    df = df.groupby(pd.TimeGrouper('D')).mean()
    rv1 = df.dropna()
    print(rv1.shape[0], 'Now I m smaller')
    print(rv1)
    #df2 = df2.groupby(pd.TimeGrouper('D')).mean()
    df2 = df2.set_index(pd.to_datetime(rv1.index))
    rv = pd.concat([rv1, df2], axis=1)
    rv['date'] = rv.index
    print(rv)
    return rv

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
    colors = np.random.rand(len(data.date))
    area = np.pi * (15 * np.array([0.6]
    *len(data.date)))**2  # 0 to 15 point radii
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
    colors = np.random.rand(len(data.date))
    area = np.pi * (15 * np.array([0.6]*len(data.date)))**2  # 0 to 15 point radii
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
    colors = np.random.rand(len(data.date))
    area = np.pi * (15 * np.array([0.6]*len(data.date)))**2  # 0 to 15 point radii
    plt.scatter(data.scores_title, data.scores_text, s=area, c=colors, alpha=0.5)
    # Linear fit for nltk comparison scores
    x = np.array(data.scores_text)
    y = np.array(data.scores_title)
    m, b = np.polyfit(x, y, 1)
    # Fontsize
    num = 12
    # Correlations
    corr1 = data.scores_text.corr(data.findata)
    corr2 = data.scores_text.corr(data.scores_title)
    #Create subplots
    f, axarr = plt.subplots(2, 2)

    axarr[0,0].scatter(data.findata, data.scores_text, s=area, c=colors, alpha=0.5, label= '{0:.3g}'.format(corr1))
    axarr[0,0].legend(loc='upper right')
    axarr[0,0].grid()
    axarr[0,0].set_title('Scatter plot financial data vs. nltk text', fontsize = num)
    axarr[0,0].set_xlabel('indicator units')
    axarr[0,0].set_ylabel('text score')
    # Comparison scatterplot
    axarr[0,1].scatter(data.scores_title, data.scores_text, s=area, c=colors, alpha=0.5, label= '{0:.3g}'.format(corr2))
    axarr[0,1].legend(loc='upper right')
    axarr[0,1].plot(x, m*x + b, '-')
    axarr[0,1].grid()
    axarr[0,1].set_title('Scatter plot nltk title vs. text', fontsize = num)
    #axarr[0,1].tick_params(axis='x',labelsize=5,width=2)
    axarr[0,1].set_xlabel('title')
    axarr[0,1].set_ylabel('text')
    # Histograms
    axarr[1,0].hist(data.scores_title.dropna(), alpha=0.5, label= "title")
    axarr[1,0].hist(data.scores_text.dropna(), alpha=0.5, label= "text")
    axarr[1,0].legend(loc='upper right')
    axarr[1,0].grid()
    axarr[1,0].set_title('Nltk Histograms title and text', fontsize = num)
    # Time series subplot
    axarr[1,1].plot(data.date, data.scores_text)
    ax2 = axarr[1,1].twinx()
    ax2.plot(data.date, data.findata, color="g")
    axarr[1,1].grid()
    axarr[1,1].set_title('Time series nltk text vs. financial data', fontsize = num)
    axarr[1,1].tick_params(axis='x', labelsize=5, width =2)
    axarr[1,1].set_ylabel('text score')
    ax2.set_ylabel('indicator units')
    f.tight_layout()



    if save_to == None:
        '''
        sleep(randint(3,5))
        #f.savefig('gettingstarted/static/test.png')
        #canvas = FigureCanvas(f)
        im = Image.new(mode='F',size=(300,200))
        left = 10
        top = 10
        right = 100
        bottom = 100
        cropped_image = im.crop( (left, top, right, bottom) )
        response = django.http.HttpResponse(cropped_image, content_type='image/png')
        #canvas.print_png(response)
        response['Content-Disposition'] = 'attachment; filename="test.png"'
        '''
        f.savefig('gettingstarted/static/test.png')
        #f.show()
        #return response

    else:
        f.savefig(save_to)

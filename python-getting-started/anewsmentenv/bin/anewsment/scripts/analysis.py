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

    df2 = pd.DataFrame(f)

    df = df.set_index(pd.to_datetime(date))
    

    df = df.groupby(pd.TimeGrouper('D')).mean()
    rv1 = df.dropna()

    df2 = df2.set_index(pd.to_datetime(rv1.index))
    rv = pd.concat([rv1, df2], axis=1)
    rv['date'] = rv.index

    return rv




def get_plots(data, save_to = None):

    '''
    Plot results from Query input given
    by the user.
    Input: A pandas DataFrame containing
          all relevant information resulting
          from the Query
    Returns:
            A Figure with for subplots analyzing 
            descriptive statitistics related to 
            the Query
            i) scatterplot (%) in indicator vs. text nltk
            ii) scatterplot title vs. text nltk
            iii) Histograms title vs. text nltk
            iv) Time series behavior (%) in indicator vs. text nltk
    '''

    # Compute Percent change in findata
    ch_findata = data.findata.pct_change()*100
    I = pd.notnull(ch_findata)

    # Inputs for scatter plots
    colors = np.random.rand(len(data.date))
    colors2 = np.random.rand(len(data.date[I]))
    area = np.pi * (15 * np.array([0.6]*len(data.date)))**2  # 0 to 15 point radii
    
    # Linear fit for nltk comparison scores
    x = np.array(data.scores_text)
    y = np.array(data.scores_title)
    m, b = np.polyfit(x, y, 1)
    # Fontsize
    num = 12

    # Correlations
    corr1 = data.scores_text[I].corr(data.findata)
    corr2 = data.scores_text.corr(data.scores_title)
    #Create subplots
    f, axarr = plt.subplots(2, 2)

    axarr[0,0].scatter(ch_findata[I], data.scores_text[I], s=area, c=colors2, alpha=0.5, label= '{0:.3g}'.format(corr1))
    axarr[0,0].legend(loc='upper right')
    axarr[0,0].grid()
    axarr[0,0].set_title('Scatterplot financial data vs. nltk text', fontsize = num)
    axarr[0,0].set_xlabel('(%) change in indicator')
    axarr[0,0].set_ylabel('text score')
    # Comparison scatterplot
    axarr[0,1].scatter(data.scores_title, data.scores_text, s=area, c=colors, alpha=0.5, label= '{0:.3g}'.format(corr2))
    axarr[0,1].legend(loc='upper right')
    axarr[0,1].plot(x, m*x + b, '-')
    axarr[0,1].grid()
    axarr[0,1].set_title('Scatterplot nltk title vs. text', fontsize = num)
    #axarr[0,1].tick_params(axis='x',labelsize=5,width=2)
    axarr[0,1].set_xlabel('title score')
    axarr[0,1].set_ylabel('text score')
    # Histograms
    axarr[1,0].hist(data.scores_title.dropna(), alpha=0.5, label= "title")
    axarr[1,0].hist(data.scores_text.dropna(), alpha=0.5, label= "text")
    axarr[1,0].legend(loc='upper right')
    axarr[1,0].grid()
    axarr[1,0].set_title('Nltk Histograms title and text', fontsize = num)
    # Time series subplot
    axarr[1,1].plot(data.date[I], data.scores_text[I])
    ax2 = axarr[1,1].twinx()
    ax2.plot(data.date[I], ch_findata[I], color="g")
    axarr[1,1].grid()
    axarr[1,1].set_title('Time series nltk text vs. financial data', fontsize = num)
    axarr[1,1].tick_params(axis='x', labelsize=5, width =2)
    axarr[1,1].set_ylabel('text score')
    ax2.set_ylabel('(%) change in indicator')
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
        f.savefig('newsapp/static/test.png')
        #f.show()
        #return response

    else:
        f.savefig(save_to)

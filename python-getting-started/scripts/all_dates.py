from datetime import date, timedelta as td
import re
from newsapp.models import Date

def get_date_ints(article_date):
    pattern = r'(?<=0)\d|\d{4}|[^/0]\d*'
    date_ints = re.findall(pattern, article_date)
    #print(date_ints)
    y,m,d = date_ints
    return int(y),int(m),int(d)

def run(date1,date2):
    '''
    Will create a list of dates between given lower and upper date bounds
    Inputs:
        date1 = lower-bound date tuple
        date2 = upper-bound date tuple
    Outputs:
        date_list = list of dates between ranges
    '''
    y1,m1,d1 = get_date_ints(date1)
    y2,m2,d2 = get_date_ints(date2)

    process_date1 = date(y1, m1, d1)
    process_date2 = date(y2, m2, d2)

    delta = process_date2 - process_date1

    for i in range(delta.days + 1):
        dj_date = Date(date=str(process_date1 + td(days=i)))
        dj_date.save()
ref1 = 'http://pqasb.pqarchiver.com/latimes/results.html?st=advanced&QryTxt=White+House&type=current&sortby=CHRON&datetype=0&frommonth=01&fromday=01&fromyear=1985&tomonth=02&today=08&toyear=2017&By=&Title=&at_curr=ALL&Sect=ALL'

'''
ref2 =http://pqasb.pqarchiver.com/<SOURCE>/results.html?st=advanced&QryTxt=<text1>+<text2>+...<textN>&type=current&sortby=CHRON&datetype=0&frommonth=<MONTH # FROM>&fromday=<DAY # FROM>&fromyear=<YEAR # FROM>&tomonth=<MONTH # TO>&today=<DAY # TO>&toyear=<YEAR # TO>&By=&Title=&at_curr=ALL&Sect=ALL
'''

def get_input(source, text, from_month, from_day, from_year, to_month, to_day, to_year):

    text_split = text.split()[0]

    archive_url = 'http://pqasb.pqarchiver.com/'+source+'/results.html?st=advanced&QryTxt='\
    +text_split+'&type=current&sortby=CHRON&datetype=0&frommonth='\
    +'&frommonth='+from_month+'&fromday='+from_day+'&fromyear='+from_year+'&tomonth='+'&today='+to_day+'&toyear='+to_year+\
    '&By=&Title=&at_curr=ALL&Sect=ALL' #need to fix text part for multiple text input

    return archive_url


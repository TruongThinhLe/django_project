from datetime import datetime

def rate(date_end,date_start):
    now=datetime.date(datetime.now())
    if (date_end-date_start).days==0:
        calc=100
        return calc
    else:
        calc=int(((now-date_start).days)/((date_end-date_start).days)*100)
        return calc
from datetime import datetime

def rate(date_end,date_start):
    now=datetime.date(datetime.now())
    return int(((now-date_start).days)/((date_end-date_start).days)*100)
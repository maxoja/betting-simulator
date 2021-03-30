__str_of_weekday = ['0-Mon', '1-Tue', '2-Wed', '3-Thu', '4-Fri', '5-Sat', '6-Sun']

def weekday_str(datetime):
    return __str_of_weekday[datetime.weekday()]

def hour_minute_str(datetime):
    return f'{datetime.hour:02d}{datetime.minute:02d}'
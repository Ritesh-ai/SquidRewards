# from datetime import datetime

# date = datetime.today()


# current_year = date.year
# current_month = date.month
# current_day = date.day

# --------------------------------------------------------------------
# from datetime import datetime, timedelta

# day = '12/Oct/2013'
# dt = datetime.strptime(day, '%d/%b/%Y')
# start = dt - timedelta(days=dt.weekday())
# end = start + timedelta(days=6)
# print(start)
# print(end)
# --------------------------------------------------------------------

# import pendulum

# today = pendulum.now()
# start = today.start_of('week')
# end = today.end_of('week')

# date_list = [str(start.year)+"-"+str(start.month)+"-"+str(i) for i in range(start.day, end.day+1)]


# import datetime 
# import calendar 
  
# def findDay(date):
#     date = date.replace("-"," ")
#     born = datetime.datetime.strptime(date, '%Y %m %d').weekday()
#     return (calendar.day_name[born]) 


# for date in date_list:
#     print(findDay(date))

#----------------------------------------------------------------------
import datetime


year = datetime.datetime.now().year
month = datetime.datetime.now().month

print(year,"-----",month)



d0 = datetime.datetime(year=year, month=month, day=1)
if month == 12:
    d1 = datetime.datetime(year=year+1, month=1, day=1)
else:
    d1 = datetime.datetime(year=year, month=int(month+1), day=1)
# print ((d1 - d0).days)

print(d0)
# print(d1)
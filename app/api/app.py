
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import re
import time

import sys
sys.path.append("./")
from config import *

from .controller import Collection


cred = credentials.Certificate('./credentails/key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : DATABASE_URL
})


application = Flask(__name__)
CORS(application)

# Configurations
application.config.from_object('config')

# Stamps Collected In last 7 days
@application.route("/stampCollect", methods=['GET', 'POST'])
def stampCollect():
    root = db.reference('Purchases')
    datesCount = 0
    epochNow = int(time.time())
    
    for k in root.get().values():
        r1 = re.findall(r'(\d+/\d+/\d+)',str(k))

        for date in r1:
            year  = int(date.split("/")[-1])
            month = int(date.split("/")[1])
            day   = int(date.split("/")[0])

            epochs = int(datetime(year,month,day,0,0).timestamp())

            if (epochNow - epochs) < 604800:
                datesCount+=1

    # return {"Stamps Collected In last 7 days ":datesCount}
    return jsonify({"Value":25})
# Unredeemed Vouchers
@application.route("/unredeemVoucher", methods=['GET', 'POST'])
def unredeemVoucher():
    pass


# Stamps Collected - InComplete Right Now
@application.route("/stampCollected", methods=["GET", "POST"])
def stampCollected():
    # if request.method == "POST":
        # startinterval = request.json['startinterval']
        # endinterval   = request.json['endinterval']
        # breakdown     = int(request.json['breakdown'])  # 0 - No break Down, 1 - Gender, 2 - Age Group
    
    startinterval = '12/06/2018'
    endinterval   = '18/06/2018'
    breakdown     = 0  # 0 - No break Down, 1 - Gender, 2 - Age Group
    
    startdate = datetime(day=1,month=11,year=2019)
    enddate   = datetime(day=25,month=11,year=2019)

    user = db.reference('Purchases')
    dict1 = {}
    for v in user.get().values():
        for i in v.values():
            for k, j in i.items():
                # print(k,"---------",j)
                r1 = re.findall(r'(\d+/\d+/\d+)',str(j))
                dates = []
                for date in r1:
                    date_li = date.split("/")
                    newDate = datetime(day=int(date_li[0]),month=int(date_li[1]),year=int(date_li[2]))
                    if startdate <= newDate <= enddate:
                        dates.append(newDate)
                dict1[k] = len(dates)

    for key, values in dict1.items():
        user = db.reference('Users/'+str(key))

        if breakdown == 1:
            # Arranged by the Gender
            gender = user.get()['Gender']
            print(gender)
        elif breakdown == 2:
            # Arranged by the Age Group
            dob = user.get()['Date of Birth'].split("/")
            year  = int(dob[2])
            month = int(dob[1])
            day   = int(dob[0])
            result = Collection().calculateAge(year, month, day)
            print(result)
        else:
            pass

    return dict1    # Total Stamp Collected by the User
        
# Rewards Redeemed By Selected Date
@application.route("/rewardRedeem", methods=["GET", "POST"])
def rewardRedeem():
    # if request.method == "POST":
        # startinterval = request.json['startinterval']
        # endinterval   = request.json['endinterval']
        # breakdown     = int(request.json['breakdown'])  # 0 - No break Down, 1 - Gender, 2 - Age Group
    
    startinterval = '12/06/2018'
    endinterval   = '18/06/2018'
    breakdown     = 2  # 0 - No break Down, 1 - Gender, 2 - Age Group
    
    startdate = datetime(day=1,month=11,year=2019)
    enddate   = datetime(day=25,month=11,year=2019)

    root = db.reference('Redemptions')
    dict1 = {}
    for v in root.get().values():
        for i in v.values():
            for k, j in i.items():
                # print(k,"---------",j)
                r1 = re.findall(r'(\d+/\d+/\d+)',str(j))
                dates = []
                for date in r1:
                    date_li = date.split("/")
                    newDate = datetime(day=int(date_li[0]),month=int(date_li[1]),year=int(date_li[2]))
                    if startdate <= newDate <= enddate:
                        dates.append(newDate)
                        dict1[k] = len(dates)

    print("-----"*80)
    print(dict1)
    print("-----"*80)
    for key, values in dict1.items():
        user = db.reference('Users/'+str(key))

        if breakdown == 1:
            # Arranged by the Gender
            gender = user.get()['Gender']
            print(gender)
        elif breakdown == 2:
            # Arranged by the Age Group
            dob = user.get()['Date of Birth'].split("/")
            year  = int(dob[2])
            month = int(dob[1])
            day   = int(dob[0])
            result = Collection().calculateAge(year, month, day)
            print(result)
        else:
            pass

    return dict1    # Total Stamp Collected by the User

# Rewards Redeemed By Day
@application.route("/rewardRedeembyDay", methods=["GET", "POST"])
def rewardRedeembyDay():
    start = time.time()
    if request.method == "POST":
        breakdown = int(request.json['breakdown'])  # 0 - No break Down, 1 - Gender, 2 - Age Group

        # breakdown = 0           # 0 - No break Down, 1 - Gender, 2 - Age Group
        Userdict = {}
        date = datetime.today()

        root = db.reference('Redemptions')

        for v in root.get().values():
            for i in v.values():
                for k, j in i.items():
                    v03   = 0
                    v36   = 0
                    v69   = 0
                    v912  = 0
                    v1215 = 0
                    v1518 = 0
                    v1821 = 0
                    v2124 = 0

                    for l in j.values():
                        dateDB = l['Date'].split("/")
                        year  = int(dateDB[2])
                        month = int(dateDB[1])
                        day   = int(dateDB[0])

                        if date.year == year and date.month == month and date.day == day:
                            hour = int(l['Time'].split(':')[0])
                            if hour > 0 and hour < 3:
                                v03+=1
                            elif hour > 3 and hour < 6:
                                v36+=1
                            elif hour > 6 and hour < 9:
                                v69+=1
                            elif hour > 9 and hour < 12:
                                v912+=1
                            elif hour > 12 and hour < 15:
                                v1215+=1
                            elif hour > 15 and hour < 18:
                                v1518+=1
                            elif hour > 18 and hour < 21:
                                v1821+=1
                            elif hour > 21 and hour < 24:
                                v2124+=1
                            else:
                                pass
                        
                    if k not in [i for i in Userdict.keys()]:
                        Userdict[k] = {'0-3':v03, '3-6':v36, '6-9':v69, '9-12':v912, '12-15':v1215, '15-18':v1518, '18-21':v1821, '21-24':v2124}
                    else:
                        Userdict[k]['0-3']  +=v03
                        Userdict[k]['3-6']  +=v36
                        Userdict[k]['6-9']  +=v69
                        Userdict[k]['9-12'] +=v912
                        Userdict[k]['12-15']+=v1215
                        Userdict[k]['15-18']+=v1518
                        Userdict[k]['18-21']+=v1821
                        Userdict[k]['21-24']+=v2124

        _temp1 = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
        _temp2 = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
        _temp3 = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}
        _temp4 = {'0-3':0, '3-6':0, '6-9':0, '9-12':0, '12-15':0, '15-18':0, '18-21':0, '21-24':0}

        print("MidTime - ",time.time()-start)
        Userdict = {
            '1L0yTMo0Vagfk0yJHesdXTYeNl6': {'0-3': 1, '3-6': 4, '6-9': 0, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}, 
            '6cDldDd83QG0w2NtxhN1qtuRiea': {'0-3': 0, '3-6': 0, '6-9': 7, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}, 
            '8hhAjvm6Z6Qwws23ptG0LEwWalQ': {'0-3': 5, '3-6': 3, '6-9': 3, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}, 
            'CB8ie9exDiggDSziOMAasTOVQyd': {'0-3': 0, '3-6': 0, '6-9': 0, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}, 
            'D3lQTI12u8JvPS57z4Thp1OWpIP': {'0-3': 0, '3-6': 0, '6-9': 0, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}, 
            'UNZLXJ1KJj4PZqybXIMkktgVO57': {'0-3': 0, '3-6': 0, '6-9': 0, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}, 
            'iZUuhlSH5cVHoOfR32flMZxoJQ6': {'0-3': 0, '3-6': 0, '6-9': 0, '9-12': 0, '12-15': 0, '15-18': 0, '18-21': 0, '21-24': 0}
            }

        if breakdown == 1:
            # Arranged by the Gender
            for key, values in Userdict.items():
                user = db.reference('Users/'+str(key))
                gender = user.get()['Gender']
                for key, value in values.items():
                    if gender == 'male':
                        _temp1[key] +=value           
                    elif gender == 'female':
                        _temp2[key] +=value
                    elif gender == 'other':
                        _temp3[key] +=value
                    else:
                        pass

            print("Total time taken : ",time.time()-start)
            return jsonify({'male':_temp1, 'female':_temp2, 'other':_temp3})

        elif breakdown == 2:
            # Arranged by the Age Group
            for key, values in Userdict.items():
                user = db.reference('Users/'+str(key))
                dob = user.get()['Date of Birth'].split("/")
                year  = int(dob[2])
                month = int(dob[1])
                day   = int(dob[0])
                result = int(Collection().calculateAge(year, month, day))
                # print(result)
                for key, value in values.items():
                    if result > 0 and result < 25:
                        _temp1[key] +=value
                    elif result > 25 and result < 50:
                        _temp2[key] +=value
                    elif result > 50 and result < 75:
                        _temp3[key] +=value
                    elif result > 75:
                        _temp4[key] +=value
            print("Total time taken : ",time.time()-start)
            return jsonify({'0-25':_temp1, '25-50':_temp2, '50-75':_temp3, '75 above':_temp4})

        else:
            for v in Userdict.values():
                for key, value in v.items():
                    _temp1[key] += value
            
            print("Total time taken : ",time.time()-start)
            return jsonify(_temp1)
        
def findDay(date):
    import calendar
    date = date.replace("-"," ")
    born = datetime.strptime(date, '%Y %m %d').weekday()
    return (calendar.day_name[born]) 


# Rewards Redeemed By Day
@application.route("/rewardRedeembyWeek", methods=["GET", "POST"])
def rewardRedeembyWeek():
    starttime = time.time()
    dict1 = {'Sunday':0, 'Monday':0, 'Tuesday':0, 'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0}
    import pendulum
    
    today = pendulum.now()
    start = today.start_of('week')
    end = today.end_of('week')

    # date_list = [str(start.year)+"-"+str(start.month)+"-"+str(i) for i in range(start.day, end.day+1)]
    date_list = ['2019-6-23', '2019-6-24', '2019-6-25', '2019-6-26', '2019-6-27', '2019-6-28', '2019-6-29']

    root = db.reference('Redemptions')

    for v in root.get().values():
        for i in v.values():
            for j in i.values():
                for l in j.values():
                    date = l['Date'].split("/")
                    year  = int(date[2])
                    month = int(date[1])
                    day   = int(date[0])
                    
                    for date in date_list:
                        year1  = int(date.split("-")[0])
                        month1 = int(date.split("-")[1])
                        day1  = int(date.split("-")[2])

                        if year == year1 and month == month1 and day == day1:
                            # print(findDay(date))
                            dict1[findDay(date)] += 1
                            date = l['Date'].split("/")

    print("Total time taken : ",time.time()-starttime)
    return jsonify(dict1)

# Rewards Redeemed By Month
@application.route("/rewardRedeembyMonth", methods=["GET", "POST"])
def rewardRedeembyMonth():
    pass

# if __name__ == "__main__":
#     application.run(host='0.0.0.0', port='8000')
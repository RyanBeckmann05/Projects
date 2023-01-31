import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np
import time
import requests
import io
import csv
import calendar

SPY_price_history = [176.020004, 181.089996, #2013
                 183.979996, 177.970001, 184.649994, 187.619995, 188.220001, 192.949997, 196.199997, 192.559998, 200.970001, 196.699997, 201.919998, 206.399994, #2014
                 206.380005, 200.050003, 210.779999, 206.389999, 209.399994, 211.940002, 207.729996, 210.460007, 193.119995, 192.080002, 208.320007, 209.440002, #2015
                 200.490005, 192.529999, 195.009995, 204.350006, 206.919998, 209.119995, 209.479996, 217.190002, 217.369995, 215.820007, 212.929993, 220.729996, #2016
                 225.039993, 227.529999, 238.389999, 235.800003, 238.679993, 241.970001, 242.880005, 247.460007, 247.919998, 251.490005, 258.040009, 264.760010, #2017
                 267.839996, 281.070007, 271.410004, 262.549988, 263.869995, 272.410004, 269.510010, 281.559998, 289.839996, 292.109985, 271.600006, 280.279999, #2018
                 245.979996, 270.149994, 280.440002, 284.700012, 294.720001, 275.309998, 296.679993, 297.600006, 290.570007, 297.739990, 304.920013, 314.589996, #2019
                 323.540009, 323.350006, 298.209991, 247.979996, 285.309998, 303.619995, 309.570007, 328.320007, 350.209991, 337.690002, 330.200012, 365.570007, #2020
                 375.309998, 373.720001, 385.589996, 398.399994, 419.429993, 422.570007, 428.869995, 440.339996, 452.559998, 430.980011, 460.299988, 461.640015, #2021
#                 476.299988, 450.679993, 435.040009, 453.309998, 412.070007, 415.170013, 376.559998, 409.149994, 392.890015 #2022
                 ]

contracts = ""
basis_price = 365 # SPY price 9/26/22 for OG model , Constant
month_number = 0 # Constant
new_price = 0 # Constant
fixer = 0
option1_list = []
option2_list = []
option3_list = []
finished_options1 = []
finished_options2 = []
finished_options3 = []
option1_price = []
option2_price = []
option3_price = []
finished_new_price1 = []
finished_new_price2 = []
new_price_list1 = []
new_price_list2 = []
pl1 = []
pl2 = []
pl3 = []
rows = []
rowdict = {}
counter = 0
syear = 2013
sm = 11 # Variable
sd = 1
smonth = 0 # Constant
sday = '0' + str(sd)  # Constant
eyear = 0
emonth = 0
eday = 0
em = 0
indexspec = 0

smonth = 0 # Constant

start = dt.date(year=2013, month=11, day=1) # Variable
end = dt.date(start.year+8, 12, 31)
business_days_rng = pd.date_range(start, end, freq='BM')
print(business_days_rng)

def lastbizday(year: int, month: int) -> int:
    return max(calendar.monthcalendar(year, month)[-1:][0][:5])

for i in SPY_price_history:
    strike = round(float(i))
    index = SPY_price_history.index(i) # Getting list location of the price
    bizdays_raw = business_days_rng[counter]
    print(bizdays_raw)

    if sm <= 9:
        smonth = str(sm).zfill(2)
    elif sm >= 10:
        smonth = sm

    sdayfixer = dt.date(int(syear), int(smonth), int(sday))
    sweekday = sdayfixer.weekday()
    sweekday = int(sweekday)

    em = int(smonth) + 6

    if sweekday == 1 or sweekday == 3 or sweekday == 6:
        sday = int(sday) + 1
    elif sweekday == 5:
        sday = int(sday) + 2
    else:
        sday = int(sday)

    if strike % 5 != 0:
        save = strike % 5
        strike = strike - save

    if str(bizdays_raw) == '2014-01-31 00:00:00':
        sday = 3
    if str(bizdays_raw) == '2014-04-30 00:00:00':
        sday = 1
    if str(bizdays_raw) == '2014-07-31 00:00:00':
        sday = 1
    if str(bizdays_raw) == '2014-09-30 00:00:00':
        sday = 2
    if str(bizdays_raw) == '2016-01-29 00:00:00':
        sday = 4
    if str(bizdays_raw) == '2017-01-31 00:00:00':
        sday = 3
    if str(bizdays_raw) == '2017-08-31 00:00:00':
        sday = 1
    if str(bizdays_raw) == '2018-01-31 00:00:00':
        sday = 2
    if str(bizdays_raw) == '2018-03-30 00:00:00':
        sday = 1
    if str(bizdays_raw) == '2018-05-31 00:00:00':
        sday = 1
    if str(bizdays_raw) == '2018-09-28 00:00:00':
        sday = 4
    if str(bizdays_raw) == '2019-03-29 00:00:00':
        sday = 4
    if str(bizdays_raw) == '2019-09-30 00:00:00':
        sday = 3
    if str(bizdays_raw) == '2019-10-31 00:00:00':
        sday = 1
    if str(bizdays_raw) == '2020-01-31 00:00:00':
        sday = 2
    if str(bizdays_raw) == '2021-01-29 00:00:00':
        sday = 4
    if str(bizdays_raw) == '2021-04-30 00:00:00':
        sday = 1

    if em > 3:
        if em % 3 == 1:
            fixer = 2
        elif em % 3 == 2:
            fixer = 1
        elif em % 3 == 0:
            fixer = 0
    elif em < 3:
        if em == 1:
            fixer = 2
        if em == 2:
            fixer = 1
    emonth = em + fixer

    if int(smonth) > 6:
        eyear = syear + 1
        emonth = emonth - 12
    elif int(smonth) <= 5:
        eyear = syear
        
    eday = lastbizday(eyear, emonth)
    if str(bizdays_raw) == '2017-07-31 00:00:00' or str(bizdays_raw) == '2017-08-31 00:00:00' or str(bizdays_raw) == '2017-09-29 00:00:00':
        eday = 29

    if emonth <= 9:
        emonth = '0' + str(emonth)

    bizdays = bizdays_raw

    with open('spy_eod_' + str(syear) + '-gghtsj/spy_eod_' + str(syear) + str(smonth) + '.txt', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            rowdict[row[' [QUOTE_DATE]'].strip() + ':' + row[' [STRIKE]'].strip() + ':' + row[' [EXPIRE_DATE]'].strip()] = row
            rows.append(row)

#    finished_options1.append(rowdict[str(syear) + '-' + str(smonth) + '-0' + str(sday) + ':' + str(strike) + '.000000:' + str(eyear) + '-' + str(emonth) + '-' + str(eday)])
#    print(rowdict[str(syear) + '-' + str(smonth) + '-0' + str(sday) + ':' + str(strike) + '.000000'])# + ':' + str(bizdays)])
#    print(rowdict[str(syear) + '-' + str(smonth) + '-0' + str(sday) + ':' + str(strike) + '.000000:' + str(eyear) + '-' + str(emonth) + '-' + str(eday)])

    #    print("\n\n\nOpton 1:\n")

    ### Edits 1:

    finished_options1.append(rowdict[str(syear) + '-' + str(smonth) + '-0' + str(sday) + ':' + str(strike) + '.000000:' + str(eyear) + '-' + str(emonth) + '-' + str(eday)])
    option1_price.append(finished_options1[index][' [C_LAST]'])
    
#    print("\n\n\nOpton 2:\n")

    ### Edits 2:

    finished_options2.append(rowdict[str(syear) + '-' + str(smonth) + '-0' + str(sday) + ':' + str(strike) + '.000000:' + str(eyear) + '-' + str(emonth) + '-' + str(eday)])
    option2_price.append(finished_options2[index][' [P_LAST]'])


    for x in option1_price:
        indexspec = option1_price.index(x)
        option1_price[indexspec] = x.replace(' ', '')
    for x in option2_price:
        indexspec = option2_price.index(x)
        option2_price[indexspec] = x.replace(' ', '')

    if str(bizdays_raw) == '2019-09-30 00:00:00': # Spec fix
        bizdays = '2019-09-27 00:00:00'
    if str(bizdays_raw) == '2018-03-30 00:00:00': # Spec fix
        bizdays = '2018-03-29 00:00:00'
    if str(bizdays_raw) == '2021-05-31 00:00:00': # Spec fix
        bizdays = '2021-05-28 00:00:00'
        
    newbizdays = str(bizdays).replace(' 00:00:00', '')

    new_price_list1.append(rowdict[str(newbizdays) + ':' + str(strike) + '.000000:' + str(eyear) + '-' + str(emonth) + '-' + str(eday)])
    finished_new_price1.append(new_price_list1[index][' [C_LAST]'])
    new_price_list2.append(rowdict[str(newbizdays) + ':' + str(strike) + '.000000:' + str(eyear) + '-' + str(emonth) + '-' + str(eday)])
    finished_new_price2.append(new_price_list2[index][' [P_LAST]'])

    for x in finished_new_price1:
        indexspec = finished_new_price1.index(x)
        finished_new_price1[indexspec] = x.replace(' ', '')
    for x in finished_new_price2:
        indexspec = finished_new_price2.index(x)
        finished_new_price2[indexspec] = x.replace(' ', '')
    

    print('Calculating month ' + str(index) + '...')

    pl1.append((float(finished_new_price1[index]) - float(option1_price[index])) * 600)
#        print(sum(pl1))
        
    pl2.append((float(finished_new_price2[index]) - float(option2_price[index])) * 300)
#        print(sum(pl2))

    print('\n')
    print(round(pl1[index]))
    print(round(pl2[index]))
    print('Month ' + str(index + 1) + ': ' + str(int(pl1[index]) + int(pl2[index])))
    print('\n')
    

    counter = counter + 1

    sday = 1
    sm = sm + 1
    if sm == 13:
        sm = sm - 12
        syear = syear + 1

if int(index) == 97:
    end = sum(pl1) + sum(pl2)
    print(end)
#    print(sum(option1_price) + sum(option2_price))

















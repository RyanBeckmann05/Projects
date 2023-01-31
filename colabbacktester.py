#!pip install yfinance
'''
'''
from scipy.stats import norm
import scipy.stats as stats

import math
import yfinance as yf
import numpy as np

import pandas as pd
from pandas.io import parsers
from pandas.core.indexes.period import parse_time_string
from pandas.tseries.holiday import *
from pandas.tseries.frequencies import DAYS

import datetime
from datetime import date, timedelta
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.dates as mdates

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.easter import easter
'''
'''
weekdeltaspec = relativedelta(days=2)
start_year = 1995
end_year = date.today().year
good_fridays = []
for year in range(start_year, end_year+1):
    good_friday = easter(year) - weekdeltaspec
    date_string = good_friday.strftime("%Y-%m-%d")
    good_fridays.append(date_string)
balanceput_list = []
balancecall_list = []
call_list = []
put_list = []
iv_list = []
rf_list = []
pu_list = []
sp_list = []
date_list = []
btdate_list = []
listoflists = [call_list, put_list, iv_list, rf_list, pu_list, sp_list]
balance = 0
ivover = False
remover = 0
pd.options.display.max_columns=10
e = 2.71828
bond = yf.Ticker("^IRX")
vol = yf.Ticker("^VIX")
underlying = yf.Ticker("SPY")
day_delta = relativedelta(days=1)
week_delta = relativedelta(days=7)
month_delta = relativedelta(months=1)
year_delta = relativedelta(years=1)
df = underlying.history(period='max')
sdt = datetime(1990, 1, 1)
edt = date.today()
cal = USFederalHolidayCalendar()
holidays = []
for holiday in cal.holidays(start=sdt, end=edt):
    holiday = str(holiday)
    holidays.append(holiday)
class Clear:
    def __init__(self, call_list, put_list, sp_list, iv_list, rf_list, pu_list, date_list, balanceput_list, balancecall_list):
        self.call_list=call_list.clear()
        self.put_list=put_list.clear()
        self.sp_list=sp_list.clear()
        self.iv_list=iv_list.clear()
        self.rf_list=rf_list.clear()
        self.pu_list=pu_list.clear()
        self.date_list=date_list.clear()
        self.balanceput_list=balanceput_list.clear()
        self.balancecall_list=balancecall_list.clear()
    def clearlists(self):
        call_list = self.call_list
        put_list = self.put_list
        sp_list = self.sp_list
        iv_list = self.iv_list
        rf_list = self.rf_list
        pu_list = self.pu_list
        date_list = self.date_list
        balanceput_list = self.balanceput_list
        balancecall_list = self.balancecall_list
    def clearbalance(self):
        balance = 0
'''
'''
class BlackScholes:
    def __init__(self, sp, te, datetime_obj, atm, printing):
        self.sp = sp
        self.te = te/365
        self.datetime_obj = datetime_obj
        self.atm = atm
        self.printing = printing
        self.call = None
        self.put = None
        self.test_date = None
        
    def date_fixer(self):
        if str(self.datetime_obj) in holidays:
            self.datetime_obj += day_delta
        test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        tof = bool(len(pd.bdate_range(test_date, test_date)))
        while tof == False:
            self.datetime_obj += day_delta
            if str(self.datetime_obj) in holidays:
                self.datetime_obj += day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
            tof = bool(len(pd.bdate_range(test_date, test_date)))
            if tof == True:
                break

        if str(test_date) in good_fridays:
            self.datetime_obj -= day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        elif str(test_date) == '2001-09-11' or str(test_date) == '2001-09-12' \
        or str(test_date) == '2001-09-13' or str(test_date) == '2001-09-14' \
        or str(test_date) == '2001-09-15' or str(test_date) == '2001-09-16' \
        or str(test_date) == '2001-09-17': # 9/11 :(
            self.datetime_obj += week_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        elif str(test_date) == '2004-06-11': # Reagen Funeral
            self.datetime_obj += day_delta
            self.datetime_obj += day_delta
            self.datetime_obj += day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        elif str(test_date) == '2007-01-02': # National Day of Mourning
            self.datetime_obj += day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        elif str(test_date) == '2012-10-29' \
        or str(test_date) == '2012-10-30': # Hurricane Sandy
            self.datetime_obj += day_delta
            self.datetime_obj += day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        elif str(test_date) == '2018-12-05': # Mourning George Bush
            self.datetime_obj += day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')
        elif str(test_date) == '2022-06-20': # Juneteenth
            self.datetime_obj += day_delta
            test_date = str(self.datetime_obj).replace(' 00:00:00', '')

        date_list.append(test_date)
        self.test_date = test_date
        return test_date

    def calculate_contract(self, test_date):
        global sp
        find = [bond, vol, underlying]
        found = []

        for i in find:
            i = i.history(period='max')#, auto_adjust=False)
            found.append(float(i.loc[test_date, 'Close']))
                   
        rf = found[0]/100
        iv = found[1]/100
        pu = round(found[2], 2) 

        rf = rf # only change if testing none historic value
        iv = iv # only change if testing none historic value
        pu = pu # only change if testing none historic value

        if self.atm == True:
            self.sp = pu

        sp_list.append(self.sp)
        rf_list.append(rf*100)
        iv_list.append(iv*100)
        pu_list.append(pu)
        
        d1 = round((math.log(pu/self.sp) + (rf+.5*(iv**2))*self.te) / (iv*float(math.sqrt(self.te))), 2)
        d2 = round(float(d1) - iv*float(math.sqrt(self.te)), 2)
        
        self.call = pu * \
               norm.cdf(d1) - \
               self.sp / e ** (rf*self.te) * \
               norm.cdf(d2)

        self.put = self.call + \
              self.sp / e ** (rf*self.te) - \
              pu
        
        call_list.append(round(self.call*100, 2))
        put_list.append(round(self.put*100, 2))
        btcall = self.call*100
        btput = self.put*100

        if self.printing == True:
            print('Date checked: ' + test_date)
            print('SPY price: $' + str(pu) + \
                  '\nStrike price: $' + str(round(self.sp, 2)) + \
                  '\nRisk free rate: ' + str(round(rf*100, 2)) + '%' + \
                  '\nImplied volatility: ' + str(round(iv*100, 2)) + '%')
            print('Call price: $' + str(round(self.call*100, 2)) + \
                  '\nPut price: $' + str(round(self.put*100, 2)) + '\n')

        sp = self.sp    
        return_values = [btcall, btput, sp, rf, iv, pu, sp_list, rf_list, iv_list, pu_list, call_list, put_list]
        return return_values

    def backtestit(self, return_values):
        global te
        global balanceput
        global balancecall
        global ivover
        global remover
        btdatetime_obj = datetime_obj
        btcall = return_values[0]
        btput = return_values[1]
        sp = return_values[2]
        rf = return_values[3]
        iv = return_values[4]
        pu = return_values[5]
        sp_list = return_values[6]
        rf_list = return_values[7]
        iv_list = return_values[8]
        pu_list = return_values[9]
        call_list = return_values[10]
        put_list = return_values[11]
        if ivover:
            remover = -3
            ivover = False
        else:
            remover = -2
            ivover = False
        if len(iv_list) >= 3:
            if int(iv_list[-1]) / int(iv_list[remover]) >= 1:
                print(str(self.datetime_obj) + ' IV change traded')
                amt_to_buyput = round((balanceput / int(put_list[-1]))*.04)
                amt_to_buycall = round((balancecall / int(put_list[-1]))*.04)
                balanceput += amt_to_buyput*int(put_list[-1]) # simulating selling the contract
                balancecall += amt_to_buycall*int(call_list[-1])

                btsp = sp_list[-1]
                te = (te - buyselltime)#/365 # simulating the waiting time before buyer executes
                btdatetime_obj += relativedelta(days=buyselltime) # simulating a month ahead
                btbs = BlackScholes(btsp, te, btdatetime_obj, atm=False, printing=True)
                btfixed_date = btbs.date_fixer()
                btoutput = btbs.calculate_contract(btfixed_date)
                btdate_list.append(btbs.test_date)

                balanceput -=  amt_to_buyput*int(put_list[-1]) # simulating buying the contract back
                balancecall -= amt_to_buycall*int(call_list[-1])
                balanceput_list.append(balanceput)
                balancecall_list.append(balancecall)
                ivover = True

                print('Price of underlying: $' + str(pu_list[-2]) + ' --> $' + str(pu_list[-1]))
                print('Implied volatility: ' + str(round(iv_list[-2], 2)) + '% --> ' + str(round(iv_list[-1], 2)) + '%')
                print('Call balance: $' + str(balancecall) + \
                      '\nPut balance: $' + str(balanceput) + '\n') # leftover
'''
'''
Clear(call_list, put_list, sp_list, iv_list, rf_list, pu_list, date_list, balanceput_list, balancecall_list).clearlists()
balance = 1000000
balanceput = balance
balancecall = balance
print('Running...')


'''
Inputs:
'''
sp = 100 # strike price, ignore if atm = True
dte = 8 # days till expiration
year = 2020 # earliest 1995, stops after; 14 years 6 months
month = 1
day = 2 # will not print second month if above 29
atm = True
printing = True
backtesting = True
periods = 'weekly' # monthly, weekly, daily

'''
Backtester
'''
datetime_str = '' + str(month) + '/' + str(day) + '/' + str(year) + ' 00:00:00'
datetime_obj = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M:%S')
today = date.today()
while True:
    te = dte
    if str(datetime_obj.year) >= str(today.year):
        if datetime_obj.date() >= datetime.today().date():
            break
    bs = BlackScholes(sp, te, datetime_obj, atm, printing)
    if periods.lower().strip() == 'monthly':
        fixed_date = bs.date_fixer()
        buyselltime = 30
        get_data = bs.calculate_contract(fixed_date)
        if backtesting:
            output = bs.backtestit(get_data)
        datetime_obj += month_delta

    elif periods.lower().strip() == 'weekly':
        fixed_date = bs.date_fixer()
        buyselltime = 7
        get_data = bs.calculate_contract(fixed_date)
        if backtesting:
            output = bs.backtestit(get_data)
        datetime_obj += week_delta

    elif periods.lower().strip() == 'daily':
        fixed_date = bs.date_fixer()
        buyselltime = 1
        get_data = bs.calculate_contract(fixed_date)
        if backtesting:
            output = bs.backtestit(get_data)
        datetime_obj += day_delta
print('Done')
'''
'''
x_values = [mdates.date2num(parse(test_dates)) if datetime.strptime(test_dates, '%Y-%m-%d') else datetime.strptime(test_dates, '%Y-%m-%d') for test_dates in date_list]
btx_values = [mdates.date2num(parse(bttest_dates)) if datetime.strptime(bttest_dates, '%Y-%m-%d') else datetime.strptime(bttest_dates, '%Y-%m-%d') for bttest_dates in btdate_list]

corrector1 = len(x_values) - len(call_list)
corrector2 = len(call_list) - len(x_values)
while int(corrector1) != int(corrector2):
    if int(corrector1) > int(corrector2):
        x_values.pop(0)
        corrector1 = len(x_values) - len(call_list)
        corrector2 = len(call_list) - len(x_values)
    elif int(corrector1) < int(corrector2):
        call_list.pop(0)
        put_list.pop(0)
        pu_list.pop(0)
        corrector1 = len(x_values) - len(call_list)
        corrector2 = len(call_list) - len(x_values)

# RF values:
fig, rf_graph = plt.subplots(figsize=(10,6))
rf_graph.plot(x_values, rf_list, color='g', label='Rf')
rf_graph.set_xlabel("Dates")
rf_graph.set_ylabel("Percent")
rf_graph.set_ylim(0, int(max(rf_list)))
fig.autofmt_xdate()
rf_graph.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# Trendline for RF:
coefficients = np.polyfit(x_values, rf_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(x_values)
plt.plot(x_values, y_trend, '-')

# IV values:
fig, iv_graph = plt.subplots(figsize=(10,6))
iv_graph.plot(x_values, iv_list, color='purple', label='Iv')
iv_graph.set_xlabel("Dates")
iv_graph.set_ylabel("Percent")
iv_graph.set_ylim(0, int(max(iv_list)))
fig.autofmt_xdate()
iv_graph.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# Trendline for IV:
coefficients = np.polyfit(x_values, iv_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(x_values)
plt.plot(x_values, y_trend, '-')

# Options values:
fig, options_graph = plt.subplots(figsize=(10,6))
options_graph.plot(x_values, call_list, color='g', label='Call')
options_graph.plot(x_values, put_list, color='r', label='Put')
#options_graph.plot(x_values, pu_list, color='b', label='PU')
options_graph.set_xlabel("Dates")
options_graph.set_ylabel("Values")
options_graph.set_ylim(0, int(max(call_list)))
fig.autofmt_xdate()
options_graph.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# Trendline for Calls:
coefficients = np.polyfit(x_values, call_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(x_values)
plt.plot(x_values, y_trend, '-')
# Trendline for Puts:
coefficients = np.polyfit(x_values, put_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(x_values)
plt.plot(x_values, y_trend, '-')

btcorrector1 = len(btx_values) - len(balancecall_list)
btcorrector2 = len(balancecall_list) - len(btx_values)
while int(btcorrector1) != int(btcorrector2):
    if int(btcorrector1) > int(btcorrector2):
        btx_values.pop(0)
        btcorrector1 = len(btx_values) - len(balancecall_list)
        btcorrector2 = len(balancecall_list) - len(btx_values)
    elif int(btcorrector1) < int(btcorrector2):
        balancecall_list.pop(0)
        balanceput_list.pop(0)
        btorrector1 = len(btx_values) - len(balancecall_list)
        btcorrector2 = len(balancecall_list) - len(btx_values)

# Balance values:
fig, balances_graph = plt.subplots(figsize=(10,6))
balances_graph.plot(btx_values, balancecall_list, color='g', label='Call')
balances_graph.plot(btx_values, balanceput_list, color='r', label='Put')
balances_graph.set_xlabel("Dates")
balances_graph.set_ylabel("Values")
balancelimiter = balancecall_list + balanceput_list
balances_graph.set_ylim(0, int(max(balancelimiter)))
fig.autofmt_xdate()
balances_graph.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Trendline for call balance:
coefficients = np.polyfit(btx_values, balancecall_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(btx_values)
plt.plot(btx_values, y_trend, '-')
# Trendline for put balance:
coefficients = np.polyfit(btx_values, balanceput_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(btx_values)
plt.plot(btx_values, y_trend, '-')

# PU values:
fig, pu_graph = plt.subplots(figsize=(10,6))
pu_graph.plot(x_values, pu_list, color='b', label='Pu')
pu_graph.set_xlabel("Dates")
pu_graph.set_ylabel("Percent")
pu_graph.set_ylim(0, int(max(pu_list)))
fig.autofmt_xdate()
pu_graph.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# Trendline for PU:
coefficients = np.polyfit(x_values, pu_list, 52)
polynomial = np.poly1d(coefficients)
y_trend = polynomial(btx_values)
plt.plot(btx_values, y_trend, '-')

plt.legend()
plt.show()


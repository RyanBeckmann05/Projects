## Risk analysis with goal to find drawdown point after target hit, length of holding, close period, and P/L

#import pandas as pd

## Set stop loss

iv = 47
strike_price = 320
underlying_price = 380
delta = 36
theta = 19
days_to_exp = 88
months_to_exp = 0
close_check = 0

if underlying_price - strike_price > underlying_price + (underlying_price * 1.05): # Option is deep OTM, what we want
    close_check = 1
else: # Option is ITM, what we don't want
    close_check = 5
riv = iv / 100
rdelta = delta / 100
if days_to_exp <= 27:
    months_to_exp = 1
elif days_to_exp > 27:
    months_to_exp = 2
run_time = (days_to_exp / months_to_exp) * 1.4

est_month_price_movement = (rdelta * (riv * months_to_exp)) * underlying_price
optimal_holding_time = (theta * run_time) / (close_check + 3) * -1
est_stop_loss = ((optimal_holding_time - days_to_exp) * (est_month_price_movement * (days_to_exp / 100))) * ((iv + 1) / 10)
set_stop_loss = (est_stop_loss * 1.1) / 10

print(optimal_holding_time)
print(est_month_price_movement)
print(set_stop_loss)


'''
atm_check = 0
otm_check = 0
itm_check = 0
vega = 0
stock_price = int(input("Enter stock price: "))
sp = int(input("Enter option strike price: "))
miv = int(input("Enter stock implied volatility: ")) / 4
delta = int(input("Enter option  delta: ")) / 100
theta = int(input("Enter option theta: "))
premium = int(input("Enter option price: ")) * 100

if sp - stock_price >= -2.5 and sp - stock_price <= 2.5:
    vega = input("Enter option vega: ")
    atm_check = 1
elif sp - stock_price <= -2.5:
    otm_check = 1
elif sp - stock_price >= 2.5:
    itm_check = 1

new_miv_neg = stock_price - ((miv / 100) * stock_price)
new_miv_pos = stock_price + ((miv / 100) * stock_price)
dd = delta * new_miv_pos
p = delta * new_miv_neg - stock_price

print(dd)
print(p)
'''

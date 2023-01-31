import pandas as pd
import numpy as np

prev_price = 365 #Constant
new_price = 322

perc_change = ((prev_price - new_price) / 365) * -1

option1_sp = 305 #LP - Constant
option2_sp = 325 #SP - Constant
option3_sp = 345 #SC - Constant
option4_sp = 365 #LC - Constant

option1_sp = option1_sp + option1_sp * perc_change
option2_sp = option2_sp + option2_sp * perc_change
option3_sp = option3_sp + option3_sp * perc_change
option4_sp = option4_sp + option4_sp * perc_change

print("Option 1 SP = " + str(option1_sp))
print("Option 2 SP = " + str(option2_sp))
print("Option 3 SP = " + str(option3_sp))
print("Option 4 SP = " + str(option4_sp))
if option2_sp - option1_sp != option4_sp - option3_sp: #Distance of the LP->SP not equal to distance of LC->SC
    print("!!! Edit spread !!!")

rounded_option1 = option1_sp % 5
if rounded_option1 <= 2:
    rounded_option1 = option1_sp - rounded_option1
elif rounded_option1 > 2:
    rounded_option1 = option1_sp + (5 - rounded_option1)
rounded_option2 = option2_sp % 5
if rounded_option2 <= 2:
    rounded_option2 = option2_sp - rounded_option2
elif rounded_option2 > 2:
    rounded_option2 = option2_sp + (5 - rounded_option2)
rounded_option3 = option3_sp % 5
if rounded_option3 <= 2:
    rounded_option3 = option3_sp - rounded_option3
elif rounded_option3 > 2:
    rounded_option3 = option3_sp + (5 - rounded_option3)
rounded_option4 = option4_sp % 5
if rounded_option4 <= 2:
    rounded_option4 = option4_sp - rounded_option4
elif rounded_option4 > 2:
    rounded_option4 = option4_sp + (5 - rounded_option4)

print("\nRounded values if neded:")
print(rounded_option1)
print(rounded_option2)
print(rounded_option3)
print(rounded_option4)

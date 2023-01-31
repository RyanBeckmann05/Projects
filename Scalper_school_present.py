from bs4 import BeautifulSoup
import requests
import time

while True:

    # URL of website page you want to be checking
    s = 'https://www.newegg.com/msi-geforce-rtx-3090-rtx-3090'\
    '-gaming-x-trio-24g/p/N82E16814137595?Description=3090'\
    '&cm_re=3090-_-14-137-595-_-Product'
    url = str(s)
    

    # Obtiain the HTML imformation from the page
    # with Python's request library 
    result = requests.get(url)

    # Using BeautifulSoup's parsing
    # (analyzing the strings or sentences that make up the HTML file)
    # capability to find the price
    doc = BeautifulSoup(result.text, "html.parser")

    

    

    # Looking for the dollar sign, the only constant
    # in the price's text in order to further
    # find the price afterwords
    prices = doc.find_all(text="$")

    # Every letter and variable in a website has
    # a parent tag in the HTML file to identify it,
    # and the HTML file is like a family tree
    parent = prices[0].parent

    # Displaying the line of HTML code in order
    # for us to locate the tag, or parent, of
    # the dollar value for our product of interest
    print(parent) 





    # After manually finding the tag in the HTML file,
    # we find the associated value with the tag
    strong = parent.find("strong")

    # Making the value readable as
    # a string to the computer
    product_price = strong.string 

    # Displaying the price to us
    print('$' + product_price) 

    
    # Adding a delay to the porgram
    # to not ddos or get booted from the website
    time.sleep(3600)














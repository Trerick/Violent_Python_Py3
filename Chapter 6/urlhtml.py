#Program to parse html code from a target website
#Chapter 6 converted Python2 to Python3

import mechanicalsoup

def viewPage(url):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    source_code = browser.get_current_page()
    print(source_code)
viewPage('http://www.yahoo.com/')

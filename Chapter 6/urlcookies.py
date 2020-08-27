#Program to parse data contained within a cookie from a session
#Chapter 6 converted Python2 to Python3

import mechanicalsoup
import http.cookiejar


def showCookies(url):
    browser = mechanicalsoup.StatefulBrowser()
    cookieJar = http.cookiejar.CookieJar()
    browser.set_cookiejar(cookieJar)
    browser.open(url)

    for cookie in cookieJar:
        print(cookie.__dict__)


if __name__ == '__main__':
    tgtUrl = 'http://www.yahoo.com'
    showCookies(tgtUrl)

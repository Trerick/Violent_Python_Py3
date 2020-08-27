#Program to examine sqlite databases linked to a firefox profile
#Returns files downloaded, search history, and cookies of the ff profile
#Chapter 3 converted Python2 to Python3

import re
import argparse
import os
import sqlite3


def foxDownloads(downloadDB):
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    c.execute('SELECT name, source, datetime(endTime/1000000,\
    \'unixepoch\') FROM moz_downloads;'
              )
    print("\n[*] --- Files Downloaded --- ")
    for row in c:
        print("[+] File: " + str(row[0]) + " from source: " \
            + str(row[1]) + " at: " + str(row[2]))


def foxCookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies')

        print("\n[*] -- Found Cookies --")
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print("[+] Host: " + host + ", Cookie: " + name \
                + ", Value: " + value)
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error: Cannot read the cookies database.")
            print("[*] Python-Sqlite3 library requires upgrade")


def foxHistory(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, \
          'unixepoch') from moz_places, moz_historyvisits \
          where visit_count > 0 and moz_places.id==\
          moz_historyvisits.place_id;")

        print("\n[*] -- Found History --")
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print("[+] " + date + " - Visited: " + url)
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error: Cannot read the places database.")
            print("[*] Python-Sqlite3 library requires upgrade")
            exit(0)


def parseGoogle(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("select url, datetime(visit_date/1000000, \
      'unixepoch') from moz_places, moz_historyvisits \
      where visit_count > 0 and moz_places.id==\
      moz_historyvisits.place_id;")

    print("\n[*] -- Found Google --")
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'google' in url.lower():
            r = re.findall(r'q=.*\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('q=', '').replace('+', ' ')
                print("[+] "+date+" - Past Searches: " + search)


def main():
	argsParser = argparse.ArgumentParser()
	argsParser.add_argument('-P', '--pathName', help="specify Firefox location")
	args = argsParser.parse_args()
	pathName = args.pathName
	if pathName is None:
		print(argsparser.usage)
		exit(0)
	elif os.path.isdir(pathName) is False:
		print("[!] Path not found: " + pathName)
		exit(0)
	else:
		downloadDB = os.path.join(pathName, 'downloads.sqlite')
		if os.path.isfile(downloadDB):
			foxDownloads(downloadDB)
		else:
			print("[!] Downloads Db not found: " + downloadDB)
		cookiesDB = os.path.join(pathName, 'cookies.sqlite')
		if os.path.isfile(cookiesDB):
			pass
			foxCookies(cookiesDB)
		else:
			print("[!] Cookies Db not found:" + cookiesDB)
		placesDB = os.path.join(pathName, 'places.sqlite')
		if os.path.isfile(placesDB):
			foxHistory(placesDB)
			parseGoogle(placesDB)
		else:
			print("[!] PlacesDb not found: " + placesDB)



if __name__ == '__main__':
    main()

#Skype data extractor to display data connected to a skype profile
#Displayed data includes account, contacts, call and message data
#Note that the args required is the dir path containing the skype profile
#Chapter 3 converted Python2 to Python3

import sqlite3
import argparse
import os


def showProf(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT fullname, skypename, city, country, \
		   datetime(profile_timestamp, 'unixepoch') FROM Accounts;")
	for row in c:
		print("[*] --Found Account --")
		print("[+] User: " + str(row[0]))
		print("[+] Skype Username: " + str(row[1]))
		print("[+] Location: " + str(row[2])+','+str(row[3]))
		print("[+] Profile Date: " + str(row[4]))

def showContacts(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT displayname, skypename, city, country, \
		     phone_mobile, birthday FROM Contacts;")	
	for row in c:
		print("\n[*] -- Found Contact --")
		print("[+] User: " + str(row[0]))
		print("[+] Skype Username: " + str(row[1]))
		if str(row[2]) != '' and str(row[2]) != 'None':
			print("[+] Location: " + str(row[2]) + ',' \
				+ str(row[3]))
		if str(row[4]) != 'None':
			print("[+] Mobile Number: " + str(row[4]))
		if str(row[5]) != 'None':
			print("[+] Birthday: " + str(row[5]))
def showCalls(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT datetime(begin_timestamp, 'unixepoch'), \
		   identity FROM calls, conversations WHERE \
		   calls.conv_dbid = conversations.id;")
	print("\n[*] -- Found Calls --")
	for row in c:
		print("[+] Time: " + str(row[0]) + \
			" | Partner: " + str(row[1]))

def showChat(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT datetime(timestamp, 'unixepoch'), \
		   dialog_partner, author, body_xml FROM Messages;")
	print("\n[*] -- Found Messages --")
	
	for row in c:
		try:
			if 'partlist' not in str(row[3]):
				if str(row[1]) != str(row[2]):
					msgDirection = 'To ' + str(row[1]) + ': '
				else:
					msgDirection = 'From ' + str(row[2]) + ': '
				print("Time: " + str(row[0]) + ' ' \
					+ msgDirection + str(row[3]))
		except:
			pass

def main():
	argsParser = argparse.ArgumentParser()
	argsParser.add_argument('-P', '--pathName', help="specify Skype profile path")
	args = argsParser.parse_args()
	pathName = args.pathName
	
	if (pathName is None):
		argsParser.print_help()
		exit(0)
	elif os.path.isdir(pathName) == False:
		print("[!] Path Does Not Exist: " + pathName)
		exit(0)
	else:
		skypeDB = os.path.join(pathName, 'main.db')
		if os.path.isfile(skypeDB):
			showProf(skypeDB)
			showContacts(skypeDB)
			showCalls(skypeDB)
			showChat(skypeDB)
		else:
			print("[!] Skype Database does not exist: " + skypeDB)

if __name__ == '__main__':
	main() 
 
		   
			
		

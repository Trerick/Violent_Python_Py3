#Program to display all networks connected to by a target Windows system
#Chapter 3 converted Python2 to Python3

from __future__ import print_function
import itertools
from winreg import *

KEY_READ_64 = KEY_READ | KEY_WOW64_64KEY
ERROR_ITEMS_OUT = 259

def netKeys(key):
	for i in itertools.count():
		try:
			yield EnumKey(key, i)
		except OSError as e:
			if e.winerror == ERROR_ITEMS_OUT:
				break
			raise
def netVals(key):
	for i in itertools.count():
		try:
			yield EnumValue(key, i)
		except OSError as e:
			if e.winerror == ERROR_ITEMS_OUT:
				break
			raise

def val2addr(val):
	return ':'.join('%02x' % b for b in bytearray(val))

netList = (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
	   r"\NetworkList\Signatures\Unmanaged")

def showNets(keystr = netList):
	key = OpenKey(HKEY_LOCAL_MACHINE, keystr, 0, KEY_READ_64)
	print("\n[*] Networks You Have Joined.")
	for guid in netKeys(key):
		netKey = OpenKey(key, guid)
		netID, netMac = '', ''
		for name, data, rtype in netVals(netKey):
			if name == 'FirstNetwork':
				netID = data
			elif name == 'DefaultGatewayMac':
				if data:
					netMac = val2addr(data)
		if netID:
			print('[*]', netID, netMac)
		CloseKey(netKey)
	CloseKey(key)
	
def main():
	showNets()
if __name__ == "__main__":
	main()

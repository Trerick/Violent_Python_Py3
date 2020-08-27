#Program to display contents of the Recycle Bin of a target Windows system
#Chapter 3 converted Python2 to Python3

from __future__ import print_function
import os
from winreg import *

def idUser(userid):
    try:
        userKey = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
                      + '\\' + userid)
        (value, type) = QueryValueEx(userKey, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except:
        return userid

def searchRecycle():
    userBins = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycleBin in userBins:
        if os.path.isdir(recycleBin):
            return recycleBin
    return None

def recycledContent(recycleBin):
    binList = os.listdir(recycleBin)
    for userid in binList:
        files = os.listdir(recycleBin + userid)
        user = idUser(userid)
        print("\n[*] Locating Files In User's Recycle Bin: " + str(user))
        for item in files:
            print("[+] Found File: " + str(item))

def main():
    recycleBin = searchRecycle()
    recycledContent(recycleBin)

if __name__ == '__main__':
    main()
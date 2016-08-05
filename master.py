#!/usr/bin/python3.4
import os
import http.client
import time

time.sleep(6)

wifi = False 

conn = http.client.HTTPConnection("www.google.com")
try:
    conn.request("HEAD", "/")
    wifi = True
    print ("dope")
except:
    print ("yikes")

if os.path.exists("/media/flash/IMAFODLER") and wifi == True:
    print ("here")
    os.system('python3 /home/pi/documentation_dropbox.py')
elif os.path.exists("/media/flash") and wifi == False:
    os.system('python3 /home/pi/documentation_usbonly.py')
elif os.path.exists("/media/flash/IMAFODLER") == False and wifi == True:
    os.system('python3 /home/pi/documentation_dboxonly.py')
else:
    sys.exit()
    


'''
Created on Oct 12, 2018

Modified on Jan 24,2020
@author doktorbrown
'''
import os 
import re
import time
from datetime import date
import csv
from bs4 import BeautifulSoup 
from time import strftime
#installation at http://www.crummy.com/software/BeautifulSoup/     $ pip install beautifulsoup4



#update with full list, abbreviations, and lower case expanded campus list
campusList = ['ABINGTON', 'ALTOONA','BEAVER', 'BEHREND', 'BERKS','BRANDYWINE', 'CARLISLE', 'DICKINSON','DUBOIS', 'ERIE', 'FAYETTE', 'GREAT', 'GREAT VALLEY', 'GREATER', 'GREATER ALLEGHENY', 'HARRISBURG', 'HAZELTON', 'HERSHEY', 'LEHIGH', 'LEHIGH VALLEY', 'MONT', 'MONT ALTO', 'NEW ', 'NEW KENSINGTON', 'SCHUYLKILL', 'SHENANGO', 'SCRANTON', 'WILKES-BARRE', 'WILLIAMSPORT','WORTHINGTON', 'WORTHINGTON SCRANTON', 'YORK']
campus = str()


#the Q&A on the printers page has to be made fullscreen in the browser window and then saved as full html
# this script is then run from the same directory the html was saved in via terminal


#delayed start to allow html download to complete
for d in range(1,10000000):
    dd=d+1

print("generating preview")

 


try:
    fname ="3DPrinterOS - Printers.html"
    
except: 
    fname = "3DPrinterOS - Printers.html"
soup = BeautifulSoup(open(fname), 'html.parser') 
out = "clipboard.txt"
log = "log.txt"
csvLogOutput = "3D_label_Logs.csv"
# 

# extract the user info from the html and assign it to the Getters
# 
firstNameGetter = soup.find_all(text = re.compile("^What is your name?"))[0].next.next
# print(firstNameGetter)

lastNameGetter = soup.find_all(text = re.compile("^What is your name?"))[0].next.next.next.next
# print(lastNameGetter)

emailGetter = soup.find_all(text = re.compile("^Please re-enter your PSU email address."))[0].next.next
# print(emailGetter)
campusGetter = soup.find_all(text = re.compile("^Campus:"))[0].next.next
# print(campusGetter)

today =str(date.today())
# whatTime = str(time.localtime())
# print(whatTime[3],":",whatTime[4])

hour=strftime("%H:%M:%S")
# print(hour)

# print today
# 
# don't add campus if UP

if campusGetter =="UNIVERSITY PARK":
    campus = " "
else:
    campus = campusGetter
          
# print to screen as verification
print (campus)
print (lastNameGetter,",", firstNameGetter)
print (today)
print (emailGetter)


#confirm preview and enter printer number

print("please enter printer number and press return if preview is correct")

printerNumber = int(input())

if printerNumber =="n" or "N":
    quit
    
else:
    pass

printerNumber=str(printerNumber)
print("Printed on ", printerNumber)





# send to clipboard
# open output file for writing results
f = open(out, 'w')
#      
#shorter for new labels 
lineOne = (campus, '\n',
           lastNameGetter," ,", firstNameGetter,'\n',
           today, '\n',
           emailGetter,  '\n',
           "Printer: ",printerNumber, '\n',
           "Consultation Scheduling:", '\n',
           "makercommons.psu.edu")
#  
# #strip extra mc label info so it doesn't clutter log
# # lineTwo = (today,",",campus,",",lastName,"," ,firstName,",",emailGetter,",",printerGetter,",",filamentGetter," ",fileNameGetter, " ", requestGetter,'\n','\n')
# lineTwo = (today,",",campus,",",lastNameGetter,"," ,firstNameGetter,",",emailGetter,",",",",filamentGetter," ",fileNameGetter, " ",'\n','\n')
# 
#  
f.writelines(lineOne)
#   
# print lineOne
#  
f.close()
# 
# this only works when the dymo labelwriter is installed and connected, otherwise comment out the following lines
os.system("lpr -o landscape -P DYMO_LabelWriter_450_Turbo clipboard.txt")
#  

# # open log file for appending results

logRowEntry = (today, campus, lastNameGetter, firstNameGetter, emailGetter, printerNumber,hour,'\n')

csvLogs = csv.writer(open(csvLogOutput, 'a')) 
csvLogs.writerow(logRowEntry)
# if  log appended message appears, then everything has been written correctly to label and logs
print (lineOne)
print ("log appended")

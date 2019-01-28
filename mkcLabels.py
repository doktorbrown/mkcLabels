'''
Modified on Oct 11, 2018

@author: tbrown
'''
import os
import re
import time
from datetime import date
import csv
from bs4 import BeautifulSoup #installation at http://www.crummy.com/software/BeautifulSoup/     $ pip install beautifulsoup4



#update with full list, abbreviations, and lower case expanded campus list
campusList = ['ABINGTON', 'ALTOONA','BEAVER', 'BEHREND', 'BERKS','BRANDYWINE', 'CARLISLE', 'DICKINSON','DUBOIS', 'ERIE', 'FAYETTE', 'GREAT', 'GREAT VALLEY', 'GREATER', 'GREATER ALLEGHENY', 'HARRISBURG', 'HAZELTON', 'HERSHEY', 'LEHIGH', 'LEHIGH VALLEY', 'MONT', 'MONT ALTO', 'NEW ', 'NEW KENSINGTON', 'SCHUYLKILL', 'SHENANGO', 'SCRANTON', 'WILKES-BARRE', 'WILLIAMSPORT','WORTHINGTON', 'WORTHINGTON SCRANTON', 'YORK']
campus = str()

fname = "3DPrinterOS - Dashboard.html"
# fname = "3DPrinterOS - Printers.html"
soup = BeautifulSoup(open(fname), 'html.parser') 
out = "clipboard.txt"
log = "log.txt"
csvLogOutput = "3D_label_Logs.csv"

# print soup.prettify()

firstNameGetter = soup.find_all(text = re.compile("^What is your name?"))[0].next.next.next
# print(firstNameGetter)
# weaselBastards=firstNameGetter
lastNameGetter = soup.find_all(text = re.compile("^What is your name?"))[0].next.next.next.next.next.next.next_element
# print(lastNameGetter)
dateFinishedGetter = soup.tbody.span.next
# print(dateFinishedGetter)
emailGetter = soup.find_all(text = re.compile("^Please re-enter your PSU email address."))[0].next.next.next
# print(emailGetter)
campusGetter = soup.find_all(text = re.compile("^Campus:"))[0].next.next.next
# print campusGetter
fileNameGetter = soup.tbody.find_all('a')[1].next
print fileNameGetter
# requestGetter = soup.find_all(text = re.compile("^Request:"))[0].next

# print soup.tbody.prettify() 

# printerGetter = soup.tbody.find_all(text = re.compile("^Printer Id"))[1].next
# print printerGetter


filamentGetter = soup.tbody.find_all('td')[3].next.next.next.next.next.next.next.next.next.next
# print(filamentGetter)
print"hammertime"

# #exception handling for uncompleted prints or variations in html
# try:
#     filamentGetter = soup.find_all(text = re.compile("Filament Usage Actual"))[0].next
# except:
#     filamentGetterEstimate = soup.find_all(text = re.compile("Filament Usage Estimate"))[0].next
# #notesGetter = soup.find_all(text = re.compile("^Campus"))#not yet implemented in form

today =str(date.today())

# 
# print lastNameGetter,",", firstNameGetter
# print emailGetter
# print "printerGetter: ",printerGetter
# print "fileNameGetter: ", fileNameGetter


# 
if campusGetter =="UNIVERSITY PARK":
    campus = " "
else:
    campus = str(campusGetter)
         
# 
print campus
print lastNameGetter,",", firstNameGetter
print today
print emailGetter, filamentGetter 
print fileNameGetter
print "NOT FOR PRODUCTION"

 
#open output file for writing results
f = open(out, 'w')
     
#format extracted text for label
# lineOne = (nameGetter,'\n', emailGetter, '\n', "\n Failing to add a Raft or \n Supports when preparing the \n .makerbot file is the most \n common reason for a failed print. \n Please check: \n makercommons.psu.edu/fail \n for more info.  Consultations \n can be scheduled by emailing  \n makercommons@psu.edu.")
#for landscape print
# lineOne = (campus, '\n',lastName,",", firstName,'\n', today, " ", emailGetter, " ", filamentGetter, " ",fileNameGetter," ", requestGetter,'\n', '\n', "Not adding a Raft or Supports when   prepping the .makerbot file is the   most common reason for failed prints. \n Info: makercommons.psu.edu/fail \n Consultation Scheduling: \n makercommons@psu.edu")
#shorter msg re: rafts to adjust formatting and fit on one label
# lineOne = (campus, '\n',lastNameGetter,",", firstNameGetter,'\n', today, " ", emailGetter, " ", filamentGetter, " ",fileNameGetter," ", requestGetter,'\n',  "Consultation Scheduling: \n makercommons@psu.edu", '\n', " makercommons.psu.edu")
#shorter for new labels
lineOne = str(campus, '\n',lastNameGetter,",", firstNameGetter,'\n', today, " ", emailGetter, " ", filamentGetter, " ",fileNameGetter," ", '\n',  "Consultation Scheduling: \n makercommons@psu.edu", '\n', " makercommons.psu.edu")
 
#strip extra mc label info so it doesn't clutter log
# lineTwo = (today,",",campus,",",lastName,"," ,firstName,",",emailGetter,",",printerGetter,",",filamentGetter," ",fileNameGetter, " ", requestGetter,'\n','\n')
lineTwo = (today,",",campus,",",lastNameGetter,"," ,firstNameGetter,",",emailGetter,",",",",filamentGetter," ",fileNameGetter, " ",'\n','\n')

 
f.writelines(lineOne)
  
print lineOne
 
f.close()
 
os.system("lpr -o landscape -P DYMO_LabelWriter_450_Turbo clipboard.txt")
 
# open log file for appending results
logs = open(log, 'a')
logs.writelines(lineTwo)
# logs.writelines(weaselBastards)
print "log appended"
# print lineTwo
logs.close()
# 
# #logsCommaSeparated.
row_to_enter = (today, campus, lastNameGetter, firstNameGetter, emailGetter, filamentGetter, "printerGetter", "requestGetter", fileNameGetter, '\n')
csvLogs = csv.writer(open(csvLogOutput, 'a'))
csvLogs.writerow(row_to_enter)
print "log appended"
print lineTwo

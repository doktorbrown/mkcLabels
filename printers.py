'''
Created on Oct 12, 2018

Modified on Jan 24,2020

Super COVID Address Label Modified on Aug 18, 2020
Additional tweaks on Aug 24, 2020

This reads in a saved html file of 3dprinterOS 'Job Details' on the printers.html 
page, and then parses the Q&A based on the custom fields. This information is 
turned into Delivery and Shipping labels that are printed on a DYMO_LabelWriter_450_Turbo.
print drivers should be installed and the printer added in system preferences so that
it can be accessed via lpr.  https://www.dymo.com/en-US/labelwriter-450-turbo-label-printer

It's ugly. But it works.

additional references:
    https://www.computerhope.com/unix/ulpr.htm



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



# not needed due to hard wired selection choices in Q&A now
#update with full list, abbreviations, and lower case expanded campus list
# campusList = ['ABINGTON', 'ALTOONA','BEAVER', 'BEHREND', 'BERKS','BRANDYWINE', 'CARLISLE', 'DICKINSON','DUBOIS', 'ERIE', 'FAYETTE', 'GREAT', 'GREAT VALLEY', 'GREATER', 'GREATER ALLEGHENY', 'HARRISBURG', 'HAZELTON', 'HERSHEY', 'LEHIGH', 'LEHIGH VALLEY', 'MONT', 'MONT ALTO', 'NEW ', 'NEW KENSINGTON', 'SCHUYLKILL', 'SHENANGO', 'SCRANTON', 'WILKES-BARRE', 'WILLIAMSPORT','WORLD CAMPUS','WORTHINGTON', 'WORTHINGTON SCRANTON', 'YORK', 'HOME DELIVERY']
# campus = str()


#Using Chrome as the browser, the Q&A on the printers.html page has to be  saved as full html.
# this script is then run from the same directory the html was saved in via terminal


#delayed start to allow html download to complete

time.sleep(1)

print("generating preview")

time.sleep(3)

 

#read html or else read html. This was only needed when labels had to be printed 
#from the Dashboard.html page.  It's probably not needed now.
try:
    fname ="3DPrinterOS - Printers.html"
    
except: 
    fname = "3DPrinterOS - Printers.html"
    
    
#prep input and output files
soup = BeautifulSoup(open(fname), 'html.parser') 
out = "clipboard.txt"
log = "log.txt"
csvLogOutput = "3D_label_Logs.csv"


# print(soup)
print(" ")
# 
# extract the user info from the html and assign it to the Getters

#not currently possible to extract Job ID (8.18.2020) which could be added to the labels
# jobIDGetter = soup.find_all(text = re.compile("^StatusText"))[0].next
# print("jobIDGetter:  ",jobIDGetter)


# debug print statements could be turned off, but they provide more information about what is being processed

deliveryMethodGetter = soup.find_all(text = re.compile("^Delivery Method?"))[0].next.next
# print(deliveryMethodGetter)

# 
firstNameGetter = soup.find_all(text = re.compile("^What is your name?"))[0].next.next
# print(firstNameGetter)

lastNameGetter = soup.find_all(text = re.compile("^What is your name?"))[0].next.next.next.next
# print(lastNameGetter)

emailGetter = soup.find_all(text = re.compile("^Please re-enter your PSU email address."))[0].next.next
# print(emailGetter)
campusGetter = soup.find_all(text = re.compile("^Campus:"))[0].next.next
# print(campusGetter)


mailingAddressStreetGetter = soup.find_all(text = re.compile("^Mailing Address for World Campus or Home Delivery"))[0].next.next
# print(mailingAddressStreetGetter)
mailingAddressCityGetter = soup.find_all(text = re.compile("^Mailing Address for World Campus or Home Delivery"))[0].next.next.next.next
# print(mailingAddressCityGetter)
mailingAddressStateGetter = soup.find_all(text = re.compile("^Mailing Address for World Campus or Home Delivery"))[0].next.next.next.next.next.next
# print(mailingAddressStateGetter)
mailingAddressZIPGetter = soup.find_all(text = re.compile("^Mailing Address for World Campus or Home Delivery"))[0].next.next.next.next.next.next.next.next
# print(mailingAddressZIPGetter)

classGetter = soup.find_all(text = re.compile("^Which class is this for?"))[0].next.next
# print(classGetter)

print(" ")  
today =str(date.today())
# whatTime = str(time.localtime())
# print(whatTime[3],":",whatTime[4])

hour=strftime("%H:%M:%S")
# print(hour)

print(today, hour)
# 
# don't display campus if UP

if campusGetter =="UNIVERSITY PARK":
    campus = " "
else:
    campus = campusGetter
print(" ")          
# print to screen as verification
print(campus)
print(lastNameGetter,",", firstNameGetter)
print(today)
print(emailGetter)


#confirm preview and enter printer number
print(" ")
print("Please enter the printer number you are sending this to, and press return if the preview is correct.")
print("Don't forget to add this to the Notes in the Job Details window before you close it.")

printerNumber = int(input())

# 
# if printerNumber =="n" or "N":
#     print("Please re-enter the printer number.")
# #     printerNumber = int(input())
#     
# else:
#     pass

#does that printer exist?

while printerNumber >= 31: 
    try:
        print("Please re-enter the printer number.", printerNumber, " does not exist.")
        printerNumber = int(input())
     
    except print("Ouch.  That wasn't a number was it??"):
        break
    
printerNumber=str(printerNumber)

print(" ")
print("Object being assigned to Printer number:  ", printerNumber)
print(" ")



#initial Delivery print labels go here. this should be turned into a function to simplify things.
#If HOME DELIVERY or WORLD CAMPUS are selected then a second label will print.
#and Delivery Method is home delivery



# send to clipboard
# open output file for writing results
f = open(out, 'w')
#      
#shorter for new labels 
lineOne = (campus, '\n',
           lastNameGetter," ,", firstNameGetter,'\n',
           today, '\n',
           emailGetter,  '\n',
           "Printer: ",printerNumber) 


addressLabel = (firstNameGetter," ",lastNameGetter,'\n',
                mailingAddressStreetGetter,'\n',
                mailingAddressCityGetter,"  ", mailingAddressStateGetter,'\n',
                mailingAddressZIPGetter,'\n'
                )
#  
# 
try: 
    f.writelines(lineOne)
    #   
#     print(lineOne)
    #  
    f.close()
    # 
    try:
        # this only works when the dymo labelwriter is installed and connected, otherwise comment out the following line
        os.system("lpr -o landscape -P DYMO_LabelWriter_450_Turbo clipboard.txt")
        print("Delivery Label printed.")
    except:
        print("No printer connected")
    pass
except:
    print("No printer connected")
    pass

if campusGetter =="HOME DELIVERY" or campusGetter =="WORLD CAMPUS":
    time.sleep(1)
    print(" ")
    print("Printing Address Label:  ")
    # send to clipboard
    # open output file for writing results
    f = open(out, 'w')
    #      
    #shorter for new labels 


    addressLabel = (firstNameGetter," ",lastNameGetter,'\n', emailGetter, printerNumber,'\n',
    mailingAddressStreetGetter, '\n',
    mailingAddressCityGetter,"  ", mailingAddressStateGetter,'\n',
    mailingAddressZIPGetter,'\n'
    )
    #  

    f.writelines(addressLabel)
    #   
#     print(addressLabel)
    print(" ")
    print(firstNameGetter ," ",lastNameGetter)
    print(emailGetter, printerNumber)
    print(mailingAddressStreetGetter)
    print(mailingAddressCityGetter, "  ", mailingAddressStateGetter, mailingAddressZIPGetter)
    print(" ")
    #  
    f.close()
    # 
    # this only works when the dymo labelwriter is installed and connected, otherwise comment out the following line
    os.system("lpr -o fit-to-page -o landscape -P DYMO_LabelWriter_450_Turbo clipboard.txt")
#     os.system("lpr -o fit-to-page -P DYMO_LabelWriter_450_Turbo clipboard.txt")#rotated 90 degrees
    #
    print(" ") 
    print("Address Label printed.")

    
# # open log file for appending results

# print(addressLabel)
logRowEntry = (today, hour, printerNumber,campus, lastNameGetter, firstNameGetter, emailGetter, classGetter,  mailingAddressStreetGetter,mailingAddressCityGetter, mailingAddressStateGetter,mailingAddressZIPGetter,'\n')


csvLogs = csv.writer(open(csvLogOutput, 'a')) 
csvLogs.writerow(logRowEntry)
# if  log appended message appears, then everything has been written correctly to label and logs
print(" ")
# print (logRowEntry)
print(" ")
print ("logs appended at ", today, hour)

# mkcLabels
Created on Oct 12, 2018 

Modified on Jan 24,2020

Super COVID Address Label Modified on Aug 18, 2020
Additional tweaks on Aug 24, 2020

Regex parsing and error handling of label data changed to reflect updated 3DPrinterOS interface  May 10, 2021

Jun 16, 2021: fixed spacing between email and printer number in address label



This reads in a saved html file of 3dprinterOS 'Job Details' on the printers.html 
page, and then parses the Q&A based on the custom fields. This information is 
turned into Delivery and Shipping labels that are printed on a DYMO_LabelWriter_450_Turbo.
print drivers should be installed and the printer added in system preferences so that
it can be accessed via lpr.  https://www.dymo.com/en-US/labelwriter-450-turbo-label-printer

It's ugly. But it works.

additional references:
    https://www.computerhope.com/unix/ulpr.htm

To use:


From Printers Page
Open Job Notes and 
File>Save Page As... to same directory as printers.py
in terminal:  python3 printers.py
verify preview and add printer number
labels should print


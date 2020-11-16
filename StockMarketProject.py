import requests                                                                                                           #Import Stuff
import datetime
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from csv import writer

date = datetime.date.today()                                                                                              #Get Today's Date

print("- {}\n- STARTING, IMPORTING COMPLETE".format(date))

stockList = ["USFD", "LMT", "MSFT", "TXN", "ES", "UAL", "UNH", "AMD", "AXP"]                                              #Set-up the lists
stockPrice = []
errorCount = 0

print("- LISTS CREATED, READY")

def getStock(stockSym):                                                                                                   #Get the stock price and add it to the list
  response = requests.get("https://money.cnn.com/quote/quote.html?symb={}".format(stockList[stockSym]))
  soup = BeautifulSoup(response.text, 'html.parser')
  stock = soup.find(class_="wsod_last").contents[0].get_text()
  stockPrice.append(float(stock))
  print("- SUCCESS FOR STOCK SYMBOL {} AT PRICE {}".format(stockList[stockSym], stock))

while(True):                                                                                                              #The main loop
  with open('{}.csv'.format(date), 'w') as csv_file:                                                                      #Opens CSV
    csv_writer = writer(csv_file)
    headers = ["Symbol", "Price"]
    csv_writer.writerow(headers)
    print("- CVS CREATED, READY FOR WRITE\n-")

    for item in range(len(stockList)):                                                                                    #Passes stock price into CSV                                                                                   
      try:
        print("- LOOP {} STARTED".format(item + 1))
        getStock(item)
        csv_writer.writerow([stockList[item], stockPrice[item]])
        print("- LOOP {} COMPLETE, WRITTEN TO CSV\n-".format(item + 1))
      except Exception:
        stockPrice.append("FAIL")
        csv_writer.writerow([stockList[item], stockPrice[item]])
        errorCount += 1
        print("- STOCK {} COULD NOT BE FOUND, CONTINUE TO {}\n-".format(stockList[item], stockList[item + 1]))

  print("- THERE WERE {} FAULTY STOCKS\n- DONE WITH CSV".format(int(errorCount)))

  read_file = pd.read_csv(r'./{}.csv'.format(date))                                                                       #Convert CSV to XLSX
  read_file.to_excel(r'./{}.xlsx'.format(date), index = None, header=True)
  os.remove("{}.csv".format(date))
  print("- SHEET CREATED, Waiting for 24 hours to runn again.\n- {}".format(date))
  stockPrice.clear()                                                                                                      #Clear stock list and error count
  errorCount = 0
  time.sleep(86400)                                                                                                      #Wait 24 hours to run again (Daily)
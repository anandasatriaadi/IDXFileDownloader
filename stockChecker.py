import os
import configparser
import time
import threading
from selenium import webdriver


# Configuration loader
config = configparser.ConfigParser()
config.read("./CheckerConfig.ini")

downloadDir = config['DEFAULT']['DownloadDirectory']
documentDir = config['DEFAULT']['FinStatementDirectory']
year = config['DEFAULT']['Year']
year = year.strip()
mode = config['DEFAULT']['Mode']
mode = mode.upper()
monthPeriod = config['DEFAULT']['MonthPeriod']
threadNumber = config['DEFAULT']['ThreadNumber']

daftarSaham = open("./ListSaham.txt", "r")
listSaham = daftarSaham.readlines()
daftarSaham.close()


# Change of Download Directory
PATH = "C:/Program Files (x86)/chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
chromeOptions.add_experimental_option("prefs", {"download.default_directory" : downloadDir})


# Global Variables
BaseURL = "http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan/"
missingList = open("./MissingStocks.txt", "w")


# Functions / Methods Declarations
def checkTW(stockName, periodInRoman, browser):
	fileLoc = documentDir + "/FinancialStatement-" + str(year) + "-" + periodInRoman + "-" + stockName + ".xlsx"

	if not os.path.isfile(fileLoc):
		missingList.write("" + stockName + " - ")
		LoopedURL = "/Laporan%20Keuangan%20Tahun%20" + str(year) + "/TW" + monthPeriod + "/" + stockName + "/FinancialStatement-" + str(year) + "-" + periodInRoman + "-" + stockName + ".xlsx"
		browser.get(BaseURL + LoopedURL)
		
		if "404" in browser.title:
			missingList.write("File is not available at IDX!\n")
		else:
			missingList.write("Is now available\n")

	browser.get("data:,")


def checkAudit(stockName, browser):
	fileLoc = documentDir + "/FinancialStatement-" + str(year) + "-Tahunan-" + stockName + ".xlsx"

	if not os.path.isfile(fileLoc) :
		missingList.write("" + stockName + " - ")
		LoopedURL = "/Laporan%20Keuangan%20Tahun%20" + str(year) + "/Audit/" + stockName + "/FinancialStatement-" + str(year) + "-Tahunan-" + stockName + ".xlsx"
		browser.get(BaseURL + LoopedURL)
		
		if "404" in browser.title:
			missingList.write("File is not available at IDX!\n")
		else:
			missingList.write("Is now available\n")

	browser.get("data:,")


# Main Program
class mainProg(threading.Thread):
	def __init__(self, startIndex, endIndex, threadNum, browser):
		threading.Thread.__init__(self)
		self.startIndex = startIndex
		self.endIndex = endIndex
		self.threadNum = threadNum
		self.browser = browser

	def run(self):
		if(mode == "TW"):
			missingList.write("Mode: " + mode + "\n")
			missingList.write("Year: " + year + "\n")

			periodInRoman = ""
			for x in range(int(monthPeriod)):
				periodInRoman += "I"
			
			missingList.write("TW: " + periodInRoman + "\n\n")

			for x in range(self.startIndex, self.endIndex):
				stockName = listSaham[x]
				stockName = stockName.strip()
				print("Thread " + str(self.threadNum) + " : " + stockName)
				checkTW(stockName, periodInRoman, self.browser)

		elif(mode == "AUDIT"):
			missingList.write("Mode: " + mode + "\n")
			missingList.write("Year: " + year + "\n\n")

			for x in range(self.startIndex, self.endIndex):
				stockName = listSaham[x]
				stockName = stockName.strip()
				print("Thread " + str(self.threadNum) + " : " + stockName)
				checkAudit(stockName, self.browser)

		else:
			print("ERROR\n   Please choose Audit or TW.")

		time.sleep(3)
		self.browser.close()
		if self.threadNum == int(threadNumber) - 1:
			for x in range(20):
				print("FINISH")
		
increment = int(len(listSaham) / int(threadNumber))
threadList = []

for x in range(int(threadNumber)):
	
	if x < int(threadNumber) - 1:
		threadList.append( mainProg(x*increment, (x+1)*increment, x, webdriver.Chrome(executable_path = PATH, options = chromeOptions)) )
	else:
		threadList.append( mainProg(x*increment, len(listSaham), x, webdriver.Chrome(executable_path = PATH, options = chromeOptions)) )
		
for x in range(int(threadNumber)):
	threadList[x].start()
			
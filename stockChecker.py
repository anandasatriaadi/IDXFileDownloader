import os
import configparser
import time
from selenium import webdriver


# Configuration loader
config = configparser.ConfigParser()
config.read("./Config.ini")

downloadDir = config['DEFAULT']['DownloadDirectory']
documentDir = config['DEFAULT']['FinStatementDirectory']
year = config['DEFAULT']['Year']
year = year.strip()
mode = config['DEFAULT']['Mode']
mode = mode.upper()
monthPeriod = config['DEFAULT']['MonthPeriod']
isSplit = config['DEFAULT']['isSplit']
isSplit = isSplit.upper()

daftarSaham = open("./ListSaham.txt", "r")
listSaham = daftarSaham.readlines()
daftarSaham.close()


# Change of Download Directory
PATH = "C:/Program Files (x86)/chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"download.default_directory" : downloadDir})
driver = webdriver.Chrome(executable_path = PATH, options = chromeOptions)


# Global Variables
BaseURL = "http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan/"


# Functions / Methods Declarations
def checkTW(stockName, periodInRoman):
	fileLoc = documentDir + "\FinancialStatement-" + str(year) + "-" + periodInRoman + "-" + stockName + ".xlsx"

	print(stockName)
	if not os.path.isfile(fileLoc):
		missingList.write("" + stockName + " - ")
		LoopedURL = "/Laporan%20Keuangan%20Tahun%20" + str(year) + "/TW" + monthPeriod + "/" + stockName + "/FinancialStatement-" + str(year) + "-" + periodInRoman + "-" + stockName + ".xlsx"
		driver.get(BaseURL + LoopedURL)
		
		if "404" in driver.title:
			missingList.write("File is not available at IDX!\n")
		else:
			missingList.write("Is now available\n")

	driver.get("data:,")


def checkAudit(stockName):
	fileLoc = documentDir + "\FinancialStatement-" + str(year) + "-Tahunan-" + stockName + ".xlsx"

	print(stockName)
	if not os.path.isfile(fileLoc) :
		missingList.write("" + stockName + " - ")
		LoopedURL = "/Laporan%20Keuangan%20Tahun%20" + str(year) + "/Audit/" + stockName + "/FinancialStatement-" + str(year) + "-Tahunan-" + stockName + ".xlsx"
		driver.get(BaseURL + LoopedURL)
		
		if "404" in driver.title:
			missingList.write("File is not available at IDX!\n")
		else:
			missingList.write("Is now available\n")

	driver.get("data:,")


# Main Program
if(mode == "TW"):
	missingList = open("./MissingStocks.txt", "w")
	missingList.write("Mode: " + mode + "\n")
	missingList.write("Year: " + year + "\n")

	periodInRoman = ""
	for i in range(int(monthPeriod)):
		periodInRoman += "I"
	
	missingList.write("TW: " + periodInRoman + "\n\n")

	for x in listSaham:
		x = x.strip()
		stockName = x
		checkTW(stockName, periodInRoman)
	
	missingList.close()


elif(mode == "AUDIT"):
	missingList = open("./MissingStocks.txt", "w")
	missingList.write("Mode: " + mode + "\n")
	missingList.write("Year: " + year + "\n\n")

	for x in listSaham:
		x = x.strip()
		stockName = x
		checkAudit(stockName)

	missingList.close()

else:
	print("ERROR\n   Please choose Audit or TW.")

for x in range(20):
	print("FINISH")

time.sleep(2.5)

driver.quit()
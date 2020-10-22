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
def downloadTW(stockName, periodInRoman):
	fileLoc = documentDir + "\FinancialStatement-" + str(year) + "-" + periodInRoman + "-" + stockName + ".xlsx"
	print(stockName, end = " ")
	if not os.path.isfile(fileLoc):
		LoopedURL = "/Laporan%20Keuangan%20Tahun%20" + str(year) + "/TW" + monthPeriod + "/" + stockName + "/FinancialStatement-" + str(year) + "-" + periodInRoman + "-" + stockName + ".xlsx"
		driver.get(BaseURL + LoopedURL)
		
		if "404" in driver.title:
			print("- File is not available at IDX!")
		else:
			print("- Downloading...")

	else:
		print("- File is already downloaded.")

	driver.get("data:,")


def downloadAudit(stockName):
	fileLoc = documentDir + "\FinancialStatement-" + str(year) + "-Tahunan-" + stockName + ".xlsx"

	print(stockName, end = " ")
	if not os.path.isfile(fileLoc) :
		LoopedURL = "/Laporan%20Keuangan%20Tahun%20" + str(year) + "/Audit/" + stockName + "/FinancialStatement-" + str(year) + "-Tahunan-" + stockName + ".xlsx"
		driver.get(BaseURL + LoopedURL)
		
		if "404" in driver.title :
			print("- File is not available at IDX!")
		else:
			print("- Downloading...")

	else:
		print("- File is already downloaded.")

	driver.get("data:,")


# Main Program
if mode == "TW":
	periodInRoman = ""
	for i in range(int(monthPeriod)):
		periodInRoman += "I"

	if(isSplit == "Y"):
		for x in range(listSaham.__len__()//2):
			stockName = listSaham[x]
			stockName = stockName.strip()
			downloadTW(stockName, periodInRoman)

	else:
		for x in listSaham:
			x = x.strip()
			stockName = x
			downloadTW(stockName, periodInRoman)
			
elif mode == "AUDIT":

	if isSplit == "Y" :
		for x in range(listSaham.__len__()//2):
			stockName = listSaham[x]
			stockName = stockName.strip()
			downloadAudit(stockName)

	else:
		for x in listSaham:
			x = x.strip()
			stockName = x
			downloadAudit(stockName)

else:
	print("ERROR\n   Please choose Audit or TW.")

for x in range(20):
	print("FINISH")

time.sleep(2.5)

driver.quit()

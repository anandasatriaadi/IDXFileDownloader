import os
import json
import configparser
from json_excel_converter import Converter
from json_excel_converter.xlsx import Writer
from selenium import webdriver

# Configuration Loader
config = configparser.ConfigParser()
config.read("./HarianConfig.ini")

downloadDir = config['DEFAULT']['DownloadDirectory']
if not os.path.isdir(downloadDir):
	os.mkdir(downloadDir)
startDate = config['DEFAULT']['StartDate']
endDate = config['DEFAULT']['EndDate']
month = config['DEFAULT']['Month']
if int(month) < 10 :
	month = '0' + str(month)
year = config['DEFAULT']['Year']

if startDate > endDate :
	temp = startDate
	startDate = endDate
	endDate = temp


# CHROME DRIVER INIT
PATH = "C:/Program Files (x86)/chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
# Change of download directory
chromeOptions.add_experimental_option("prefs", {"download.default_directory" : downloadDir})
driver = webdriver.Chrome(executable_path = PATH, options = chromeOptions)


# FUNCTION / METHODS DECLARATION
def accessAndConvert(url, fileName):
		driver.get(url)

		textCode = driver.find_element_by_tag_name("pre").text
		jsonCode = json.loads(textCode)
		if int(jsonCode['ResultCount']) == 0:
			print("Data not found!")
		else:
			print()
			jsonCode = json.dumps(jsonCode['Results'])
			jsonCode = json.loads(jsonCode)

			conv = Converter()
			conv.convert(jsonCode, Writer(file= downloadDir + "\\" + fileName + ".xlsx"))

def ringkasanSaham():
	for x in range(int(startDate), int(endDate) + 1):
		if int(x) < 10:
			x = '0' + str(x)
		print(str(x) + "/" + str(month) + "/" + str(year), end=" ")

		fileName = "Ringkasan Saham-" + str(year) + str(month) + str(x)
		fileLoc = downloadDir + "\\" + fileName + ".xlsx"
		if not os.path.isfile(fileLoc):
			url = "https://www.idx.co.id/umbraco/Surface/TradingSummary/DownloadStockSummary?date=" + str(year) + str(month) + str(x)
			accessAndConvert(url, fileName)

		# Index Download Part
		fileName = "Ringkasan Index-" + str(year) + str(month) + str(x)
		fileLoc = downloadDir + "\\" + fileName + ".xlsx"
		url = "https://www.idx.co.id/umbraco/Surface/TradingSummary/DownloadIndexSummary?date=" + str(year) + str(month) + str(x)
		accessAndConvert(url, fileName)

# MAIN PROGRAM
ringkasanSaham()

driver.close()

from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests


# baseURL = "https://www.techcombank.com.vn/branches-atm-locations/list?fCityId=50&fDistrictId=563&fKeyword="
baseURL = "https://www.techcombank.com.vn/branches-atm-locations/list?"
payload = {'chkBranch': 'True', 'chkAtm': 'True','chkBranch': 'True','chkPriority': 'True','page': '1','pageItems':20}

url = "https://www.techcombank.com.vn/branches-atm-locations/list?fKeyword=&fCityId=0&fDistrictId=0&chkBranch=True&chkAtm=True&chkPriority=True&lng=0&lat=0&page=1&pageItems=20"

addressList = []

def captureAddressOfPage(pageIndex):
    payload['page']=pageIndex
    r = requests.get(baseURL,params=payload)
    # r = requests.get(url)
    print(r.text)
    soup = BeautifulSoup(r.text,"html.parser")
    # print(soup.prettify())
    addressBox = soup.select("div.content-entries")
    print(len(addressBox[0].select(".address")))
    addressTags = addressBox[0].select(".address")
    for entry in addressTags:
        # print(entry.string)
        addressList.append(str(entry.string).upper())

def writeToFile(path):
    outFile = open(path, mode='w',encoding="UTF-8")
    for address in addressList:
        print(address)
        print(address,file=outFile)
    outFile.close()


for pageindex in range(48):
    captureAddressOfPage(pageindex)


writeToFile('c:\\temp\\TechnoBankAddress.txt')



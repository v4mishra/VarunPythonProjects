from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import json
import csv
import pickle

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


def launchPage(url, payload):
    r = requests.get(baseURL, params=payload)
    return BeautifulSoup(r.text,"html.parser")


def extractOptionsMap(provinceOptions):
    optionsDict = {}
    for option in provinceOptions:
        value =option["value"]
        name = option.text
        print(value , name , sep="=")
        optionsDict[value]=name

    return optionsDict


def createProviceMap(soup):
    provinceOptions = soup.select("#fCityId option")
    provinceMap = extractOptionsMap(provinceOptions)
    ProvinceFile = open("c:/Temp/ProvinceFile.txt", "w", encoding="UTF-8")
    print(provinceMap, file=ProvinceFile)
    ProvinceFile.close()
    return provinceMap




def createDistrictMap(soup):
    districtOptions = soup.select("#fDistrictId option")
    districtMap = extractOptionsMap(districtOptions)
    DistrictFile = open("c:/Temp/DistrictFile.txt", "w", encoding="UTF-8")
    print(districtMap, file=DistrictFile )
    DistrictFile.close()
    return districtMap


def collateAndPrintLocations(addressMap, provinceMap, districtMap):
    csvList=[["address","districtName","cityName","lat","lng"]]
    csvfile = open('c:/Temp/finalAddress.csv', 'w',encoding="UTF-8")
    for address in addressMap:
        address["districtName"]=districtMap[str(address['district'])]
        address["cityName"] = provinceMap[str(address['city'])]
        addressItem = [address['address'],address['districtName'],address['cityName'],address['lat'],address['lng']]
        csvList.append(addressItem)

    csv.register_dialect('mydialect',delimiter='|')
    csvWriter = csv.writer(csvfile,dialect="mydialect")
    for row in csvList:
        csvWriter.writerow(row)

    csvfile.close()
    return None




def mainFunction():
    soup = launchPage(baseURL,payload)
    # # print(soup.prettify())

    loadFresh = False
    if(loadFresh):
        provinceMap = createProviceMap(soup)
        districtMap = createDistrictMap(soup)
        pickle.dump(provinceMap, open("c:/Temp/provincePickle.pk", "wb"))
        pickle.dump(districtMap, open("c:/Temp/districtPickle.pk", "wb"))
    else:
        provinceMap =pickle.load(open("c:/Temp/provincePickle.pk", "rb"))
        districtMap = pickle.load(open("c:/Temp/districtPickle.pk", "rb"))


    print("**************")
    print("province count = " + str(len(provinceMap)))
    print("district count = " + str(len(districtMap)))
    print("**************")

    addressMap = extractLatLong(districtMap,provinceMap)
    # addressMap = [{"lng":106.6810763,"id":30,"district":39,"lat":10.7763157,"city":2,"districtName":"","cityName":"","address":"574đường3tháng2,phường14,Quận10,ThànhphốHồChíMinh"},{"lng":107.1152133,"id":31,"district":570,"lat":10.3978266,"city":51,"districtName":"","cityName":"","address":"429đường30/4,phườngRạchDừa,ThànhphốVũngTàu,BàRịa-VũngTàu"}]
    # collateAndPrintLocations(addressMap,provinceMap,districtMap)


def extractLatLong(districtMap,provinceMap):
    url = "https://www.techcombank.com.vn//customfield/getBranchesById?"
    payload={"id":1}
    locationMap=[]
    # json = [{}] final = 1075
    res = None
    csvfile = open('c:/Temp/finalAddress.csv', 'a', encoding="UTF-8")
    csv.register_dialect('mydialect', delimiter='|')
    csvWriter = csv.writer(csvfile, dialect="mydialect")

    for i in range(900,1075):
        payload['id']=i

        try:
            r = requests.get(url, params=payload)
            res = r.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)

        print("id= "+ str(i)+ " : json = "+ str(res))
        if(res != None and  len(res)>0):
            print(res[0]["address"])
            map = {}
            map["id"] = res[0]["id"]
            map["address"] = res[0]["address"]
            map["lat"] = res[0]["lat"]
            map["lng"] = res[0]["lng"]
            map["district"] = res[0]["district"]
            map["districtName"] = ""
            map["city"] = res[0]["city"]
            map["cityName"] = ""
            print(map)
            map["districtName"] = districtMap[str(map['district'])]
            map["cityName"] = provinceMap[str(map['city'])]
            addressItem = [map["id"],map['address'], map['districtName'], map['cityName'], map['lat'],
                           map['lng']]
            csvWriter.writerow(addressItem)
            csvfile.flush()

            print("****")
            locationMap.append(map);


    print("finally locations captured : "+ str(len(locationMap)))
    addressFile = open("c:/Temp/addressMap.txt", "w", encoding="UTF-8")

    json.dump(locationMap, addressFile, ensure_ascii=False, indent=2)
    addressFile.close();

    return locationMap







mainFunction()



# list = [[1,"TÒA NHÀ LOTTE, SỐ 54 LIỄU GIAI, QUẬN BA ĐÌNH, QUẬN BA ĐÌNH, THÀNH PHỐ HÀ NỘI"],[2,"THANH LIỆT, HUYỆN THANH TRÌ, THÀNH PHỐ HÀ NỘI"],[3,"SỐ 10 HỒ TÙNG MẬU, THÀNH PHỐ ĐÀ LẠT, LÂM ĐỒNG"]]
# outFile = open("c:/Temp/finalAddress.csv",encoding="UTF=8",mode="w")
# csv.register_dialect(
#     'mydialect',
#     delimiter = '|')
# myWriter = csv.writer(outFile,dialect="mydialect")
# myWriter.writerow(list[0])
# myWriter.writerow(list[1])
# myWriter.writerow(list[2])
# outFile.close()
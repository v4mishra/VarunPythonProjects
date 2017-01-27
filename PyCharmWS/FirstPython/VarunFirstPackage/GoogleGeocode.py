import requests
import json
import csv
import pickle





baseURL = "http://maps.googleapis.com/maps/api/geocode/json"
payload = {'address':'','region':''}

inputFile = "D:/GeocodingProjects/Vietnam_VNM/16Sept_Runs/csv/VNM_Real_BulkTester_Comparison_BM.txt"
outputFile = "D:/GeocodingProjects/Vietnam_VNM/16Sept_Runs/csv/GoogleGeocodeOutput_Test.txt"
outputHeader = "Address|G_Latitude|G_Longitude|G_Street|G_Locality|G_City|G_District|G_State"
indexAddressInInputfile = 0  # This is index of mainAddressLine in input file.
csv.register_dialect('pipes', delimiter='|')
countryCode = "VN"





def loadAddressFile(inputFilePath):
    inputAddressList = []

    with open(inputFilePath,encoding="UTF-8",mode="r") as addressFile:
        csvReader = csv.reader(addressFile, dialect='pipes')
        inputAddressList = [row[indexAddressInInputfile] for row in csvReader]
        print(len(inputAddressList))
    addressFile.close()
    return inputAddressList


def extractGoogleAddressComponents(components):
    streetCode = 'route'
    subLocCode = 'sublocality_level_1'
    cityCode = 'locality'
    districtCode = 'administrative_area_level_2'
    stateCode = 'administrative_area_level_1'


    street = None
    subLoc = None
    city = None
    district = None
    state = None
    for addressComponent in components:
        componentType = set(addressComponent['types'])
        if streetCode in componentType: street = addressComponent['long_name']
        elif subLocCode in componentType: subLoc = addressComponent['long_name']
        elif cityCode in componentType: city = addressComponent['long_name']
        elif districtCode in componentType: district= addressComponent['long_name']
        elif stateCode in componentType: state = addressComponent['long_name']

    return [street,subLoc,city,district,state]


def googleGeocode(fullAddress):
    payload['address'] = fullAddress
    payload['region'] =countryCode
    r = requests.get(baseURL, params=payload)
    try:
        res = r.json()
        print(r.json())
        try:
            location =res['results'][0]['geometry']['location']
            addressComponentsJson = res['results'][0]['address_components']  # this is a list
            addressComponents = extractGoogleAddressComponents(addressComponentsJson)
        except IndexError:
            location ={'lat':0,'lng':0}
            addressComponents=[None,None,None,None,None]

        lat = location['lat']
        long = location['lng']
        print("{0},{1}".format(lat,long))
        # print(str(lat)+ ", "+ str(long))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("exception for address= "+ fullAddress)
        print(e)

    return [fullAddress, lat,long] + addressComponents


def bulkGeocode(fullAddressList):
    output = []
    for address in fullAddressList:
        geocodedOutput= googleGeocode(address)
        output.append(geocodedOutput)
    return output


def writeOutputToFile(geocodedOutput):
    with open(outputFile,mode="w",encoding="UTF-8",newline='') as outFile:
        writer = csv.writer(outFile,dialect="pipes")
        writer.writerow(outputHeader.split("|"))
        writer.writerows(geocodedOutput)



def testVarun(inputFilePath):
    geocodedOutput = googleGeocode("Đường Lê Lợi Bến Thành Quận 1 Hồ Chí Minh")
    print("output: ")
    print(geocodedOutput)
    writeOutputToFile([geocodedOutput])




def main(inputFilePath):
     fullAddressList  = loadAddressFile(inputFilePath)
     geocodedOutput = bulkGeocode(fullAddressList)
     writeOutputToFile(geocodedOutput)
     pass



main(inputFile)

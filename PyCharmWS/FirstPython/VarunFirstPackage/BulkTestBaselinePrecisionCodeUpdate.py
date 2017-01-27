import os
import re

import sys

bulkTestSummaryFile = "D:/GeocodingProjects/Vietnam_VNM/TeamCityArtifacts/Stable_testresults/TC_testresults_37061/testresults-functional/engine/VNM_RealAddr_BulkTester/VNM_Real_BulkTestMatchResults.txt"
bulkTestPropertyFile = "D:/MapMarker/MM_Code/MM_Maven/branches/Noida/local/VNM-CGGE/test/java/functional/com/mapinfo/mapmarker/test/VNM/TT/bulkgeocoding/vnm/VNM_Real_BulkGeocoderSettings.properties"
updatedBaselineFile = "D:/MapMarker/MM_Code/MM_Maven/branches/Noida/local/VNM-CGGE/test/java/functional/com/mapinfo/mapmarker/test/VNM/TT/bulkgeocoding/vnm/NEW_VNM_Real_BulkGeocoderSettings.properties"



def loadFileContents(inputFileName):
    with open(inputFileName) as f:
        content = f.readlines()
        return content


def main():
    return None


def extractStatsFromResults(bulkTestResult):
    startMarker = 'Current Build Match'
    endMarker ='Bench'
    startCapture = False

    results = PrecisionStats()

    for line in bulkTestResult:
        if(startMarker in line):
            startCapture = True
        elif(endMarker in line):
            startCapture = False
            break

        if(startCapture):
            matchedItem =  re.match("([GSZ]\d)|No", line, re.IGNORECASE)
            if(matchedItem !=None):
                code = matchedItem.group()
                value =line.partition("=")[2]
                results.precision.update({code:int(float(value))})



    return results


def getNewBaseLine(oldBaseline, resultCodes):
    oldBaseline = oldBaseline.replace("\n",'')

    # if this baseline is not monitored , dont touch it.
    if(re.search("=-\d",oldBaseline)):
        return oldBaseline


    precisionCodeMatch = re.search("([GSZ]\d)|No", oldBaseline, re.IGNORECASE)
    newBaseLine = ""
    if (precisionCodeMatch == None):
        newBaseLine = oldBaseline
    else:
        precisionCode = precisionCodeMatch.group()
        if(precisionCode in resultCodes.precision):
            value = resultCodes.precision.get(precisionCode,0)
            newBaseLine = oldBaseline.partition('=')[0] + " = " + str(value)
        else:
            newBaseLine = oldBaseline
    return newBaseLine


def isBaselineTxt(line):
    return line.startswith("Baseline")


def getUpdatedBaselines(propertyFileContents, resultCodes):
    newBaseline = []
    # for line in propertyFileContents:
    #     if(isBaselineTxt(line)):
    #         newBaseline.append(getNewLine(line,resultCodes))


    newBaseline =[getNewBaseLine(line,resultCodes)  for line in propertyFileContents if(isBaselineTxt(line))]

    return newBaseline


def getSummaryFile():
    resultFilePath = input("Enter full path to BulkTestMatchResults.txt: ")

    if (os.path.exists(resultFilePath)):
        print("BulkTestMatchResult file found.")
        return resultFilePath

    else:
        print("path dont exists")
        sys.exit()

def testVarun():
    bulkTestSummaryFile = getSummaryFile()
    bulkTestResultsContents = loadFileContents(bulkTestSummaryFile)
    resultCodes = extractStatsFromResults(bulkTestResultsContents)

    propertyFileContents = loadFileContents(bulkTestPropertyFile)
    updatedBaseLines = getUpdatedBaselines(propertyFileContents,resultCodes)

    print(type(updatedBaseLines))
    print(*updatedBaseLines,sep='\n')


    outfile = open(updatedBaselineFile , mode="w", encoding="UTF-8", newline='\n')
    print(*updatedBaseLines, file=outfile, sep='\n')
    outfile.flush()
    outfile.close()
    return None




class PrecisionStats:
    def __init__(self):
        self.precision = dict()

        pass



testVarun()


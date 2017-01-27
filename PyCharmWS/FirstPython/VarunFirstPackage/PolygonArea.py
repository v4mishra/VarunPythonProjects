#import numpy
#import fileinput
import re
import csv
import os
filepath = "C:/Users/VA009MI/Desktop/Measurements/UK/MM_GBR_GEOCODED.csv"
csv.register_dialect('pipes', delimiter='|')

def shoelacearea(pts):
    """ calculates the area using the shoelace formula """
    maxsides = len(pts)
    if(maxsides<3):
        area = None
    else:
        additive = 0
        for i in range(maxsides):
            # print i
            x1 = pts[i][0]
            y2 = pts[(i+1)%maxsides][1]
            # print(x1,y2, sep="~")
            additive += float(x1) * float(y2)
        area = abs(additive) * 0.5
    # print additive
    print (area)

def getPoint(x):
    if(len(x.strip())>0):
        return float(x)
    else:
        return 0.0



def calculateArea(inputFilePath):
    inputfile = open(inputFilePath)
    filename,ext = os.path.splitext(inputFilePath)
    outputFilePath = filename+"_output"+ext
    outputfile = open(outputFilePath,mode="w",newline="")
    csvWriter = csv.writer(outputfile,  dialect="pipes")

    print(inputFilePath)

    # read the points
    headerSkip = True
    for line in inputfile.readlines():

        if(headerSkip):
            headerSkip = False
            continue
        pts = []
        myarr = line.strip().split(';')
        # print(line.strip() + ';')  ### print out the ID
        for i in range(1, len(myarr), 2):
            pts.append([getPoint(x) for x in myarr[i:i + 2]])
        # print pts
        area = shoelacearea(pts)
        myarr.append(area)
        csvWriter.writerow(myarr)

    inputfile.close()
    outputfile.flush()
    outputfile.close()


    #     pts.append(line.strip().split())
    # # print pts
    # shoelacearea(pts)


calculateArea("C:/Users/VA009MI/Desktop/Measurements/3.input")
# inputFilePath = "C:/Users/VA009MI/Desktop/Measurements/3.input"
# # inputfile = open(inputFilePath)
# filename,ext = os.path.splitext(inputFilePath)
# outputFilePath = filename+"_output"+ext
# print(outputFilePath)
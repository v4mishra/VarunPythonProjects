
# Assuming inputFile contains just input address.
inputFile = "D:/MapMarker/MM_Code/MM_Maven/branches/Noida/local/VNM-CGGE/test/engperf/SingleLineAddress_Copy.txt"
outputFile = "D:/MapMarker/MM_Code/MM_Maven/branches/Noida/local/VNM-CGGE/test/engperf/MultiLine.txt"

def loadFileContents(inputFilePath):
    with open(inputFilePath, encoding="UTF-8", mode="r") as f:
        # content = f.readlines()
        content = f.read().splitlines()
        return content

def writeListToFile(ouputFilePath, listToWrite):
    outfile = open(ouputFilePath, mode="w", encoding="UTF-8", newline='\n')

    # print(*listToWrite, file=outfile, sep='\n')

    print("**********************")
    for record in listToWrite:
        # for item in record:
            print(*record, file=outfile, sep="|")

    outfile.flush()
    outfile.close()
    return None


def getMLAddress(slAddress):
    breakup =slAddress.rsplit(",", maxsplit=3)
    street = ""
    an3 = ""
    an2 = ""
    an1 = ""
    size = len(breakup)
    print(size)
    if (size == 4):
        street, an3, an2, an1 = breakup
    elif (size < 4):
        if (size >= 1): street = breakup[0]
        if (size == 2): an2 = breakup[1]
        if (size == 3):
            an2 = breakup[1]
            an1 = breakup[2]

    print('Street = {0}; AN3 = {1}; AN2= {2}; AN1 = {3}'.format(street, an3, an2, an1))

    return [slAddress, street, an3, an2, an1]


def transformToML(listSLAddresses):
    listMLAddress=[]

    for slAddress in listSLAddresses:
        listMLAddress.append(getMLAddress(slAddress))

    # listMLAddress.append([getMLAddress(slAddress) for slAddress in listSLAddresses])
    # print(*listMLAddress, sep="\n")
    return listMLAddress


def testVarun():
    listSLAddresses = loadFileContents(inputFile)
    # listSLAddresses = ["Phòng 317, CT5-ĐN5 , Khu ĐTM Mỹ Đình-Mễ Trì, Phường Mễ Trì, Quận Nam Từ Liêm, Hà Nội ",
    #                    "Phòng 601, tầng 6, tòa nhà Kim Ánh, ngõ 78, phố Duy Tân, Cầu Giấy, Hà Nội",
    #                    "KCN 1, THÀNH PHỐ BIÊN HÒA, ĐỒNG NAI"]
    listMLAddress = transformToML(listSLAddresses)
    writeListToFile(outputFile, listMLAddress)


def testSplit():
    input = "Phòng 317, CT5-ĐN5 , Khu ĐTM Mỹ Đình-Mễ Trì, Phường Mễ Trì, Quận Nam Từ Liêm, Hà Nội "
    rs = input.rsplit(",", maxsplit=3)

    street = ""
    an3 = ""
    an2 = ""
    an1 = ""
    size = len(rs)
    print(size)
    if (size == 4): street, an3, an2, an1 = rs
    if (size < 4):
        if (size >= 1): street = rs[0]
        if (size == 2): an2 = rs[1]
        if (size == 3):
            an2 = rs[1]
            an1 = rs[2]
    print('Street = {0}\nAN3 = {1}\nAN2= {2}\nAN1 = {3}'.format(street, an3, an2, an1))


testVarun()
# testSplit()

def printLol(item, level):
    if isinstance(item, list):
        for innerItem in item:
            printLol(innerItem, item)
    else:
        for tabIndex in range(level):
            print("\t", end='')
        print(item)


def printSimpleList(list):
    thefile = open('c:\\temp\\TechnoBankAddress.txt', 'w')
    for item in list:
        print(item, file=thefile)




myList = ["a","b","c","d","e"]

printSimpleList(myList)

print("inside printLOL module")

def printLol(item, level):
    if isinstance(item, list):
        for innerItem in item:
            printLol(innerItem, level+1)
    else:
        print("\t", end='')
        print(item)


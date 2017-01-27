import os




path = input("path ?")
print("thx")
if(os.path.exists(path)):
    print("path exists")
    with open(path,newline='\n') as resultFile:
        print(resultFile.readlines())
else:
    print("path dont exists")






import json
import pickle



def copyContentsWithPickle(file1, file2):
        try:
            with open(file1) as inputFile:

               #inputLoad = pickle.load(inputFile.readlines())

                with open(file2, "wb") as outputFile:
                    pickle.dump(inputFile.readlines(),outputFile)
        except IOError as err:
            print("Varun-Error: " + str(err))
        except pickle.PickleError as perr:
            print("Varun-Pickle-Error: " + str(perr))
        except TypeError as terr:
            print("Varun-type-Error: " + str(terr))


def copyContents(file1, file2):
    try:
        with open(file1,"r") as inputFile:
            with open(file2, "wb") as outputFile:
                inputFile.seek(0)
                for line in inputFile.readlines():
                    print(line,file=outputFile, end="")

    except IOError as err:
        print("Varun-Error: "+str(err))





copyContentsWithPickle("C:/varunTemp/txtFiles/source.txt", "c:/varunTemp/txtFiles/target.txt")
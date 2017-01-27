import pyperclip

def generateDistString():
    lat1 = input( "enter latitude 1:")
    lon1 = input( "enter longitude 1:")
    lat2 = input( "enter latitude 2:")
    lon2 = input( "enter longitude 2:")


    formula = "=(ACOS(COS(RADIANS(90-lat1dd))*COS(RADIANS(90-lat2dd))+SIN(RADIANS(90-lat1dd))*SIN(RADIANS(90-lat2dd))*COS(RADIANS(long1dd-long2dd))))*6373000"

    formula = formula.replace("lat1dd", lat1)
    formula = formula.replace("lat2dd", lat2)
    formula = formula.replace("long1dd", lon1)
    formula = formula.replace("long2dd", lon2)
    print("Distance between given geo-point in meters is calculated as - ")
	
    print(formula)
    print ("*** Formula Copied to your Clipboard *** ")
    pyperclip.copy(formula)
    


generateDistString()




    

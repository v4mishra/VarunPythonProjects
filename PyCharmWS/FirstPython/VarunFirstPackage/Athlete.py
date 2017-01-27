class Athlete:
    def __init__(self, name="", score=""):
        print("inside init method")
        self.name = name
        self.score = score

    def getName(self):
        return self.name

    def getScore(self):
        return self.score


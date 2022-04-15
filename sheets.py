import pygsheets

class Sheets:
    def __init__(self):
        self.client = pygsheets.authorize(service_file="boilpoint-bb8dfdb6d09a.json")

    def getTable(self):
        return self.client.open("BoilPoint")
        #wks = sh.sheet1

        #print(wks.cell('A2').value)
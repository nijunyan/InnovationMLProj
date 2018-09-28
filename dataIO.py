import os, json


def makeUpDataWithCategory(oData, aFeatures):
    oTargetData = {}
    for i in range(len(aFeatures)):
        oTargetData[aFeatures[i]] = oData[aFeatures[i]]
    return oTargetData

def getAllDataWithCategory(aFeatures = None):
    if aFeatures is None:
        aFeatures = [
            "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
            "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
            "PrjName", "PrjDescription", "PrjURL"
        ]

    dir = os.getcwd() + os.sep + "dataSet"
    file = "allprjdata.json"
    sData = retriveAllData(dir, file)

    aData = json.loads(sData)
    mData = {}
    for i in range(len(aData)):
        if aData[i]['SmartIndex1'] not in mData:
            mData[ aData[i]['SmartIndex1'] ] = []
        oTargetData = makeUpDataWithCategory(aData[i], aFeatures)
        mData[ aData[i]['SmartIndex1'] ].append(oTargetData)

    return mData

def makeUpDataInArray(oData, aFeatures):
    aTargetData = []
    for i in range(len(aFeatures)):
        aTargetData.append(oData[aFeatures[i]])
    return aTargetData

def getAllDataInArray(aFeatures = None):
    if aFeatures is None:
        aFeatures = [
            "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
            "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
            "PrjName", "PrjDescription", "PrjURL"
        ]

    dir = os.getcwd() + os.sep + "dataSet"
    file = "allprjdata.json"
    sData = retriveAllData(dir, file)

    aData = json.loads(sData)
    mData = {}
    for i in range(len(aData)):
        if aData[i]['SmartIndex1'] not in mData:
            mData[ aData[i]['SmartIndex1'] ] = []
        oTargetData = makeUpDataInArray(aData[i], aFeatures)
        mData[ aData[i]['SmartIndex1'] ].append(oTargetData)

    return mData

def getFileName(dir, file):
    return dir.strip(' ') + os.sep + file.strip(' ')

def buildFolder(aFolders=['SmartIndex1']):
    mData = getAllDataWithCategory(aFolders)
    dir = os.getcwd().strip(' ') + os.sep + 'dataSet' + os.sep + 'Categories'
    for k in mData.keys():
        mkdir(dir.strip(' ') + os.sep + k.strip(' '))

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print
        "---  new folder...  ---"
        print
        "---  OK  ---"

    else:
        print
        "---  There is this folder!  ---"

def createFile(dir, name, text=None, mode='w'):
    if not os.path.exists(dir):
        os.makedirs(dir)
    fileName = getFileName(dir, name)
    file = open(fileName, mode)
    if text != None:
        file.write(text)
    file.close()
    print('ok')

def readFileContent(dir, file):
    fileName = getFileName(dir, file)
    f = open(fileName, 'r', encoding='utf8')
    str = f.read()
    f.close()
    return str

def writeFileWithContent(dir, file, content):
    fileName = getFileName(dir, file)
    f = open(fileName, 'w', encoding='utf8')
    f.write(content)
    f.close()

def appendStrDatatoJsonFile(strData, jsonFile, jsonFiledir):
    sJsonFileData = readFileContent(jsonFiledir, jsonFile)
    obj = json.loads(sJsonFileData)

    newObj = getPyObject(strData)
    newObj["ID"] = len(obj) + 1

    obj.append(newObj)
    obj = json.dumps(obj, indent=2)
    writeFileWithContent(jsonFiledir, jsonFile, obj)
    return obj

def getPyObject(strData):
    tmpFileDir = os.getcwd() + os.sep + "tmp"
    tmpFile = "tmp.json"
    createFile(tmpFileDir, tmpFile, text=strData, mode='w')
    nstr = readFileContent(tmpFileDir, tmpFile)
    newObj = json.loads(nstr)
    return newObj

def retriveAllData(dir, file):
    fileName = getFileName(dir, file)
    f = open(fileName, 'r', encoding='utf8')
    str = f.read()
    return str

def main():
    strData = '''{
                                    "ID": 3,
                                    "City": "Stuttgart",
                                    "Country": "Germany",
                                    "IndexGrp": "Real_time_traveller_Information",
                                    "CityArea": 297.36,
                                    "Population": 623738,
                                    "PerCapita": 65262,
                                    "SmartIndex1": "Traffic_Time_Index",
                                    "SmartIndexValue": 32.05,
                                    "PrjDuration": 7,
                                    "PrjCost": 8,
                                    "PrjROI": 7,
                                    "PrjName": "The moveBW project offers drivers an attractive option that links motorized personal transport with alternative modes of transportation. An easy-to-use mobility assistant on your smartphone helps you choose a mode of transportation and reliably guides you to your destination. Users of the mobility assistant can book different types of transportation â€“ yet receive just one bill that lists every mode booked during the past month. To plan intermodal routes, the mobility assistant considers services such as public transportation, car sharing, bike sharing, and parking-space management as well as information on traffic jams and construction areas. MoveBW encourages people in the greater Stuttgart area to efficiently utilize all modes of transportation, which eases congestion. This project also aids local authorities in optimizing regional traffic flows.MoveBW is overseen by a consortium of six companies, led by Robert Bosch GmbH: transportation solutions company highQ, parking-space operator Parkraumgesellschaft Baden-WÃ¼rttemberg, TraffiCon GmbH, PRISMA Solutions GmbH, and MRK Management Consultants. The moveBW project began in mid-2016 and will end in late 2017.",
                                    "PrjDescription": "moveBW - mobility assistant for intermodal information, planning routes, and buying tickets",
                                    "PrjURL": "https://hyp.is/0W2vcK_8Eei-2AfXYJ_wFw"
                                  }'''.strip('"')
    dir = os.getcwd() + os.sep + "dataSet"
    file = 'allprjdata.json'
    appendStrDatatoJsonFile(strData, file, dir)
if __name__ == "__main__":
    main()
import os, json
from sklearn.externals import joblib

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
    os.chdir('..')
    dir = os.getcwd() + os.sep + "dataSet"
    file = "all-data.json"
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
    os.chdir('..')
    dir = os.getcwd() + os.sep + "dataSet"
    file = "all-data.json"
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
    os.chdir('..')
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

    aNewData = getPyObject(strData)
    for i in range(len(aNewData)):
        aNewData[i]["ID"] = len(obj) + i + 1
        obj.append(aNewData[i])

    obj = json.dumps(obj, indent=2)
    writeFileWithContent(jsonFiledir, jsonFile, obj)
    return obj

def getPyObject(strData):
    os.chdir('..')
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

def getModel(category, sModelType):
    os.chdir('..')
    dir = os.getcwd() + os.sep + 'Models' + os.sep + category.strip(' ')
    file = category.strip(' ') + '-' + sModelType.strip(' ') + ".m"
    modelFileName = getFileName(dir, file)
    model = joblib.load(modelFileName)
    return model

def preserveModel(category, sModelType, model):
    os.chdir('..')
    dir = os.getcwd() + os.sep + 'Models' + os.sep + category.strip(' ')
    file = category.strip(' ') + '-' + sModelType.strip(' ') + ".m"
    modelFileName = getFileName(dir, file)
    joblib.dump(model, modelFileName)

def initJSONfiles():
    def initJSONFilesInDir(dirName):
        aFeatures = [
            "SmartIndex1"
        ]
        mData = getAllDataWithCategory(aFeatures)
        for k in mData.keys():
            dir = os.getcwd() + os.sep + 'dataSet' + os.sep + dirName.strip(' ')
            file = dirName.strip(' ')  + '-' + k.strip(' ') + '-data.json'
            createFile(dir, file, text="[]")
        pass

    initJSONFilesInDir("DataWithCategories")
    initJSONFilesInDir("DataWithLabels")
    initJSONFilesInDir("DataProcessedWithLabels")

def initFolders():
    aFeatures = [
        "SmartIndex1"
    ]
    mData = getAllDataWithCategory(aFeatures)
    for k in mData.keys():
        os.chdir('..')
        dir = os.getcwd() + os.sep + 'Models' + os.sep + k.strip(' ')
        mkdir(dir)

if __name__ == "__main__":
    initFolders()
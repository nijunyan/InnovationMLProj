import os, json
from sklearn.externals import joblib

def makeUpDataWithCategory(oData, aFeatures):
    oTargetData = {}
    for i in range(len(aFeatures)):
        oTargetData[aFeatures[i]] = oData[aFeatures[i]]
    return oTargetData

def getAllDataWithCategory(aFeatures = None, dir = None):
    if aFeatures is None:
        aFeatures = [
            "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
            "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
            "PrjName", "PrjDescription", "PrjURL"
        ]
    if dir is None:
        dir = os.path.abspath('../..') + os.sep + "dataSet"
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

def getAllOriginalData():
    dir = os.path.abspath('../..') + os.sep + "dataSet"
    file = "all-data.json"
    sData = readFileContent(dir, file)
    aData = json.loads(sData)
    return json.dumps(aData, indent=2)

def getOneOriginalData():
    dir = os.path.abspath('../..') + os.sep + "dataSet"
    file = "all-data.json"
    sData = readFileContent(dir, file)
    aData = json.loads(sData)
    return json.dumps(aData[0], indent=2)

def makeUpDataInArray(oData, aFeatures):
    aTargetData = []
    for i in range(len(aFeatures)):
        aTargetData.append(oData[aFeatures[i]])
    return aTargetData

def getAllData(aFeatures = None):
    if aFeatures is None:
        aFeatures = [
            "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
            "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
            "PrjName", "PrjDescription", "PrjURL"
        ]
    dir = os.path.abspath('../..') + os.sep + "dataSet"
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
    dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + 'Categories'
    for k in mData.keys():
        mkdir(dir.strip(' ') + os.sep + k.strip(' '))

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)
        print
        "---  new folder../...  ---"
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

def appendStrDatatoJsonFile(sData, jsonFiledir, jsonFile, beginID = 0):
    sJsonFileData = readFileContent(jsonFiledir, jsonFile)
    obj = json.loads(sJsonFileData)

    aNewData = getPyObject(sData)

    if isinstance(aNewData, dict):
        aNewData = [aNewData]

    aFeatures = [
        "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
        "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
        "PrjName", "PrjDescription", "PrjURL"
    ]
    iSize = len(obj)
    for i in range(len(aNewData)):
        oData = {}
        aNewData[i]["ID"] = beginID + iSize + i + 1
        for j in range(len(aFeatures)):
            if aFeatures[j] not in aNewData[i]:
                aNewData[i][aFeatures[j]] = " "
            oData[aFeatures[j]] = aNewData[i][aFeatures[j]]
        obj.append(oData)

    str = json.dumps(obj, indent=2)
    createFile(jsonFiledir, jsonFile, str, mode='w')
    return obj

def getTmpAllDataID(dir=None, file=None):
    if dir is None:
        dir = os.path.abspath('../..') + os.sep + "dataSet"
        file = "all-data.json"
    str = readFileContent(dir, file)
    j = json.loads(str)
    id = len(j)
    return id

def appendStrData(sData, sFileLocation, sCategory):
    if sFileLocation == "DataWithCategories":
        dir = os.path.abspath('../..') + os.sep + "dataSet" + os.sep + "tmp" + os.sep + sCategory.strip(' ')
        file = "tmp-DataWithCategories-" + sCategory.strip(' ') + "-data.json"
    elif sFileLocation == "DataWithLabels":
        dir = os.path.abspath('../..') + os.sep + "dataSet" + os.sep + "tmp" + os.sep + sCategory.strip(' ')
        file = "tmp-DataWithLabels-" + sCategory.strip(' ') + "-data.json"
    elif sFileLocation == "tmpAllData":
        dir = os.path.abspath('../..') + os.sep + "dataSet"
        file = "all-data.json"
        beginID = getTmpAllDataID(dir, file)
        dir = os.path.abspath('../..') + os.sep + "dataSet" + os.sep + "tmp"
        file = "tmp-allData.json"
    elif sFileLocation == "importTmpAllData": # merge tmpData to all-data.json
        dir = os.path.abspath('../..') + os.sep + "dataSet" + os.sep + "tmp"
        file = "tmp-allData.json"
        sData = readFileContent(dir, file)
        dir = os.path.abspath('../..') + os.sep + "dataSet"
        file = "all-data.json"
        beginID = 0

    appendStrDatatoJsonFile(sData, dir, file, beginID)

def getData(sFileLocation, sCategory):
    if sFileLocation == "DataWithLabels":
        dir = os.path.abspath('../..') + os.sep + "dataSet" + os.sep + "DataWithLabels" + os.sep + sCategory.strip(' ')
        file = "DataWithLabels-" + sCategory.strip(' ') + "-data.json"
    elif sFileLocation == "Cluster":
        dir = os.path.abspath('../..') + os.sep + "Models" + os.sep + sCategory.strip(' ')
        file = sCategory.strip(' ') + "-cluster.json"

    sData = readFileContent(dir, file)
    return json.loads(sData)

def getPyObject(sData):
    tmpFileDir = os.path.abspath('../..') + os.sep + "tmp"
    tmpFile = "tmp.json"
    createFile(tmpFileDir, tmpFile, text=sData, mode='w')
    nstr = readFileContent(tmpFileDir, tmpFile)
    newObj = json.loads(nstr)
    return newObj

def getStrFromJSON(obj):
    return json.dumps(obj, indent=2)

def retriveAllData(dir, file):
    fileName = getFileName(dir, file)
    f = open(fileName, 'r', encoding='utf8')
    str = f.read()
    f.close()
    return str

def retriveAllClusters():
    aFeatures = [
        "SmartIndex1"
    ]
    mData = getAllDataWithCategory(aFeatures)
    mClusters = {}
    for key in mData.keys():
        dir = os.path.abspath('../..') + os.sep + 'Models'+ os.sep + key.strip(' ')
        file = key.strip(' ') + "-cluster.json"
        mClusters[key.strip(' ')] = {}
        sData = readFileContent(dir, file)
        aData = json.loads(sData)
        for i in range(len(aData)):
            sLabel = str(i)
            mClusters[key.strip(' ')][sLabel] = aData[i]
    return json.dumps(mClusters, indent=2)

def getModel(category, sModelType):
    dir = os.path.abspath('../..') + os.sep + 'Models' + os.sep + category.strip(' ')
    file = category.strip(' ') + '-' + sModelType.strip(' ') + ".m"
    modelFileName = getFileName(dir, file)
    model = joblib.load(modelFileName)
    return model

def preserveModel(category, sModelType, model):
    dir = os.path.abspath('../..') + os.sep + 'Models' + os.sep + category.strip(' ')
    file = category.strip(' ') + '-' + sModelType.strip(' ') + ".m"
    modelFileName = getFileName(dir, file)
    joblib.dump(model, modelFileName)

def preserveProcessedData(mMarkedX, mDataWithLabels, mDataWithCategories, mClusters):
    def preserveMData(dir, file, aList, aFeatures):
        aData = []

        for i in range(len(aList)):
            mData = {}
            for j in range(len(aFeatures)):
                mData[aFeatures[j]] = aList[i][j]
            aData.append(mData)

        str = json.dumps(aData, indent=2)
        createFile(dir, file, str)

    for k in mClusters.keys():
        aFeatures = [
            "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
            "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
            "PrjName", "PrjDescription", "PrjURL", "Label"
        ]
        dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + 'DataWithLabels' + os.sep + k.strip(' ')
        file = 'DataWithLabels-' + k.strip(' ') + '-data.json'
        preserveMData(dir, file, mDataWithLabels[k], aFeatures)

        aFeatures = [
            "ID", "City", "Country", "IndexGrp", "CityArea", "Population", "PerCapita",
            "SmartIndex1", "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI",
            "PrjName", "PrjDescription", "PrjURL"
        ]
        dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + 'DataWithCategories'+ os.sep + k.strip(' ')
        file = 'DataWithCategories-' + k.strip(' ') + '-data.json'
        preserveMData(dir, file, mDataWithCategories[k],aFeatures)

        aFeatures = [
            "CityArea", "Population", "PerCapita",
            "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI"
        ]
        dir = os.path.abspath('../..') + os.sep + 'Models' + os.sep + k.strip(' ')
        file = k.strip(' ') + '-cluster.json'
        preserveMData(dir, file, mClusters[k], aFeatures)

    pass

def checkJSON():
    aFeatures = [
        "SmartIndex1"
    ]
    mData = getAllDataWithCategory(aFeatures)
    for k in mData.keys():
        dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + 'DataWithLabels' + os.sep + k.strip(' ')
        file = 'DataWithLabels-' + k.strip(' ') + '-data.json'
        str = readFileContent(dir, file)
        j = json.loads(str)
        pass

##########################
def initJSONfiles():
    def initJSONFilesInDir(dirName):
        aFeatures = [
            "SmartIndex1"
        ]
        mData = getAllDataWithCategory(aFeatures)
        for k in mData.keys():
            dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + dirName.strip(' ')
            file = dirName.strip(' ')  + '-' + k.strip(' ') + '-data.json'
            createFile(dir, file, text="[]")
        pass

    initJSONFilesInDir("DataWithCategories")
    initJSONFilesInDir("DataWithLabels")
    initJSONFilesInDir("DataProcessedWithLabels")

def initTMPJSONfiles():
    # dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + 'tmp'
    # initFolders(dir)
    aFeatures = [
        "SmartIndex1"
    ]
    mData = getAllDataWithCategory(aFeatures)
    for k in mData.keys():
        dir = os.path.abspath('../..') + os.sep + 'dataSet' + os.sep + 'tmp' + os.sep + k.strip(' ')
        file = 'tmp-DataWithCategories-' + k.strip(' ') + '-data.json'
        createFile(dir, file, text="[]")
        file = 'tmp-DataWithLabels-' + k.strip(' ') + '-data.json'
        createFile(dir, file, text="[]")
    pass

def initFolders(dir):
    aFeatures = [
        "SmartIndex1"
    ]
    mData = getAllDataWithCategory(aFeatures)
    for k in mData.keys():
        cdir = dir + os.sep + k.strip(' ')
        mkdir(cdir)

if __name__ == "__main__":
    # appendStrData("", "importTmpAllData", None)
    j = retriveAllClusters()
    pass

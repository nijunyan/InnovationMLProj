import src.MLapp.DataIO as DataIO
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import KMeans

from tmp import SVM


def dataPreprocessingForAll(mData):
    mX = {}
    mScaler = {}
    for key, X in mData.items():
        mScaler[key] = {}
        mX[key], mScaler[key] = dataProcessing(key, X)
    return mX, mScaler

def dataProcessing(key, X):
    originalX = np.array(X)
    scaler = preprocessing.StandardScaler()
    X = scaler.fit_transform(originalX)

    DataIO.preserveModel(key, 'scaler', scaler)

    return X, scaler

def doClustering(X):
    if X.shape[0] >= 3:
        n_clusters_guess = 3
    else:
        n_clusters_guess = X.shape[0]
    print(X)
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_guess, n_init=5)
    k_means.fit(X)

    return k_means.cluster_centers_, k_means.labels_

def doAnalyzing(mX, aDtaWithCategory):
    index = 1
    mMarkedX = mX
    mClusters = {}
    mDataWithLabels = {}
    for key, X in mX.items():
        print(key)
        mClusters[key], labels = doClustering(X)
        mMarkedX[key] = np.c_[mMarkedX[key], labels]
        mDataWithLabels[key] = np.c_[aDtaWithCategory[key], labels]
        index += 1
        print (labels)


    return mMarkedX, mClusters, mDataWithLabels

def doTraining(mMarkedX):
    for key, X in mMarkedX.items():
        doSVM(X[:,0:-1], mMarkedX[key][:, -1], key)

def doSVM(X, Y, key):
    clf = SVM.doSVM(X, Y)
    DataIO.preserveModel(key, 'clf', clf)
    pass

def transformOnePiceOfData():
    pass

#initial clustering
def initialClusteringAndBuildCLF():
    mDataWithCategories = DataIO.getAllData()
    aFeatures = [
        "CityArea", "Population", "PerCapita",
        "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI"
    ]
    mDataWithCategoriesForClustering = DataIO.getAllData(aFeatures)

    mNewX, mScaler = dataPreprocessingForAll(mDataWithCategoriesForClustering)

    mMarkedX, mClusters, mDataWithLabels = doAnalyzing(mNewX, mDataWithCategories)

    DataIO.preserveProcessedData(mMarkedX, mDataWithLabels, mDataWithCategories, mClusters)

    doTraining(mMarkedX)

    print

def predict():
    category = 'Traffic_Time_Index'
    sData = '''{
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
    predictFromCLF(category, sData)

def predictFromCLF(category, sData):
    clf = DataIO.getModel(category, 'clf')
    scaler = DataIO.getModel(category, 'scaler')

    aFeatures = [
        "CityArea", "Population", "PerCapita",
        "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI"
    ]

    oData = DataIO.getPyObject(sData)
    aData = [(DataIO.makeUpDataInArray(oData, aFeatures))]
    aTransformedData = scaler.transform(aData)
    label = clf.predict(aTransformedData)
    print(label)
    return label

def commitData(sList):
    aData = DataIO.getPyObject(sList)
    aRetData = []
    for i in range(len(aData)):
        sCategory = aData[i]["SmartIndex1"]
        oData = aData[i]
        sData = DataIO.getStrFromJSON(oData)
        label = predictFromCLF(sCategory, sData)
        sLabel = str(int(label[0]))
        DataIO.appendStrData(sData, "tmpAllData", sCategory)

        aCategoryData = DataIO.getData("DataWithLabels", sCategory)

        aOneRetData = [aCategoryData[j] for j in range(len(aCategoryData)) if aCategoryData[j]["Label"] == sLabel ]
        oRetData = {}
        oData["ID"] = DataIO.getTmpAllDataID()
        oData["Label"] = sLabel
        oRetData["queryData"] = oData
        oRetData["neighbourCnt"] = len(aOneRetData)
        oRetData["neighbourData"] = aOneRetData
        aRetData.append(oRetData)

    return DataIO.getStrFromJSON(aRetData)

def main():
    sData = '''[{
        "ID": "4724",
        "City": "David",
        "Country": "Panama",
        "IndexGrp": " Parking Management",
        "CityArea": "1004.4426",
        "Population": "2423851.85",
        "PerCapita": "92053.29",
        "SmartIndex1": " Traffic_Time_Index",
        "SmartIndexValue": "41.4827",
        "PrjDuration": "7.6",
        "PrjCost": "7.6",
        "PrjROI": "6.6",
        "PrjName": "Fast and easy to shop or to go to the city center? This works very easy in Hamburg. With the Park and Joy app, drivers can quickly find, book and pay for free parking spaces - all via smartphone. Parking has never been so much fun!",
        "PrjDescription": "Park and Joy",
        "PrjURL": "https://www.parkandjoy.de/hamburg",
        "Label": "1"
      }]'''.strip('"')

    s = commitData(sData)
    pass
if __name__=="__main__":
    main()
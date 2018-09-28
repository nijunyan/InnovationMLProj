import os
import numpy as np

from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.cluster import KMeans

import dataIO, SVM

def dataPreprocessingForAll(mData):
    mX = {}
    mRangeX = {}
    for key, value in mData.items():
        mRangeX[key] = {}
        mX[key], mRangeX[key]["data_max_"], mRangeX[key]["data_min_"] = dataProcessing(value)
    return mX, mRangeX

def dataProcessing(data):
    original_X = np.array(data)
    min_max_scaler = preprocessing.MinMaxScaler()
    X = min_max_scaler.fit_transform(original_X)
    return X, min_max_scaler.data_max_, min_max_scaler.data_min_

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
        doSVM(X, mMarkedX[key][:, -1], key)

def doSVM(X, Y, key):
    clf = SVM.doSVM(X, Y)
    dir = os.getcwd().strip(' ') + os.sep + 'dataSet' + os.sep + 'Categories' + os.sep + key.strip()
    file = key.strip(' ') + ".m"
    dataIO.createFile(dir, file)
    clfFileName = dataIO.getFileName(dir, file)
    joblib.dump(clf, clfFileName)
    pass

def transformOnePiceOfData():
    pass

#initial clustering
def initialClustering():
    aDataWithCategory = dataIO.getAllDataInArray( )
    aFeatures = [
        "CityArea", "Population", "PerCapita",
        "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI"
    ]
    aDataWithCategoryForClustering = dataIO.getAllDataInArray(aFeatures)

    mNewX, mRangeX = dataPreprocessingForAll(aDataWithCategoryForClustering)

    mMarkedX, mClusters, mDataWithLabels = doAnalyzing(mNewX, aDataWithCategory)

    doTraining(mMarkedX)

    print


def predictFromCLF(dir, file):
    clfName = dataIO.getFileName(dir, file)
    clf = joblib.load(clfName)
    aFeatures = [
        "CityArea", "Population", "PerCapita",
        "SmartIndexValue", "PrjDuration", "PrjCost", "PrjROI"
    ]

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

    oData = dataIO.getPyObject(sData)
    aData = dataIO.makeUpDataInArray(oData, aFeatures)
    print(clf.predit(aData))

def main():
    # initialClustering()
    dir = os.getcwd() + os.sep + 'dataSet' + os.sep + 'Categories' + os.sep + 'Traffic_Time_Index'
    file = 'Traffic_Time_Index.m'
    predictFromCLF(dir, file)

if __name__=="__main__":
    main()
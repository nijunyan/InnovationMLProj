import xlrd, time
import numpy as np

from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#open excel
def open_excel(file= 'test.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))

def aquire_column_for_features(colnames):
    feature_columns = [
        'City Area (in SQ KM)',
        'City Population',
        'City Per Capita Income ($)'
    ]
    # feature_columns = [
    #     'Project Duration Index',
    #     'Project Cost Index',
    #     'Project ROI Index'
    # ]

    feature_column_indexes = []
    for colname_index in range(0, len(colnames)):
        for feature_column_index in range(0, len(feature_columns)):
            if colnames[colname_index] == feature_columns[feature_column_index]:
                feature_column_indexes.append(colname_index)
                break

    return feature_column_indexes

#convert excel to list
def excel_table_byname(file= 'test.xlsx', colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #sum of rows
    colnames = table.row_values(colnameindex) #row header

    feature_columns = aquire_column_for_features(colnames)

    list =[]
    for rownum in range(1, nrows): #traverse the rows
         row = table.row_values(rownum) #row number
         if row:
             app = []
             for i in range(len(feature_columns)): #traverse columns
                app.append(row[feature_columns[i]])
             list.append(app) #load data
    return list

def dataPreprocessing(data):

    # return preprocessing.scale(np.array(data)) #normalize can not fit new piece of data

    X = np.array(data)
    min_max_scaler = preprocessing.MinMaxScaler()
    X = min_max_scaler.fit_transform(X)
    # pca = PCA(n_components=2)
    # pca.fit(X)
    return X

def doClustering(X):
    n_clusters_guess = 4
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_guess, n_init=5)
    t0 = time.time()
    k_means.fit(X)
    t_batch = time.time() - t0

    #prepare result
    k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)
    k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)

    print(k_means_cluster_centers)
    # colors = ['#4EACC5', '#FF9C34', '#4E9A06', 'r']
    colors = ['r','g','b','black']
    fig = plt.figure(figsize=(15, 15))

    # plot 3D
    ax = plt.subplot(111, projection='3d')
    for k, col in zip(range(n_clusters_guess), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.scatter(X[my_members, 0], X[my_members, 1], X[my_members, 2], c=col, s=80)
        ax.scatter(cluster_center[0], cluster_center[1], cluster_center[2], c=col, s=300)

    #plot 2D
    # ax = fig.add_subplot(1, 1, 1)
    # for k, col in zip(range(n_clusters_guess), colors):
    #     my_members = k_means_labels == k
    #     cluster_center = k_means_cluster_centers[k]
    #     ax.plot(X[my_members, 0], X[my_members, 1], 'w',
    #             markerfacecolor=col, marker='.', markersize=16)
    #     # ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #     #         markeredgecolor='k', markersize=16)

    plt.show()

#main
def main():
   filename = 'C:\Data_04_Sept_2018.xlsx'
   raw_data = excel_table_byname(file=filename, by_name='Data_ML_Input')
   new_X = dataPreprocessing(raw_data)
   doClustering(new_X)

   print


if __name__=="__main__":
    main()
import xlrd, time
import numpy as np
import pandas as pd

from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

all_labels = {}


# open excel
def open_excel(file='test.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


def aquire_column_for_features(colnames):
    feature_columns = [
        'City Area (in SQ KM)',
        'City Population',
        'City Per Capita Income ($)',
        'Smart City Index Value',
        'Project Duration Index',
        'Project Cost Index',
        'Project ROI Index'
    ]

    project_type = 'Smart City Index Name'

    feature_column_indexes = []
    project_type_index = 0
    for colname_index in range(0, len(colnames)):
        for feature_column_index in range(0, len(feature_columns)):
            if colnames[colname_index] == feature_columns[feature_column_index]:
                feature_column_indexes.append(colname_index)
                break
        if project_type == colnames[colname_index]:
            project_type_index = colname_index

    return feature_column_indexes, project_type_index


# convert excel to list
def excel_table_byname(file='test.xlsx', colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows  # sum of rows
    colnames = table.row_values(colnameindex)  # row header

    feature_columns, project_type_index = aquire_column_for_features(colnames)

    list = []
    project_tag_list = []
    project_features_for_each_tag = {}
    project_for_each_tag = {}
    for rownum in range(1, nrows):  # traverse the rows
        row = table.row_values(rownum)  # row number
        bNumeric = True
        if row:
            app = []
            for i in range(len(feature_columns)):  # traverse columns
                if type(row[feature_columns[i]]) != float:
                    bNumeric = False
                    break
                app.append(row[feature_columns[i]])
            if bNumeric:
                list.append(app)
                project_tag_list.append(row[project_type_index])

                if row[project_type_index] not in project_features_for_each_tag:
                    project_features_for_each_tag[row[project_type_index]] = []
                project_features_for_each_tag[row[project_type_index]].append(app)

                if row[project_type_index] not in project_for_each_tag:
                    project_for_each_tag[row[project_type_index]] = []
                project_for_each_tag[row[project_type_index]].append(rownum)

    return list, project_tag_list, project_for_each_tag, project_features_for_each_tag


def dataPreprocessing(data):
    Xs = {}
    labels = {}
    for key, value in data.items():
        X = np.array(value)
        min_max_scaler = preprocessing.MinMaxScaler()
        X = min_max_scaler.fit_transform(X)
        # pca = PCA(n_components=3)
        # pca.fit(X)
        Xs[key] = X
        # print(Xs[key])
        labels[key] = [-1] * len(X)
    return Xs, labels


def doAnalyzing(Xs, labels):
    plt.figure(figsize=(30, 50))
    index = 1
    marked_Xs = Xs
    for key, X in Xs.items():
        print(key)
        labels[key] = doClustering(X, index, key)
        marked_Xs[key] = np.c_[marked_Xs[key], labels[key]]
        print(labels[key])
        index += 1
    # plt.show()
    return marked_Xs, labels


def doClustering(X, index, key, ):
    if X.shape[0] >= 3:
        n_clusters_guess = 3
    else:
        n_clusters_guess = X.shape[0]
    print(X)
    k_means = KMeans(init='k-means++', n_clusters=n_clusters_guess, n_init=5)
    # t0 = time.time()
    k_means.fit(X)
    # t_batch = time.time() - t0

    # prepare result
    # k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)
    # k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)

    # print(k_means_cluster_centers)
    colors = ['r', 'g', 'b', 'black']

    # plot 3D
    # ax = plt.subplot(3, 5, index, projection='3d')
    # ax.set_title(key)
    # for k, col in zip(range(n_clusters_guess), colors):
    #     my_members = k_means_labels == k
    #     cluster_center = k_means_cluster_centers[k]
    #     ax.scatter(X[my_members, 0], X[my_members, 1], X[my_members, 2], c=col, s=20)
    #     ax.scatter(cluster_center[0], cluster_center[1], cluster_center[2], c=col, s=80)
    #
    # f = plt.figure(index)

    return k_means.labels_


# main
def main():
    # clustering
    filename = 'C://Users//I341712//Downloads//SmartCityProjectsData.xlsx'
    raw_data, project_tag_list, project_for_each_tag, project_features_for_each_tag = excel_table_byname(file=filename,
                                                                                                         by_name='Data_ML_Input')
    new_Xs, labels = dataPreprocessing(project_features_for_each_tag)
    marked_Xs, marked_labels = doAnalyzing(new_Xs, labels)
    print
    # search item


if __name__ == "__main__":
    main()
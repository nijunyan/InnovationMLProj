import numpy as np
from sklearn import svm

from tmp import dataIO


def doSVM(X, Y):
    clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    clf.fit(X, Y)
    # dec = clf.decision_function([[1]])
    # print(dec.shape[1])
    # clf.decision_function_shape = "ovr"
    # dec = clf.decision_function([[1]])
    # print(dec.shape[1])
    # print(clf.predict([[4]]))
    # folder = "C://Users//I341712//Downloads//ML_Folders"
    # IO.createFile(dir = folder, name = 'train_model.m', mode='rb')
    return clf


if __name__ == '__main__':
    X = np.array([[1, 2, 3], [2, 3, 3], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]])
    Y = np.array([1, 2, 3, 4, 5, 6])

    clf = dataIO.getModel('Traffic_Time_Index', 'clf')

    print(clf.predict([[-1.2181079,  -1.05912942,  0.3075477,  -0.66615276, -0.17745426,  0.80554649,
  1.20684575]]))
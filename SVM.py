from sklearn import svm
from sklearn.externals import joblib
import numpy as np, mIO

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
    joblib.dump(clf, "C://Users//I341712//Downloads//ML_Folders//train_model.m")
    return clf


if __name__ == '__main__':
    X = np.array([[0], [0], [0], [0], [0], [0]])
    Y = np.array([0, 0, 0,0,0,0])
    doSVM(X, Y)
    clf = joblib.load("C:\\Users\\I341712\\Downloads\\ML_Folders\\train_model.m")
    print(clf.predict([[4]]))
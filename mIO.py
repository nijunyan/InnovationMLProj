import xlrd, os, json

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
    fileName = dir.strip(' ') + os.sep + name.strip(' ')
    file = open(fileName, mode)
    if text != None:
        file.write(text)
    file.close()
    print('ok')

def open_excel(file= 'test.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (str(e))


def aquire_column_for_features(colnames, feature_columns=[
    'City',
    'Country',
    'Index Group',
    'City Area (in SQ KM)',
    'City Population',
    'City Per Capita Income ($)',
    'Smart City Index Name',
    'Smart City Index Value',
    'Project Duration Index',
    'Project Cost Index',
    'Project ROI Index',
    'Project Name',
    'Project Description',
    'Project URL'
]):
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

def jsonToStr(j):
    str = json.loads(s=j)
    return str

def strToJson(s):
    j = json.dumps(s)
    return j

def readJsonFile(file="read_json.json"):
    f = open(file, 'r', encoding='utf8')
    str = f.read()
    d = json.loads(str)
    return d

def appendStrtoJsonFile(str, file):
    pass

def retriveAllData():
    return {}

def main():
    file = "C:\\Users\\I341712\\Downloads\\ML_Folders\\dataSet\\allprjdata.json"
    readJsonFile(file)

if __name__ == "__main__":
    a = 1
    b = a + 2
    c = b
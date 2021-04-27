import pandas as pd
def listMaker(data,column,initial):
    """
    it's mainly used to remove duplicates and add the 'all' parameter)
    """
    newList = data[column].tolist()
    newList = list(set(newList))
    newList.append(initial)
    return tuple(newList)

def findTowerType(data):
    """
    find tower types from the main use column
    """
    criteria= '|'.join(['commercial','mall','retail'])
    search1 = data['Main use'].str.contains('residential').tolist()
    search2 = data['Main use'].str.contains(criteria).tolist()
    other =[]
    for i in range(len(search1)):
        if search1[i] == False and search2[i] == False:
            other.append(True)
        else:
            other.append(False)
    data['r'] = search1
    data['c'] = search2
    data['o'] = other
    return data

def dataForMap(data):
    """
    colors and lat/lon
    """
    colorList=[]
    #creating a list of colors
    for i in range(len(data.index)):
        if data['r'].tolist()[i] == True:
            colorList.append('red')
        elif data['c'].tolist()[i] == True:
            colorList.append('blue')
        else:
            colorList.append('green')
    usefuldata = {'name':data['Name'].tolist(),'height':data['Meters'].tolist(),'remark':data['Remarks'].tolist(),'lat':data['Lat'].tolist(),'lon':data['Lon'].tolist(),'colors':colorList}
    newData = pd.DataFrame(usefuldata)
    return newData

def sortData(data,country='All',height={'min':0,'max':830},types={'r':True,'c':True,'o':True}):
    """
    will sort the data
    """
    data = findTowerType(data)
    if country != 'All':
        filtered = data.loc[data['Country'] == country]
    else:
        filtered = data
    #removing skyscrapers outside the height range choosen by the user
    filterHeight = filtered.loc[data['Meters'] >= height['min']]
    filterHeight = filterHeight.loc[filterHeight['Meters'] <= height['max']]
    #type filtering
    finaleDataFrame = pd.DataFrame()
    for j,row in filterHeight.iterrows():
        for i in list(types.items()):
            if i[1] == True:
                if row[i[0]] == i[1]:
                    finaleDataFrame = finaleDataFrame.append(row,ignore_index=True)
    if len(finaleDataFrame.index)>0:
        return dataForMap(finaleDataFrame)
    else:
        return finaleDataFrame

def specificTowers(data,towerNames):
    """
    return usefull data for the map orresponding to one specific tower
    """
    specificRows = data.loc[data['Name'].isin(towerNames)]
    return specificRows
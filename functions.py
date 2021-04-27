import pandas as pd
def listMaker(data,column,initial):
    """
    Function that takes a pandas dataFrame and gets the list of all the items in it, it also adds an option(initial)
    """
    newList = data[column].tolist()
    newList = list(set(newList))
    #adding value to the end of the list
    newList.append(initial)
    return tuple(newList)

def findTowerType(data):
    """
    find tower main usage, this function takes a pandas dataframe and adds 3 new columns each corresponding to a domain( residential ...)
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
    #Adding the data to the dataframe
    data['r'] = search1
    data['c'] = search2
    data['o'] = other
    return data

def dataForMap(data):
    """
    function that formats data to a lighter dataframe, called before rendering
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
    #creation of new data frame
    usefuldata = {'name':data['Name'].tolist(),'height':data['Meters'].tolist(),'remark':data['Remarks'].tolist(),'lat':data['Lat'].tolist(),'lon':data['Lon'].tolist(),'colors':colorList}
    newData = pd.DataFrame(usefuldata)
    return newData

def sortData(data,country='All',height={'min':0,'max':830},types={'r':True,'c':True,'o':True}):
    """
    main function that filters all the data depending on user input
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
    #returning filtered data or empty dataframe if no results where found
    if len(finaleDataFrame.index)>0:
        return dataForMap(finaleDataFrame)
    else:
        return finaleDataFrame

def specificTowers(data,towerNames):
    """
    function that filters the data and leaves only the towers choosen by the user
    """
    #filtering the data
    specificRows = data.loc[data['Name'].isin(towerNames)]
    return specificRows
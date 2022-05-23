import pandas as pd
import numpy as np

def UPGMA(distanceMatrix):

    tree=[]
    print("ORIGINAL MATRIX:")
    print("****************")
    print(distanceMatrix)
    iterations =1
    while(True):
        if(len(distanceMatrix. columns) == 2):
            for col in distanceMatrix.columns:
                found = False
                for treeElement in tree:
                    if col == treeElement.replace('+',''):                                             #3shan ahot al F ale htetb2a lwhdaha fl akher
                        found = True
                if found==False:
                    tree.append(col)
            break

        min = distanceMatrix.replace(0, np.NaN).min(skipna= True).min()    #returns minimum value in the whole dataframe
        temp= distanceMatrix.replace(0, np.NaN).idxmin(skipna=True)        #return list of (row,col) names for the smallest value in EACH row
        #print(temp)
        for row, col in temp.items():
            if distanceMatrix.at[row, col] == min:                          #which row,col names in "temp" tb3 al min value de?
                minRow= row
                minCol = col
                break

        if minRow not in tree:
            if minCol not in tree:
                tree.append(minRow+minCol)
                new_colRowName = minRow + minCol
            else:
                x = tree[tree.index(minCol)] + minRow
                tree[tree.index(minCol)] = x
                new_colRowName =minCol + minRow
        elif minCol not in tree:
            tree[tree.index(minRow)] +=minCol
            new_colRowName = minRow + minCol
        else:
            if tree.index(minRow) < tree.index(minCol):
                tree[tree.index(minRow)] += "+"+minCol
                del tree[tree.index(minCol)]
                new_colRowName = minRow + minCol
            else:
                tree[tree.index(minCol)]+= "+"+minRow
                del tree[tree.index(minRow)]
                new_colRowName = minCol + minRow
        #print(tree)
        newMatrix = distanceMatrix.drop([minRow, minCol], axis=0).drop([minRow, minCol], axis=1)    #create new matrix , b3ml drop l 4 hagat 2 rows w 2 cols
        newMatrix = pd.DataFrame(newMatrix)
        columns = distanceMatrix.columns
        minRowIndex_asAcol = columns.get_loc(minRow)

        if(minRowIndex_asAcol == len(distanceMatrix.columns)-2):                                    #when to add the new row&col fel akher? lw kano al last 2 rows
            newMatrix[new_colRowName] = 0  # add col
            inde = [new_colRowName]#add row
            temp = pd.DataFrame(data=0, columns=newMatrix.columns, index=inde)
            newMatrix = newMatrix.append(temp)

        else:                                                                                       #when to add the new row& col fel awl? otherwise
            newMatrix.insert(0, new_colRowName, 0) #add col
            inde = [new_colRowName]#add row
            temp = pd.DataFrame(data=0, columns=newMatrix.columns, index=inde)
            newMatrix = pd.concat([newMatrix.iloc[0:0], temp[0:], newMatrix.iloc[0:]])


        for column in distanceMatrix:                                                                   #fill the added rows and cols with avg
            if(column != minRow and column != minCol):
                avg = distanceMatrix.at[minRow, column] + distanceMatrix.at[minCol, column]
                avg = avg/2.0
                newMatrix.at[new_colRowName, column] = avg
                newMatrix.at[column, new_colRowName] = avg
        print("ITERATION NUMBER:", iterations)
        print("*****************")
        print(newMatrix, '\n')
        distanceMatrix = newMatrix
        iterations+=1
    treeRepresentation(tree)

def treeRepresentation(tree):

    finalTree=[]
    splits = []
    for item in tree:
        splits = item.split('+')
        temp = ''
        for split in splits:
            if temp != '':                                                          #3shan yhot al comma been al two brackets dol (A,C),
                temp+=', '
            if len(split) == 2:
                temp += '(' + split[0] + ', ' + split[1] + ')'
            elif len(split) == 3:
                temp += '((' + split[0] + ', ' + split[1] + ')' + ', ' + split[2] + ')'
            else:
                temp += split
        finalTree.append(temp)
    print("*******")
    print("TREE : ")
    print("*******")
    print("(("+finalTree[0]+'),'+finalTree[1]+")")

#----------------------------------------------MAIN---------------------------------------------


data = [[0.0, 9.0, 2.0, 4.0, 9.0, 10.0],
         [9.0, 0.0, 9.0, 6.0, 2.0, 10.0],
         [2.0, 9.0, 0.0, 5.0, 9.0, 10.0],
         [4.0, 6.0, 5.0, 0.0, 6.0, 10.0],
         [9.0, 2.0, 9.0, 6.0, 0.0, 10.0],
        [10.0, 10.0, 10.0, 10.0, 10.0,0.0]]

colNames = ["A", "B", "C", "D", "E", "F"]
'''
data = [[0.0, 20.0, 60.0, 100.0, 90.0],
         [20.0, 0.0, 50.0, 90.0, 80.0],
         [60.0, 50.0, 0.0, 40.0, 50.0],
         [100.0, 90.0, 40.0, 0.0, 30.0],
         [90.0, 80.0, 50.0, 30.0, 0.0]]

colNames = ["A", "B", "C", "D", "E"]
'''
distanceMatrix = pd.DataFrame(data, columns= colNames, index=colNames)
UPGMA(distanceMatrix)


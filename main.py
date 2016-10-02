from sklearn import svm
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.metrics import confusion_matrix
import numpy as np


def team_converter(s):
    if s == "BourgeB":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)
    if s == "Strasburgo":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0)
    if s == "Gazelec":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)
    if s == "Brest":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0)
    if s == "Nimes":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0)
    if s == "Laval":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0)
    if s == "Niort":
        return (0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)
    if s == "Lens":
        return (0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0)
    if s == "Orleans":
        return (0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0)
    if s == "Havre":
        return (0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0)
    if s == "Tours":
        return (0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0)
    if s == "Ajaccio":
        return (0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Troyes":
        return (0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Sochaux":
        return (0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Valenciennes":
        return (0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Clermont":
        return (0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "RedStar":
        return (0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Auxerre":
        return (0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Amiens":
        return (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    if s == "Reims":
        return (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

# def team_converter(s):
#     if s == "BourgeB":
#         return (0)
#     if s == "Strasburgo":
#         return (1)
#     if s == "Gazelec":
#         return (2)
#     if s == "Brest":
#         return (3)
#     if s == "Nimes":
#         return (4)
#     if s == "Laval":
#         return (5)
#     if s == "Niort":
#         return (6)
#     if s == "Lens":
#         return (7)
#     if s == "Orleans":
#         return (8)
#     if s == "Havre":
#         return (9)
#     if s == "Tours":
#         return (10)
#     if s == "Ajaccio":
#         return (11)
#     if s == "Troyes":
#         return (12)
#     if s == "Sochaux":
#         return (13)
#     if s == "Valenciennes":
#         return (14)
#     if s == "Clermont":
#         return (15)
#     if s == "RedStar":
#         return (16)
#     if s == "Auxerre":
#         return (17)
#     if s == "Amiens":
#         return (18)
#     if s == "Reims":
#         return (19)

def convert_dict_to_list(dic):
    x = []
    y = []
    for key in dic:
        #print key[0]
        #print key[1]
        x.append(team_converter(key[0]) + team_converter(key[1]))
        if dic[key] == 0:
            y.append(0)
        else:
            y.append(1)

    return x, y

resultsday1 = {("BourgeB", "Strasburgo"): 0, ("Gazelec","Brest"): 0, ("Nimes","Laval"): 0, ("Niort","Lens"): 0, ("Orleans","Havre"): 2,
           ("Tours","Ajaccio"): 0, ("Troyes","Sochaux"): 2, ("Valenciennes","Clermont"): 1, ("RedStar","Auxerre"): 0, ("Amiens","Reims"): 0}

resultsday2 = {("Ajaccio","Troyes"): 1, ("Auxerre","Gazelec"): 2, ("Brest","Orleans"): 1, ("Clermont","RedStar"): 0,
               ("Laval","Niort"): 0, ("Havre","Nimes"): 1, ("Lens","Tours"): 0, ("Reims","BourgeB"): 1,
               ("Sochaux","Valenciennes"): 0, ("Strasburgo","Amiens"): 1}

resultsday3 = {("Amiens","Niort"): 1, ("BourgeB","Auxerre"): 2, ("Clermont","Sochaux"): 2, ("Gazelec","Havre"): 0,
               ("Orleans","Ajaccio"): 1, ("RedStar","Brest"): 2, ("Tours","Strasburgo"): 2, ("Troyes","Laval"): 1,
               ("Valenciennes","Reims"): 0, ("Nimes","Lens"): 2}

resultsday4 = {("Ajaccio","BourgeB"): 1, ("Auxerre","Clermont"): 2, ("Brest","Valenciennes"): 1, ("Laval","Gazelec"): 2,
               ("Havre","Troyes"): 2, ("Niort","Tours"): 2, ("Sochaux","Orleans"): 0, ("Strasburgo", "Nimes"): 0,
               ("Lens","Amiens"): 2, ("Reims","RedStar"): 1}

resultsday5 = {("BourgeB","Niort"): 0, ("Clermont","Ajaccio"): 1, ("Gazelec","Strasburgo"): 0, ("Nimes","Amiens"): 2,
               ("Orleans","Auxerre"): 0, ("Tours","Reims"): 0, ("Troyes","Lens"): 0, ("Valenciennes","Laval"): 1,
               ("RedStar","Havre"): 0, ("Sochaux","Brest"): 0}

resultsday6 = {("Ajaccio","RedStar"): 2, ("Amiens","Tours"): 1, ("Auxerre","Sochaux"): 0, ("Brest","Clermont"): 2,
               ("Laval","Orleans"): 1, ("Lens","BourgeB"): 0, ("Niort","Nimes"): 2, ("Reims","Gazelec"): 1,
               ("Havre","Valenciennes"): 0, ("Strasburgo","Troyes"): 1}

resultsday7 = {("BourgeB","Havre"):1,("Clermont","Lens"):0,("Orleans","Strasburgo"):1,("RedStar","Laval"):1, ("Sochaux","Reims"):0,
               ("Tours","Nimes"):2,("Troyes","Niort"):0,("Valenciennes","Ajaccio"):0,("Brest","Auxerre"):1,("Gazelec","Amiens"):0}

resultsday8 = {("Strasburgo","RedStar"):0, ("Ajaccio","Auxerre"):1, ("Amiens","Valenciennes"):0, ("Laval","Sochaux"): 0,
             ("Havre","Brest"):0, ("Lens","Orleans"):1, ("Nimes","Troyes"):0, ("Niort","Gazelec"):0, ("Reims","Clermont"): 1,
             ("Tours","BourgeB"): 2}

resultsday9 = {("Auxerre","Havre"): 2, ("BourgeB","Laval"): 0, ("Clermont","Strasburgo"):0,("Gazelec","Nimes"): 2,
               ("Orleans", "Amiens"): 2, ("RedStar","Niort"): 2, ("Troyes","Tours"): 1, ("Sochaux","Ajaccio"): 1,
               ("Valenciennes","Lens"): 2, ("Brest","Reims"): 1}

new_dict = {}
new_dict = resultsday1.copy()
new_dict.update(resultsday2)
new_dict.update(resultsday3)
new_dict.update(resultsday4)
new_dict.update(resultsday5)
new_dict.update(resultsday6)
new_dict.update(resultsday7)
new_dict.update(resultsday8)



X , y = convert_dict_to_list(new_dict)
clf = linear_model.LinearRegression()
#clf = svm.SVC(kernel='linear', degree=3, probability=True, C=1)
#clf = svm.SVC()

X1, y1 = convert_dict_to_list(resultsday9)

clf.fit(X,y)
print (y1)
print (clf.predict(X1))
print (clf.predict_proba(X1))
print (clf.score(X1, y1))

cm = confusion_matrix(y1, clf.predict(X1))

tp = float(cm[0][0])/np.sum(cm[0])
tn = float(cm[1][1])/np.sum(cm[1])
print (tp)
print (tn)
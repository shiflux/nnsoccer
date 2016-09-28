import sklearn

resultsday1 = {("BourgeB", "Strasburgo"): 0, ("Gazelec","Brest"): 0, ("Nimes","Laval"): 0, ("Niort","Lens"): 0, ("Orleans","Havre"): 2,
           ("Tours","Ajaccio"): 0, ("Troyes","Sochaux"): 2, ("Valenciennes","Clermont"): 1, ("RedStar","Auxerre"): 0, ("Amiens","Reims"): 0}

resultsday7 = {("BourgeB","Havre"):1,("Clermont","Lens"):0,("Orleans","Strasburgo"):1,("RedStar","Laval"):1, ("Sochaux","Reims"):0,
               ("Tours","Nimes"):2,("Troyes","Niort"):0,("Valenciennes","Ajaccio"):0,("Brest","Auxerre"):1,("Gazelec","Amiens"):0}

resultsday8 = {("Strasburgo","RedStar"):0, ("Ajaccio","Auxerre"):1, ("Amiens","Valenciennes"):0, ("Laval","Sochaux"): 0,
             ("Havre","Brest"):0, ("Lens","Orleans"):1, ("Nimes","Troyes"):0, ("Niort","Gazelec"):0, ("Reims","Clermont"): 1,
             ("Tours","BourgeB"): 2}

resultsday9 = {("Auxerre","Havre"): 2, ("BourgeB","Laval"): 0, ("Clermont","Strasburgo"):0,("Gazelec","Nimes"): 2,
               ("Orleans", "Amiens"): 2, ("RedStar","Niort"): 2, ("Troyes","Tours"): 1, ("Sochaux","Ajaccio"): 1,
               ("Valenciennes","Lens"): 2, ("Brest","Reims"): 1}

#X = [[0, 0], [1, 1]]
#y = [0, 1]
#clf = svm.SVC()
#clf.fit(X,y)
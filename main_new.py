import unirest
from sklearn import svm
import numpy
import utils

#my_features = ["draws", "wins", "goal_difference", "scores", "conceded", "losts", "points"]
my_features = ["draws", "wins", "scores", "conceded"]
'''
next_games_list= [("Napoli","Roma"),("Pescara","Sampdoria"),("Juventus","Udinese"),("Fiorentina","Atalanta"),
                  ("Genoa","Empoli"), ("Inter","Cagliari"),("Lazio","Bologna"),("Sassuolo","Crotone"),
                  ("Chievo","Milan"),("Palermo","Torino")]
'''
next_games_list= [("Torino","Chievo"),("Empoli","Milan"),("Palermo","Lazio"),("Bologna","Atalanta"),("Cagliari","Udinese"),
		  ("Crotone","Sampdoria"),("Genoa","Juventus"),("Roma","Pescara"),("Napoli","Sassuolo"),("Inter","Fiorentina")]
#x, y = create_training_set([1], get_features())
#print x
#utils.test(n1=1, n2=10, binar = 2, serie="serie-a", old=True, C1=0.1, gamma=0.01)
print utils.predict_test2(next_games_list, serie="serie-a", C1= 3, gamma=0.01)
'''
res = {}
highest = -1
ch = -1
gammah = -1
for c in range(1, 150, 10):
	for gamma in range(1, 100, 5):
		res[(c,gamma)] = numpy.mean(utils.test2(C1=c/10.0, gamma=gamma/100.0))
		if res[(c,gamma)] > highest:
			highest = res[(c,gamma)]
			ch = c
			gammah = gamma

print res
print highest
print ch
print gammah
'''

#print utils.test2(C1=3, gamma=0.01)
#print utils.get_season_rounds(serie="serie-a", season="14-15")

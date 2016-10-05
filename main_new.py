import unirest
from sklearn import svm
import numpy
import utils

my_features = ["draws", "wins", "goal_difference", "scores", "conceded", "losts", "points"]
next_games_list= [("Napoli","Roma"),("Pescara","Sampdoria"),("Juventus","Udinese"),("Fiorentina","Atalanta"),
                  ("Genoa","Empoli"), ("Inter","Cagliari"),("Lazio","Bologna"),("Sassuolo","Crotone"),
                  ("Chievo","Milan"),("Palermo","Torino")]


#x, y = create_training_set([1], get_features())
#print x
utils.test(binar = 2, serie="serie-a")
#print utils.predict_test(next_games_list, serie="serie-a")

import unirest
from sklearn import svm
import numpy
import utils

my_features = ["draws", "wins", "goal_difference", "scores", "conceded", "losts", "points"]
next_games_list= [("Novara","Ascoli"),("Cittadella","Frosinone"),("Verona","Brescia"),("Bari","Virtus Entella"),
		("Latina","Trapani"),("Perugia","Avellino"),("Pisa","Spal"),("Pro Vercelli","Ternana"),
		("Spezia","Carpi"),("Vicenza","Cesena"),("Salernitana","Benevento")]



#x, y = create_training_set([1], get_features())
#print x
#utils.test(binar = 2, serie="serie-b")
print utils.predict_test(next_games_list, serie="serie-b")

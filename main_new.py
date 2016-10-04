import unirest
from sklearn import svm
import numpy

my_features = ["draws", "wins", "goal_difference", "scores", "conceded", "losts", "points"]
next_games_list= [("Napoli","Roma"),("Pescara","Sampdoria"),("Juventus","Udinese"),("Fiorentina","Atalanta"),
                  ("Genoa","Empoli"), ("Inter","Cagliari"),("Lazio","Bologna"),("Sassuolo","Crotone"),
                  ("Chievo","Milan"),("Palermo","Torino")]

def get_features():
  temp_dict = {}
  response = unirest.get("http://soccer.sportsopendata.net/v1/leagues/serie-a/seasons/16-17/standings",
                         headers={
                           "X-Mashape-Key": "s52gil4p6Tmshxp5pyFfiTfIYrTlp1dcNCTjsnLJTpnVtyrycd",
                           "Accept": "application/json"
                         }
                         )
  r = response.body
  for x in range(len(r['data']['standings'])):
    f_list = []
    for f in my_features:
      f_list.append(r['data']['standings'][x]["overall"][f])
    temp_dict[[r['data']['standings'][x]["team"]][0]] = f_list
  return temp_dict

def get_round_data(giornata):
  response = unirest.get(
    "http://soccer.sportsopendata.net/v1/leagues/serie-a/seasons/16-17/rounds/giornata-"+str(giornata),
    headers={
      "X-Mashape-Key": "s52gil4p6Tmshxp5pyFfiTfIYrTlp1dcNCTjsnLJTpnVtyrycd",
      "Accept": "application/json"
    }
    )
  r = response.body
  matches =  r['data']['rounds'][0]['matches']
  temp_dict = {}
  for m in range(len(matches)):
    temp_dict[(matches[m]['home_team'], matches[m]['away_team'])] = matches[m]['match_result']

  return temp_dict

def create_training_set(train_list, features):
  x, y = [], []
  for tl in train_list:
    temp_data = get_round_data(tl)
    for key in temp_data:
      #lx = (features[key[0]]+features[key[1]])
      lx =[a - b for a, b in zip(features[key[0]], features[key[1]])]
      ly = (temp_data[key])
      if ly == "":
        break
      x.append(lx)
      split_s = ly.split("-", 1)
      if int(split_s[0])< int(split_s[1]):
        ly = 0
      elif int(split_s[0])== int(split_s[1]):
        ly = 0
      elif int(split_s[0]) > int(split_s[1]):
        ly = 1
      y.append(ly)
  return x, y

def fit(X,y,X1,y1, C1=1):
  clf = svm.SVC(kernel='linear', C=C1)
  clf.fit(X, y)
  print (y1)
  print (clf.predict(X1))
  score = clf.score(X1, y1)
  print score
  return score

def predict(X,y,X1, C1=1):
  clf = svm.SVC(kernel='linear', C=C1)
  clf.fit(X, y)
  print (clf.predict(X1))
  return (clf.predict(X1))

def create_predict_set(games_list, features):
  x = []
  for gl in games_list:
    x.append([a - b for a, b in zip(features[gl[0]], features[gl[1]])])
    #x.append(features[gl[0]] + features[gl[1]])
  return x

def fit_test(giornata):
  features = get_features()
  x, y = create_training_set(range(1, giornata, 1), features)
  x1, y1 = create_training_set([giornata], features)
  return fit(x, y, x1, y1, C1=2)

def test(n1=4,n2=7):
  results= []
  for x in range(n1,n2,1):
    results.append(fit_test(x))
  print numpy.mean(results)

def predict_test():
  features = get_features()
  giornata = 7
  x, y = create_training_set(range(1, giornata, 1), features)
  x1 = create_predict_set(next_games_list, features)
  return predict(x, y, x1, C1=2)


#x, y = create_training_set([1], get_features())
#print x
test()
predict_test()

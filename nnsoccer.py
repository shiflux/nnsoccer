import unirest
import settings
from sklearn import svm
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SoccerPredictor:
    def __init__(self):
        self.training_set = None
        self.clf = None
        self.list_of_0 = []
        self.list_of_1 = []
        self.list_of_2 = []
        self.threshold = 0
        self.max_threshold = 2

    def createTrainingSet(self):
        self.training_set = self.createSeasonTrainingSet(serie="serie-a", season="15-16")
        self.training_set += self.createSeasonTrainingSet(serie="serie-a", season="14-15")
        self.training_set += self.createSeasonTrainingSet(serie="serie-b", season="15-16")
        self.clf = svm.SVC(kernel='linear', C=settings.C1, gamma=settings.gamma, probability=True)
        self.clf.fit(self.training_set[0], self.training_set[1])


    def createSeasonTrainingSet(self, serie, season, trainingType=None):
        x, y = [], []
        features = self.getFeatures(serie=serie, season=season)
        rounds = self.getSeasonRounds(serie, season)
        for round in rounds:
            temp_data = self.getDetailedRoundData(round, serie, season)
            for match in temp_data:
                homet = match[0]
                awayt = match[1]
                if not (features.has_key(homet) and features.has_key(awayt)):
                    continue
                lx = features[homet] + features[awayt]
                ly = temp_data[match]
                if ly == "":
                    break
                split_ly = ly.split("-", 1)

                if trainingType == "golnogol":
                    if int(split_ly[0]) == 0 or int(split_ly[1]) == 0:
                        ly = 0
                    else:
                        ly = 1
                else:
                    if int(split_ly[0]) < int(split_ly[1]):
                        ly = 2
                    elif int(split_ly[0]) == int(split_ly[1]):
                        ly = 1
                    else:
                        ly = 0

                x.append(lx)
                y.append(ly)
        return x, y

    def getFeatures(self, serie, season, my_features=settings.my_global_features):
        temp_dict = {}
        response = unirest.get(
            settings.api_link + "leagues/" + serie + "/seasons/" + season + "/standings",
            headers={
                "X-Mashape-Key": settings.mashape_key,
                 "Accept": "application/json"
            }
         )
        r = response.body
        for st in r['data']['standings']:
            f_list = []
            matches_played = st["overall"]["wins"] + st["overall"]["draws"] + st["overall"]["losts"]
            for f in my_features:
                f_list.append(1.0 * st["overall"][f] / matches_played)
            temp_dict[st["team"]] = f_list
        return temp_dict

    def getSeasonRounds(self, serie, season):
        response = unirest.get(
            settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds",
            headers={
                "X-Mashape-Key": settings.mashape_key,
                "Accept": "application/json"
            }
        )
        r = response.body
        rounds = r['data']['rounds']
        temp_list = []
        for r in rounds:
            temp_list.append(r['round_slug'])
        return temp_list

    def getDetailedRoundData(self, round, serie, season):
        response = unirest.get(
            settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds/" + round,
            headers={
                "X-Mashape-Key": settings.mashape_key,
                "Accept": "application/json"
            }
        )
        r = response.body
        if r['data']['rounds'] == []:
            return []
        matches = r['data']['rounds'][0]['matches']
        temp_dict = {}
        for m in range(len(matches)):
            temp_dict[(matches[m]['home_team'], matches[m]['away_team'])] = matches[m]['match_result']
        return temp_dict

    def predictGames(self, games_list, serie):
        if self.clf is None:
            print ("Error, no clf created")
            return
        predict_set = self.createPredictSet(games_list, serie=serie, season=settings.current_season)

        results = {}
        new_list = []
        temp_games = []
        for key in predict_set:
            new_list.append(predict_set[key])
            temp_games.append(key)
        res = self.clf.predict_proba(new_list)
        for x in xrange(len(temp_games)):
            results[temp_games[x]] = res[x]
        return results

    def createPredictSet(self, games_list, serie, season):
        x = {}
        features = self.getFeatures(serie=serie, season=season)
        for gl in games_list:
            f = features[gl[0]] + features[gl[1]]
            x[gl] = f
        return x

    def test(self, serie):
        if self.clf is None:
            print ("Error, no clf created")
            return

        X1, Y1 = self.createSeasonTrainingSet(serie, season=settings.current_season)
        predicted_prob = (self.clf.predict_proba(X1))
        predicted = (self.clf.predict(X1))
        temp_res = []
        self.list_of_0 = []
        self.list_of_1 = []
        self.list_of_2 = []
        for x in range(len(Y1)):
            if self.max_threshold > predicted_prob[x][predicted[x]] >= self.threshold:
                if predicted[x] == Y1[x]:
                    temp_res.append(1)
                else:
                    temp_res.append(0)
                if predicted[x] == 0:
                    self.list_of_0.append(temp_res[-1])
                elif predicted[x] == 1:
                    self.list_of_1.append(temp_res[-1])
                else:
                    self.list_of_2.append(temp_res[-1])
        return temp_res

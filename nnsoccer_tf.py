import urllib.request
import settings
import tensorflow as tf
import numpy as np
import json
from sklearn import svm
from datetime import datetime
import os.path
import pickle
from collections import OrderedDict


class SoccerPredictorTF:
    def __init__(self):
        self.list_of_0 = list()
        self.list_of_1 = list()
        self.list_of_2 = list()
        self.threshold = 0
        self.max_threshold = 3
        self.tf_session = tf.InteractiveSession()
        self.training_x = list()
        self.training_y = list()
        tf.logging.set_verbosity(tf.logging.ERROR)

    def createTrainingSet(self, trainingType=None):
        if os.path.exists("training_games_list.save"):
            f = open("training_games_list.save", "rb")
            x0 = pickle.load(f)
            y0 = pickle.load(f)
            f.close()
        else:
            x0, y0 = self.createSeasonTrainingSet(serie="serie-a", season="15-16", trainingType=trainingType)
            x1, y1 = self.createSeasonTrainingSet(serie="serie-a", season="14-15", trainingType=trainingType)
            x0 += x1
            y0 += y1
            x1, y1 = self.createSeasonTrainingSet(serie="serie-b", season="15-16", trainingType=trainingType)
            x0 += x1
            y0 += y1
            f = open("training_games_list.save", "wb")
            pickle.dump(x0, f, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(y0, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()
        self.training_x = x0
        self.training_y = y0
        feature_columns = [tf.contrib.layers.real_valued_column("", dimension=len(settings.my_global_features))]
        self.classifier = tf.contrib.learn.DNNClassifier(model_dir="models",
                                                            feature_columns=feature_columns,
                                                         hidden_units=[int(len(settings.my_global_features)/2)],
                                                         n_classes=2 if trainingType == "golnogol" else 3)
        if not os.listdir("models"):
            self.classifier.fit(x=np.array(self.training_x).astype(np.float32), y=np.array(self.training_y).astype(np.int32), steps=settings.steps)
        self.clf = svm.SVC(kernel='linear', C=settings.C1, gamma=settings.gamma, probability=True)
        self.clf.fit(self.training_x, self.training_y)



    def createSeasonTrainingSet(self, serie, season, trainingType=None):
        x, y = [], []
        features = self.getFeatures(serie=serie, season=season)
        rounds = self.getSeasonRounds(serie, season)
        for r in rounds:
            temp_data = self.getDetailedRoundData(r, serie, season)
            for match in temp_data:
                homet = match[0]
                awayt = match[1]
                if not (homet in features and awayt in features):
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
        temp_dict = OrderedDict()
        response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/standings")
        r = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        for st in r['data']['standings']:
            f_list = []
            matches_played = st["overall"]["wins"] + st["overall"]["draws"] + st["overall"]["losts"]
            for f in my_features:
                f_list.append(1.0 * st["overall"][f] / matches_played)
            temp_dict[st["team"]] = f_list
        return self.get_extra_features(serie=serie, season=season, dict=temp_dict)

    def get_extra_features(self, serie, season, dict, my_features=settings.my_global_extra_features):
        temp_dict = OrderedDict()
        for key in dict:
            temp_dict[key] = OrderedDict()
        rounds = self.getSeasonRounds(serie, season)
        for r in rounds:
            response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds/" + r + "/matches")
            r = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
            matches = r['data']['matches']
            for match in matches:
                homet = match["home"]["team"]
                awayt = match["away"]["team"]
                for f in my_features:
                    print(match["home"])
                    temp_dict[homet][f].append(match["home"][f])
                    temp_dict[awayt][f].append(match["away"][f])
        for team in temp_dict:
            for feat in temp_dict[team]:
                dict[team].append(np.mean(temp_dict[team][feat]))
        return dict

    def getSeasonRounds(self, serie, season):
        response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds")
        r = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        rounds = r['data']['rounds']
        temp_list = []
        for r in rounds:
            temp_list.append(r['round_slug'])
        return temp_list

    def getDetailedRoundData(self, round, serie, season):
        response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds/" + round)
        r = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        if r['data']['rounds'] == []:
            return []
        matches = r['data']['rounds'][0]['matches']
        temp_dict = OrderedDict()
        for m in range(len(matches)):
            temp_dict[(matches[m]['home_team'], matches[m]['away_team'])] = matches[m]['match_result']
        return temp_dict

    def predictGames(self, games_list, serie):
        if self.clf is None:
            print ("Error, no clf created")
            return
        predict_set = self.createPredictSet(games_list, serie=serie, season=settings.current_season)

        results = OrderedDict()
        new_list = []
        temp_games = []
        for key in predict_set:
            new_list.append(predict_set[key])
            temp_games.append(key)
        res = self.clf.predict_proba(new_list)
        for x in range(len(temp_games)):
            results[temp_games[x]] = res[x]
        return results

    def createPredictSet(self, games_list, serie, season):
        x = OrderedDict()
        features = self.getFeatures(serie=serie, season=season)
        for gl in games_list:
            f = features[gl[0]] + features[gl[1]]
            x[gl] = f
        return x

    def test(self, serie, trainingType=None):
        x1, y1 = self.createSeasonTrainingSet(serie, season=settings.current_season, trainingType=trainingType)
        accuracy_score = self.classifier.evaluate(x=np.array(x1).astype(np.float32), y=np.array(y1).astype(np.int32))["accuracy"]
        print('Accuracy: {0:f}'.format(accuracy_score))

        #predicted = list(self.classifier.predict(np.array(X1), as_iterable=True))
        predicted_prob = list(self.classifier.predict_proba(np.array(x1).astype(np.float32), as_iterable=True))

        predicted_prob_svm = (self.clf.predict_proba(x1))
        #predicted_svm = (self.clf.predict(X1))

        temp_res = []
        self.list_of_0 = []
        self.list_of_1 = []
        self.list_of_2 = []
        for x in range(len(y1)):
            probs = list()
            for p in range(2 if trainingType == "golnogol" else 3):
                #probs.append((predicted_prob_svm[x][p])/2)
                probs.append((predicted_prob[x][p] + predicted_prob_svm[x][p]) / 2)
            max_prob = max(probs)
            max_index = probs.index(max_prob)
            if self.max_threshold > max_prob >= self.threshold:
                if max_index == y1[x]:
                    temp_res.append(1)
                else:
                    temp_res.append(0)
                if max_index == 0:
                    self.list_of_0.append(temp_res[-1])
                elif max_index == 1:
                    self.list_of_1.append(temp_res[-1])
                else:
                    self.list_of_2.append(temp_res[-1])
        return temp_res

    def predictGames(self, games_list, serie):
        predict_set = self.createPredictSet(games_list, serie=serie, season=settings.current_season)

        results = OrderedDict()
        new_list = []
        temp_games = []
        for key in predict_set:
            new_list.append(predict_set[key])
            temp_games.append(key)
        res_svm = self.clf.predict_proba(new_list)
        res = list(self.classifier.predict_proba(np.array(new_list).astype(np.float32), as_iterable=True))
        for x in range(len(temp_games)):
            temp = []
            for y in range(len(res[x])):
                temp.append(res[x][y]/2 + res_svm[x][y]/2)
            results[temp_games[x]] = temp
        return results

    def saveLog(self, to_write):
        with open("log/"+str(datetime.now())+".txt", 'w+') as myFile:
            for item in to_write:
                myFile.write("%s\n" % item)
            print("Wrote log to file " + myFile.name)


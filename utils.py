import numpy
import unirest
from sklearn import svm
import settings
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

threshold = 0
max_threshold = 2

def get_features(serie="serie-a", my_features=settings.my_global_features, season="16-17"):
    temp_dict = {}
    response = unirest.get("http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/" + season + "/standings",
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


def get_round_data(giornata, serie="serie-a", season="16-17"):
    response = unirest.get(
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/" + season + "/rounds/giornata-" + str(
            giornata),
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


def get_season_teams(serie="serie-a", season="16-17"):
    response = unirest.get(
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/" + season + "/teams",
        headers={
            "X-Mashape-Key": settings.mashape_key,
            "Accept": "application/json"
        }
    )
    r = response.body
    temp_list = []
    for t in r['data']['teams']:
        temp_list.append(t['name'])
    return temp_list


def get_detailed_round_data(giornata, serie="serie-a", season="16-17"):
    response = unirest.get(
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/" + season + "/rounds/" + giornata,
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


def get_season_rounds(serie="serie-a", season="16-17"):
    response = unirest.get(
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/" + season + "/rounds",
        headers={
            "X-Mashape-Key": settings.mashape_key,
            "Accept": "application/json"
        }
    )
    r = response.body
    rounds = r['data']['rounds']
    temp_list = []
    for round in rounds:
        temp_list.append(round['round_slug'])
    return temp_list


def create_season_training_set(serie="serie-a", season="16-17", div=1.0):
    x, y = [], []
    teams = get_season_teams(serie, season)
    features = {}
    for t in teams:
        features[t] = [0, 0, 0, 0, 0]
    rounds = get_season_rounds(serie, season)
    n_round = 0.0
    for round in rounds:
        n_round += 1
        temp_data = get_detailed_round_data(round, serie, season)
        for match in temp_data:
            homet = match[0]
            awayt = match[1]
            lx = features[homet] + features[awayt]
            lx = [a / n_round for a in lx]
            ly = temp_data[match]
            if ly == "":
                break
            split_ly = ly.split("-", 1)
            features[homet][3] += int(split_ly[0])  # scored
            features[homet][4] += int(split_ly[1])  # conceded
            features[awayt][3] += int(split_ly[1])
            features[awayt][4] += int(split_ly[0])

            if int(split_ly[0]) < int(split_ly[1]):
                ly = 2
                features[homet][2] += 1
                features[awayt][0] += 1
            elif int(split_ly[0]) == int(split_ly[1]):
                ly = 1
                features[homet][1] += 1
                features[awayt][1] += 1
            else:
                ly = 0
                features[homet][0] += 1
                features[awayt][2] += 1

            x.append(lx)
            y.append(ly)
    return x, y


def create_season_training_set2(serie="serie-a", season="16-17", div=1.0):
    x, y = [], []
    # teams = get_season_teams(serie, season)
    features = get_features(serie=serie, season=season)
    rounds = get_season_rounds(serie, season)
    for round in rounds:
        temp_data = get_detailed_round_data(round, serie, season)
        for match in temp_data:
            homet = match[0]
            awayt = match[1]
            if not (features.has_key(homet) and features.has_key(awayt)):
                continue
            lx = features[homet] + features[awayt]
            lx = [a / div for a in lx]
            ly = temp_data[match]
            if ly == "":
                break
            split_ly = ly.split("-", 1)

            if int(split_ly[0]) < int(split_ly[1]):
                ly = 2
            elif int(split_ly[0]) == int(split_ly[1]):
                ly = 1
            else:
                ly = 0

            x.append(lx)
            y.append(ly)
    return x, y


def create_season_training_set_goalnogoal(serie="serie-a", season="16-17"):
    x, y = [], []
    # teams = get_season_teams(serie, season)
    features = get_features(serie=serie, season=season)
    rounds = get_season_rounds(serie, season)
    for round in rounds:
        temp_data = get_detailed_round_data(round, serie, season)
        for match in temp_data:
            homet = match[0]
            awayt = match[1]
            if not (features.has_key(homet) and features.has_key(awayt)):
                continue
            lx = features[homet] + features[awayt]
            lx = [a for a in lx]
            ly = temp_data[match]
            if ly == "":
                break
            split_ly = ly.split("-", 1)

            if int(split_ly[0]) > 0 and int(split_ly[1] > 0):
                ly = 1
            else:
                ly = 0

            x.append(lx)
            y.append(ly)
    return x, y


def create_training_set(train_list, features, binar=2, serie="serie-a", season="16-17", div=1.0):
    x, y = [], []
    div = div
    for tl in train_list:
        temp_data = get_round_data(tl, serie=serie, season=season)
        for key in temp_data:
            lx = (features[key[0]] + features[key[1]])
            lx = [a / div for a in lx]
            # lx = [(a - b) for a, b in zip(features[key[0]], features[key[1]])]
            ly = (temp_data[key])
            if ly == "":
                break
            x.append(lx)
            split_s = ly.split("-", 1)
            if int(split_s[0]) < int(split_s[1]):
                if binar == 2:
                    ly = 2
                else:
                    ly = 1
            elif int(split_s[0]) == int(split_s[1]):
                if binar == 0:
                    ly = 0
                else:
                    ly = 1
            elif int(split_s[0]) > int(split_s[1]):
                ly = 0
            y.append(ly)
    return x, y


def fit(X, y, X1, y1, C1=2, gamma=0.2):
    clf = svm.SVC(kernel='linear', C=C1, gamma=gamma, probability=True)
    clf.fit(X, y)
    print(y1)
    predicted = (clf.predict(X1))
    print(predicted)
    predicted_prob = (clf.predict_proba(X1))
    print(predicted_prob)
    temp_res = []
    for x in range(len(y1)):
        flag1 = numpy.absolute(predicted_prob[x][predicted[x]] - predicted_prob[x][(predicted[x] + 1) % 3])
        flag2 = numpy.absolute(predicted_prob[x][predicted[x]] - predicted_prob[x][(predicted[x] + 2) % 3])
        #
        # if predicted[x] == 1:
        #     if max_threshold > predicted_prob[x][1] >= threshold:
        #         if predicted[x] == y1[x]:
        #             temp_res.append(1)
        #         else:
        #             temp_res.append(0)
        #         fit.list_of_1.append(temp_res[-1])
        #if max_threshold > flag1 >= threshold and max_threshold > flag2 >= threshold:
        if max_threshold > predicted_prob[x][predicted[x]] >= threshold:
            if predicted[x] == y1[x]:
                temp_res.append(1)
            else:
                temp_res.append(0)
            if predicted[x] == 0:
                fit.list_of_0.append(temp_res[-1])
            elif predicted[x] == 1:
                fit.list_of_1.append(temp_res[-1])
            else:
                fit.list_of_2.append(temp_res[-1])
    print(len(temp_res))
    print(numpy.mean(temp_res))
    score = clf.score(X1, y1)
    return temp_res

fit.list_of_0 = []
fit.list_of_1 = []
fit.list_of_2 = []




def predict(X, y, X1, C1=2, gamma=0.01):
    clf = svm.SVC(kernel='linear', C=C1, gamma=gamma, probability=True)
    clf.fit(X, y)
    p = clf.predict(X1)
    print(clf.predict_proba(X1))
    return p


def create_predict_set2(games_list, serie, season, div=1.0):
    x = []
    features = get_features(serie=serie, season=season)
    for gl in games_list:
        print(gl)
        f = features[gl[0]] + features[gl[1]]
        f = [a / div for a in f]
        x.append(f)
    return x


def create_predict_set(games_list, features, div=1.0):
    x = []
    for gl in games_list:
        # x.append([a - b for a, b in zip(features[gl[0]], features[gl[1]])])
        f = features[gl[0]] + features[gl[1]]
        f = [a / div for a in f]
        x.append(f)
    return x


def fit_test(giornata, binar=2, serie="serie-a", old=False, C1=2, gamma=0.2):
    features = get_features(serie=serie)
    x, y = create_training_set(range(1, giornata, 1), features, binar, serie=serie, div=8.0)
    x1, y1 = create_training_set([giornata], features, binar, serie=serie, div=8.0)
    if (old):
        xold, yold = create_training_set(range(1, 39, 1), get_features(serie=serie, season="15-16"), binar, serie=serie,
                                         season="15-16", div=38.0)
        x = xold
        y = yold
    return fit(x, y, x1, y1, C1=C1, gamma=gamma)


def test(serie="serie-a", C1=0.1, gamma=0.01, lastonly=False):
    results = []
    x, y = create_training_set()
    x1, y1 = create_season_training_set2(serie=serie, season="16-17")
    return fit(x, y, x1, y1, C1=C1, gamma=gamma)

def testgoalnogoal(serie="serie-a", C1=0.1, gamma=0.01, lastonly=False):
    results = []
    x, y = create_training_set_goalnogoal()
    x1, y1 = create_season_training_set_goalnogoal(serie=serie, season="16-17")
    return fit(x, y, x1, y1, C1=C1, gamma=gamma)


def predict_test(next_games_list, serie="serie-a", C1=1, gamma=0.1):
    x0, y0 = create_training_set()
    xp = create_predict_set2(next_games_list, serie=serie, season="16-17")
    return predict(x0, y0, xp, C1=C1, gamma=gamma)


def create_training_set():
    if create_training_set.res is None:
        x0, y0 = create_season_training_set2(serie="serie-a", season="15-16")
        x1, y1 = create_season_training_set2(serie="serie-a", season="14-15")
        x0 += x1
        y0 += y1
        x1, y1 = create_season_training_set2(serie="serie-b", season="15-16")
        x0 += x1
        y0 += y1
        create_training_set.res = x0, y0
    return create_training_set.res

create_training_set.res = None


def create_training_set_goalnogoal():
    if create_training_set.res is None:
        x0, y0 = create_season_training_set_goalnogoal(serie="serie-a", season="15-16")
        x1, y1 = create_season_training_set_goalnogoal(serie="serie-a", season="14-15")
        x0 += x1
        y0 += y1
        x1, y1 = create_season_training_set_goalnogoal(serie="serie-b", season="15-16")
        x0 += x1
        y0 += y1
        create_training_set_goalnogoal.res = x0, y0
    return create_training_set_goalnogoal.res

create_training_set_goalnogoal.res = None


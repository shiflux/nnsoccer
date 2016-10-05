import numpy
import unirest
from sklearn import svm
import settings


def get_features(serie="serie-a", my_features=settings.my_global_features):
    temp_dict = {}
    response = unirest.get("http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/16-17/standings",
                           headers={
                               "X-Mashape-Key": settings.mashape_key,
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


def get_round_data(giornata, serie="serie-a"):
    response = unirest.get(
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/16-17/rounds/giornata-" + str(giornata),
        headers={
            "X-Mashape-Key": settings.mashape_key,
            "Accept": "application/json"
        }
    )
    r = response.body
    matches = r['data']['rounds'][0]['matches']
    temp_dict = {}
    for m in range(len(matches)):
        temp_dict[(matches[m]['home_team'], matches[m]['away_team'])] = matches[m]['match_result']

    return temp_dict


def create_training_set(train_list, features, binar=2, serie="serie-a"):
    x, y = [], []
    for tl in train_list:
        temp_data = get_round_data(tl, serie=serie)
        for key in temp_data:
            # lx = (features[key[0]]+features[key[1]])
            lx = [a - b for a, b in zip(features[key[0]], features[key[1]])]
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


def fit(X, y, X1, y1, C1=1):
    clf = svm.SVC(kernel='linear', C=C1)
    clf.fit(X, y)
    print (y1)
    print (clf.predict(X1))
    score = clf.score(X1, y1)
    print score
    return score


def predict(X, y, X1, C1=1):
    clf = svm.SVC(kernel='linear', C=C1)
    clf.fit(X, y)
    print clf.predict(X1)
    return clf.predict(X1)


def create_predict_set(games_list, features):
    x = []
    for gl in games_list:
        x.append([a - b for a, b in zip(features[gl[0]], features[gl[1]])])
        # x.append(features[gl[0]] + features[gl[1]])
    return x


def fit_test(giornata, binar=2, serie="serie-a"):
    features = get_features(serie=serie)
    x, y = create_training_set(range(1, giornata, 1), features, binar)
    x1, y1 = create_training_set([giornata], features, binar)
    return fit(x, y, x1, y1, C1=2)


def test(n1=4, n2=8, binar=2, serie="serie-a"):
    results = []
    for x in range(n1, n2, 1):
        results.append(fit_test(x, binar))
    print numpy.mean(results)
    return results


def predict_test(next_games_list, serie="serie-a"):
    features = get_features(serie=serie)
    giornata = 8
    x0, y0 = create_training_set(range(1, giornata, 1), features, binar=0, serie=serie)
    x1, y1 = create_training_set(range(1, giornata, 1), features, binar=1, serie=serie)
    xp = create_predict_set(next_games_list, features)
    pred0 = predict(x0, y0, xp, C1=2)
    pred1 = predict(x1, y1, xp, C1=2)
    return [a + b for a, b in zip(pred0, pred1)]

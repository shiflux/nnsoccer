import numpy
import unirest
from sklearn import svm
import settings


def get_features(serie="serie-a", my_features=settings.my_global_features, season="16-17"):
    temp_dict = {}
    response = unirest.get("http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/"+season+"/standings",
                           headers={
                               "X-Mashape-Key": settings.mashape_key,
                               "Accept": "application/json"
                           }
                           )
    r = response.body
    for st in r['data']['standings']:
        f_list=[]
        matches_played = st["overall"]["wins"] + st["overall"]["draws"] + st["overall"]["losts"]
        for f in my_features:
            f_list.append(1.0*st["overall"][f]/matches_played)
        temp_dict[st["team"]] = f_list
    return temp_dict


def get_round_data(giornata, serie="serie-a", season="16-17"):
    response = unirest.get(
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/"+season+"/rounds/giornata-" + str(giornata),
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
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/"+season+"/teams",
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
        "http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/"+season+"/rounds/" + giornata,
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
		"http://soccer.sportsopendata.net/v1/leagues/"+serie+"/seasons/"+season+"/rounds",
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

def create_season_training_set(serie="serie-a", season="16-17", div = 1.0):
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
			lx = [a/n_round for a in lx]
			ly = temp_data[match]
			if ly == "":
				break
			split_ly = ly.split("-", 1)
			features[homet][3] += int(split_ly[0]) #scored
			features[homet][4] += int(split_ly[1]) #conceded
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

def create_season_training_set2(serie="serie-a", season="16-17", div = 1.0):
        x, y = [], []
        teams = get_season_teams(serie, season)
        features = get_features(serie=serie, season=season)
        rounds = get_season_rounds(serie, season)
        for round in rounds:
                temp_data = get_detailed_round_data(round, serie, season)
                for match in temp_data:
                        homet = match[0]
                        awayt = match[1]
                        lx = features[homet] + features[awayt]
                        lx = [a/div for a in lx]
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
	return x,y

def create_training_set(train_list, features, binar=2, serie="serie-a", season="16-17", div=1.0):
    x, y = [], []
    div = div
    for tl in train_list:
        temp_data = get_round_data(tl, serie=serie, season=season)
        for key in temp_data:
            lx = (features[key[0]]+features[key[1]])
	    lx = [a/div for a in lx]
            #lx = [(a - b) for a, b in zip(features[key[0]], features[key[1]])]
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
    print (y1)
    predicted  = (clf.predict(X1))
    print (predicted)
    predicted_prob  = (clf.predict_proba(X1))
    print (predicted_prob)
    print (predicted[0])
    print (predicted_prob[0])
    temp_res = []
    temp_res2 = []
    for x in range(len(y1)):
        if predicted[x] == y1[x]:
            temp_res2.append(1)
        else:
            temp_res2.append(0)
        if predicted_prob[x][predicted[x]] > 0.5:
            if predicted[x] == y1[x]:
                temp_res.append(1)
            else:
                temp_res.append(0)
    print(numpy.mean(temp_res2))
    print(numpy.mean(temp_res))
    score = clf.score(X1, y1)
    return score


def predict(X, y, X1, C1=2, gamma=0.01):
    clf = svm.SVC(kernel='linear', C=C1, gamma=gamma, probability=True)
    clf.fit(X, y)
    p = clf.predict(X1)
    print (clf.predict_proba(X1))
    return p


def create_predict_set2(games_list, serie, season, div=1.0):
	x = []
	features = get_features(serie=serie, season=season)
	for gl in games_list:
		print (gl)
		f = features[gl[0]] + features[gl[1]]
		f = [a/div for a in f]
		x.append(f)
	return x


def create_predict_set(games_list, features, div=1.0):
    x = []
    for gl in games_list:
        #x.append([a - b for a, b in zip(features[gl[0]], features[gl[1]])])
        f = features[gl[0]] + features[gl[1]]
	f = [a/div for a in f]
	x.append(f)
    return x


def fit_test(giornata, binar=2, serie="serie-a", old=False, C1=2, gamma=0.2):
    features = get_features(serie=serie)
    x, y = create_training_set(range(1, giornata, 1), features, binar, serie=serie, div = 8.0)
    x1, y1 = create_training_set([giornata], features, binar, serie=serie, div = 8.0)
    if(old):
	xold, yold = create_training_set(range(1, 39, 1), get_features(serie=serie, season="15-16"), binar, serie=serie, season="15-16", div = 38.0)
	x = xold
	y = yold
    return fit(x, y, x1, y1, C1=C1, gamma=gamma)

def test2(serie="serie-a", C1=0.1, gamma=0.01):
	results = []
	x, y = create_season_training_set2(serie=serie, season="15-16")
	xx, yy = create_season_training_set2(serie=serie, season="14-15")
	x += xx
	y += yy
	x1, y1 = create_season_training_set2(serie=serie, season="16-17")
	pred = fit(x,y,x1,y1,C1=C1, gamma=gamma)
	return pred

def test(n1=4, n2=8, binar=2, serie="serie-a", old=False, C1=2, gamma=0.2):
    results = []
    for x in range(n1, n2, 1):
        results.append(fit_test(x, binar, serie, old=old, C1=C1, gamma=gamma))
    print numpy.mean(results)
    return results

def predict_test2(next_games_list, serie="serie-a", C1=1, gamma= 0.1):
	x0, y0 = create_season_training_set2(serie=serie, season="15-16")
	x1, y1 = create_season_training_set2(serie=serie, season="14-15")
	x0 += x1
	y0 += y1
	xp = create_predict_set2(next_games_list, serie=serie, season="16-17")
	pred = predict(x0, y0, xp, C1=C1, gamma=gamma)
	return pred

def predict_test(next_games_list, serie="serie-a", iniziale=1, giornate=8, C1=1, gamma=0.01, old=False):
    features = get_features(serie=serie)
    featuresold = get_features(serie=serie, season="15-16")
    x0, y0 = create_training_set(range(iniziale, giornate, 1), features, binar=0, serie=serie, div=8.0)
    x00, y00 = create_training_set(range(iniziale, giornate, 1), featuresold, binar=0, serie=serie, season="15-16", div=38.0)
    x1, y1 = create_training_set(range(iniziale, giornate, 1), features, binar=1, serie=serie, div=8.0)
    x11, y11 = create_training_set(range(iniziale, giornate, 1), featuresold, binar=1, serie=serie, season="15-16", div=38.0)
    x22, y22 = create_training_set(range(iniziale, giornate, 1), featuresold, binar=2, serie=serie, season="15-16", div=38.0)
    x2, y2 = create_training_set(range(iniziale, giornate, 1), features, binar=2, serie=serie, div=8.0)
    xp = create_predict_set(next_games_list, features, div=8.0)

    pred0 = predict(x0+x00, y0+y00, xp, C1=C1, gamma=gamma)
    pred1 = predict(x1+x11, y1+y11, xp, C1=C1, gamma=gamma)
    pred2 = predict(x2+x22, y2+y22, xp, C1=C1, gamma=gamma)
    print pred0
    print pred1
    print pred2
    return [(float(a) + float(b) + (float(c)/2.0))/1.5 for a, b,c in zip(pred0, pred1, pred2)]

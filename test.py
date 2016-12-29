import urllib.request
import settings
import importlib
import tensorflow as tf
import sys
import numpy as np

importlib.reload(sys)
sys.setdefaultencoding('utf-8')
trainingType = None

def runTest():
    tf_session = tf.InteractiveSession()
    x0, y0 = createSeasonTrainingSet(serie="serie-a", season="15-16", trainingType=trainingType)
    x1, y1 = createSeasonTrainingSet(serie="serie-a", season="14-15", trainingType=trainingType)
    x0 += x1
    y0 += y1
    x1, y1 = createSeasonTrainingSet(serie="serie-b", season="15-16", trainingType=trainingType)
    x0 += x1
    y0 += y1
    x = tf.placeholder(tf.float32, shape=[None, len(settings.my_global_features)])
    y_ = tf.placeholder(tf.int32, shape=[None,  2 if trainingType == "golnogol" else 3])
    W = tf.Variable(tf.zeros([len(settings.my_global_features), 2 if trainingType == "golnogol" else 3]))
    b = tf.Variable(tf.zeros([2 if trainingType == "golnogol" else 3]))
    y = tf.matmul(x, W) + b
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    i = 1
    while(len(x0) > i*100):
        batch = (np.array(x0[(i-1)*100:i*100]), np.array(y0[(i-1)*100:i*100]))
        train_step.run(feed_dict={x: batch[0], y_: batch[1]})



def createSeasonTrainingSet(serie, season, trainingType=None):
    x, y = [], []
    features = getFeatures(serie=serie, season=season)
    rounds = getSeasonRounds(serie, season)
    for round in rounds:
        temp_data = getDetailedRoundData(round, serie, season)
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

def getFeatures(serie, season, my_features=settings.my_global_features):
    temp_dict = {}
    response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/standings")
    r = response.body
    for st in r['data']['standings']:
        f_list = []
        matches_played = st["overall"]["wins"] + st["overall"]["draws"] + st["overall"]["losts"]
        for f in my_features:
            f_list.append(1.0 * st["overall"][f] / matches_played)
        temp_dict[st["team"]] = f_list
    return temp_dict

def getSeasonRounds(serie, season):
    response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds")
    r = response.body
    rounds = r['data']['rounds']
    temp_list = []
    for r in rounds:
        temp_list.append(r['round_slug'])
    return temp_list

def getDetailedRoundData(round, serie, season):
    response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds/" + round)
    r = response.body
    if r['data']['rounds'] == []:
        return []
    matches = r['data']['rounds'][0]['matches']
    temp_dict = {}
    for m in range(len(matches)):
        temp_dict[(matches[m]['home_team'], matches[m]['away_team'])] = matches[m]['match_result']
    return temp_dict
from nnsoccer_tf import SoccerPredictorTF
import argparse
import numpy

series_list = ["serie-a", "serie-b", "premier-league","liga", "eredivisie"]
############
#   MAIN   #
############
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict results from a file')
    parser.add_argument('-serie', type=str, required=False, help='Serie (serie-a, bundesliga, ...)')
    parser.add_argument('-C', type=float, required=False, help='C parameter')
    parser.add_argument('-gamma', type=float, required=False, help='Gamma parameter')
    parser.add_argument('-threshold', type=float, required=False, help='Threshold')
    parser.add_argument('-maxthreshold', type=float, required=False, help='Max Threshold')
    parser.add_argument('-type', type=str, required=False, help='golnogol')
    myPredictor = SoccerPredictorTF()
    args = parser.parse_args()
    if args.gamma is None:
        gamma = 0.01
    else:
        gamma = args.gamma
    if args.C is None:
        C = 3
    else:
        C = args.C
    if args.serie is None:
        serie = "serie-a"
    else:
        serie = args.serie
    if args.threshold is not None:
        myPredictor.threshold = args.threshold
    if args.maxthreshold is not None:
        myPredictor.max_threshold = args.maxthreshold

    res = []
    list_of_0 = []
    list_of_1 = []
    list_of_2 = []
    for_log = list()
    if args.type == "golnogol":
        myPredictor.createTrainingSet(trainingType="golnogol")
    else:
        myPredictor.createTrainingSet()
    if args.serie == "all":
        for s in series_list:
            res.append((s, myPredictor.test(serie=s, trainingType=args.type)))
            list_of_0.extend(myPredictor.list_of_0)
            list_of_1.extend(myPredictor.list_of_1)
            list_of_2.extend(myPredictor.list_of_2)
    else:
        res.append((serie, myPredictor.test(serie=serie, trainingType=args.type)))
        list_of_0.extend(myPredictor.list_of_0)
        list_of_1.extend(myPredictor.list_of_1)
        list_of_2.extend(myPredictor.list_of_2)
    for result in res:
        print(result[0], numpy.mean(result[1]), len(result[1]))
        for_log.append(str(result[0]) + " " +  str(numpy.mean(result[1])) + " " + str(len(result[1])))
    print (numpy.mean([numpy.mean(prob[1]) for prob in res]))
    for_log.append(str(numpy.mean([numpy.mean(prob[1]) for prob in res])))

    print ("Number of 0: " + str(len(list_of_0)) + " - accuracy: " + str(numpy.mean(list_of_0)))
    for_log.append("Number of 0: " + str(len(list_of_0)) + " - accuracy: " + str(numpy.mean(list_of_0)))
    print ("Number of 1: " + str(len(list_of_1)) + " - accuracy: " + str(numpy.mean(list_of_1)))
    for_log.append("Number of 1: " + str(len(list_of_1)) + " - accuracy: " + str(numpy.mean(list_of_1)))
    if not args.type == "golnogol":
        print ("Number of 2: " + str(len(list_of_2)) + " - accuracy: " + str(numpy.mean(list_of_2)))
        for_log.append("Number of 2: " + str(len(list_of_2)) + " - accuracy: " + str(numpy.mean(list_of_2)))
    if len(for_log) > 0:
        myPredictor.saveLog(for_log)

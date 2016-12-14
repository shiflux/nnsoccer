import utils
import argparse
import numpy

series_list = ["serie-a", "premier-league","liga"]
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
        utils.threshold = args.threshold
    if args.maxthreshold is not None:
        utils.max_threshold = args.maxthreshold

    res = []
    if args.serie == "all":
        for s in series_list:
            res.append((s, utils.test2(serie=s, C1=C, gamma=gamma)))
    else:
        res.append((serie, utils.test2(serie=serie, C1=C, gamma=gamma)))
    for result in res:
        print (result[0], numpy.mean(result[1]), len(result[1]))
    print (numpy.mean([numpy.mean(prob[1]) for prob in res]))

    print ("Number of 0: " + str(len(utils.fit.list_of_0)) + " - accuracy: " + str(numpy.mean(utils.fit.list_of_0)))
    print ("Number of 1: " + str(len(utils.fit.list_of_1)) + " - accuracy: " + str(numpy.mean(utils.fit.list_of_1)))
    print ("Number of 2: " + str(len(utils.fit.list_of_2)) + " - accuracy: " + str(numpy.mean(utils.fit.list_of_2)))

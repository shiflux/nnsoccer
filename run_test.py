import utils
import argparse

############
#   MAIN   #
############
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict results from a file')
    parser.add_argument('-serie', type=str, required=False, help='Serie (serie-a, bundesliga, ...)')
    parser.add_argument('-C', type=str, required=False, help='C parameter')
    parser.add_argument('-gamma', type=str, required=False, help='Gamma parameter')
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
    print utils.test2(serie=serie, C1=C, gamma=gamma)
import utils
import argparse

############
#   MAIN   #
############
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict results from a file')
    parser.add_argument('filename', type=str, help='Games to predict')
    parser.add_argument('-serie', type=str, required=False, help='Serie (serie-a, bundesliga, ...)')
    parser.add_argument('-C', type=str, required=False, help='C parameter')
    parser.add_argument('-gamma', type=str, required=False, help='Gamma parameter')
    args = parser.parse_args()
    if args.filename is not None and args.serie is not None:
        my_game_list = []
        myFile = open(args.filename, 'r')
        if myFile.readable():
            for line in myFile:
                game = line.split(';')
                if len(game) == 2:
                    my_game_list.append((game[0], game[1]))
        if(args.gamma is None):
            gamma = 0.01
        else:
            gamma = args.gamma
        if(args.C is None):
            C = 0.01
        else:
            C = args.C

        print (utils.predict_test2(my_game_list, serie=args.serie, C1= 3, gamma=0.01))


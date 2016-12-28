from nnsoccer import SoccerPredictor
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#todo
############http://soccer.sportsopendata.net/v1/leagues/serie-a/seasons/16-17/rounds/round-16/matches
#   MAIN   #
############
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict results from a file')
    parser.add_argument('filename', type=str, help='Games to predict')
    parser.add_argument('-serie', type=str, required=False, help='Serie (serie-a, bundesliga, ...)')
    parser.add_argument('-v', type=bool, required=False, help='Verbose')
    parser.add_argument('-C', type=str, required=False, help='C parameter')
    parser.add_argument('-gamma', type=str, required=False, help='Gamma parameter')
    args = parser.parse_args()
    myPredictor = SoccerPredictor()
    if args.filename is not None and args.serie is not None:
        my_game_list = []
        with open(args.filename) as myFile:
            stocks = myFile.read().splitlines()

            for line in stocks:
                game = line.decode('utf-8').split(';')
                if args.v:
                    print game
                if len(game) == 2:
                    my_game_list.append((game[0].strip(), game[1].strip()))
            if args.gamma is None:
                gamma = 0.01
            else:
                gamma = args.gamma
            if args.C is None:
                C = 0.01
            else:
                C = args.C

            if len(my_game_list) > 0:
                myPredictor.createTrainingSet()
                result = myPredictor.predictGames(my_game_list, serie=args.serie)
                for game, r in result:
                    print(game, result)
            else:
                print ("Error not enough games")


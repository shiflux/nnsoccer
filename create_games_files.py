import argparse
import unirest
import settings
import os
import sys


def read_games(round, serie="serie-a", season="16-17"):
    response = unirest.get("http://soccer.sportsopendata.net/v1/leagues/" + serie + "/seasons/" + season + "/rounds/"
                           + round + "matches",
                           headers={
                               "X-Mashape-Key": settings.mashape_key,
                               "Accept": "application/json"
                           }
                           )
    r = response.body
    g_list = []
    for match in r['data']['matches']['match_slug']:
        match = match.split('-')
        if match == 2:
            g_list.append((match[0],match[1]))
    return g_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict results from a file')
    parser.add_argument('serie', type=str, help='Serie (serie-a, bundesliga, ...)')
    parser.add_argument('-round', type=int, required=True, help='Round (1, 2, 3, ...)')
    parser.add_argument('-season', type=str, required=False, help='Season (16-17, ...)')
    args = parser.parse_args()

    if args.round < 1:
        print ("Round must be higher than 0")
        sys.exit(0)

    if args.season is None:
        season = "16-17"
    else:
        season = args.season

    response = unirest.get("http://soccer.sportsopendata.net/v1/leagues/" + args.serie + "/seasons/" + season +
                           "/rounds",
                           headers={
                               "X-Mashape-Key": settings.mashape_key,
                               "Accept": "application/json"
                           }
                           )
    r = response.body
    print r['data']['rounds'][0]
    round = r['data']['rounds'][args.round-1]['round_slug']
    games = read_games(round, args.serie, season)

    with open("games_" + args.serie) as myFile:
        myFile.truncate()
        for game in games:
            myFile.write(game[0]+';'+game[1]+os.linesep)
    print ("Wrote games to file games_" + args.serie)

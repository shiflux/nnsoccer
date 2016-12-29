import argparse
import settings
import os
import sys
import urllib.request
import json

def read_games(round, serie="serie-a", season="16-17"):
    response = urllib.request.urlopen(settings.api_link + "leagues/" + serie + "/seasons/" + season + "/rounds/"+ round + "/matches")
    r = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    g_list = []
    for match in r['data']['matches']:
        g_list.append((match['home']['team'], match['away']['team']))
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

    response = urllib.request.urlopen(settings.api_link + "leagues/" + args.serie + "/seasons/" + season + "/rounds")
    r = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    round = r['data']['rounds'][args.round-1]['round_slug']
    games = read_games(round, args.serie, season)

    with open("games_" + args.serie + ".txt", 'w+') as myFile:
        #myFile.truncate()
        for game in games:
            myFile.write(game[0]+';'+game[1]+os.linesep)
    print ("Wrote games to file " + myFile.name)

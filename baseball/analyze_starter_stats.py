import os
import json
import os.path

from bs4 import BeautifulSoup

from baseball.initialization.create_game_folders_from_scoreboards import get_scoreboard_file
from baseball.initialization.scrape_xml_scoreboards import get_games_by_date
from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import is_summer_month
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR
from search_player_file import get_player_name_by_id

# '571448': 'Nolan Arenado'

best_batter_ids = {'502517': 'Daniel Murphy', '514888': 'Jose Altuve', '542255': 'Ender Inciarte',
                   '605141': 'Mookie Betts', '453568': 'Charlie Blackmon',
                   '547989': 'Jose Abreu', '608369': 'Corey Seager'}


def process_starter_stats(url_dictionary):
    all_stats_array = {}
    starting_pitcher_stats = {}

    matchups = {}
    pass
    pitchers = print_pitchers_with_highest_averages()

    # We iterate from the oldest to newest
    for year in sorted(url_dictionary.keys()):
        item = url_dictionary[year]

        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                process_player_data_for_today(year, month, day, all_stats_array, matchups, pitchers)

    return matchups


def process_player_data_for_today(year, month, day, all_stats_array, matchups, pitchers):
    base_file_name = get_scoreboard_file(year, month, day)
    base_scoreboard_directory = str(str(os.getcwd()) + '/data/' + str(year) + '/' +
                                    convert_month_int_to_string(month) + '/' +
                                    convert_number_to_string(day) + '/')

    print base_scoreboard_directory

    tree = BeautifulSoup(open(base_scoreboard_directory + base_file_name), 'lxml')

    for game in tree.find_all('game'):
        game_dir_path = base_scoreboard_directory + 'gid_' + str(game['id']) + '/'
        get_starter_stats(game_dir_path, all_stats_array, matchups, pitchers)


def get_starter_stats(game_directory_path, all_stats_array, matchups, pitchers):

    starters_by_id = read_starter_stats(game_directory_path)
    if not starters_by_id:
        return
    if starters_by_id['postponed'] or not starters_by_id['valid']:
        return

    # home_team_name = starters_by_id['home_team_name']
    # if home_team_name != 'COL':
    #     return
    # if not is_summer_month(starters_by_id['date']):
    #     return

    # print starters_by_id
    home_starter_stats = starters_by_id['home_starting_players']
    away_starter_stats = starters_by_id['away_starting_players']
    home_starting_pitcher = home_starter_stats['pitcher']
    away_starting_pitcher = away_starter_stats['pitcher']

    for index in range(1, 10):

        position = str(index * 100)
        # if home_starting_pitcher['id'] in pitchers:
        player = home_starter_stats[position]
        save_starter_stats(player, all_stats_array)
        # if away_starting_pitcher['id'] in pitchers:
        player = away_starter_stats[position]
        save_starter_stats(player, all_stats_array)

    # Record the pitchers
    # save_pitcher_stats(home_starting_pitcher, all_stats_array)
    # save_pitcher_stats(away_starting_pitcher, all_stats_array)

    # Record batter matchups

    measured_batter_matchups = read_batter_matchups(game_directory_path)
    home_pitcher_id = home_starting_pitcher['id']
    away_pitcher_id = away_starting_pitcher['id']
    save_batter_matchups(measured_batter_matchups.get(home_pitcher_id, {}),
                         home_pitcher_id, matchups)
    save_batter_matchups(measured_batter_matchups.get(away_pitcher_id, {}),
                         away_pitcher_id, matchups)


def save_pitcher_matchups(batter_versus_pitcher, pitcher, matchups):

    hits = batter_versus_pitcher['hits']
    atbats = batter_versus_pitcher['atbats']
    sacrifice_fly_events = batter_versus_pitcher['sacrifice_fly_events']

    saved_streak_game = 0.
    if not atbats and not sacrifice_fly_events:
        saved_streak_game = 1.

    if hits:
        game_with_hit = 1.
        saved_streak_game = 1
    else:
        game_with_hit = 0.

    if pitcher not in matchups:
        # Create new matchup
        matchups[pitcher] = {'games_with_hit': game_with_hit,
                             'games_started_number': 1.,
                             'games_with_hit_total_ratio': game_with_hit / 1.,
                             'saved_streak_games': saved_streak_game,
                             'saved_streak_ratio': saved_streak_game}

    else:
        # Extend matchup stats
        matchups[pitcher]['games_with_hit'] += game_with_hit
        matchups[pitcher]['games_started_number'] += 1.
        matchups[pitcher]['saved_streak_games'] += saved_streak_game

        saved_streak_games = matchups[pitcher]['saved_streak_games']
        starts = matchups[pitcher]['games_started_number']
        games_with_hit = matchups[pitcher]['games_with_hit']
        matchups[pitcher]['saved_streak_ratio'] = saved_streak_games / starts
        matchups[pitcher]['games_with_hit_total_ratio'] = games_with_hit / starts


def save_batter_matchups(matchups_by_pitcher, pitcher, matchups):
    # Find all batter stats against this starter
    for batter, batter_versus_pitcher in matchups_by_pitcher.iteritems():
        if batter not in best_batter_ids.keys():
            continue

        if batter not in matchups:
            matchups[batter] = {}
            save_pitcher_matchups(batter_versus_pitcher, pitcher, matchups[batter])
        else:
            save_pitcher_matchups(batter_versus_pitcher, pitcher, matchups[batter])


def save_pitcher_stats(pitcher, all_stats_array):
    player_id_number = pitcher['id']
    hits = pitcher['hits']
    outs = pitcher['outs']
    batters_faced_number = pitcher['batters_faced_number']

    if player_id_number not in all_stats_array:

        all_stats_array[player_id_number] = {'games': 1., 'hits_per_game': hits, 'hits': hits,
                                             'outs_per_game': outs / 1.,
                                             'batters_per_game': batters_faced_number / 1.,
                                             'outs': outs,
                                             'batters_faced_number': batters_faced_number}

    else:
        all_stats_array[player_id_number]['games'] += 1.
        all_stats_array[player_id_number]['hits'] += hits
        all_stats_array[player_id_number]['outs'] += outs
        all_stats_array[player_id_number]['batters_faced_number'] += batters_faced_number

        games = all_stats_array[player_id_number]['games']
        hits = all_stats_array[player_id_number]['hits']
        outs = all_stats_array[player_id_number]['outs']
        batters_faced_number = all_stats_array[player_id_number]['batters_faced_number']
        all_stats_array[player_id_number]['hits_per_game'] = hits / games
        all_stats_array[player_id_number]['batters_per_game'] = batters_faced_number / games
        all_stats_array[player_id_number]['outs_per_game'] = outs / games


def save_starter_stats(player, all_stats_array):
    player_id_number = player['id']
    hits = player['hits']
    atbats = player['atbats']
    sacrifice_fly_events = player['sacrifice_fly_events']

    saved_streak_game = 0.
    if not atbats and not sacrifice_fly_events:
        saved_streak_game = 1.

    if hits:
        game_with_hit = 1.
        saved_streak_game = 1
    else:
        game_with_hit = 0.

    if player_id_number not in all_stats_array:
        all_stats_array[player_id_number] = {'games_with_hit': game_with_hit,
                                             'games_started_number': 1.,
                                             'games_with_hit_total_ratio': game_with_hit / 1.,
                                             'saved_streak_games': saved_streak_game,
                                             'saved_streak_ratio': saved_streak_game}

    else:

        all_stats_array[player_id_number]['games_with_hit'] += game_with_hit
        all_stats_array[player_id_number]['games_started_number'] += 1.
        all_stats_array[player_id_number]['saved_streak_games'] += saved_streak_game

        saved_streak_games = all_stats_array[player_id_number]['saved_streak_games']
        starts = all_stats_array[player_id_number]['games_started_number']
        games_with_hit = all_stats_array[player_id_number]['games_with_hit']
        all_stats_array[player_id_number]['saved_streak_ratio'] = saved_streak_games / starts
        all_stats_array[player_id_number]['games_with_hit_total_ratio'] = games_with_hit / starts


def print_players_with_most_games_with_hit():
    parsed_starter_stats = read_all_starting_player_stats()
    top_hitters_dictionary = {}

    print parsed_starter_stats

    for player_id_number, player in parsed_starter_stats.iteritems():
        if player['games_with_hit'] > 12:
            top_hitters_dictionary[player_id_number] = player
            # if player['saved_streak_ratio'] > player['games_with_hit_total_ratio']:
            #     print player

            if player['saved_streak_ratio'] > .75:
                print get_player_name_by_id(player_id_number)
                print player
                print ''

    # print top_hitters_dictionary


def print_pitchers_with_highest_averages():
    parsed_starter_stats = read_all_starting_pitcher_stats()
    top_pitchers_dictionary = {}

    for player_id_number, player in parsed_starter_stats.iteritems():
        if player['hits_per_game'] > 6 and player['games'] > 12:
            top_pitchers_dictionary[player_id_number] = player

            print get_player_name_by_id(player_id_number)
            print player
            print ''

    # print top_pitchers_dictionary
    # print len(top_pitchers_dictionary.keys())
    return top_pitchers_dictionary.keys()


def best_batter_matchups():

    measured_batter_matchups = read_all_measured_batter_matchups()
    for batter in measured_batter_matchups:
        print '---------------------'
        print get_player_name_by_id(batter)
        print '---------------------'

        for pitcher in measured_batter_matchups[batter]:
            games_started_number = measured_batter_matchups[batter][pitcher]["games_started_number"]
            saved_streak_ratio = measured_batter_matchups[batter][pitcher]["saved_streak_ratio"]

            if games_started_number >= 3 and saved_streak_ratio > .7:
                print get_player_name_by_id(pitcher)
                print measured_batter_matchups[batter][pitcher]


def write_starter_stats(stats_by_starter):

    path = os.getcwd() + '/scrubbed_data_sets/'
    with open(path + 'parsed_starting_players.json', 'w') as f:
        json.dump(stats_by_starter, f, indent=3, sort_keys=True, separators=(',', ': '))


def write_starting_pitcher_stats_file(stats_by_starter):

    path = os.getcwd() + '/scrubbed_data_sets/'
    with open(path + 'parsed_starting_pitchers.json', 'w') as f:
        json.dump(stats_by_starter, f, indent=3, sort_keys=True, separators=(',', ': '))


def write_measured_batter_matchups_file(stats_by_starter):

    path = os.getcwd() + '/scrubbed_data_sets/'
    with open(path + 'measured_batter_matchups.json', 'w') as f:
        json.dump(stats_by_starter, f, indent=3, sort_keys=True, separators=(',', ': '))


def read_starter_stats(game_directory_path):

    path = game_directory_path + 'parsed_starting_players.json'
    if not os.path.exists(path):
        return {}

    with open(path, 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data


def read_batter_matchups(game_directory_path):

    path = game_directory_path + 'measured_batter_matchups.json'
    if not os.path.exists(path):
        return {}

    with open(path, 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data


def read_all_starting_player_stats():
    # load from file
    path = os.getcwd() + '/scrubbed_data_sets/'

    with open(path + 'parsed_starting_players.json', 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data


def read_all_starting_pitcher_stats():
    # load from file
    path = os.getcwd() + '/scrubbed_data_sets/'

    with open(path + 'parsed_starting_pitchers.json', 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data


def read_all_measured_batter_matchups():
    # load from file
    path = os.getcwd() + '/scrubbed_data_sets/'

    with open(path + 'measured_batter_matchups.json', 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data


if __name__ == '__main__':
    # Create a dict of all relevant scoreboard urls
    this_url_dictionary = {}

    for this_year in range(FIRST_ACCEPTED_YEAR + 3 - 3, LAST_ACCEPTED_YEAR + 1 - 0):
        these_days_by_month = get_games_by_date(this_year)
        this_url_dictionary[this_year] = these_days_by_month

    # stats = process_starter_stats(this_url_dictionary)

    # write_starter_stats(stats)
    # write_starting_pitcher_stats_file(stats)
    # write_measured_batter_matchups_file(stats)

    # print_players_with_most_games_with_hit()
    # print_pitchers_with_highest_averages()
    best_batter_matchups()

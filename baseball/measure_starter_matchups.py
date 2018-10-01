import os
import json
import os.path

from bs4 import BeautifulSoup

from baseball.initialization.create_game_folders_from_scoreboards import get_scoreboard_file
from baseball.initialization.scrape_xml_scoreboards import get_games_by_date
from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR
from search_player_file import get_player_name_by_id


def process_starter_stats(url_dictionary):

    all_stats_array = {}

    # We iterate from the oldest to newest
    for year in sorted(url_dictionary.keys()):
        item = url_dictionary[year]

        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                process_player_data_for_today(year, month, day, all_stats_array)

    return all_stats_array


def process_player_data_for_today(year, month, day, all_stats_array):
    base_file_name = get_scoreboard_file(year, month, day)
    base_scoreboard_directory = str(str(os.getcwd()) + '/data/' + str(year) + '/' +
                                    convert_month_int_to_string(month) + '/' +
                                    convert_number_to_string(day) + '/')

    print base_scoreboard_directory

    tree = BeautifulSoup(open(base_scoreboard_directory + base_file_name), 'lxml')

    for game in tree.find_all('game'):
        game_dir_path = base_scoreboard_directory + 'gid_' + str(game['id']) + '/'
        get_starter_stats(game_dir_path, all_stats_array)


def get_starter_stats(game_directory_path, all_stats_array):

    starters_by_id = read_starter_stats(game_directory_path)
    if not starters_by_id:
        return
    if starters_by_id['postponed'] or not starters_by_id['valid']:
        return

    # print starters_by_id
    home_starter_stats = starters_by_id['home_starting_players']
    away_starter_stats = starters_by_id['away_starting_players']
    home_starting_pitcher = home_starter_stats['pitcher']
    away_starting_pitcher = away_starter_stats['pitcher']

    for index in range(1, 10):

        position = str(index * 100)
        player = home_starter_stats[position]
        save_starter_stats(player, all_stats_array)
        player = away_starter_stats[position]
        save_starter_stats(player, all_stats_array)


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


def print_high_hits_starter_matchups():
    parsed_starter_stats = read_all_measured_starter_matchups()
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


def write_all_measured_starter_matchups(stats_by_starter):

    path = os.getcwd() + '/scrubbed_data_sets/'
    with open(path + 'measured_starter_matchups.json', 'w') as f:
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


def read_all_measured_starter_matchups():
    # load from file
    path = os.getcwd() + '/scrubbed_data_sets/'

    with open(path + 'measured_starter_matchups.json', 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data


if __name__ == '__main__':
    # Create a dict of all relevant scoreboard urls
    this_url_dictionary = {}

    for this_year in range(FIRST_ACCEPTED_YEAR + 3 - 3, LAST_ACCEPTED_YEAR + 1 - 3):
        these_days_by_month = get_games_by_date(this_year)
        this_url_dictionary[this_year] = these_days_by_month

    stats = process_starter_stats(this_url_dictionary)

    print stats
    # write_all_measured_starter_matchups(stats)
    # print_high_hits_starter_matchups()

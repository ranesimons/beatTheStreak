import os
import json

from bs4 import BeautifulSoup

from baseball.utility.useful_utility_functions import first_date_directory_is_earlier
from baseball.utility.useful_utility_functions import get_earliest_possible_date_directory
from baseball.utility.useful_utility_functions import extract_date_directory
from baseball.initialization.create_game_folders_from_scoreboards import get_scoreboard_file
from baseball.initialization.scrape_xml_scoreboards import get_games_by_date
from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR


def process_player_data(url_dictionary):
    players_by_id = {}
    # We iterate from the oldest to newest
    for year in sorted(url_dictionary.keys()):
        item = url_dictionary[year]

        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                process_player_data_for_today(year, month, day, players_by_id)

    return players_by_id


def process_player_data_for_today(year, month, day, players_by_id):
    base_file_name = get_scoreboard_file(year, month, day)
    base_scoreboard_directory = str(str(os.getcwd()) + '/data/' + str(year) + '/' +
                                    convert_month_int_to_string(month) + '/' +
                                    convert_number_to_string(day) + '/')

    print base_scoreboard_directory

    try:
        tree = BeautifulSoup(open(base_scoreboard_directory + base_file_name), 'lxml')
        for game in tree.find_all('game'):
            game_dir_path = base_scoreboard_directory + 'gid_' + str(game['id']) + '/'
            get_players_data(game_dir_path, players_by_id, base_scoreboard_directory)
    except Exception as exception:
        print exception


def get_players_data(game_directory_path, players_by_id, base_scoreboard_directory):

    try:
        tree = BeautifulSoup(open(game_directory_path + 'players.xml'), 'lxml')
    except IOError as error:
        print 'Unable to retrieve: ' + str(game_directory_path + 'players.xml') + ' - ' + str(error)
        return

    game_date_dir = extract_date_directory(base_scoreboard_directory)

    for player in tree.find_all('player'):
        # rl => throws right or left handed
        bats = str(player.get('bats', ''))

        new_player_name = str(player['first']) + ' ' + str(player['last'])
        if player['id'] not in players_by_id:
            players_by_id[player['id']] = {'name': new_player_name,
                                           'bats': bats,
                                           'throws': str(player['rl']),
                                           'alternate_player_names': [],
                                           'team_by_first_game_dir': {game_date_dir:
                                                                      str(player['team_abbrev'])}}
            continue

        teams_by_date = players_by_id[player['id']]['team_by_first_game_dir']
        new_team_name = str(player['team_abbrev'])
        # Track first appearance on a new team
        if new_team_name not in teams_by_date.values():
            players_by_id[player['id']]['team_by_first_game_dir'][game_date_dir] = new_team_name

        # Track if the player returned to the team after being on another
        elif player_was_traded_back_to_previous_team(teams_by_date, new_team_name):
            players_by_id[player['id']]['team_by_first_game_dir'][game_date_dir] = new_team_name

        current_player_name = players_by_id[player['id']]['name']
        alternate_player_names = players_by_id[player['id']]['alternate_player_names']
        if current_player_name != new_player_name and new_player_name not in alternate_player_names:
            # New player name must be an alias
            players_by_id[player['id']]['alternate_player_names'].append(new_player_name)

        player_bat_hand = players_by_id[player['id']]['bats']
        if bats and not player_bat_hand:
            players_by_id[player['id']]['bats'] = bats

        # Always prefer calling them a switch hitter
        elif bats == 'S':
            players_by_id[player['id']]['bats'] = bats

        # The batter must be a switch hitter
        elif bats == 'R' and player_bat_hand == 'L':
            players_by_id[player['id']]['bats'] = 'S'

        # The batter must be a switch hitter
        elif bats == 'L' and player_bat_hand == 'R':
            players_by_id[player['id']]['bats'] = 'S'

        elif player_bat_hand != 'S':
            assert not bats or player_bat_hand == bats, \
                'bats changed from ' + player_bat_hand + ' to ' + bats

        assert players_by_id[player['id']]['throws'] == str(player['rl'])


def player_was_traded_back_to_previous_team(teams_by_date, new_team_name):
    # Find the last time this player played a game on this team
    most_recent_date = get_earliest_possible_date_directory()

    for date, team in teams_by_date.iteritems():
        if team == new_team_name and first_date_directory_is_earlier(most_recent_date, date):
            most_recent_date = date

    for date, team in teams_by_date.iteritems():
        if team != new_team_name and first_date_directory_is_earlier(most_recent_date, date):
            return True  # The player switched teams at this point

    return False


def print_alternate_and_duplicated_names(players_by_id):
    all_alternate_names = []
    duplicated_player_names = []

    for pid, player in players_by_id.iteritems():
        name = player['name']
        alternate_names_list = player['alternate_player_names']

        for alternative in alternate_names_list:
            if alternative in all_alternate_names:
                duplicated_player_names.append(alternative)
            else:
                all_alternate_names.append(alternative)

        for other_player_id, other_player_entry in players_by_id.iteritems():
            other_player_name = other_player_entry['name']
            other_alternate_names = other_player_entry['alternate_player_names']

            # Only compare players with different player ids
            if other_player_name == name and other_player_id != pid:
                duplicated_player_names.append(name)
            if name in other_alternate_names:
                duplicated_player_names.append(name)

    print len(players_by_id.values())
    print all_alternate_names
    print list(set(duplicated_player_names))


def write_player_file(players_by_id):
    # add special check for names like J.D. Martinez
    # save to file

    path = os.getcwd() + '/scrubbed_data_sets/'
    with open(path + 'players_by_id.json', 'w') as f:
        json.dump(players_by_id, f, indent=3, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    # Create a dict of all relevant scoreboard urls
    this_url_dictionary = {}

    for this_year in range(FIRST_ACCEPTED_YEAR + 3 - 3, LAST_ACCEPTED_YEAR + 1 - 0):
        these_days_by_month = get_games_by_date(this_year)
        this_url_dictionary[this_year] = these_days_by_month

    player_id_dictionary = process_player_data(this_url_dictionary)
    print_alternate_and_duplicated_names(player_id_dictionary)
    write_player_file(player_id_dictionary)

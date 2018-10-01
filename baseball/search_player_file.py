import json
import os

from baseball.utility.useful_utility_functions import first_directory_is_earlier_or_the_same
from baseball.utility.useful_utility_functions import get_earliest_possible_date_directory


def get_player_id_by_name_and_game(name, current_team_name, game_dir_date):
    # Get the matching players dictionary
    matching_players_data = search_for_player(name)

    # print matching_players_data

    # I assume that no two players with the same name are on the same team at the same time
    # Therefore, this dictionary then have unique keys
    player_id_by_first_game_on_team = {}

    for matching_player_id, matching_player_info in matching_players_data.iteritems():
        teams_by_date = matching_player_info['team_by_first_game_dir']
        for date, team in teams_by_date.iteritems():
            if current_team_name == team:
                player_id_by_first_game_on_team[date] = matching_player_id

    # print player_id_by_first_game_on_team

    correct_player_id = None
    most_recent_date_on_team = get_earliest_possible_date_directory()
    for current_team_date, current_player_id in player_id_by_first_game_on_team.iteritems():
        if first_directory_is_earlier_or_the_same(current_team_date, game_dir_date):
            if first_directory_is_earlier_or_the_same(most_recent_date_on_team, current_team_date):
                most_recent_date_on_team = current_team_date
                correct_player_id = current_player_id

    if not correct_player_id:
        raise Exception('Unable to find the given player: ' + str(name))
    return correct_player_id


def search_for_player(name):
    # Sanitize search name
    name = handle_name_conversion_edge_cases(name)

    # print str('|') + name + str('|')
    players_by_id = read_player_file()
    matching_players_data = {}

    for index, player in players_by_id.iteritems():
        if player_data_matches_name(name, player):
            matching_players_data[index] = player

    return matching_players_data


def get_player_name_by_id(given_player_id):
    players_by_id = read_player_file()
    player = players_by_id.get(given_player_id)

    if not player:
        return None
    return player['name']


def player_data_matches_name(name, player):
    if name == player['name']:
        return True
    elif name in player['alternate_player_names']:
        return True

    if name + '.' == player['name']:
        return True
    for other_possible_name in player['alternate_player_names']:
        if name + '.' == other_possible_name:
            return True

    # Edge case for names like 'A.J. Reed'
    if '. ' in name and '. ' in player['name']:
        last_period_index = player['name'].rfind('. ')
        abbreviated_player_name = player['name'][:last_period_index - 1]
        abbreviated_player_name += player['name'][last_period_index + 1:]
        if abbreviated_player_name == name:
            return True

    for alternate in player['alternate_player_names']:
        if '. ' in name and '. ' in alternate:
            last_period_index = alternate.rfind('. ')
            abbreviated_player_name = alternate[:last_period_index - 1]
            abbreviated_player_name += alternate[last_period_index + 1:]
            if abbreviated_player_name == name:
                return True

    return False


# No names contain three consecutive
def adjust_player_names():
    players_by_id = read_player_file()
    matching_player_names = []

    for index, player in players_by_id.iteritems():
        if player['name'][-1] == '.':
            # print '---------------------'
            # print player['name']
            # print '---------------------'
            matching_player_names.append(player['name'])
        for name in player['alternate_player_names']:
            if name[-1] == '.':
                # print '---------------------'
                # print name
                # print '---------------------'
                matching_player_names.append(name)

    # adjusted_player_names = []
    # for special_player_name in matching_player_names:
    #     index = special_player_name.rfind('. ')
    #     adjusted_player_names.append(special_player_name[index + 2:])
    #
    # print len(list(set(adjusted_player_names)))
    # print len(matching_player_names)
    # return adjusted_player_names


def handle_name_conversion_edge_cases(name):
    name = name.strip()
    if '   ' in name:
        name = name.replace('  ', '')
    return name


def read_player_file():
    # load from file
    path = os.getcwd() + '/scrubbed_data_sets/'

    with open(path + 'players_by_id.json', 'r') as f:
        try:
            data = json.load(f)

        # the ValueError will be thrown if empty
        except ValueError:
            data = {}

    return data

if __name__ == '__main__':
    # print search_for_player('A.  J.   Ramos')
    print search_for_player('Nolan Arenado')
    # print adjust_player_names()
    pass

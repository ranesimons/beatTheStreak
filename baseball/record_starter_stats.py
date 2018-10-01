from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR

from baseball.utility.parse_plate_appearances import extract_pitch_list
from baseball.utility.parse_plate_appearances import is_actual_atbat
from baseball.utility.parse_plate_appearances import is_a_hit
from baseball.utility.parse_plate_appearances import is_a_homer
from baseball.utility.parse_plate_appearances import is_a_strikeout
from baseball.utility.parse_plate_appearances import is_a_walk
from baseball.utility.parse_plate_appearances import hitter_replaced_with_two_strikes
from baseball.utility.parse_plate_appearances import pitcher_replaced_with_more_walks
from baseball.utility.parse_plate_appearances import special_strikeout_case
from baseball.utility.parse_plate_appearances import special_walk_case
from baseball.utility.parse_plate_appearances import parse_strikeout_event
from baseball.utility.parse_plate_appearances import is_an_atbat
from baseball.utility.parse_plate_appearances import runner_thrown_out
from baseball.utility.parse_plate_appearances import save_starting_players
from baseball.utility.parse_plate_appearances import is_sacrifice_fly
from baseball.utility.parse_plate_appearances import is_sacrifice_bunt

from search_player_file import get_player_id_by_name_and_game

from baseball.utility.handle_hitter_lineups import save_starting_lineup
from baseball.utility.handle_hitter_lineups import save_defensive_substitution
from baseball.utility.handle_hitter_lineups import save_offensive_substitution
from baseball.utility.handle_hitter_lineups import save_pitching_substitution
from baseball.utility.handle_hitter_lineups import update_batter_dictionary
from baseball.utility.handle_hitter_lineups import update_pitcher_dictionary
from baseball.utility.handle_hitter_lineups import update_matchups_dictionary
from baseball.utility.handle_hitter_lineups import update_pitcher_outs
from baseball.utility.handle_hitter_lineups import validate_lineup_data

from baseball.initialization.scrape_xml_scoreboards import get_games_by_date
from baseball.initialization.create_game_folders_from_scoreboards import get_scoreboard_file

from bs4 import BeautifulSoup
import os


def process_player_data(url_dictionary):
    all_events_array = {}
    # We iterate from the oldest to newest
    for year in sorted(url_dictionary.keys()):
        item = url_dictionary[year]

        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                process_player_data_for_today(year, month, day, all_events_array)

    return all_events_array


def process_player_data_for_today(year, month, day, all_events_array):
    base_file_name = get_scoreboard_file(year, month, day)
    base_scoreboard_directory = str(str(os.getcwd()) + '/data/' + str(year) + '/' +
                                    convert_month_int_to_string(month) + '/' +
                                    convert_number_to_string(day) + '/')

    print base_scoreboard_directory

    tree = BeautifulSoup(open(base_scoreboard_directory + base_file_name), 'lxml')

    for game in tree.find_all('game'):
        game_dir_path = base_scoreboard_directory + 'gid_' + str(game['id']) + '/'
        team_name_abbreviations = get_linescore_data(game_dir_path)
        expected_player_stats = get_boxscore_data(game_dir_path)
        outcome = get_outcomes_data(game_dir_path, expected_player_stats,
                                    team_name_abbreviations,
                                    base_scoreboard_directory)

        if outcome:
            all_events_array[game_dir_path] = outcome
            # all_events_array.update(outcome)


def get_outcomes_data(game_directory_path, expected_game_stats, team_name_abbreviations, date):

    try:
        tree = BeautifulSoup(open(game_directory_path + 'game_events.xml'), 'lxml')
    except IOError as error:
        print 'Unable to get: ' + str(game_directory_path + 'game_events.xml') + ' - ' + str(error)
        return

    measured_game_stats = {'measured_batter_stats': {}, 'measured_pitcher_stats': {},
                           'last_inning_played': 0, 'last_inning_frame': '',
                           'number_of_outs': 0, 'measured_batter_matchups': {}}
    previous_home_pitches = []
    previous_away_pitches = []

    lineup = {'previous_home_batter': None, 'home_pinch_hitters': {}, 'home_atbat_number': 0,
              'recorded_home_starters': False, 'recorded_away_starters': False,
              'home_batting_interference': [], 'away_batting_interference': [],
              'previous_away_batter': None, 'away_pinch_hitters': {}, 'away_atbat_number': 0,
              'home_pitchers_order': [], 'away_pitchers_order': []}

    for inning in tree.find_all('inning'):

        top_inning_events = inning.top.find_all(['atbat', 'action'])
        if not top_inning_events:
            break

        # The game has officially started right now
        measured_game_stats['number_of_outs'] = 0
        measured_game_stats['last_inning_played'] = inning['num']

        previous_away_pitches = get_atbats_data(top_inning_events, previous_away_pitches,
                                                measured_game_stats, team_name_abbreviations,
                                                date, lineup, 'top')

        bottom_inning_events = inning.bottom.find_all(['atbat', 'action'])
        if not bottom_inning_events:
            break

        measured_game_stats['number_of_outs'] = 0

        previous_home_pitches = get_atbats_data(bottom_inning_events, previous_home_pitches,
                                                measured_game_stats, team_name_abbreviations,
                                                date, lineup, 'bottom')

    result = validate_lineup_data(expected_game_stats, measured_game_stats, lineup)
    save_starting_players(lineup, expected_game_stats, measured_game_stats,
                          game_directory_path, team_name_abbreviations, date)

    return result


def get_atbats_data(events, previous_pitches_list, stats, teams, date, lineup, frame):
    measured_pitcher_stats = stats['measured_pitcher_stats']
    measured_batter_stats = stats['measured_batter_stats']

    measured_batter_matchups = stats['measured_batter_matchups']
    away_team_name = teams['away_team_name']
    home_team_name = teams['home_team_name']

    if frame == 'top':
        batting_team_name = away_team_name
        pitching_team_name = home_team_name
        stats['last_inning_frame'] = 'top'
        ordered_pitcher_appearances = 'home_pitchers_order'

    elif frame == 'bottom':
        batting_team_name = home_team_name
        pitching_team_name = away_team_name
        stats['last_inning_frame'] = 'bottom'
        ordered_pitcher_appearances = 'away_pitchers_order'
    else:
        raise Exception('Unable to recognize the frame: ' + str(frame))

    ordered_pitchers_list = lineup[ordered_pitcher_appearances]

    # Use this for the special strikeout case
    potential_substitute_strikeout = False
    potential_substitute_walk = False

    dictionary_of_outs = {'previous_outs_number': 0, 'current_outs_number': 0}

    for event in events:  # use action and event xml
        if hitter_replaced_with_two_strikes(event):
            potential_substitute_strikeout = True
        if pitcher_replaced_with_more_walks(event):
            potential_substitute_walk = True

        if event['event'] == 'Offensive Sub' or event['event'] == 'Offensive sub':
            save_offensive_substitution(event, lineup, frame, batting_team_name,
                                        date, measured_batter_stats)

        if event['event'] == 'Pitching Substitution':
            save_pitching_substitution(event, lineup, frame, pitching_team_name,
                                       date, measured_batter_stats, measured_pitcher_stats)

        if event['event'] == 'Defensive Sub':
            save_defensive_substitution(event, lineup, frame, pitching_team_name,
                                        date, measured_batter_stats)

        # Handling the 2014 fielder interference edge case

        reaches = 'reaches on an interference error'
        if event.name == 'action' and event['event'] == 'Field Error' and reaches in event['des']:
            assert ordered_pitchers_list, 'The first pitcher has not been tracked'

            current_pitcher_id = ordered_pitchers_list[-1]
            current_outs_number = event['o']
            dictionary_of_outs['current_outs_number'] = current_outs_number

            stats['number_of_outs'] = current_outs_number
            save_starting_lineup(measured_batter_stats, event['player'],
                                 current_pitcher_id, lineup, frame, True)

            update_batter_dictionary(measured_batter_stats, event['player'], 'appearance')
            update_pitcher_dictionary(measured_pitcher_stats, current_pitcher_id, 'appearance')
            update_pitcher_outs(current_pitcher_id, dictionary_of_outs, measured_pitcher_stats)
            update_matchups_dictionary(measured_batter_matchups, event['player'],
                                       current_pitcher_id, 'appearance')

        if runner_thrown_out(event):
            current_pitcher_id = ordered_pitchers_list[-1]
            current_outs_number = event['o']

            stats['number_of_outs'] = current_outs_number
            dictionary_of_outs['current_outs_number'] = current_outs_number
            update_pitcher_outs(current_pitcher_id, dictionary_of_outs, measured_pitcher_stats)

        # print '------------'
        if event.name == 'action':
            continue

        atbat = event
        is_valid_appearance = True
        interference = False
        if 'reaches on an interference error by' in atbat['des']:
            interference = True

        current_pitches_list = extract_pitch_list(atbat.find_all('pitch'))
        if not is_actual_atbat(current_pitches_list, previous_pitches_list, atbat['event']):
            print '---------------------'
            print atbat
            print '---------------------'
            is_valid_appearance = False

        elif is_a_homer(atbat['event'], atbat['des']):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'homer')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'homer')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'homer')

        elif is_a_hit(atbat['event'], atbat['des']):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'hit')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'hit')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'hit')

        # Walk goes to the original pitcher here
        elif special_walk_case(atbat['event'], atbat['des'], potential_substitute_walk):
            previous_pitcher_id = ordered_pitchers_list[-2]
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'walk')
            update_pitcher_dictionary(measured_pitcher_stats, previous_pitcher_id, 'walk')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       previous_pitcher_id, 'walk')

        elif is_a_walk(atbat['event'], atbat['des']):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'walk')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'walk')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'walk')

        # Strikeout goes to the original batter here
        elif special_strikeout_case(atbat['event'], atbat['des'], potential_substitute_strikeout):
            previous_player_name = parse_strikeout_event(atbat['des'])
            previous_player_id = get_player_id_by_name_and_game(previous_player_name,
                                                                batting_team_name, date)

            # Save event information
            update_batter_dictionary(measured_batter_stats, previous_player_id, 'strikeout')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'strikeout')
            update_matchups_dictionary(measured_batter_matchups, previous_player_id,
                                       atbat['pitcher'], 'strikeout')

        elif is_a_strikeout(atbat['event'], atbat['des']):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'strikeout')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'strikeout')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'strikeout')

        elif is_sacrifice_fly(atbat['event']):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'sacrifice_fly_event')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'appearance')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'sacrifice_fly_event')

        elif is_sacrifice_bunt(atbat['event']):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'sacrifice_bunt_event')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'appearance')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'sacrifice_bunt_event')

        elif is_an_atbat(atbat['event'], atbat['des'], atbat.find_all('pitch')):
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'atbat')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'appearance')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'atbat')

        elif is_valid_appearance:
            update_batter_dictionary(measured_batter_stats, atbat['batter'], 'appearance')
            update_pitcher_dictionary(measured_pitcher_stats, atbat['pitcher'], 'appearance')
            update_matchups_dictionary(measured_batter_matchups, event['batter'],
                                       atbat['pitcher'], 'appearance')

        if is_valid_appearance:
            save_starting_lineup(measured_batter_stats, atbat['batter'], atbat['pitcher'],
                                 lineup, frame, interference)

        current_outs_number = event['o']
        dictionary_of_outs['current_outs_number'] = current_outs_number
        update_pitcher_outs(atbat['pitcher'], dictionary_of_outs, measured_pitcher_stats)

        stats['number_of_outs'] = current_outs_number

        previous_pitches_list = current_pitches_list
        potential_substitute_strikeout = False
        potential_substitute_walk = False
        if int(current_outs_number) == 3:
            break

    return previous_pitches_list


def get_linescore_data(game_directory_path):

    try:
        tree = BeautifulSoup(open(game_directory_path + 'linescore.xml'), 'lxml')
    except IOError as error:
        print 'Unable to get: ' + str(game_directory_path + 'linescore.xml') + ' - ' + str(error)
        return [0, 0]

    for game in tree.find_all('game'):
        # print str(game['venue'])
        # print str(game['time'])
        # print str(game['time_zone'])
        # print str(game['ampm'])
        return {'away_team_name': str(game['away_name_abbrev']),
                'home_team_name': str(game['home_name_abbrev'])}


def get_boxscore_data(game_directory_path):

    try:
        tree = BeautifulSoup(open(game_directory_path + 'boxscore.xml'), 'lxml')
    except IOError as error:
        print 'Unable to get: ' + str(game_directory_path + 'boxscore.xml') + ' - ' + str(error)
        return [0, 0]

    print game_directory_path

    away_team_code = ''
    home_team_code = ''
    for linescore in tree.find_all('boxscore'):
        away_team_code = linescore['away_team_code']
        home_team_code = linescore['home_team_code']
    assert away_team_code, 'Unable to parse the away team code'
    assert home_team_code, 'Unable to parse the home team code'

    away_team_runs = 0
    home_team_runs = 0
    for linescore in tree.find_all('linescore'):
        away_team_runs = linescore['away_team_runs']
        home_team_runs = linescore['home_team_runs']

    total_plate_appearances = {}

    for pitching in tree.find_all('pitching'):
        if pitching['team_flag'] == 'away':
            total_plate_appearances['home_plate_appearances'] = int(pitching['bf'])
        if pitching['team_flag'] == 'home':
            total_plate_appearances['away_plate_appearances'] = int(pitching['bf'])

    batter_stats_dictionary = {}
    for batter in tree.find_all('batter'):
        batter_actually_batted = batter.get('bo', None)
        if batter_actually_batted is None:
            continue

        if batter['id'] not in batter_stats_dictionary:
            batter_stats_dictionary[batter['id']] = {'atbats': batter['ab'],
                                                     'batting_lineup_position': batter['bo'],
                                                     'hits': batter['h'], 'walks': batter['bb'],
                                                     'strikeouts': batter['so'],
                                                     'homers': batter['hr'],
                                                     'sacrifices': batter['sac']}

    pitcher_stats_dictionary = {}

    for pitcher in tree.find_all('pitcher'):

        if pitcher['id'] not in pitcher_stats_dictionary:
            pitcher_stats_dictionary[pitcher['id']] = {'outs': pitcher['out'],
                                                       'batters_faced_number': pitcher['bf'],
                                                       'hits': pitcher['h'],
                                                       'walks': pitcher['bb'],
                                                       'strikeouts': pitcher['so'],
                                                       'homers': pitcher['hr']}

    return {'total_plate_appearances': total_plate_appearances,
            'expected_pitcher_stats': pitcher_stats_dictionary,
            'expected_batter_stats': batter_stats_dictionary,
            'away_team_runs': away_team_runs,
            'home_team_runs': home_team_runs,
            'away_team_code': away_team_code,
            'home_team_code': home_team_code}


if __name__ == '__main__':
    # Create a dict of all relevant scoreboard urls
    this_url_dictionary = {}

    for this_year in range(LAST_ACCEPTED_YEAR + 3 - 3, LAST_ACCEPTED_YEAR + 1 - 0):
        these_days_by_month = get_games_by_date(this_year)
        this_url_dictionary[this_year] = these_days_by_month

    all_game_events = process_player_data(this_url_dictionary)

    print all_game_events

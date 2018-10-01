from baseball.search_player_file import get_player_name_by_id
import json
import os


def extract_pitch_list(pitches):
    pitch_id_list = []
    for pitch in pitches:
        pitch_id_list.append(pitch['sv_id'])
    return pitch_id_list


def pitch_was_duplicated(previous_pitch_list, current_pitch_list):
    edge_case_values = ["170415_021422", "170415_042714", "170416_011955",
                        "170427_015250", "170503_001140", "170503_001702",
                        "170503_001702", "170503_003140", "170503_003139",
                        "170503_020204", "170503_002010", '_']
    for pitch in current_pitch_list:
        if pitch and (pitch not in edge_case_values) and (pitch in previous_pitch_list):
            return True
    return False


def is_fan_interference_ruled_hit(event, description_of_event):
    if event != 'Fan interference':
        return False

    fan_interference_hits = ['ground-rule double', 'doubles', 'triples', 'homers', 'singles']
    for fan_interference_hit in fan_interference_hits:
        if fan_interference_hit in description_of_event:
            return True
    return False


def is_double_play_ruled_hit(event, double_play_description):
    if event != 'Double Play':
        return False

    double_play_hits = ['singles']
    for double_play_hit in double_play_hits:
        if double_play_hit in double_play_description:
            return True
    return False


def is_double_play_ruled_walk(event, double_play_description):
    if event != 'Double Play':
        return False

    double_play_walks = ['walks']
    for double_play_walk in double_play_walks:
        if double_play_walk in double_play_description:
            return True
    return False


def is_actual_atbat(current_atbat_pitches, previous_atbat_pitches, event):
    if event == 'Runner Out':  # The batter will bat again next inning
        return False
    if not current_atbat_pitches:
        return True

    # This is an occasional mlb generated bug
    if pitch_was_duplicated(previous_atbat_pitches, current_atbat_pitches):
        return False

    return True


def is_runner_out(event):
    # The batter will bat again next inning
    if event == 'Runner Out':
        return True
    return False


def is_a_hit(event, description_of_event):
    # is actual atbat must be called before
    hits = ['Single', 'Double', 'Home Run', 'Triple']
    if event in hits:
        return True

    if is_fan_interference_ruled_hit(event, description_of_event):
        return True
    if is_double_play_ruled_hit(event, description_of_event):
        return True
    return False


def is_a_homer(event, description_of_event):
    # must be called after is actual atbat and before is a hit
    if event == 'Home Run':
        return True
    if event == 'Fan interference' and 'homers' in description_of_event:
        return True
    return False


def is_a_strikeout(event, description_of_event):
    if event == 'Strikeout' or event == 'Strikeout - DP':
        return True

    # Only consider batter interference cases for now
    if event != 'Batter Interference':
        return False

    strikeout_event_descriptions = [' called out on strikes', ' strikes out']

    for strikeout in strikeout_event_descriptions:
        index = description_of_event.rfind(strikeout)
        if index > 0:
            return True
    return False


def is_a_walk(event, description_of_event):
    # is actual atbat must be called before
    walks = ['Walk', 'Intent Walk']
    if event in walks:
        return True

    if is_double_play_ruled_walk(event, description_of_event):
        return True
    return False


def hitter_replaced_with_two_strikes(current_action_xml):
    if current_action_xml.name != 'action':
        return False

    # Return True if the strikeout credit might go to the previous batter
    offensive_substitution_cases = ['Offensive Sub', 'Offensive sub']
    if current_action_xml and current_action_xml['event'] in offensive_substitution_cases:
        if current_action_xml['s'] == '2' and 'Pinch-hitter' in current_action_xml['des']:
            return True

    return False


def pitcher_replaced_with_more_walks(current_action_xml):
    if current_action_xml.name != 'action':
        return False

    # Return True if the walk credit might go to the previous pitcher
    if current_action_xml and current_action_xml['event'] == 'Pitching Substitution':
        balls = int(current_action_xml['b'])
        strikes = int(current_action_xml['s'])
        # True if relief pitcher inherits unfavorable count
        if (balls > strikes) and (balls != 1 or strikes != 0):
            return True

    return False


def special_strikeout_case(event, description_of_event, two_strike_substitution):
    if not is_a_strikeout(event, description_of_event):
        return False

    if not two_strike_substitution:
        return False
    return True


def special_walk_case(event, description_of_event, more_walks_substitution):
    if not is_a_walk(event, description_of_event):
        return False

    if not more_walks_substitution:
        return False
    return True


def parse_strikeout_event(description_of_event):
    # All possible events include
    #   ' called out on strikes'
    #   ' strikes out swinging'
    #   ' strikes out on a foul tip'
    #   ' strikes out on a missed bunt'
    #   ' strikes out on a foul bunt'
    #   ' strikes out'
    strikeout_event_descriptions = [' called out on strikes', ' strikes out']

    for strikeout in strikeout_event_descriptions:
        index = description_of_event.rfind(strikeout)
        if index > 0:
            return description_of_event[:index]
    raise Exception('Unable to parse strikeout event: ' + str(description_of_event))


def is_an_atbat(event, description_of_event, pitches):
    non_atbat_events = ['Sac Fly', 'Hit By Pitch', 'Sac Fly DP', 'Sacrifice Bunt DP',
                        'Sac Bunt', 'Runner Out', 'Catcher Interference']

    for non_atbat_event in non_atbat_events:
        if event == non_atbat_event:
            return False

    pitcher_interference_case = 'reaches on an interference error by pitcher'
    if event == 'Field Error' and pitcher_interference_case in description_of_event:
        final_pitch_result = pitches[-1]
        final_pitch_outcome = final_pitch_result['des']
        # If the pitch event said "out" but they reached, count the atbat

        if final_pitch_outcome == 'In play, out(s)':
            return True
        return False

    return True


def is_sacrifice_fly(description_of_event):
    sacrifice_fly_events = ['Sac Fly', 'Sac Fly DP']
    for sacrifice_fly_event in sacrifice_fly_events:
        if sacrifice_fly_event == description_of_event:
            return True

    return False


def is_sacrifice_bunt(description_of_event):
    sacrifice_fly_events = ['Sac Bunt', 'Sacrifice Bunt DP']
    for sacrifice_fly_event in sacrifice_fly_events:
        if sacrifice_fly_event == description_of_event:
            return True

    return False


def runner_thrown_out(event):
    if event.name != 'action':
        return False

    thrown_out_events = ['Runner Out', 'Pickoff 1B', 'Pickoff 2B', 'Pickoff 3B',
                         'Base Running Double Play', 'Picked off stealing 2B',
                         'Picked off stealing 3B', 'Picked off stealing home',
                         'Caught Stealing 2B', 'Caught Stealing 3B', 'Caught Stealing Home']
    if event['event'] in thrown_out_events:
        return True
    return False


def save_starting_players(lineup, expected_game_stats, measured_game_stats, directory, teams, date):
    measured_pitcher_stats = measured_game_stats['measured_pitcher_stats']
    measured_batter_stats = measured_game_stats['measured_batter_stats']

    measured_batter_matchups = measured_game_stats['measured_batter_matchups']
    home_pinch_hitters = lineup['home_pinch_hitters']
    away_pinch_hitters = lineup['away_pinch_hitters']
    home_pitchers_order = lineup['home_pitchers_order']
    away_pitchers_order = lineup['away_pitchers_order']

    last_inning_played = int(measured_game_stats['last_inning_played'])
    frame = measured_game_stats['last_inning_frame']
    outs = int(measured_game_stats['number_of_outs'])
    away_team_runs = int(expected_game_stats['away_team_runs'])
    home_team_runs = int(expected_game_stats['home_team_runs'])
    away_team_code = expected_game_stats['away_team_code']
    home_team_code = expected_game_stats['home_team_code']

    # Record the base data for every game
    away_team_name = teams['away_team_name']
    home_team_name = teams['home_team_name']
    parsed_starting_players = {'postponed': True, 'valid': False, 'home_team_name': home_team_name,
                               'away_team_name': away_team_name, 'date': date}

    # This game must have never actually started
    if not last_inning_played and not frame and not outs:
        write_player_file(parsed_starting_players, directory)
        print '---THIS GAME MUST HAVE BEEN OFFICIALLY POSTPONED---'
        return

    valid = True
    parsed_starting_players['postponed'] = False
    parsed_starting_players['valid'] = valid

    # Games longer than 5 innings are valid
    # The away team must complete the fifth
    # The trailing team must complete the fifth
    if last_inning_played > 5:
        valid = True
    elif last_inning_played < 5:
        valid = False

    elif home_team_runs == away_team_runs:  # This must be in the fifth inning
        if frame == 'bottom':
            valid = True
        elif frame == 'top' and outs == 3:
            valid = True
        elif frame == 'top' and outs < 3:
            valid = False

    elif home_team_runs > away_team_runs:  # This must be in the fifth inning
        if frame == 'bottom':
            valid = True
        elif frame == 'top' and outs == 3:
            valid = True
        elif frame == 'top' and outs < 3:
            valid = False

    elif home_team_runs < away_team_runs:  # This must be in the fifth inning
        if frame == 'top':
            valid = False
        elif frame == 'bottom' and outs < 3:
            valid = False
        elif frame == 'bottom' and outs == 3:
            valid = True

    else:
        raise Exception('Unable to parse game validity: ' + frame + ' of ' +
                        str(last_inning_played) + ' with ' + str(outs) + ' outs')

    # Refer to the beat the streak rules
    if not valid:
        parsed_starting_players['valid'] = False
        write_player_file(parsed_starting_players, directory)
        return

    last_inning_played = str(measured_game_stats['last_inning_played'])
    outs = str(measured_game_stats['number_of_outs'])
    print 'LAST INNING PLAYED: ' + frame + ' of ' + last_inning_played + ' with ' + outs + ' outs'

    print 'HOME TEAM RUNS: ' + str(home_team_runs)
    print 'HOME TEAM CODE: ' + str(home_team_code)
    print '----HOME STARTING PLAYERS----'

    if not home_pitchers_order:
        raise Exception('No home starting pitcher has been recorded')
    measured_pitcher_data = measured_pitcher_stats[home_pitchers_order[0]]
    measured_pitcher_data['id'] = home_pitchers_order[0]
    home_starting_players = {'pitcher': measured_pitcher_data}

    pitcher = get_player_name_by_id(home_pitchers_order[0])
    if pitcher:
        print 'Pitcher: ' + str(pitcher)
    else:
        raise Exception('Unable to find home team starting pitcher')

    for position in range(1, 10):
        starting_player_position = str(position * 100)
        player = home_pinch_hitters.get(starting_player_position)
        if not player:
            raise Exception('Unable to find the home team player: ' + starting_player_position)

        name = get_player_name_by_id(player)
        if name:
            print str(position) + ') ' + str(name)
        else:
            raise Exception('Unable to find home team player name')

        measured_batter_data = measured_batter_stats[player]
        measured_batter_data['id'] = player
        measured_batter_data['team'] = home_team_name

        home_starting_players[starting_player_position] = measured_batter_data

    print 'AWAY TEAM RUNS: ' + str(away_team_runs)
    print 'AWAY TEAM CODE: ' + str(away_team_code)
    print '----AWAY STARTING PLAYERS----'

    if not away_pitchers_order:
        raise Exception('No away starting pitcher has been recorded')
    measured_pitcher_data = measured_pitcher_stats[away_pitchers_order[0]]
    measured_pitcher_data['id'] = away_pitchers_order[0]
    away_starting_players = {'pitcher': measured_pitcher_data}

    pitcher = get_player_name_by_id(away_pitchers_order[0])
    if pitcher:
        print 'Pitcher: ' + str(pitcher)
    else:
        raise Exception('Unable to find away team starting pitcher')

    for position in range(1, 10):
        starting_player_position = str(position * 100)
        player = away_pinch_hitters.get(starting_player_position)
        if not player:
            raise Exception('Unable to find the away team player: ' + starting_player_position)

        name = get_player_name_by_id(player)
        if name:
            print str(position) + ') ' + str(name)
        else:
            raise Exception('Unable to find away team player name')

        measured_batter_data = measured_batter_stats[player]
        measured_batter_data['id'] = player
        measured_batter_data['team'] = away_team_name

        away_starting_players[starting_player_position] = measured_batter_data

    parsed_starting_players['home_starting_players'] = home_starting_players
    parsed_starting_players['away_starting_players'] = away_starting_players
    write_player_file(parsed_starting_players, directory)

    write_matchups_file(measured_batter_matchups, directory)


def write_player_file(parsed_starting_players, game_directory_path):
    with open(game_directory_path + 'parsed_starting_players.json', 'w') as f:
        json.dump(parsed_starting_players, f, indent=3, sort_keys=True, separators=(',', ': '))


def write_matchups_file(measured_batter_matchups, game_directory_path):
    with open(game_directory_path + 'measured_batter_matchups.json', 'w') as f:
        json.dump(measured_batter_matchups, f, indent=3, sort_keys=True, separators=(',', ': '))

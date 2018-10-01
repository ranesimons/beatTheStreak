from baseball.search_player_file import get_player_id_by_name_and_game


def update_matchups_dictionary(measured_batter_matchups, batter, pitcher, type_of_event):
    # The matchups are stored by pitcher id
    batters_by_pitcher = measured_batter_matchups.get(pitcher)

    if not batters_by_pitcher:
        measured_batter_matchups[pitcher] = {}
        update_batter_dictionary(measured_batter_matchups[pitcher], batter, type_of_event)
    else:
        update_batter_dictionary(measured_batter_matchups[pitcher], batter, type_of_event)


def update_batter_dictionary(measured_batter_stats, batter, type_of_event):

    if type_of_event == 'hit':
        if batter in measured_batter_stats:
            measured_batter_stats[batter]['hits'] += 1
            measured_batter_stats[batter]['atbats'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 1, 'homers': 0, 'walks': 0, 'strikeouts': 0,
                                             'atbats': 1, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}

    if type_of_event == 'homer':

        if batter in measured_batter_stats:
            measured_batter_stats[batter]['hits'] += 1
            measured_batter_stats[batter]['homers'] += 1
            measured_batter_stats[batter]['atbats'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 1, 'homers': 1, 'walks': 0, 'strikeouts': 0,
                                             'atbats': 1, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}

    if type_of_event == 'strikeout':
        if batter in measured_batter_stats:
            measured_batter_stats[batter]['strikeouts'] += 1
            measured_batter_stats[batter]['atbats'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 0, 'strikeouts': 1,
                                             'atbats': 1, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}

    if type_of_event == 'walk':

        if batter in measured_batter_stats:
            measured_batter_stats[batter]['walks'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 1, 'strikeouts': 0,
                                             'atbats': 0, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}

    if type_of_event == 'atbat':

        if batter in measured_batter_stats:
            measured_batter_stats[batter]['atbats'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 0, 'strikeouts': 0,
                                             'atbats': 1, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}

    if type_of_event == 'sacrifice_fly_event':

        if batter in measured_batter_stats:
            measured_batter_stats[batter]['sacrifice_fly_events'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 0, 'strikeouts': 0,
                                             'atbats': 0, 'sacrifice_fly_events': 1,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}

    if type_of_event == 'sacrifice_bunt_event':

        if batter in measured_batter_stats:
            measured_batter_stats[batter]['sacrifice_bunt_events'] += 1
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 0, 'strikeouts': 0,
                                             'atbats': 0, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 1,
                                             'plate_appearances_number': 1}

    if type_of_event == 'appearance':
        if batter in measured_batter_stats:
            measured_batter_stats[batter]['plate_appearances_number'] += 1

        else:
            measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 0, 'strikeouts': 0,
                                             'atbats': 0, 'sacrifice_fly_events': 0,
                                             'sacrifice_bunt_events': 0,
                                             'plate_appearances_number': 1}


def update_pitcher_dictionary(measured_pitcher_stats, pitcher, type_of_event):

    if type_of_event == 'hit':

        if pitcher in measured_pitcher_stats:
            measured_pitcher_stats[pitcher]['hits'] += 1
            measured_pitcher_stats[pitcher]['batters_faced_number'] += 1

        else:
            measured_pitcher_stats[pitcher] = {'hits': 1, 'homers': 0, 'walks': 0, 'outs': 0,
                                               'strikeouts': 0, 'batters_faced_number': 1}

    if type_of_event == 'homer':
        if pitcher in measured_pitcher_stats:
            measured_pitcher_stats[pitcher]['hits'] += 1
            measured_pitcher_stats[pitcher]['homers'] += 1
            measured_pitcher_stats[pitcher]['batters_faced_number'] += 1

        else:
            measured_pitcher_stats[pitcher] = {'hits': 1, 'homers': 1, 'walks': 0, 'outs': 0,
                                               'strikeouts': 0, 'batters_faced_number': 1}

    if type_of_event == 'strikeout':

        if pitcher in measured_pitcher_stats:
            measured_pitcher_stats[pitcher]['strikeouts'] += 1
            measured_pitcher_stats[pitcher]['batters_faced_number'] += 1

        else:
            measured_pitcher_stats[pitcher] = {'hits': 0, 'homers': 0, 'walks': 0, 'outs': 0,
                                               'strikeouts': 1, 'batters_faced_number': 1}

    if type_of_event == 'walk':

        if pitcher in measured_pitcher_stats:
            measured_pitcher_stats[pitcher]['walks'] += 1
            measured_pitcher_stats[pitcher]['batters_faced_number'] += 1

        else:
            measured_pitcher_stats[pitcher] = {'hits': 0, 'homers': 0, 'walks': 1, 'outs': 0,
                                               'strikeouts': 0, 'batters_faced_number': 1}

    if type_of_event == 'appearance':
        if pitcher in measured_pitcher_stats:
            measured_pitcher_stats[pitcher]['batters_faced_number'] += 1

        else:
            measured_pitcher_stats[pitcher] = {'hits': 0, 'homers': 0, 'walks': 0, 'outs': 0,
                                               'strikeouts': 0, 'batters_faced_number': 1}


def save_starting_lineup(measured_batter_stats, batter, pitcher, lineup, frame, interference):

    if frame == 'top':
        previous_batter_position = 'previous_away_batter'
        pinch_hitter_dictionary = 'away_pinch_hitters'
        current_atbat_number = 'away_atbat_number'
        recorded_starting_lineup = 'recorded_away_starters'
        batting_interference_count = 'away_batting_interference'
        ordered_pitcher_appearances = 'home_pitchers_order'

    elif frame == 'bottom':
        previous_batter_position = 'previous_home_batter'
        pinch_hitter_dictionary = 'home_pinch_hitters'
        current_atbat_number = 'home_atbat_number'
        recorded_starting_lineup = 'recorded_home_starters'
        batting_interference_count = 'home_batting_interference'
        ordered_pitcher_appearances = 'away_pitchers_order'

    # The only frames are 'top' and 'bottom'
    else:
        raise Exception('Unable to recognize the frame: ' + str(frame))

    lineup[current_atbat_number] += 1
    # print '--CURRENT ATBAT NUMBER-- ' + str(current_atbat_number)
    # print lineup['previous_away_batter']
    # print lineup['previous_home_batter']
    # print lineup[current_atbat_number]

    # Use this to validate interference edge cases
    if interference:
        lineup[batting_interference_count].append({pitcher: batter})

    # The position ranges from 100 to 900
    if not lineup[previous_batter_position]:
        lineup[previous_batter_position] = 100

    elif lineup[previous_batter_position] == 900:
        lineup[previous_batter_position] = 100
        lineup[recorded_starting_lineup] = True
    else:
        lineup[previous_batter_position] += 100

    position = lineup[previous_batter_position]

    # Keep track of new hitters
    if str(position) not in lineup[pinch_hitter_dictionary]:
        lineup[pinch_hitter_dictionary][str(position)] = batter

    # Keep track of new pitchers
    if pitcher not in lineup[ordered_pitcher_appearances]:
            lineup[ordered_pitcher_appearances].append(pitcher)

    synchronize_lineup_substitutions(batter, position, measured_batter_stats)


def update_pitcher_outs(pitcher, outs, pitcher_hitters_dictionary):
    # print '------------------'
    # print pitcher
    # print outs
    # print '------------------'
    previous_outs_number = int(outs['previous_outs_number'])
    current_outs_number = int(outs['current_outs_number'])
    if previous_outs_number == current_outs_number:
        return

    new_outs_made = current_outs_number - previous_outs_number
    if pitcher in pitcher_hitters_dictionary:
        pitcher_hitters_dictionary[pitcher]['outs'] += new_outs_made
    else:
        pitcher_hitters_dictionary[pitcher] = {'hits': 0, 'homers': 0, 'walks': 0,
                                               'outs': new_outs_made, 'strikeouts': 0,
                                               'batters_faced_number': 0}

    outs['previous_outs_number'] = outs['current_outs_number']


def get_position_by_pinch_id(pinch_hitter_id, hitters_by_position):
    for position, player in hitters_by_position.iteritems():
        if player == pinch_hitter_id:
            return position
    raise Exception('Unable to find position for hitter id: ' + str(pinch_hitter_id))


def save_offensive_substitution(event, lineup, frame, team, date, measured_batter_stats):

    if frame == 'top':
        pinch_hitter_positions = 'away_pinch_hitters'
        previous_batter_position = 'previous_away_batter'

    elif frame == 'bottom':
        pinch_hitter_positions = 'home_pinch_hitters'
        previous_batter_position = 'previous_home_batter'

    # The only frames are 'top' and 'bottom'
    else:
        raise Exception('Unable to recognize the frame: ' + str(frame))

    # Typo edge case
    if 'Dropped foul pop error' in event['des']:
        return

    old_player_name = parse_pinch_hitter(event['des'])
    old_player_id = get_player_id_by_name_and_game(old_player_name, team, date)
    new_player_id = event['player']

    if 'runner' in event['des']:  # Assume pinch runners inherit their replacement's position
        position = get_position_by_pinch_id(old_player_id, lineup[pinch_hitter_positions])
        position = position[0]

    else:
        # Pinch hitters happen right before their atbat
        position = str(lineup[previous_batter_position])
        if position == 'None':
            position = 1  # This is this team's first recorded batter

        else:
            position = int(position[0])
            position += 1
            if position == 10:
                position = 1

    # Update hitters dictionary
    save_lineup_substitution(lineup, str(position), pinch_hitter_positions,
                             old_player_id, new_player_id, measured_batter_stats)


def save_pitching_substitution(event, lineup, frame, team, date, batters, pitchers):
    if frame == 'top':
        pinch_hitter_positions = 'home_pinch_hitters'
        ordered_pitcher_appearances = 'home_pitchers_order'
    elif frame == 'bottom':
        pinch_hitter_positions = 'away_pinch_hitters'
        ordered_pitcher_appearances = 'away_pitchers_order'
    else:
        raise Exception('Unable to recognize the frame: ' + str(frame))

    new_player_position = parse_new_batting_lineup_position(event['des'])

    # This is an American League pitching change
    if not new_player_position:
        update_pitcher_lineup(lineup, ordered_pitcher_appearances,
                              event['des'], team, date, pitchers)
        return

    if 'enters the batting order' in event['des']:
        new_player_id = event['player']
        if new_player_id not in lineup[ordered_pitcher_appearances]:
            lineup[ordered_pitcher_appearances].append(new_player_id)
        old_player_id = None

    else:
        old_player_name = parse_new_batting_lineup_player(event['des'])
        old_player_id = get_player_id_by_name_and_game(old_player_name, team, date)
        new_player_name = parse_pitching_change_new_player(event['des'])
        new_player_id = get_player_id_by_name_and_game(new_player_name, team, date)

        update_pitcher_lineup(lineup, ordered_pitcher_appearances,
                              event['des'], team, date, pitchers)

        player_was_processed = new_player_id in lineup[pinch_hitter_positions].values()
        if new_player_id == old_player_id and player_was_processed:
            return

    # Save changes to the batter hits dictionary
    save_lineup_substitution(lineup, str(new_player_position), pinch_hitter_positions,
                             old_player_id, new_player_id, batters)


def update_pitcher_lineup(lineup, ordered_pitcher_appearances, description, team, date, pitchers):

    if lineup[ordered_pitcher_appearances]:
        new_player_name = parse_pitching_change_new_player(description)
        new_player_id = get_player_id_by_name_and_game(new_player_name, team, date)
        if new_player_id != lineup[ordered_pitcher_appearances][-1]:
            lineup[ordered_pitcher_appearances].append(new_player_id)

    else:
        old_player_name = parse_pitching_change_old_player(description)
        old_player_id = get_player_id_by_name_and_game(old_player_name, team, date)

        if old_player_id not in lineup[ordered_pitcher_appearances]:
            save_pitcher_stats(old_player_id, pitchers)
            lineup[ordered_pitcher_appearances].append(old_player_id)

        new_player_name = parse_pitching_change_new_player(description)

        new_player_id = get_player_id_by_name_and_game(new_player_name, team, date)
        if new_player_id not in lineup[ordered_pitcher_appearances]:
            lineup[ordered_pitcher_appearances].append(new_player_id)


def save_defensive_substitution(event, lineup, frame, team, date, measured_batter_stats):
    if frame == 'top':
        pinch_hitter_positions = 'home_pinch_hitters'
    elif frame == 'bottom':
        pinch_hitter_positions = 'away_pinch_hitters'
    else:
        raise Exception('Unable to recognize the frame: ' + str(frame))

    new_player_position = parse_new_batting_lineup_position(event['des'])
    if not new_player_position:
        return

    if 'remains ' in event['des']:
        new_player_id = event['player']
        old_player_id = None

    else:
        old_player_name = parse_new_batting_lineup_player(event['des'])
        old_player_id = get_player_id_by_name_and_game(old_player_name, team, date)

        new_player_id = event['player']
        if new_player_id == old_player_id:
            return

    # Save changes to the batter hits dictionary
    save_lineup_substitution(lineup, str(new_player_position), pinch_hitter_positions,
                             old_player_id, new_player_id, measured_batter_stats)


def find_most_recent_matching_id(position, pinch_hitters_dictionary):
    position = str(position)
    position = position[0]
    matching_hitter_positions = []
    for current_hitter_position, player_id in pinch_hitters_dictionary.iteritems():
        if current_hitter_position[0] == position:
            matching_hitter_positions.append(int(current_hitter_position))

    if not matching_hitter_positions:
        return None
    newest_hitter_position = str(max(matching_hitter_positions))
    newest_hitter_id = pinch_hitters_dictionary[newest_hitter_position]
    return newest_hitter_id


def save_lineup_substitution(lineup, position, subs, previous_player_id, new_player_id, hits):
    pinch_hitter_dictionary = lineup[subs]
    current_hitter_positions = pinch_hitter_dictionary.keys()

    # Find a match
    matching_hitter_positions = []
    for current_hitter_position in current_hitter_positions:
        if current_hitter_position[0] == position:
            matching_hitter_positions.append(int(current_hitter_position))

    if not matching_hitter_positions:
        previous_position_id = position + '00'
        new_position_id = position + '01'

        assert previous_player_id, 'Refactor this logic'
        lineup[subs][previous_position_id] = previous_player_id
        lineup[subs][new_position_id] = new_player_id

        synchronize_lineup_substitutions(previous_player_id, previous_position_id, hits)
        synchronize_lineup_substitutions(new_player_id, new_position_id, hits)
        return

    newest_hitter_position = max(matching_hitter_positions)
    new_position_id = str(newest_hitter_position + 1)
    # The player shouldn't be able to reenter the lineup

    if new_player_id not in lineup[subs].values():
        lineup[subs][new_position_id] = new_player_id
        synchronize_lineup_substitutions(new_player_id, new_position_id, hits)


def synchronize_lineup_substitutions(batter, position, measured_batter_stats):
    if batter in measured_batter_stats:
        previously_recorded_position = measured_batter_stats[batter].get('batting_lineup_position')
        if not previously_recorded_position:
            measured_batter_stats[batter]['batting_lineup_position'] = position

    else:
        measured_batter_stats[batter] = {'hits': 0, 'homers': 0, 'walks': 0,
                                         'strikeouts': 0, 'atbats': 0,
                                         'batting_lineup_position': position,
                                         'sacrifice_fly_events': 0,
                                         'sacrifice_bunt_events': 0,
                                         'plate_appearances_number': 0}


def save_pitcher_stats(pitcher, measured_pitcher_stats):
    # Only use this for special swapped pitchers
    if pitcher not in measured_pitcher_stats:
        measured_pitcher_stats[pitcher] = {'hits': 0, 'homers': 0, 'walks': 0, 'outs': 0,
                                           'strikeouts': 0, 'batters_faced_number': 0}


def parse_new_batting_lineup_position(description_of_event):
    index = description_of_event.rfind('batting ')
    if index > 0:
        position = description_of_event[index + len('batting ')]
        return position

    return 0


def parse_pinch_hitter(description_of_event):
    index = description_of_event.rfind('replaces ')
    assert index > 0, 'Invalid event description: ' + str(description_of_event)

    player = description_of_event[index + len('replaces '):]
    player = player.strip()
    player = player[:-1]

    return player


def parse_pitching_change_new_player(description_of_event):
    assert 'Pitching Change: ' in description_of_event, \
        'Invalid event description' + str(description_of_event)

    description_of_event = description_of_event[len('Pitching Change: '):]
    index = description_of_event.rfind('replaces ')
    assert index > 0, 'Invalid event description: ' + str(description_of_event)

    return description_of_event[:index]


def parse_pitching_change_old_player(description_of_event):
    assert 'Pitching Change: ' in description_of_event, \
        'Invalid event description' + str(description_of_event)

    description_of_event = description_of_event.strip()
    if description_of_event[-1] == '.':
        description_of_event = description_of_event[:-1]

    if 'replacing ' in description_of_event:
        index = description_of_event.rfind(',')
        description_of_event = description_of_event[:index]

    index = description_of_event.rfind(',')
    if index > 0:
        description_of_event = description_of_event[:index]

    description_of_event = description_of_event[len('Pitching Change: '):]
    index = description_of_event.rfind('replaces ')
    assert index > 0, 'Invalid event description: ' + str(description_of_event)

    return description_of_event[index + len('replaces '):]


def parse_new_batting_lineup_player(description_of_event):
    # Handle edge case
    if 'replacing ' in description_of_event:
        index = description_of_event.rfind('replacing ')
        player = description_of_event[index + len('replacing '):]
        player = player.strip()
        player = player[:-1]

    else:
        index = description_of_event.rfind('replaces ')
        assert index > 0, 'Invalid event description: ' + str(description_of_event)

        player = description_of_event[index + len('replaces '):]
        first_comma_index = player.find(',')
        assert first_comma_index > 0, 'Invalid event description: ' + str(description_of_event)

        player = player[:first_comma_index]

    possible_player_positions = ['pitcher ', 'catcher ', 'first baseman ', 'second baseman ',
                                 'third baseman ', 'shortstop ', 'left fielder ',
                                 'center fielder ', 'right fielder ', 'designated hitter ']

    for position in possible_player_positions:
        if position in player:
            player = player.replace(position, '')

    return player


def validate_lineup_data(expected_game_stats, measured_game_stats, lineup):

    measured_pitcher_stats = measured_game_stats['measured_pitcher_stats']
    measured_batter_stats = measured_game_stats['measured_batter_stats']
    expected_pitcher_stats = expected_game_stats['expected_pitcher_stats']
    expected_batter_stats = expected_game_stats['expected_batter_stats']
    total_plate_appearances = expected_game_stats['total_plate_appearances']

    measured_home_apps = lineup['home_atbat_number']
    adjusted_home_apps = measured_home_apps - len(lineup['home_batting_interference'])
    expected_home_apps = total_plate_appearances['home_plate_appearances']

    assert expected_home_apps == measured_home_apps or expected_home_apps == adjusted_home_apps, \
        str('got ' + str(lineup['home_atbat_number']) + '/' +
            str(total_plate_appearances['home_plate_appearances']) + ' home plate appearances')

    measured_away_apps = lineup['away_atbat_number']
    adjusted_away_apps = measured_away_apps - len(lineup['away_batting_interference'])
    expected_away_apps = total_plate_appearances['away_plate_appearances']

    assert expected_away_apps == measured_away_apps or expected_away_apps == adjusted_away_apps, \
        str('got ' + str(lineup['away_atbat_number']) + '/' +
            str(total_plate_appearances['away_plate_appearances']) + ' away plate appearances')

    interference_by_pitcher = {}
    for batter_by_pitcher in lineup['home_batting_interference']:
        id_of_pitcher = batter_by_pitcher.keys()[0]
        if id_of_pitcher not in interference_by_pitcher:
            interference_by_pitcher[id_of_pitcher] = 1
        else:
            interference_by_pitcher[id_of_pitcher] += 1

    for batter_by_pitcher in lineup['away_batting_interference']:
        id_of_pitcher = batter_by_pitcher.keys()[0]
        # Sometimes mlb doesn't count these plate appearances
        if id_of_pitcher not in interference_by_pitcher:
            interference_by_pitcher[id_of_pitcher] = 1
        else:
            interference_by_pitcher[id_of_pitcher] += 1

    # Rain shortened game or a rescheduled game
    if not lineup['previous_home_batter'] or not lineup['previous_away_batter']:
        # return 'game was rescheduled?'
        return
    if not lineup['recorded_home_starters'] or not lineup['recorded_away_starters']:
        # return 'rain shortened game?'
        return

    all_expected_appearances = measured_home_apps + measured_away_apps
    all_measured_appearances = 0
    for batter in expected_batter_stats:

        expected_batter_hits = int(expected_batter_stats[batter]['hits'])
        expected_batter_homers = int(expected_batter_stats[batter]['homers'])
        expected_batter_walks = int(expected_batter_stats[batter]['walks'])
        expected_batter_strikeouts = int(expected_batter_stats[batter]['strikeouts'])
        expected_batter_atbats = int(expected_batter_stats[batter]['atbats'])
        expected_batter_position = int(expected_batter_stats[batter]['batting_lineup_position'])
        expected_batter_sacrifices = int(expected_batter_stats[batter]['sacrifices'])

        measured_batter_data = measured_batter_stats.get(batter)

        measured_batter_hits = 0
        if measured_batter_data:
            measured_batter_hits = int(measured_batter_data.get('hits', 0))

        measured_batter_homers = 0
        if measured_batter_data:
            measured_batter_homers = int(measured_batter_data.get('homers', 0))

        measured_batter_walks = 0
        if measured_batter_data:
            measured_batter_walks = int(measured_batter_data.get('walks', 0))

        measured_batter_strikeouts = 0
        if measured_batter_data:
            measured_batter_strikeouts = int(measured_batter_data.get('strikeouts', 0))

        # measured_sacrifice_flies = 0
        # if measured_batter_data:
        #     measured_sacrifice_flies = int(measured_batter_data.get('sacrifice_fly_events', 0))

        measured_sacrifice_bunts = 0
        if measured_batter_data:
            measured_sacrifice_bunts = int(measured_batter_data.get('sacrifice_bunt_events', 0))

        measured_batter_atbats = 0
        if measured_batter_data:
            measured_batter_atbats = int(measured_batter_data.get('atbats', 0))

        measured_batter_position = 0
        if measured_batter_data:
            measured_batter_position = int(measured_batter_data.get('batting_lineup_position', 0))

        measured_plate_apps = 0
        if measured_batter_data:
            measured_plate_apps = int(measured_batter_data.get('plate_appearances_number', 0))

        assert measured_batter_hits == expected_batter_hits, \
            str(str(batter) + ' has ' + str(measured_batter_stats) + '/' +
                str(expected_batter_hits) + ' hits')

        assert measured_batter_homers == expected_batter_homers, \
            str(str(batter) + ' has ' + str(measured_batter_homers) + '/' +
                str(expected_batter_homers) + ' homers')

        assert measured_batter_walks == expected_batter_walks, \
            str(str(batter) + ' has ' + str(measured_batter_walks) + '/' +
                str(expected_batter_walks) + ' walks')

        assert measured_sacrifice_bunts == expected_batter_sacrifices, \
            str(str(batter) + ' has ' + str(measured_sacrifice_bunts) +
                '/' + str(expected_batter_sacrifices) + ' sacrifices')

        assert measured_batter_strikeouts == expected_batter_strikeouts, \
            str(str(batter) + ' has ' + str(measured_batter_strikeouts) + '/' +
                str(expected_batter_strikeouts) + ' strikeouts')

        assert measured_batter_atbats == expected_batter_atbats, \
            str(str(batter) + ' has ' + str(measured_batter_atbats) + '/' +
                str(expected_batter_atbats) + ' atbats')

        assert measured_batter_position == expected_batter_position, \
            str(str(batter) + ' has ' + str(measured_batter_position) + '/' +
                str(expected_batter_position) + ' position')

        all_measured_appearances += measured_plate_apps

    assert all_measured_appearances == all_expected_appearances, \
        str('got ' + str(all_measured_appearances) + '/' +
            str(all_expected_appearances) + ' plate appearances')

    for pitcher in expected_pitcher_stats:
        expected_pitcher_hits = int(expected_pitcher_stats[pitcher]['hits'])
        expected_pitcher_homers = int(expected_pitcher_stats[pitcher]['homers'])
        expected_pitcher_walks = int(expected_pitcher_stats[pitcher]['walks'])
        expected_pitcher_strikeouts = int(expected_pitcher_stats[pitcher]['strikeouts'])
        expected_pitcher_outs = int(expected_pitcher_stats[pitcher]['outs'])
        expected_batters_faced = int(expected_pitcher_stats[pitcher]['batters_faced_number'])

        measured_pitcher_data = measured_pitcher_stats.get(pitcher)

        measured_pitcher_hits = 0
        if measured_pitcher_data:
            measured_pitcher_hits = int(measured_pitcher_data.get('hits', 0))

        measured_pitcher_homers = 0
        if measured_pitcher_data:
            measured_pitcher_homers = int(measured_pitcher_data.get('homers', 0))

        measured_pitcher_walks = 0
        if measured_pitcher_data:
            measured_pitcher_walks = int(measured_pitcher_data.get('walks', 0))

        measured_pitcher_strikeouts = 0
        if measured_pitcher_data:
            measured_pitcher_strikeouts = int(measured_pitcher_data.get('strikeouts', 0))

        measured_pitcher_outs = 0
        if measured_pitcher_data:
            measured_pitcher_outs = int(measured_pitcher_data.get('outs', 0))

        measured_batters_faced = 0
        if measured_pitcher_data:
            measured_batters_faced = int(measured_pitcher_data.get('batters_faced_number', 0))

        # Still note interference as a plate appearance
        measured_interference_events = interference_by_pitcher.get(pitcher, 0)
        adjusted_batters_faced = measured_batters_faced - measured_interference_events
        batters_faced_matches = measured_batters_faced == expected_batters_faced
        matches_without_interference = adjusted_batters_faced == expected_batters_faced

        assert measured_pitcher_hits == expected_pitcher_hits, \
            str(str(pitcher) + ' has ' + str(measured_pitcher_hits) + '/' +
                str(expected_pitcher_hits) + ' hits')

        assert measured_pitcher_homers == expected_pitcher_homers, \
            str(str(pitcher) + ' has ' + str(measured_pitcher_homers) + '/' +
                str(expected_pitcher_homers) + ' homers')

        assert measured_pitcher_walks == expected_pitcher_walks, \
            str(str(pitcher) + ' has ' + str(measured_pitcher_walks) + '/' +
                str(expected_pitcher_walks) + ' walks')

        assert measured_pitcher_strikeouts == expected_pitcher_strikeouts, \
            str(str(pitcher) + ' has ' + str(measured_pitcher_strikeouts) + '/' +
                str(expected_pitcher_strikeouts) + ' strikeouts')

        assert measured_pitcher_outs == expected_pitcher_outs, \
            str(str(pitcher) + ' has ' + str(measured_pitcher_outs) + '/' +
                str(expected_pitcher_outs) + ' outs')

        assert batters_faced_matches or matches_without_interference, \
            str(str(pitcher) + ' has ' + str(measured_batters_faced) + '/' +
                str(expected_batters_faced) + ' batters faced')

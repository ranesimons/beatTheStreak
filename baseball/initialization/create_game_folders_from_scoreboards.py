import os
from datetime import datetime
from bs4 import BeautifulSoup

from baseball.utility.useful_utility_functions import is_valid_year
from baseball.utility.useful_utility_functions import is_valid_day_in_month
from baseball.utility.useful_utility_functions import get_first_and_last_game_of_year
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import get_default_start_and_end_of_month
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR


def get_scoreboard_file(year, month, day):
    is_valid_year(year)
    is_valid_day_in_month(month, day)

    base_file_name = 'game_mlb_year_'
    base_file_name += str(year) + '_month_'
    base_file_name += convert_number_to_string(month) + '_day_'
    base_file_name += convert_number_to_string(day) + '_scoreboard.xml'
    return base_file_name


def create_folders_from_xml_scoreboard(year, month, day):
    base_file_name = get_scoreboard_file(year, month, day)
    # Assume we're already in the right directory

    tree = BeautifulSoup(open(base_file_name), 'lxml')
    for game in tree.find_all('game'):
        # Create game folder
        game_dir_path = str(os.getcwd()) + '/gid_' + str(game['id'])
        if game['status'] != 'FINAL':
            print str(os.getcwd())
            print game_dir_path
            print game['status']

        if not os.path.exists(game_dir_path):
            os.makedirs(game_dir_path)


def create_game_directories_since_date(target_start_day, target_start_month, year):
    game_date_info = get_first_and_last_game_of_year(year)
    today = datetime.now().day
    month_of_today = datetime.now().month
    year_of_today = datetime.now().year

    start_day = game_date_info['start_day']
    start_month = game_date_info['start_month']
    end_day = game_date_info['end_day']
    end_month = game_date_info['end_month']
    all_star_day = game_date_info['all_star_day']

    assert year_of_today == year, 'the year must be the current year: ' + str(year)
    print '-'
    print month_of_today
    print end_month
    print '-'
    if month_of_today < end_month:
        end_month = month_of_today
        end_day = today
    elif month_of_today == end_month:
        if today < end_day:
            end_day = today

    print end_day

    os.chdir('data')
    os.chdir(str(year))
    first_month = True

    if target_start_month >= start_month:
        start_month = target_start_month
        if target_start_day >= start_day:
            start_day = target_start_day
    for month in range(start_month, end_month):

        if first_month:
            create_month_of_game_directories(year, month, start_day, 0, 0)
            first_month = False
        elif month == 7:
            create_month_of_game_directories(year, month, 0, 0, all_star_day)
        else:
            create_month_of_game_directories(year, month, 0, 0, 0)

    create_month_of_game_directories(year, end_month, 0, end_day, 0)  # Create last month
    os.chdir('..')
    os.chdir('..')
    pass


def create_year_of_game_directories(year):
    is_valid_year(year)
    game_date_info = get_first_and_last_game_of_year(year)

    start_day = game_date_info['start_day']
    start_month = game_date_info['start_month']
    end_day = game_date_info['end_day']
    end_month = game_date_info['end_month']
    all_star_day = game_date_info['all_star_day']

    os.chdir('data')
    os.chdir(str(year))
    first_month = True

    for month in range(start_month, end_month):

        if first_month:
            create_month_of_game_directories(year, month, start_day, 0, 0)
            first_month = False
        elif month == 7:
            create_month_of_game_directories(year, month, 0, 0, all_star_day)
        else:
            create_month_of_game_directories(year, month, 0, 0, 0)

    create_month_of_game_directories(year, end_month, 0, end_day, 0)  # Create last month
    os.chdir('..')
    os.chdir('..')


def create_month_of_game_directories(year, month, start_day, end_day, all_star_day):

    start_and_end = get_default_start_and_end_of_month(month)
    if not start_day:
        start_day = start_and_end['start']
    if not end_day:
        end_day = start_and_end['end']

    month_as_string = convert_month_int_to_string(month)
    os.chdir(month_as_string)
    # print os.getcwd()

    for day in range(start_day, end_day + 1):
        if month == 7 and day in range(all_star_day - 1, all_star_day + 3):
            continue  # skip the all star break

        os.chdir(convert_number_to_string(day))
        # print os.getcwd()
        create_folders_from_xml_scoreboard(year, month, day)

        os.chdir('..')

    os.chdir('..')


if __name__ == '__main__':
    # for this_year in range(LAST_ACCEPTED_YEAR, LAST_ACCEPTED_YEAR + 1):
    #     create_year_of_game_directories(this_year)

    create_game_directories_since_date(12, 5, 2017)

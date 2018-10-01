import os

from baseball.utility.useful_utility_functions import get_first_and_last_game_of_year
from baseball.utility.useful_utility_functions import is_valid_year
from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import get_default_start_and_end_of_month
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR


def create_year_of_data_directories(year):
    is_valid_year(year)
    game_date_info = get_first_and_last_game_of_year(year)

    start_day = game_date_info['start_day']
    start_month = game_date_info['start_month']
    end_day = game_date_info['end_day']
    end_month = game_date_info['end_month']
    all_star_day = game_date_info['all_star_day']

    os.chdir('data')
    year_dir_path = str(os.getcwd()) + '/' + str(year)

    print year_dir_path

    if not os.path.exists(year_dir_path):
        os.makedirs(year_dir_path)

    os.chdir(str(year))

    month_dir_path = str(os.getcwd()) + '/' + str(convert_month_int_to_string(start_month))
    print month_dir_path

    first_month = True
    for month in range(start_month, end_month):
        month_as_string = convert_month_int_to_string(month)
        month_dir_path = str(os.getcwd()) + '/' + month_as_string
        if not os.path.exists(month_dir_path):
            os.makedirs(month_dir_path)

        if first_month:
            create_month_of_data_directories(month, start_day, 0, 0)
            first_month = False
        elif month == 7:
            create_month_of_data_directories(month, 0, 0, all_star_day)
        else:
            create_month_of_data_directories(month, 0, 0, 0)

    # Create last month
    month_as_string = convert_month_int_to_string(end_month)
    month_dir_path = str(os.getcwd()) + '/' + month_as_string
    if not os.path.exists(month_dir_path):
        os.makedirs(month_dir_path)

    create_month_of_data_directories(end_month, 0, end_day, 0)
    os.chdir('..')
    os.chdir('..')


def create_month_of_data_directories(month, start_day, end_day, all_star_day):
    start_and_end = get_default_start_and_end_of_month(month)
    if not start_day:
        start_day = start_and_end['start']
    if not end_day:
        end_day = start_and_end['end']

    month_as_string = convert_month_int_to_string(month)
    os.chdir(month_as_string)
    print os.getcwd()

    for day in range(start_day, end_day + 1):
        # skip the all star break
        if month == 7 and day in range(all_star_day - 1, all_star_day + 3):
            continue
        day_dir_path = str(os.getcwd()) + '/' + convert_number_to_string(day)
        if not os.path.exists(day_dir_path):
            os.makedirs(day_dir_path)

    os.chdir('..')


if __name__ == '__main__':
    for this_year in range(LAST_ACCEPTED_YEAR, LAST_ACCEPTED_YEAR + 1):
        create_year_of_data_directories(this_year)

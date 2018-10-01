from datetime import datetime
FIRST_ACCEPTED_YEAR = 2013
LAST_ACCEPTED_YEAR = 2017


def convert_scoreboard_directory_to_date(base_scoreboard_directory):
    directory = base_scoreboard_directory[:-1]
    day = directory[-2:]

    directory = directory[:-3]
    month_slash_index = directory.rfind('/')
    month = directory[month_slash_index + 1: month_slash_index + 3]

    directory = directory[:month_slash_index]
    year = directory[-4:]
    return {'day': int(day), 'month': int(month), 'year': int(year)}


def extract_date_directory(base_scoreboard_directory):
    date = convert_scoreboard_directory_to_date(base_scoreboard_directory)
    day = date['day']
    month = date['month']
    year = date['year']

    directory = str(year) + '/' + convert_month_int_to_string(month)
    directory += '/' + convert_number_to_string(day) + '/'
    return directory


def get_earliest_possible_date_directory():
    year = FIRST_ACCEPTED_YEAR
    year_game_data = get_first_and_last_game_of_year(year)
    day = year_game_data['start_day']
    month = year_game_data['start_month']

    directory = str(year) + '/' + convert_month_int_to_string(month)
    directory += '/' + convert_number_to_string(day) + '/'
    return directory


def convert_month_int_to_string(month):
    if month == 3:
        return '03_March'
    elif month == 4:
        return '04_April'
    elif month == 5:
        return '05_May'
    elif month == 6:
        return '06_June'
    elif month == 7:
        return '07_July'
    elif month == 8:
        return '08_August'
    elif month == 9:
        return '09_September'
    elif month == 10:
        return '10_October'
    else:
        raise Exception('Invalid month integer: ' + str(month))


def get_default_start_and_end_of_month(month):
    if month == 3:
        return {'start': 1, 'end': 31}
    elif month == 4:
        return {'start': 1, 'end': 30}
    elif month == 5:
        return {'start': 1, 'end': 31}
    elif month == 6:
        return {'start': 1, 'end': 30}
    elif month == 7:
        return {'start': 1, 'end': 31}
    elif month == 8:
        return {'start': 1, 'end': 31}
    elif month == 9:
        return {'start': 1, 'end': 30}
    elif month == 10:
        return {'start': 1, 'end': 31}
    else:
        raise Exception('Invalid month integer: ' + str(month))


def convert_number_to_string(number):
    if 0 <= number < 10:
        string = '0' + str(number)
        return string
    return str(number)


def is_valid_year(year):
    assert FIRST_ACCEPTED_YEAR <= year <= LAST_ACCEPTED_YEAR, \
        'This given year is not currently accepted: ' + str(year)


def is_valid_day_in_month(month, day):
    assert 3 <= month <= 10, 'This given month is not currently accepted: ' + str(month)
    # The day must exist in the month
    if month in [3, 5, 7, 8, 10]:
        assert 1 <= day <= 31, 'Day ' + str(day) + 'does not exist in this month: ' + str(month)
    if month in [4, 6, 9]:
        assert 1 <= day <= 30, 'Day ' + str(day) + 'does not exist in this month: ' + str(month)


def get_first_and_last_game_of_year(year):
    if year == 2013:
        start_day = 31
        start_month = 3
        end_day = 30
        end_month = 9
        all_star_day = 16

    elif year == 2014:
        start_day = 31
        start_month = 3
        end_day = 28
        end_month = 9
        all_star_day = 15

    elif year == 2015:
        start_day = 5
        start_month = 4
        end_day = 4
        end_month = 10
        all_star_day = 14

    elif year == 2016:
        start_day = 4
        start_month = 4
        end_day = 2
        end_month = 10
        all_star_day = 12

    elif year == 2017:
        start_day = 2
        start_month = 4
        end_day = 1
        end_month = 10
        all_star_day = 11

    else:
        raise Exception('Invalid year: ' + str(year))

    return dict(start_day=start_day, start_month=start_month, end_day=end_day,
                end_month=end_month, all_star_day=all_star_day)


def date_directories_are_the_same(first_date_directory, second_date_directory):
    first_date_data = convert_scoreboard_directory_to_date(first_date_directory)
    second_date_data = convert_scoreboard_directory_to_date(second_date_directory)

    if these_dates_are_the_same(first_date_data, second_date_data):
        return True
    return False


def first_directory_is_earlier_or_the_same(first_date_directory, second_date_directory):
    first_date_data = convert_scoreboard_directory_to_date(first_date_directory)
    second_date_data = convert_scoreboard_directory_to_date(second_date_directory)

    if these_dates_are_the_same(first_date_data, second_date_data):
        return True
    return the_first_date_is_earlier(first_date_data, second_date_data)


def first_date_directory_is_earlier(first_date_directory, second_date_directory):
    first_date_data = convert_scoreboard_directory_to_date(first_date_directory)
    second_date_data = convert_scoreboard_directory_to_date(second_date_directory)

    if these_dates_are_the_same(first_date_data, second_date_data):
        return False
    return the_first_date_is_earlier(first_date_data, second_date_data)


def the_first_date_is_earlier(first_given_date, second_given_date):
    # Return True if the first comes before the second; otherwise return False
    first_given_day = first_given_date['day']
    first_given_month = first_given_date['month']
    first_given_year = first_given_date['year']

    second_given_day = second_given_date['day']
    second_given_month = second_given_date['month']
    second_given_year = second_given_date['year']

    # Continue if the years are the same
    if first_given_year < second_given_year:
        return True
    if first_given_year > second_given_year:
        return False

    # Continue if the months are the same
    if first_given_month < second_given_month:
        return True
    if first_given_month > second_given_month:
        return False

    # Continue if the days are the same
    if first_given_day < second_given_day:
        return True
    if first_given_day > second_given_day:
        return False
    # Dates are the same should be called first to prevent this case
    return False


def these_dates_are_the_same(first_given_date, second_given_date):
    # Return True if and only if the two dates are the same
    first_given_day = first_given_date['day']
    first_given_month = first_given_date['month']
    first_given_year = first_given_date['year']

    second_given_day = second_given_date['day']
    second_given_month = second_given_date['month']
    second_given_year = second_given_date['year']

    if first_given_year != second_given_year:
        return False
    if first_given_month != second_given_month:
        return False
    if first_given_day != second_given_day:
        return False
    return True


def is_summer_month(base_scoreboard_directory):
    date = convert_scoreboard_directory_to_date(base_scoreboard_directory)
    month = date['month']

    if 5 < month < 9:
        return True
    return False

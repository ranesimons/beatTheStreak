from datetime import datetime
import urllib
import os

from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import is_valid_year
from baseball.utility.useful_utility_functions import get_first_and_last_game_of_year
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import is_valid_day_in_month
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR


def get_scoreboard_urls_for_days(first_day, last_day, year, month):
    url_by_day = {}
    # get urls from first day to last day inclusive

    for day in range(first_day, last_day + 1):
        url = get_base_url(year, month, day)
        url_by_day[day] = url
    return url_by_day


def get_scoreboard_urls_for_month(start_day, end_day, all_star_day, year, month, start, end):
    # July ==> all star game
    if month == 7:
        if start and end:
            url_by_day = get_scoreboard_urls_for_days(start_day, all_star_day - 2, year, 7)
            after_break_urls = get_scoreboard_urls_for_days(all_star_day + 3, end_day, year, 7)
            url_by_day.update(after_break_urls)
            return url_by_day

        elif start:
            url_by_day = get_scoreboard_urls_for_days(start_day, all_star_day - 2, year, 7)
            after_break_urls = get_scoreboard_urls_for_days(all_star_day + 3, 31, year, 7)
            url_by_day.update(after_break_urls)
            return url_by_day

        elif end:
            url_by_day = get_scoreboard_urls_for_days(1, all_star_day - 2, year, 7)
            after_break_urls = get_scoreboard_urls_for_days(all_star_day + 3, end_day, year, 7)
            url_by_day.update(after_break_urls)
            return url_by_day

        else:
            url_by_day = get_scoreboard_urls_for_days(1, all_star_day - 2, year, 7)
            after_break_urls = get_scoreboard_urls_for_days(all_star_day + 3, 31, year, 7)
            url_by_day.update(after_break_urls)
            return url_by_day

    elif month in [3, 5, 8, 10]:  # 1 <= day <= 31

        if start and end:
            url_by_day = get_scoreboard_urls_for_days(start_day, end_day, year, month)
            return url_by_day

        elif start:
            url_by_day = get_scoreboard_urls_for_days(start_day, 31, year, month)
            return url_by_day

        elif end:
            url_by_day = get_scoreboard_urls_for_days(1, end_day, year, month)
            return url_by_day

        else:
            url_by_day = get_scoreboard_urls_for_days(1, 31, year, month)
            return url_by_day

    elif month in [4, 6, 9]:  # 1 <= day <= 30

        if start and end:
            url_by_day = get_scoreboard_urls_for_days(start_day, end_day, year, month)
            return url_by_day

        elif start:
            url_by_day = get_scoreboard_urls_for_days(start_day, 30, year, month)
            return url_by_day

        elif end:
            url_by_day = get_scoreboard_urls_for_days(1, end_day, year, month)
            return url_by_day

        else:
            url_by_day = get_scoreboard_urls_for_days(1, 30, year, month)
            return url_by_day


def get_games_since_given_date(target_start_day, target_start_month, year):
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

    if target_start_month >= start_month:
        start_month = target_start_month
        if target_start_day >= start_day:
            start_day = target_start_day
    return get_scoreboard_urls_from_dates(start_day, start_month, end_day,
                                          end_month, all_star_day, year)


def get_scoreboard_urls_from_dates(start_day, start_month, end_day, end_month, all_star_day, year):
    days_by_month = {}
    print start_day
    print start_month
    print end_day
    print end_month
    # start month until end month inclusive

    for month in range(start_month, end_month + 1):

        if month == start_month and month == end_month:
            urls_by_day = get_scoreboard_urls_for_month(start_day, end_day, all_star_day,
                                                        year, month, True, True)

        elif month == start_month:
            urls_by_day = get_scoreboard_urls_for_month(start_day, end_day, all_star_day,
                                                        year, month, True, False)

        elif month == end_month:
            urls_by_day = get_scoreboard_urls_for_month(start_day, end_day, all_star_day,
                                                        year, month, False, True)

        else:
            urls_by_day = get_scoreboard_urls_for_month(start_day, end_day, all_star_day,
                                                        year, month, False, False)
        days_by_month[month] = urls_by_day
    return days_by_month


def get_games_by_date(year):
    is_valid_year(year)
    game_date_info = get_first_and_last_game_of_year(year)

    start_day = game_date_info['start_day']
    start_month = game_date_info['start_month']
    end_day = game_date_info['end_day']
    end_month = game_date_info['end_month']
    all_star_day = game_date_info['all_star_day']
    return get_scoreboard_urls_from_dates(start_day, start_month, end_day,
                                          end_month, all_star_day, year)


def get_base_url(year, month, day):
    is_valid_year(year)
    is_valid_day_in_month(month, day)

    base_url = 'http://gd2.mlb.com/components/game/mlb/'
    base_url = base_url + 'year_' + str(year) + '/'
    base_url = base_url + 'month_' + convert_number_to_string(month) + '/'
    base_url = base_url + 'day_' + convert_number_to_string(day) + '/'
    return base_url


def print_url_dictionary(url_dictionary):

    for year in sorted(url_dictionary.keys()):
        item = url_dictionary[year]
        print 'year: ' + str(year)

        for month, item2 in item.iteritems():
            print 'month: ' + str(month)
            for day, url in item2.iteritems():
                print 'day: ' + str(day)
                print url


def download_scoreboards(url_dictionary):
    for year, item in url_dictionary.iteritems():
        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                download_scoreboard(url, year, month, day)


def download_scoreboard(url, year, month, day):
    scoreboard_url = url + 'scoreboard.xml'
    testfile = urllib.URLopener()
    file_name = scoreboard_url[30:].replace('/', '_')
    print file_name

    month_as_string = convert_month_int_to_string(month)
    directory = str(str(os.getcwd()) + '/data/' + str(year) + '/' +
                    month_as_string + '/' + convert_number_to_string(day) + '/')

    print scoreboard_url
    print directory
    testfile.retrieve(scoreboard_url, directory + str(file_name))


def generate_urls_from_date_until_now(month, day, year):
    today = datetime.now().day
    month_of_today = datetime.now().month
    year_of_today = datetime.now().year
    print today
    print month_of_today
    print year_of_today

    # The given date must be occur acceptably
    # Only accept the current year for now
    if year < FIRST_ACCEPTED_YEAR:
        return {}
    if year_of_today < year:
        return {}
    if year_of_today > year:
        return {}
    elif month_of_today < month:
        return {}
    elif today < day:
        return {}

    if year < year_of_today:
        gap_years_number = year_of_today - year
        new_url_dictionary = {}
        for this_year in range(year, year_of_today):
            these_days_by_month = get_games_by_date(this_year)
            # print these_days_by_month
            new_url_dictionary[this_year] = these_days_by_month
        print gap_years_number
        # print new_url_dictionary
    else:
        new_url_dictionary = {}
        these_days_by_month = get_games_since_given_date(day, month, year)
        print these_days_by_month
        print 'cool'
        pass
    pass
    print 'good'
    return new_url_dictionary


if __name__ == '__main__':

    # Create a dict of all relevant scoreboard urls
    # this_url_dictionary = {}
    # for this_year in range(LAST_ACCEPTED_YEAR, LAST_ACCEPTED_YEAR + 1):
    #     these_days_by_month = get_games_by_date(this_year)
    #     this_url_dictionary[this_year] = these_days_by_month
    #
    # print this_url_dictionary
    #
    # download_scoreboards(this_url_dictionary)
    this_url_dictionary = generate_urls_from_date_until_now(3, 12, 2017)
    print this_url_dictionary

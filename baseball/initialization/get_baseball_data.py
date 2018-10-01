import urllib
import os
from datetime import datetime

from bs4 import BeautifulSoup

from baseball.utility.useful_utility_functions import convert_month_int_to_string
from baseball.utility.useful_utility_functions import convert_number_to_string
from baseball.utility.useful_utility_functions import FIRST_ACCEPTED_YEAR
from baseball.utility.useful_utility_functions import LAST_ACCEPTED_YEAR
from baseball.initialization.scrape_xml_scoreboards import get_games_by_date
from baseball.initialization.scrape_xml_scoreboards import get_games_since_given_date
from baseball.initialization.create_game_folders_from_scoreboards import get_scoreboard_file

from baseball.initialization.scrape_xml_scoreboards import generate_urls_from_date_until_now


def download_all_data(url_dictionary):
    for year, item in url_dictionary.iteritems():
        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                download_game_data_for_today(url, year, month, day)


def download_boxscore_only(url_dictionary):
    for year, item in url_dictionary.iteritems():
        for month, item2 in item.iteritems():
            for day, url in item2.iteritems():
                download_game_data_for_today(url, year, month, day)


def download_game_data_for_today(url, year, month, day):
    base_file_name = get_scoreboard_file(year, month, day)
    base_scoreboard_directory = str(str(os.getcwd()) + '/data/' + str(year) + '/' +
                                    convert_month_int_to_string(month) + '/' +
                                    convert_number_to_string(day) + '/')

    print base_scoreboard_directory

    tree = BeautifulSoup(open(base_scoreboard_directory + base_file_name), 'lxml')
    for game in tree.find_all('game'):
        game_dir_path = base_scoreboard_directory + 'gid_' + str(game['id']) + '/'

        line_score_url = url + 'gid_' + str(game['id']) + '/linescore.xml'
        players_file_url = url + 'gid_' + str(game['id']) + '/players.xml'
        game_events_url = url + 'gid_' + str(game['id']) + '/game_events.xml'
        box_score_url = url + 'gid_' + str(game['id']) + '/boxscore.xml'

        print game_dir_path

        # print line_score_url
        # print players_file_url
        # print game_events_url
        print box_score_url
        retrieve_data_file(line_score_url, game_dir_path + 'linescore.xml')
        retrieve_data_file(players_file_url, game_dir_path + 'players.xml')
        retrieve_data_file(game_events_url, game_dir_path + 'game_events.xml')
        retrieve_data_file(box_score_url, game_dir_path + 'boxscore.xml')


def retrieve_data_file(file_path_url, game_dir_path):

    testfile = urllib.URLopener()
    try:
        testfile.retrieve(file_path_url, game_dir_path)
    except IOError as error:
        print 'Unable to retrieve: ' + str(file_path_url) + ' -- ' + str(error)


if __name__ == '__main__':

    # Create a dict of all relevant scoreboard urls
    # this_url_dictionary = {}
    # for this_year in range(LAST_ACCEPTED_YEAR, LAST_ACCEPTED_YEAR + 1):
    #     these_days_by_month = get_games_by_date(this_year)
    #     this_url_dictionary[this_year] = these_days_by_month
    this_url_dictionary = generate_urls_from_date_until_now(3, 12, 2017)
    print this_url_dictionary
    # download_all_data(this_url_dictionary)

from __future__ import print_function
import mlbgame

month = mlbgame.games(2015, 6, home="Mets")
games = mlbgame.combine_games(month)
for game in games:
    print(game)

print('---------------------')

day = mlbgame.day(2015, 4, 12, home="Royals", away="Royals")
game = day[0]
output = "Winning pitcher: %s (%s) - Losing Pitcher: %s (%s)"
print(output % (game.w_pitcher, game.w_team, game.l_pitcher, game.l_team))

print('---------------------')

game = mlbgame.day(2015, 11, 1, home="Mets")[0]
stats = mlbgame.player_stats(game.game_id)
for stat in stats:
    print('---------------------')
    print(stat)
    for test in stats[stat]:
        print(test)
    print('---------------------')
# for player in stats['home_batting']:
#     print(player)

# game = mlbgame.day(2015, 11, 1, home="Mets")[0]
# events = mlbgame.game_events(game.game_id)
# testing = sorted(map(int, events.keys()))
# print(events.keys())
# print(testing)
# for event in testing:
#     print('---------------------')
#     print(event)
#
#     print('-------TOP--------------')
#     for test2 in events[str(event)]['top']:
#         print(test2)
#
#     print('-------BOTTOM--------------')
#     for test2 in events[str(event)]['bottom']:
#         print(test2)

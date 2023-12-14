from functools import reduce
import re

games = {}

balls_available = {'red': 12, 'green': 13, 'blue': 14}

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input2.txt') as f:

    lines = f.readlines()

    for line in lines:
        game, game_data = line.split(': ')

        # get the game number
        game_num = int(game[4:])

        # break game data up into 'sets'
        grab_texts = game_data.split('; ')
        grabs = []
        for grab_text in grab_texts:
            grab = {}

            # break 'set' up into the balls in each one
            balls = grab_text.split(', ')
            for ball in balls:
                num, colour = ball.split(' ')
                grab[colour.strip()] = int(num)

            grabs.append(grab)

        games[game_num]=grabs

    #print(games)

    total = 0
    for game_id, game_data in games.items():
        maxes = {'red': 0, 'green': 0, 'blue': 0}
        for grab in game_data:
            for ball_colour, ball_count in grab.items():
                if ball_count > maxes[ball_colour]:
                    maxes[ball_colour] = ball_count
                    
        score = maxes['red'] * maxes['green'] * maxes['blue']
        total += score

        #print(game_id, score)        
        
    print(total)
                    

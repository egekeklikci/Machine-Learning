# EGE KEKLIKCI Blind mouse chasing the cheese project

import random
import numpy as np

# prints the status of the game
def print_game_state(game, n):
    for i in range(n):
        for j in range(n):
            if game[i*n+j] == 1:
                print("mouse", end=' ')
            elif game[i*n+j] == 2:
                print("cheese", end='     ')
            else:
                print(game[i*n+j], end='     ')
        print()

# initializes new game
def init_game(n):
    game = []
    for i in range(n * n):
        game.append(0)
    game[n * n - 1] = 2
    return game

# initializes new qtable
def init_qtable(n):
    qtable = []
    for i in range(n * n):
        qtable.append([0, 0, 0, 0])
    qtable[n * n - 1][3] = 100
    return qtable

# move the mouse in the corresponding position
def move(game, way, n, position):
    if way == 0:
        # go left
        if position % n == 0:
            return game
        new_position = position-1
        game[position] = 0
        game[new_position] = 1
    elif way == 1:
        # go up
        if position < n:
            return game
        new_position = position-n
        game[position] = 0
        game[new_position] = 1
    elif way == 2:
        # go right
        if position % n == n-1:
            return game
        new_position = position+1
        game[position] = 0
        game[new_position] = 1
    elif way == 3:
        # go down
        if n*(n-1) <= position < n*n:
            return game
        new_position = position+n
        game[position] = 0
        game[new_position] = 1
    return game

# find the mouse's position in the grid
def find_place(game):
    position = 0
    while position < len(game):
        if game[position] == 1:
            return position
        position += 1
    return -1

# check if the mouse ate the cheese
def is_won(game, n):
    if game[n*n-1] == 1:
        return True
    return False


def calculate_pos(pos, direction, n):
    if direction == 0:
        if pos % n == 0:
            return pos
        return pos - 1
    if direction == 1:
        if pos < n:
            return pos
        return pos - n
    if direction == 2:
        if pos % n == n-1:
            return pos
        return pos + 1
    if direction == 3:
        if n*(n-1) <= pos < n*n:
            return pos
        return pos + n


if __name__ == "__main__":
    """qtable looks like this:
    qtable = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0], 
                 [0, 0, 0, 0], 
                 [0, 0, 0, 100]]"""
    # get size of the grid from the user
    n = int(input("Size of the grid: "))
    qtable = init_qtable(n)
    empty_game = init_game(n)

    # define the variables
    epsilon = 0.3
    eps_reduce_factor = 0.001
    alpha = 0.3
    gamma = 0.9
    max_iteration = 100000
    # do max_iteration times in order to learn
    for _ in range(max_iteration):
        # reduce the epsilon every 1000 episodes by eps_reduce_factor
        if _ % 1000 == 0:
            if _ % 5000 == 0:
                print('Episode: ' + str(_))
            epsilon -= eps_reduce_factor
        # copy new game
        game = empty_game.copy()
        counter = 0
        # start the game
        random_choice = random.choice(np.arange(0, n - 1))
        game[random_choice] = 1
        first_position = random_choice
        if is_won(game, n):
            continue
        while counter < 10000:
            # stopping condition
            counter += 1
            # if there is no previous data or random
            if sum(qtable[random_choice]) == 0 or random.random() < epsilon:
                # try random things
                random_choice = random.choice([0, 1, 2, 3])
                # move
                game = move(game, random_choice, n, first_position)
                second_position = calculate_pos(first_position, random_choice, n)
                # update q table
                qtable[first_position][random_choice] += alpha*(gamma*(max(qtable[second_position])) - qtable[first_position][random_choice])
            else:
                # find the biggest q table value in that position (up, down, right or down)
                move_to_be_made = qtable[first_position][0]
                move_to_be_made_number = 0
                for i in range(3):
                    if qtable[first_position][i+1] > move_to_be_made:
                        move_to_be_made_number = i + 1
                        move_to_be_made = qtable[first_position][i+1]
                    elif qtable[first_position][i+1] == move_to_be_made:
                        if random.random() < 0.5:
                            move_to_be_made_number = i + 1
                            move_to_be_made = qtable[first_position][i + 1]
                    elif sum(qtable[first_position]) == 2:
                        move_to_be_made_number = random.choice([0, 1, 2, 3])
                # make the move
                game = move(game, move_to_be_made_number, n, first_position)
                second_position = calculate_pos(first_position, move_to_be_made_number, n)
                # update qtable
                qtable[first_position][move_to_be_made_number] += alpha * (gamma * (max(qtable[second_position])) - qtable[first_position][move_to_be_made_number])
            # check if the mouse reached the cheese
            if is_won(game, n):
                break
            first_position = second_position

    # play 1 last game to print
    game = empty_game.copy()
    game[0] = 1
    print_game_state(game, n)
    counter = 0
    # stopping condition
    while counter < 10000:
        # find which move to be made using q table values, find biggest q table value on that position
        counter += 1
        first_position = find_place(game)
        move_to_be_made = qtable[first_position][0]
        move_to_be_made_number = 0
        for i in range(3):
            if qtable[first_position][i + 1] > move_to_be_made:
                move_to_be_made_number = i + 1
                move_to_be_made = qtable[first_position][i + 1]
            elif qtable[first_position][i + 1] == move_to_be_made:
                if random.random() < 0.5:
                    move_to_be_made_number = i + 1
                    move_to_be_made = qtable[first_position][i + 1]
            elif sum(qtable[first_position]) == 2:
                move_to_be_made_number = random_choice([0, 1, 2, 3])
        # make the move
        game = move(game, move_to_be_made_number, n, first_position)
        second_position = calculate_pos(first_position, move_to_be_made_number, n)
        # update q table
        qtable[first_position][move_to_be_made_number] += alpha * (gamma * (max(qtable[second_position])) - qtable[first_position][move_to_be_made_number])
        # print next in order to understand the next move
        print("NEXT")
        print_game_state(game, n)
        if is_won(game, n):
            break

    # print how many moves has been made by the mouse when he learned
    print(str(counter)+" moves made")
    # print the last q table values
    for i in range(n):
        print("Left,  Up,    Right, Down", end='   /  ')
    print()
    for i in range(n):
        for j in range(n):
            for k in range(4):
                print("%.2f" % qtable[i*n+j][k], end='  ')
            print("/", end='  ')
        print()
    # check if the position is optimal
    if counter == n*2-2:
        print("Optimal")

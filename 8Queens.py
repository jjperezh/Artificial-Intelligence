#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" 8Queens Program """
__author__ = "Jorge Perez"

import sys
from collections import Counter
from random import randrange


def generate_board(board):
    return [randrange(8) for _ in range(8)]


def calculate_heuristic(state: list):
    heuristics = 0
    a, b, c = [Counter() for _ in range(3)]

    for row, col in enumerate(state):
        a[col] += 1
        b[row - col] += 1
        c[row + col] += 1

    for count in [a, b, c]:
        for key in count:
            heuristics += count[key] * (count[key] - 1) / 2

    return heuristics


def get_neighbours(state):
    neighbours = []

    for row in range(8):
        for col in range(8):
            if col != state[row]:
                new_state = list(state)
                new_state[row] = col
                neighbours.append(list(new_state))

    return neighbours


def random_restart_hill_climbing(board, steps_climbed, completed, iterations,
                                 new_heuristics):
    current_state = generate_board(board)
    climbed = steps_climbed
    total = completed

    for i in range(iterations):
        total += 1
        while True:
            calculate_heuristic(current_state)
            neighbours = get_neighbours(current_state)

            neighbour = min(neighbours, key=lambda state: calculate_heuristic(state))
            if calculate_heuristic(neighbour) >= calculate_heuristic(current_state):
                break

            current_state = neighbour
            climbed += 1
            new_heuristics = calculate_heuristic(current_state)

        if new_heuristics > 0.0:
            current_state = generate_board(board)
        else:
            completed += 1
            return climbed, completed


n = int(sys.argv[1])

m = n
board = 8
results = 0
completed = 0
all_completed = 0
steps_climbed = 0
new_heuristics = 0
iterations = 5000

while n > 0:
    n -= 1
    climbed_thru, completed = random_restart_hill_climbing(board, steps_climbed, completed,
                                                           iterations, new_heuristics)
    results += climbed_thru
    all_completed += completed

print("Number of puzzles: {}.".format(m))
print(f"Restart Hill-Climbing: {completed / m * 100}% solved,", end='')
print(" Average search cost: {}.".format(results))

'''
mój przykład :

sqn| numerator |   denominator|
___|___________|______________|
1  |a          |      aaa     |
2  | abaaa     |        ab    |
3  | ab        |        b     |
--------------------------------
ex1                             ex2
rozwiazanie : 2 1 1 3           rozwiazanie : 1 2 1 3
numerator  : abaaaaaab          numerator  : aabbaaabb
denominator: abaaaaaab          denominator: aabbaaabb

ex 3
rozwiazanie : 1 3 1 1 3 2 2
numerator  : abb a abb abb a b
denominator: abb a abb abb a b
'''

import ast
import math
import random
import copy
from random import randint
from itertools import permutations


def goal_function(sequence, numerator, denominator):
    """
    DEFINICJA PROBLEMU
    kolejność ustawianych bloczków - górna warstwa bloczka - dolna wartswa bloczka
    """
    numeratorstr = ""
    denominatorstr = ""
    for i in range(0, len(sequence), 1):
        numeratorstr = numeratorstr + numerator[sequence[i] - 1]
        denominatorstr = denominatorstr + denominator[sequence[i] - 1]
    return numeratorstr, denominatorstr


def generate_random_sequece(block_size, sequence_size):
    random_sequence = []
    blocks = [i for i in range(1, block_size + 1, 1)]

    for i in range(0, sequence_size):
        p = int(random.uniform(0, len(blocks)))
        random_sequence.append(blocks[p])
    return random_sequence


def random_probe(goal, iteracions):
    n = 7
    m = len(numerator)
    current_best = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while n > m:
        for i in range(0, iteracions, 1):
            new_sol = generate_random_sequece(block_size=m, sequence_size=n)
            print(new_sol)
            if goal(new_sol)[0] == goal(new_sol)[1]:
                # print("rozwiązanie nr " + str(i) + " " + goal(new_sol)[0])
                # print("liczba sekwencji " + str(len(new_sol)))
                # print("sekwencja " + str(new_sol))
                if len(new_sol) <= len(current_best):
                    current_best = new_sol
                # print("znalazł :", current_best)

        n -= 1
    return current_best


def generate_problem(sequence_size, block_size):
    sequence = []
    for i in range(1, sequence_size + 1, 1):
        sequence.append(random.randint(1, block_size))
    return sequence


def full_search(goal, iteracions):
    current_best = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    v = 7
    m = len(numerator)
    while v > m:
        for i in range(0, iteracions, 1):
            sqc = generate_random_sequece(block_size=m, sequence_size=v)
            # print(sqc)
            for new_sol in permutations(sqc):
                # print("zmienna new_sol" , new_sol)
                if goal(new_sol)[0] == goal(new_sol)[1]:
                    # print("rozwiązanie nr " + goal(new_sol)[0])
                    # print("liczba sekwencji " + str(len(new_sol)))
                    # print("sekwencja " + str(new_sol))
                    if int(len(new_sol)) <= int(len(current_best)):
                        current_best = new_sol
                        # print("znalazł :", current_best)
        v -= 1
    return current_best


def random_neighbour(sqc):
    '''
    sqc - wylosowana sekwencja
'''

    str_pt = int(randint(0, len(sqc) - 1))
    tmpsqc = copy.deepcopy(sqc)
    tmpsqc[(str_pt + 1) % len(sqc)] = sqc[str_pt]
    tmpsqc[str_pt] = sqc[(str_pt + 1) % len(sqc)]
    return tmpsqc


def hill_climbing_rand(goal, gen_neigbour, iterations):
    """
    goal - funkcja celu ,
    gensol - generowanie losowego rozwiązania ,
    gen_neigbour - generowanie losowego punktu z otoczenia rozwiązania
    iteracion - liczba iteracji petli

    """

    m = len(numerator)
    v = 7
    current_best = [0, 0, 0, 0, 0, 0, 0, 0]
    print("best cur", current_best)
    while v > m:
        for j in range(0, iterations, 1):
            sol = generate_random_sequece(block_size=m, sequence_size=v)
            # print(sol)
            if goal(sol)[0] != goal(sol)[1] and len(current_best) >= len(sol):
                for i in range(0, iterations, 1):
                    new_sol = gen_neigbour(sol)
                    # print(new_sol)
                    if goal(new_sol)[0] == goal(new_sol)[1] and len(current_best) >= len(new_sol):
                        current_best = new_sol
                    # print("znalazłem ", current_best)
            elif goal(sol)[0] == goal(sol)[1] and len(current_best) >= len(sol):
                current_best = sol
                # print("znalazłem 2", current_best)
        v -= 1

    # print("obecnie najlepszy", current_best)
    return current_best


def best_neighbour(sqc, goal):
    """
    goal - funkcja celu
    sqc - wylosowana sekwencja??
    """

    best = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # print("zmienna best ", best)

    for str_pt in range(0, len(sqc) - 1):
        str_pt = int(randint(0, len(sqc) - 1))
        tmpsqc = copy.deepcopy(sqc)
        tmpsqc[(str_pt + 1) % len(sqc)] = sqc[str_pt]
        tmpsqc[str_pt] = sqc[(str_pt + 1) % len(sqc)]

        if goal(tmpsqc)[1] == goal(tmpsqc)[0] and goal(tmpsqc)[1] <= goal(best)[0]:
            best = tmpsqc
            # print("jest!")
            # print("zmienna best3 ", best)
            return best
    # print("zmienna best2 ", best)
    return best


def hill_climbing_deterministic(goal, iterations):
    m = len(numerator)
    v = 7
    current_best = [0, 0, 0, 0, 0, 0, 0, 0]
    # print("best cur", current_best)
    while v > m:
        for j in range(0, iterations, 1):
            sol = generate_random_sequece(block_size=m, sequence_size=v)
            # print(sol)
            if goal(sol)[0] != goal(sol)[1] and len(current_best) >= len(sol):
                for i in range(0, iterations, 1):
                    new_sol = best_neighbour(sqc=sol, goal=goal)
                    # print(new_sol)
                    if goal(new_sol)[0] == goal(new_sol)[1] and len(current_best) >= len(new_sol):
                        current_best = new_sol
                    # print("znalazłem ", current_best)
            elif goal(sol)[0] == goal(sol)[1] and len(current_best) >= len(sol):
                current_best = sol
                # print("znalazłem 2", current_best)
        v -= 1

    # print("obecnie najlepszy", current_best)
    return current_best


def sim_anealin(goal, gen_neigbour, T, iterations):
    m = len(numerator)
    v = 7
    current_best = generate_random_sequece(block_size=m, sequence_size=v)
    # print("best cur", current_best)
    V = [current_best]
    while v > m:
        for j in range(0, iterations, 1):
            sol = generate_random_sequece(block_size=m, sequence_size=v)
            # print(sol)
            if goal(sol)[0] != goal(sol)[1] and len(current_best) >= len(sol):
                for i in range(1, iterations + 1, 1):
                    new_sol = gen_neigbour(sol)
                    # print(new_sol)
                    if goal(new_sol)[0] == goal(new_sol)[1] and len(current_best) >= len(new_sol):
                        current_best = new_sol
                        V.append(current_best)
                    else:
                        e = math.exp(- abs(len(goal(new_sol)[0]) - len(goal(current_best)[0])) / T(i))
                        u = random.uniform(0.0, 1.0)
                        if u < e and goal(new_sol)[0] == goal(new_sol)[1]:
                            current_best = new_sol
                            V.append(current_best)
                    # print("znalazłem ", current_best)
            elif goal(sol)[0] == goal(sol)[1] and len(current_best) >= len(sol):
                current_best = sol
                # print("znalazłem 2", current_best)
        v -= 1

    # print("obecnie najlepszy", current_best)
    return min(V, key=goal)


ex = input("wybierz przykład 1 - 3:\n"
           "==>")
with open("ex" + ex + ".txt", 'r') as f:
    numerator, denominator = map(ast.literal_eval, f.readlines())

method = input("wybierz metode: \n"
               "1. random_probe\n"
               "2. full_search\n"
               "3. hill_climbing_rand\n"
               "4. hill_climbing_deterministic \n"
               "5.  sim_annealin \n"
               "==>")

if method == "1":

    sol = random_probe(goal=lambda s: goal_function(s, numerator, denominator),
                       iteracions=10000)
    print(sol)
    print(goal_function(sequence=sol,
                        numerator=numerator,
                        denominator=denominator))

elif method == "2":

    sol = full_search(goal=lambda s: goal_function(s, numerator, denominator),
                      iteracions=500)
    print(sol)
    print(goal_function(sequence=sol,
                        numerator=numerator,
                        denominator=denominator))

elif method == "3":
    sol = hill_climbing_rand(goal=lambda s: goal_function(s, numerator, denominator),
                             gen_neigbour=random_neighbour,
                             iterations=300)
    print(sol)
    print(goal_function(sequence=sol,
                        numerator=numerator,
                        denominator=denominator))
elif method == "4":
    sol = hill_climbing_deterministic(goal=lambda s: goal_function(s, numerator, denominator),
                                      iterations=300)
    print(sol)
    print(goal_function(sequence=sol,
                        numerator=numerator,
                        denominator=denominator))
elif method == "5":
    sol = sim_anealin(goal=lambda s: goal_function(s, numerator, denominator),
                      gen_neigbour=random_neighbour,
                      T=lambda k: 1000 / k,
                      iterations=300)
    print(sol)
    print(goal_function(sequence=sol,
                        numerator=numerator,
                        denominator=denominator))
else:
    pass

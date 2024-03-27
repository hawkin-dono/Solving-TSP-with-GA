import time
import random
from tsp import TSP_GA_Solver, Route
   
def test_get_first_generation():
    n = 50
    cities = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
              (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), 
              (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), 
              (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), 
              (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), 
              (47, 47), (48, 48), (49, 49)]
    
    population_size = 50
    solver = TSP_GA_Solver(n, cities, population_size= population_size)
    generation = solver.get_first_generation()
    
    assert len(generation) == population_size
    for i in generation:
        print(i)
        
def test_crossover():
    n = 5
    cities = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    population_size = 50
    solver = TSP_GA_Solver(n, cities, population_size= population_size)
    generation = solver.get_first_generation()
    
    i, j = random.sample(range(population_size), 2)
    parent1 = generation[i]
    parent2 = generation[j]
    
    print("Parent1: \n", parent1.route)
    print("Parent2: \n", parent2.route)
    for i in solver.crossover(parent1, parent2):
        print(i.route)
        
def test_mutate():
    n = 5
    cities = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    population_size = 50
    solver = TSP_GA_Solver(n, cities, population_size= population_size)
    generation = solver.get_first_generation()
    
    i, j = random.sample(range(population_size), 2)
    parent1 = generation[i]
    
    child = solver.mutate(parent1)
    print("Parent: \n", parent1.route)
    print("Child: \n", child.route)
    
def test_get_next_generation():
    n = 5
    cities = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    population_size = 5
    solver = TSP_GA_Solver(n, cities, population_size= population_size, acceptable_ratio= 1)
    generation = solver.get_first_generation()
    print("First generation: ")
    for i in generation:
        print(i)
    
    for _ in range(5):
        next_generation = solver.get_next_generation(generation)
        print("Next generation:  ")
        for i in next_generation:
            print(i)
            
def test_intersect():
    
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        elif val > 0:
            return 1  # clockwise
        else:
            return 2  # counterclockwise

    def on_segment(p, q, r):
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False

    def do_intersect(p1, q1, p2, q2):
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1, p2, q1):
            return True

        if o2 == 0 and on_segment(p1, q2, q1):
            return True

        if o3 == 0 and on_segment(p2, p1, q2):
            return True

        if o4 == 0 and on_segment(p2, q1, q2):
            return True

        return False
    
    p1 = (1, 1) 
    q1 = (10, 1) 
    p2 = (1, 2) 
    q2 = (10, 2) 
    
    res1 = do_intersect(p1, q1, p2, q2)
    assert res1 == False
    
    p1 = (10, 0) 
    q1 = (0, 10) 
    p2 = (0, 0) 
    q2 = (10,10) 
    res2 = do_intersect(p1, q1, p2, q2)
    assert res2 == True
    print('pass')
    

# start_time = time.time()
# # n, cities = get_input()
# n = 20
# cities = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)]
# POPULATION_SIZE = 2000
# TOURNAMENT_SELECTION_SIZE = 4
# MUTATION_RATE = 0.1
# CROSSOVER_RATE = 0.9
# PATIENCE_STEPS = 5
# MAX_GENERATIONS = 1000
test_intersect()
"""
Yêu cầu: Cài đặt Giải thuật di truyền giải bài toán tìm đường đi tối ưu cho người bán hàng (TSP).

Quy ước:

- Giữa 2 thành phố bất kỳ đều có đường đi và độ dài được tính bằng khoảng cách Euclid.

Dữ liệu:

- Input: Số thành phố n, n cặp số nguyên dương (x, y) là tọa độ của các thành phố

- Output: Giá trị thực d là tổng quãng đường đi tối ưu tìm được và chuỗi n số là thứ tự các thành phối trong đường đi  

 Giới hạn:

- n < 100

- Thời gian thực hiện < 300 giây

"""
import random
import math
import time
import matplotlib.pyplot as plt
from collections import defaultdict

class Route:
    cities = None
    distance_map = dict()
    def __init__(self, route: list[int]):
        self.route = route
        self.distance: float = self.cal_distance(self.route)
        
    # the higher the fitness, the worse the route
    def cal_distance(self, route):
        total_distance = 0
        for i in range(len(self.route) - 1):
            city1, city2 = route[i], route[i + 1]
            connection = self.convert_connection_to_string(city1, city2)
            if connection in self.distance_map:
                total_distance += self.distance_map[connection] 
            else:
                dis = self.euclidean_distance(city1, city2)
                self.distance_map[connection] = dis
                total_distance += dis
        return total_distance / len(self.route)
    
    def euclidean_distance(self, city1: int, city2: int):
        x1, y1 = self.cities[city1]
        x2, y2 = self.cities[city2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def drawMap(self):
        for i in range(len(self.route)):
            plt.plot(self.cities[i][0], self.cities[i][1], 'ro')
        
        for i in range(len(self.route) - 1):
            city1 = self.route[i]
            city2 = self.route[i + 1]
            x1, y1 = self.cities[city1]
            x2, y2 = self.cities[city2]
            plt.plot([x1, x2], [y1, y2], 'g')
        plt.show()
    
    def convert_connection_to_string(self, city1: int, city2: int):
        s = str(city1) + '-' + str(city2)
        return s
    
    def __str__(self):
        return f'Route: {self.route}, distance: {self.distance}'
    
    def orientation(self, p, q, r):
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

    
    def do_intersect(self, city1, city2, city3, city4):
        p1, q1, p2, q2 = self.cities[city1], self.cities[city2], self.cities[city3], self.cities[city4]
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True

        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True

        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True

        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True

        return False
        
    

class TSP_GA_Solver:
    def __init__(self, n, cities, population_size= 200, tournament_selection_size= 4, 
                 mutation_rate= 0.1, crossover_rate= 0.9, patience_steps= 5, max_generations= 500,
                 acceptable_ratio = 1.5, acceptable_ratio_decay = 0.99):
        self.n = n
        self.cities = cities
        Route.cities = cities
        self.population_size = population_size
        self.tournament_selection_size = tournament_selection_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.patience_steps = patience_steps
        self.max_generations = max_generations
        self.acceptable_ratio = acceptable_ratio
        self.acceptable_ratio_decay = acceptable_ratio_decay
        
        
        # self.population = self.initial_population()
        
    def get_first_generation(self):
        generation = []
        while len(generation) < self.population_size:
            route1 = Route(random.sample(range(self.n), self.n))
            route2 = Route(random.sample(range(self.n), self.n))
            
            if route1.distance < route2.distance:
                generation.append(route1)
            else:    
                generation.append(route2)
        return generation
    
    def order1_crossover(self, parent1: Route, parent2: Route):
        start = random.randint(0, self.n - 2)
        end = random.randint(start + 1, self.n - 1)
        
        child = [-1] * self.n
        for i in range(start, end + 1):
            child[i] = parent1.route[i]
        remaining_cities = [city for city in parent2.route if city not in child]
        j = 0
       
        for i in range(self.n):
            if child[i] == -1:
                child[i] = remaining_cities[j]
                j += 1
        return Route(child)
        
    
    def normal_crossover(self, parent1: Route, parent2: Route):
        slice = random.randint(0, self.n - 1)
        child1 = parent1.route[:slice] + parent2.route[slice:]
        child2 = parent2.route[:slice] + parent1.route[slice:]

        return Route(child1), Route(child2)
        
    def crossover(self, parent1: Route, parent2: Route):
        # rand = random.randint(0, 1)
        rand = 1
        if rand == 1:
            # print("order1 crossover")
            child1 = self.order1_crossover(parent1, parent2)
            child2 = self.order1_crossover(parent2, parent1)
        else:
            # print("normal crossover")
            child1, child2 = self.normal_crossover(parent1, parent2)
        
        return child1, child2

    def mutate(self, parent: Route):
        # i, j = random.sample(range(self.n), k = 2)
        # child = parent.route.copy()
        # child[i], child[j] = child[j], child[i]
        # return Route(child)
        i = 0
        while True:
            if i == 5:
                break
            try:
                i, j = random.sample(range(self.n), k = 2)
                # print(parent.route)
                # print(parent.route[i], parent.route[i + 1],  parent.route[j], parent.route[j + 1])
                city1, city2, city3, city4 = parent.route[i], parent.route[i + 1],  parent.route[j], parent.route[j + 1]
                # print(city1)
                
                if parent.do_intersect(city1, city2, city3, city4):
                    parent.route[i], parent.route[j] = parent.route[j], parent.route[i]
                i += 1
            
            except Exception as e:
                # print(e)
                continue
        child = parent.route.copy()      
        return Route(child)
                
            

    def get_next_generation(self, generation: list[Route]):
        next_generation = []
        
        # sap xep theo fitness, route co fitness thap nhat o dau
        sort_generation = sorted(generation, key=lambda x: x.distance, reverse=True)
        
        # chon ra 2 route co fitness thap nhat
        next_generation.append(sort_generation[0])
        next_generation.append(sort_generation[1])
        
        # increase the rate of the best route
        sort_generation.append(sort_generation[0])
        sort_generation.append(sort_generation[1])
        
        # create new generation
        while len(next_generation) < self.population_size:
            random_range = 1000
            rand = random.randint(0, random_range)
            
            if rand < self.crossover_rate * random_range:
                parent1_index, parent2_index = sorted(random.sample([i for i in range(self.population_size + 2)], self.tournament_selection_size))[: 2]
                parent1, parent2 = sort_generation[parent1_index], sort_generation[parent2_index]
            
                child1, child2 = self.crossover(parent1, parent2)
                
                if child1.distance > parent1.distance * self.acceptable_ratio:
                    continue
                if child2.distance > parent2.distance * self.acceptable_ratio:
                    continue
                
                
            # If crossover not happen
            else:
                parent1_index, parent2_index = random.sample([i for i in range(self.population_size + 2)], 4)[: 2]
                child1, child2 = sort_generation[parent1_index], sort_generation[parent2_index]

            rand = random.randint(0, random_range)
            if rand < self.mutation_rate * random_range:
                child1_mutate = self.mutate(child1)
                child2_mutate = self.mutate(child2)
            
                if child1_mutate.distance < child1.distance * self.acceptable_ratio:
                    next_generation.append(child1_mutate)
                if child2_mutate.distance < child1.distance * self.acceptable_ratio:
                    next_generation.append(child2_mutate)
                
        return next_generation[: self.population_size]


    def solve(self):
        unimproved_steps = 0
        check_improvement = False
        best_route: Route = None
        best_distance = float('inf')
        curr_generation = self.get_first_generation()
        start_time = time.time()
        generation_cnt = 0
        
        while time.time() - start_time < 280:
            if unimproved_steps >= self.patience_steps:
                break
            curr_generation = self.get_next_generation(curr_generation)
            
            for route in curr_generation:
                if  route.distance < best_distance:
                    best_distance = route.distance
                    best_route = route
                    check_improvement = True
            if not check_improvement:
                unimproved_steps += 1
            else:
                unimproved_steps = 0
                check_improvement = False
            self.acceptable_ratio = max(1, self.acceptable_ratio_decay * self.acceptable_ratio) if generation_cnt %  3 == 0 else self.acceptable_ratio
            generation_cnt += 1
        best_route.drawMap()
        return best_route
            

def get_input():
    n = input("Nhập số lượng thành phố: ")
    cities = []
    for i in range(n):
        x, y = map(int, input().split("Nhập tọa độ của các thành phố"))
        cities.append((x, y))
        
    return n, cities

def main():
    start_time = time.time()
    n, cities = get_input()
    # n = 30
    # cities = [(682, 125), (830, 615), (251, 382), (136, 176), (35, 247), (651, 732), (225, 759), (602, 610), (348, 188), (731, 400), (153, 697), (659, 934), (341, 239), (364, 931), (110, 331), (824, 143), (331, 777), (429, 803), (714, 818), (988, 954), (120, 668), (725, 22), (159, 934), (87, 86), (829, 671), (314, 565), (853, 120), (963, 10), (19, 707), (729, 198), (143, 915), (270, 700), (74, 597), (522, 483), (252, 61), (3, 158), (102, 497), (402, 744), (558, 562), (603, 312), (985, 306), (521, 184), (591, 142), (619, 172), (766, 717), (927, 266), 
    #           (101, 271), (885, 61), (378, 28), (854, 49), (863, 148), (980, 106), (408, 543), (860, 370), (815, 528), (18, 195), (781, 861), (367, 426), (856, 823), (858, 687), (164, 850), (611, 889), (516, 286), (389, 96), (186, 65), (331, 784), (763, 657), (556, 105), (605, 581), (707, 783), (219, 29), (573, 331), (416, 893), (30, 644), (448, 831), (217, 406), (662, 800), (250, 10), (58, 918), (804, 936), (169, 431), (448, 907), (224, 549), (19, 585), (521, 681), (992, 402), (763, 264), (871, 409), (207, 726), (367, 102), (202, 457), (855, 433), (5, 163), (199, 168), (762, 626), (218, 130), (547, 895), (820, 883), (377, 120)]
    POPULATION_SIZE = n * 5
    TOURNAMENT_SELECTION_SIZE = 4
    MUTATION_RATE = 0.6
    CROSSOVER_RATE = 0.9
    PATIENCE_STEPS = 1000
    MAX_GENERATIONS = 2000
    ACCEPTABLE_RATIO = 2
    ACCEPTABLE_RATIO_DECAY = 0.99
    
    
    solver = TSP_GA_Solver(n, cities, population_size= POPULATION_SIZE, tournament_selection_size= TOURNAMENT_SELECTION_SIZE,
                           mutation_rate= MUTATION_RATE, crossover_rate= CROSSOVER_RATE, patience_steps= PATIENCE_STEPS,
                           max_generations= MAX_GENERATIONS, acceptable_ratio= ACCEPTABLE_RATIO, acceptable_ratio_decay= ACCEPTABLE_RATIO_DECAY)
    route = solver.solve()
    end_time = time.time()
    print(f'total time: {end_time - start_time}')
    
if __name__ == "__main__":
    main()

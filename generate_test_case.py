import random
def gen_test(n):
    cities = []
    for i in range(n):
        x, y = random.randint(0, 1000), random.randint(0, 1000)
        cities.append((x, y))
    
    return cities

def main():
    n = 30
    cities = gen_test(99)
    print(cities)


if __name__ == "__main__":
    main()
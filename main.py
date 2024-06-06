import sys

from faker import Faker
import random
import math

random = random.SystemRandom()
global size
cities = []


class City:
    name: str
    x: float
    y: float

    def __init__(self, name, x, y):
        self.name = name
        self.x = round(float(x), 2)
        self.y = round(float(y), 2)

    def __str__(self):
        return "" + self.name + ", " + self.x.__str__() + ", " + self.y.__str__()

    def get_name(self):
        return self.name


def generate_cities():
    faker = Faker(['en_GB', 'en_US', 'pl_PL', 'fr_FR', 'de_DE', 'es_ES'])

    with open("miasta.txt", "w", encoding='utf-8') as miasta:
        i = 0
        while i != size:
            city = faker.city()
            if city not in cities:
                miasta.write(
                    city + "," + round((random.random() * i), 2).__str__() + "," + round((random.random() * i), 2).__str__() + "\n")
                i += 1


def read_file():
    with open("miasta.txt", "r", encoding='utf-8') as miasta:
        line = miasta.readline()
        while line:
            split_line = line.split(",")
            cities.append(City(split_line[0], split_line[1], split_line[2]))
            line = miasta.readline()


def calculate_distance(first_city: City, second_city: City):
    return math.sqrt(math.pow(second_city.x - first_city.x, 2) + math.pow(second_city.y - first_city.y, 2))


def simulated_annealing(resultList):
    T = 2.0
    T_min = 1.0
    distance = sum(calculate_distance(pair[0], pair[1]) for pair in resultList)
    while T > T_min:
        new_result = change_neighbor(resultList)
        new_distance = sum(calculate_distance(pair[0], pair[1]) for pair in new_result)
        dE = new_distance - distance
        if dE < 0 or math.exp(-dE / T) > random.random():
            resultList = new_result[:]
            distance = new_distance
        T *= 0.9999
    return resultList


def change_neighbor(resultList):
    copy = resultList[:]
    first_pair, second_pair = random.sample(copy, 2)
    first_index, second_index = copy.index(first_pair), copy.index(second_pair)
    copy[first_index] = (first_pair[0], second_pair[1])
    copy[second_index] = (second_pair[0], first_pair[1])
    return copy


def random_pair_city():
    copy_cities = cities[:]
    resultList = []
    while copy_cities:
        first_city: City = random.choice(copy_cities)
        copy_cities.remove(first_city)
        second_city: City = random.choice(copy_cities)
        copy_cities.remove(second_city)
        resultList.append((first_city, second_city))
    return resultList


def closest_city_pair():
    copy = cities[:]
    while len(copy) != 0:
        closest_city: City
        start_city: City = random.choice(copy)
        distance = sys.maxsize
        for city in copy:
            if start_city != city:
                dist = calculate_distance(start_city, city)
                if dist < distance:
                    distance = dist
                    closest_city = city
        print(start_city.get_name() + "-" + closest_city.get_name())
        copy.remove(start_city)
        copy.remove(closest_city)


if __name__ == '__main__':
    size = 10000
    # generate_cities()
    read_file()
    closest_city_pair()
    print("\n\n\n")
    result = random_pair_city()
    result = simulated_annealing(result)
    for cities in result:
        first_city: City = cities[0]
        second_city: City = cities[1]
        print(first_city.get_name() + " - " + second_city.get_name())

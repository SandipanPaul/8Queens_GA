import random
import string

maxFitness = 28

def GenerateInitialChromosomes(size):
    return [ random.randint(0, 7) for _ in range(8) ]

def fitness(individual):
    horizontal_collisions = sum([individual.count(queen)-1 for queen in individual])/2
    diagonal_collisions = 0

    n = len(individual)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + individual[i] - 1] += 1
        right_diagonal[len(individual) - i + individual[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(maxFitness - (horizontal_collisions + diagonal_collisions))

def survival(individual):
    return fitness(individual) / maxFitness

def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
        
def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(0, n-1)
    x[c] = m
    return x

def GA(population, fitness):
    mutation_probability = 0.03
    new_population = []
    probabilities = [survival(n) for n in population]
    for i in range(len(population)):
        parent1 = random_pick(population, probabilities)
        parent2 = random_pick(population, probabilities)
        child = reproduce(parent1, parent2)
        if random.random() < mutation_probability:
            child = mutate(child)
        print_individual(child)
        new_population.append(child)
        if fitness(child) == 28: break
    return new_population

def print_individual(x):
    print("{},  fitness = {}, probability = {:.6f}"
        .format(str(x), fitness(x), survival(x)))

if __name__ == "__main__":
    POPULATION_SIZE=100
    population = [GenerateInitialChromosomes(8) for _ in range(POPULATION_SIZE)]
    generation = 1

    while not 28 in [fitness(x) for x in population]:
        print("=== Generation {} ===".format(generation))
        population = GA(population, fitness)
        print("Maximum fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1

    print("Solved in Generation {}!".format(generation-1))
    for x in population:
        if fitness(x) == 28:
            print_individual(x)

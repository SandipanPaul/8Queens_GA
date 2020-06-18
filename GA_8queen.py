import numpy as np
import sys

nQueen=8
MAX_FITNESS=28
MUTATE = 0.000001
MUTATE_FLAG=True
MAX_ITER=100000
POPULATION=None

class BoardPosition:

    def __init__(self):
        self.sequence=None
        self.fitness=None
        self.survival=None
    
    def setSequence(self,val):
        self.sequence=val

    def setFitness(self,val):
        self.fitness=val

    def setSurvival(self,val):
        self.survival=val
    
    def getAttr(self):
        return {'sequence':sequence, 'fitness':fitness, 'survival':survival}

    def __eq__(self,other):
        if(isinstance(self.sequence,list)):
            return (self.sequence==other.sequence and self.fitness==other.fitness and self.survival==other.survival)
        else:
            return ((self.sequence==other.sequence).all() and self.fitness==other.fitness and self.survival==other.survival)

def fitness(chromosome=None):
    clashes=0
    row_col_clash=abs(len(chromosome)-len(np.unique(chromosome)))
    clashes+=row_col_clash

    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if(i!=j):
                dx=abs(i-j)
                dy=abs(chromosome[i]-chromosome[j])
                if(dx==dy):
                    clashes+=1

    return 28-clashes

def generateChromosome():
    global nQueen
    init_distribution=np.arange(nQueen)
    np.random.shuffle(init_distribution)
    return init_distribution


def generatePopulation(population_size=100):
    global POPULATION

    POPULATION=population_size

    population=[BoardPosition() for i in range(population_size)]

    for i in range(population_size):
        population[i].setSequence(generateChromosome())
        population[i].setFitness(fitness(population[i].sequence))

    return population

def getParent():
    globals()
    parent1,parent2=None,None

    summation_fitness=np.sum([x.fitness for x in population])
    for each in population:
        each.survival=each.fitness/(summation_fitness*1.0)
    while True:
        parent1_random=np.random.rand()
        parent1_rn=[x for x in population if x.survival<parent1_random]
        try:
            parent1=parent1_rn[0]
            break
        except:
            pass

    while True:
        parent2_random = np.random.rand()
        parent2_rn = [x for x in population if x.survival <= parent2_random]
        try:
            t = np.random.randint(len(parent2_rn))
            parent2 = parent2_rn[t]
            #print(parent2 == parent1)
            if (parent2 != parent1):
                break
            else:
                continue
        except:
            continue

    if parent1 is not None and parent2 is not None:
        return (parent1, parent2)
    else:
        sys.exit(-1)

def reproduce_crossover(parent1, parent2):
    globals()
    n = len(parent1.sequence)
    c = np.random.randint(n, size=1)[0]
    child = BoardPosition()
    child.sequence = []
    child.sequence.extend(parent1.sequence[0:c])
    child.sequence.extend(parent2.sequence[c:])
    child.setFitness(fitness(child.sequence))
    return child

def mutate(child):
    c = np.random.randint(8)
    child.sequence[c] = np.random.randint(8)
    return child

def GA(iteration):
    print (" #"*10 ,"Executing Genetic  generation : ", iteration , " #"*10)
    globals()
    newpopulation = []
    for i in range(len(population)):
        parent1, parent2 = getParent()
        # print "Parents generated : ", parent1, parent2

        child = reproduce_crossover(parent1, parent2)

        if(MUTATE_FLAG):
            child = mutate(child)

        newpopulation.append(child)
    return newpopulation

def stop():
    globals()
    # print population[0], " printing population[0]"
    fitnessvals = [pos.fitness for pos in population]
    if MAX_FITNESS in fitnessvals:
        return True
    if MAX_ITER == iteration:
        return True
    return False

if __name__=="__main__":
    population = generatePopulation(100)

    print ("POPULATION size : ", len(population))

    iteration = 0;
    while not stop():
        # keep iteratin till  you find the best position
        population = GA(iteration)
        iteration +=1 
        print ("Iteration number : ", iteration)
        tempFitnessVal=0
        tempSequence=[]
        for each in population:
            if each.fitness == 28:
                print (each.sequence)
                sys.exit(0)
            else:
                if(each.fitness>tempFitnessVal):
                    tempFitnessVal=each.fitness
                    tempSequence=each.sequence
        if(len(tempSequence)>0):
            print (tempFitnessVal)
            print (tempSequence)

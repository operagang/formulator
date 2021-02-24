import datetime
import random
import unittest
import copy

def baseball():
    length = 6
    global target
    target = pick_baseball_num(length, False)
    print('target : {}'.format(target))
    guess_baseball(target)

def pick_baseball_num(length, is_duplicate_allowed):
    if is_duplicate_allowed is True or length > 10:
        return ''.join(random.choice(geneset) for _ in range(length))

    baseball_list = []
    num = random.randrange(0,10)
    for i in range(length):
        while str(num) in baseball_list:
            num = random.randrange(0,10)
        baseball_list.append(str(num))

    return ''.join(baseball_list)

def guess_baseball(target):
    global startTime
    startTime = datetime.datetime.now()

    optimalFitness = len(target) * 5
    global geneset
    child_list = get_best(len(target), optimalFitness, geneset)

    display_list(child_list, target, startTime)

def get_best(targetLen, optimalFitness, geneSet):
    random.seed()
    bestParentList = generate_parent(targetLen, geneSet)
    global target, startTime
    display_list(bestParentList, target, startTime)

    gen_count = 0
    maximum_average = 0
    while True:
        gen_count += 1
        print('generation : {}'.format(gen_count))
        child_list = generate_child(bestParentList, geneSet)

        fitness_sum = 0
        for child in child_list:
            fitness_sum += child.Fitness

        average = fitness_sum / 10
        if average > maximum_average:
            print('new maximum fitness : {}'.format(average))
            bestParentList = child_list
            maximum_average = average
            display_list(child_list, target, startTime)
        if average >= optimalFitness:
            return child_list

def generate_parent(length, geneSet):
    chromosome_list = []
    global target
    for i in range(0, 10):
        genes = []
        while len(genes) < length:
            sampleSize = min(length - len(genes), len(geneSet))
            genes.extend(random.sample(geneSet, sampleSize))
        fitness = get_fitness(genes, target)
        chromosome_list.append(Chromosome(genes, fitness))
    return chromosome_list

def get_fitness(guess, target):
    fitness = 0
    for expected, actual in zip(target, guess):
        if expected == actual:
            fitness += 5
        elif actual in target:
            fitness += 1

    return fitness

class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

def display_list(candidate_list, target, startTime):
    fitness_sum = 0
    for candidate in candidate_list:
        display(candidate, target, startTime)
        fitness_sum += candidate.Fitness
    print('average fitness : {}'.format(fitness_sum / len(candidate_list)))

def display(candidate, target, startTime):
    timeDiff = datetime.datetime.now() - startTime
    strike = 0
    ball = 0
    for expected, actual in zip(target, candidate.Genes):
        if expected == actual:
            strike += 1
        elif actual in target:
            ball += 1
    if strike == 0 and ball == 0:
        result = 'out'
    else:
        result = '{}/{}'.format(strike, ball)
    print('{}\t{}\t{}\t{}'.format(''.join(candidate.Genes), result, candidate.Fitness, timeDiff))

def generate_child(parent_list, geneSet):
    child_list = []
    fitness_percent_list = []
    fitness_accum_list = []
    fitness_sum = 0
    for parent in parent_list:
        fitness_sum += parent.Fitness
    for parent in parent_list:
        fitness_percent_list.append(parent.Fitness / fitness_sum)
    fitness_sum = 0
    for fitness_percent in fitness_percent_list:
        fitness_sum += fitness_percent
        fitness_accum_list.append(fitness_sum)

    # Fitness proportionate selection
    for i in range(0, 10):
        rand = random.random()
        before = 0
        for j in range(0, len(fitness_accum_list)):
            if rand > before and rand <= fitness_accum_list[j]:
                child_list.append(copy.deepcopy(parent_list[j]))
                break
            before = fitness_accum_list[j]

    global target
    crossover_rate = 0.20
    selected = None
    for i in range(0, len(child_list)):
        rand = random.random()
        if rand < crossover_rate:
            if selected is None:
                selected = i
            else:
                child_list[selected].Genes[2:], child_list[i].Genes[2:] = \
                    child_list[i].Genes[2:], child_list[selected].Genes[2:]
                selected = None

    for i in range(0, len(child_list)):
        child_list[i].Fitness = get_fitness(child_list[i].Genes, target)

    global geneset
    mutate_rate = 0.2
    for i in range(0, len(child_list)):
        rand = random.random()
        if rand < mutate_rate:
            child = mutate(child_list[i], geneset)
            child_list[i] = child
    return child_list

def mutate(parent, geneSet):
    global target
    childGenes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    fitness = get_fitness(childGenes, target)
    return Chromosome(childGenes, fitness)

if __name__ == '__main__':
    geneset = '0123456789'
    target = ''
    startTime = ''
    baseball()


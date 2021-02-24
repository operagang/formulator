import random
import math
import copy

def generateProcessTimes(start, end, num):
    #return tuple([random.randrange(start, end+1) for _ in range(num)])
    return (10, 10, 10, 10, 10, 10, 10, 10, 10, 10)

def generateSetupTimes(start, end, num):
    #return tuple([tuple((random.randrange(start, end+1)) for _ in range(num)) for _ in range(num)])
    return ((0,0,0,0,10,10,10,10,10,10),(10,0,0,0,10,10,10,10,10,10),(10,10,0,0,10,10,10,10,10,10) \
            ,(10,10,10,0,10,10,10,10,10,10),(10,10,10,10,0,0,0,10,10,10),(10,10,10,10,20,0,0,10,10,10) \
            ,(10,10,10,10,20,20,0,10,10,10),(10,10,10,10,10,10,10,0,0,0),(10,10,10,10,10,10,10,20,0,0) \
            ,(10,10,10,10,10,10,10,20,20,0))

def generateParents(integerSet, numChromosome, numJob):
    parent_list = []
    for _ in range(0, numChromosome):
        parent_unit = []
        chromosome_list = []
        for _ in range(0, numJob):
            newChromosome = random.choice(integerSet) + random.randrange(0,100)/100
            while newChromosome in chromosome_list:
                newChromosome = random.choice(integerSet) + random.randrange(0,100) / 100
            chromosome_list.append(newChromosome)
        parent_unit.append(chromosome_list)

        fitness = get_fitness(integerSet, chromosome_list)
        parent_unit.append(fitness)
        parent_list.append(parent_unit)
    return parent_list

def get_fitness(set, chromosome):
    global processTime
    global setupTime
    schedule = [[] for _ in range(0, len(set))]
    for i in range(0, len(chromosome)):
        job = []
        job.append(i)
        job.append(chromosome[i])
        schedule[int(chromosome[i])-1].append(job)
    makespan = 0
    for assignment in schedule:
        assignment.sort(key = lambda x : x[1])
        completionTime = 0
        for i in range(0, len(assignment)):
            completionTime += processTime[assignment[i][0]]
            if i >= 1:
                completionTime += setupTime[assignment[i-1][0]][assignment[i][0]]
        if completionTime >= makespan:
            makespan = completionTime
    return makespan

def generateChild(schedule_list):
    global numChromosomes, numJobs, machineSet
    schedule_list.sort(key = lambda x: x[1])
    #print(len(schedule_list), min(schedule_list, key = lambda x: x[1]))
    newChild_list = []
    firstPart = math.ceil(numChromosomes * 0.2)
    secondpart = int(numChromosomes * 0.79)
    if numChromosomes - firstPart - secondpart < 1 and secondpart > 0:
        secondpart -= 1
    thirdpart = numChromosomes - firstPart - secondpart
    # print(schedule_list)
    # print(len(schedule_list))
    for i in range(0, firstPart):
        newChild_list.append(copy.deepcopy(schedule_list[i]))
    # print(newChild_list)
    # print(len(newChild_list))
    for _ in range(0, secondpart):
        leftIndex = random.randrange(0, 100)
        rightIndex = random.randrange(0, 100)
        while rightIndex == leftIndex:
            rightIndex = random.randrange(0, 100)
        left = copy.deepcopy(schedule_list[leftIndex][0])
        right = copy.deepcopy(schedule_list[rightIndex][0])
        # print(left)
        # print(right)
        child = []
        for i in range(0, numJobs):
            rand = random.random()
            if rand < 0.7:
                child.append(left[i])
            else:
                child.append(right[i])
        fitness_child = get_fitness(machineSet, child)
        newChild = [child, fitness_child]
        newChild_list.append(newChild)
    # print(newChild_list)
    # print(len(newChild_list))

    for _ in range(0, thirdpart):
        mutated_child = mutate(machineSet, numJobs)
        newChild_list.append(mutated_child)
    # print(newChild_list)
    # print(len(newChild_list))
    return newChild_list

def mutate(integerSet, numJob):
    chromosome_list = []
    for _ in range(0, numJob):
        newChromosome = random.choice(integerSet) + random.randrange(0, 100) / 100
        while newChromosome in chromosome_list:
            newChromosome = random.choice(integerSet) + random.randrange(0, 100) / 100
        chromosome_list.append(newChromosome)
    fitness = get_fitness(integerSet, chromosome_list)
    mutated_chromosome = [chromosome_list, fitness]
    return mutated_chromosome

def display(chromosome, set):
    print()
    print('Best solution : {}'.format(chromosome[0]))
    schedule = [[] for _ in range(0, len(set))]
    for i in range(0, len(chromosome[0])):
        job = []
        job.append(i)
        job.append(chromosome[0][i])
        schedule[int(chromosome[0][i]) - 1].append(job)

    for assignment in schedule:
        assignment.sort(key=lambda x: x[1])

    for i in range(0, len(set)):
        print('Machine{}:'.format(i + 1), end='')
        for j in range(0, len(schedule[i])):
            print(' {} '.format(schedule[i][j][0]+1), end='')
        print(' / ', end='')
    print('\nBest makespan : {}'.format(chromosome[1]))

def geneticAlgorithm(machineSet, numChromosomes, numJobs):
    global numIteration
    bestSchedule_list = generateParents(machineSet, numChromosomes, numJobs)
    minMakespan = min(bestSchedule_list, key = lambda x: x[1])[1]
    bestSchedule = bestSchedule_list[bestSchedule_list.index(min(bestSchedule_list, key = lambda x: x[1]))]
    count = 0
    while count < numIteration:
        child_list = generateChild(bestSchedule_list)
        newMakespan = min(child_list, key = lambda x: x[1])[1]
        if newMakespan < minMakespan:
            print('Makespan has improved : {} -> {}'.format(minMakespan, newMakespan))
            minMakespan = newMakespan
            bestSchedule_list = child_list
            bestSchedule = bestSchedule_list[bestSchedule_list.index(min(bestSchedule_list, key=lambda x: x[1]))]
            count = 0
        else:
            bestSchedule_list = child_list
            bestSchedule = bestSchedule_list[bestSchedule_list.index(min(bestSchedule_list, key=lambda x: x[1]))]
            count += 1
    return bestSchedule

if __name__ == '__main__':
    numIteration = 1000
    machineSet = [1, 2, 3]
    numChromosomes = 100
    numJobs = 10
    processTime = generateProcessTimes(1, 100, numJobs)
    setupTime = generateSetupTimes(1, 30, numJobs)

    finalSchedule = geneticAlgorithm(machineSet, numChromosomes, numJobs)

    display(finalSchedule, machineSet)




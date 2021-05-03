from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import numpy

import matplotlib.pyplot as plt
import seaborn as sns

import knapsack
from utils import processing_str_lst

# Genetic Algorithm constants:
POPULATION_SIZE = 50
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 1


def processing_data_genetic_algorithm(process_lst):
    lst_processed = processing_str_lst(process_lst)

    items = []
    for i in range(2, int(lst_processed[0]) + 2):
        items.append((f"{i - 2}", int(lst_processed[i].split()[0]), int(lst_processed[i].split()[1])))

    capacities = int(lst_processed[1])

    return items, capacities

def initData(items, capacities):
    knapsack_init = knapsack.Knapsack01Problem(items, capacities)
    return knapsack_init


def run(items, capacities):
    # set the random seed:
    knapsack_init = initData(items, capacities)
    RANDOM_SEED = 19522081
    random.seed(RANDOM_SEED)

    toolbox = base.Toolbox()

    # create an operator that randomly returns 0 or 1:
    toolbox.register("zeroOrOne", random.randint, 0, 1)

    # define a single objective, maximizing fitness strategy:
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # create the Individual class based on list:
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # create the individual operator to fill up an Individual instance:
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, len(knapsack_init))

    # create the population operator to generate a list of individuals:
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


    # fitness calculation
    def knapsackValue(individual):
        return knapsack_init.getValue(individual), # return a tuple


    toolbox.register("evaluate", knapsackValue)

    # genetic operators:mutFlipBit

    # Tournament selection with tournament size of 3:
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Single-point crossover:
    toolbox.register("mate", tools.cxTwoPoint)

    # Flip-bit mutation:
    # indpb: Independent probability for each attribute to be flipped
    toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/len(knapsack_init))

    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print best solution found:
    best = hof.items[0]
    print("-- Best Ever Individual = ", best)
    print("-- Best Ever Fitness = ", best.fitness.values[0])

    knapsack_init.printItems(best)

    # extract statistics:
    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    # plot statistics:
    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max / Average Fitness')
    plt.title('Max and Average fitness over Generations')
    plt.savefig(f'{a}.png')

from random import uniform, choice, choices
from operator import attrgetter


def get_weights(rankings):
    """
    Args:
        rankings: list of ranked individuals.

    Returns:
        weights: the weight (importance) of each individual, according to its position in the rank. """
    denominator = sum(rankings)
    denominator = float(denominator)
    weights = [float(e) / denominator for e in rankings]
    return weights


def qsort(inlist, reverse=False):
    """ implementation of a quick sort algorithm """
    if not inlist:
        return []
    else:
        pivot = inlist[0]
        lesser = qsort([x for x in inlist[1:] if x.fitness < pivot.fitness], reverse)
        greater = qsort([x for x in inlist[1:] if x.fitness >= pivot.fitness], reverse)
        if reverse:
            return greater + [pivot] + lesser
        else:
            return lesser + [pivot] + greater


def ranking_sel(population):
    """Ranking selection implementation.

    Args:
        population (Population): The Population we want to select from.

    Returns:
        Individual: Best individual in the rank."""
    if population.optim == "max":
        # Store all individuals in the population and sort them by their fitness
        # since it is a maximization problem, the 1st position will be the one with the lowest fitness
        # and the nth position will be the one with the highest fitness
        individuals = population.get_individuals()
        sorted_individuals = qsort(individuals)
        # Creating a list with the individual's ranking position, according to their indexes (after sorted)
        ranking = [i + 1 for i in range(len(individuals))]
        # Getting their weights, according to their ranking (the higher their fitness,
        # the higher the probability of being selected)
        weights = get_weights(ranking)

        # Choosing the individual, randomly, according to its weight (probability)
        individual = choices(sorted_individuals, weights=weights, k=1)
        individual = individual[0]

        return individual

    elif population.optim == "min":
        # Store all individuals in the population and sort them by their fitness
        # since it is a minimization problem, the 1st position will be the one with the highest fitness
        # and the nth position will be the one with the lowest fitness
        individuals = population.get_individuals()
        sorted_individuals = qsort(individuals, reverse=True)
        # Creating a list with the individual's ranking position, according to their indexes (after sorted)
        ranking = [i + 1 for i in range(len(individuals))]
        # Getting their weights, according to their ranking (the lower their fitness,
        # the higher the probability of being selected)
        weights = get_weights(ranking)

        # Choosing the individual, randomly, according to its weight (probability)
        individual = choices(sorted_individuals, weights=weights, k=1)
        individual = individual[0]

        return individual

    else:
        raise Exception("No optimization specified (min or max).")


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Sum total fitness
    total_fitness = sum([i.fitness for i in population])

    if population.optim == "max":
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        # Calculating the probability of being selected, according to their fitness value
        probs = [float(total_fitness) / float(i.fitness) for i in population]
        total_probs = sum(probs)
        # Since it is a minimization problem, we need to make the probabilities of being selected,
        # proportional to the total probability (so, now, the proportions add up to 1)
        # Notice that, the lower the fitness value, the higher the probability of being selected
        proportions = [float(prob) / float(total_probs) for prob in probs]
        # Get a 'position' on the wheel
        spin = uniform(0, 1)
        position = 0
        # Find individual in the position of the spin
        for i in range(len(population)):
            position += proportions[i]
            if position > spin:
                return population[i]

    else:
        raise Exception("No optimization specified (min or max).")


def tournament(population, size=3):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """
    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]

    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")

from random import randint, sample, choice


def template_mutation(individual):
    """[summary]

    Args:
        individual ([type]): [description]

    Returns:
        [type]: [description]
    """
    return individual


# This mutation method will not be applied to our problem
def binary_mutation(individual):
    """Binary mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """
    mut_point = randint(0, len(individual) - 1)

    if individual[mut_point] == 0:
        individual[mut_point] = 1
    elif individual[mut_point] == 1:
        individual[mut_point] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")

    return individual


def swap_mutation(individual):
    """Swap mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py
    Returns:
        grid: Mutated Individual
    """
    # Choosing one possible grid
    grid_index = choice(range(9))
    # Accessing the chosen grid, by its index value
    grid = individual.get_item_grid(grid_index)
    # Get two mutation points
    mut_points = sample(range(len(grid)), 2)

    # Swap them
    grid[mut_points[0]], grid[mut_points[1]] = grid[mut_points[1]], grid[mut_points[0]]

    individual.set_item_grid(grid_index, grid)

    return individual


def inversion_mutation(individual):
    """Inversion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Choosing one possible grid
    grid_index = choice(range(9))
    # Accessing the chosen grid, by its index value
    grid = individual.get_item_grid(grid_index)
    # Position of the start and end of substring
    mut_points = sample(range(len(individual)), 2)
    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    # Invert for the mutation
    grid[mut_points[0]:mut_points[1]] = grid[mut_points[0]:mut_points[1]][::-1]
    individual.set_item_grid(grid_index, grid)
    return individual

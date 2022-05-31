from random import randint, sample, uniform


# Note: we are introducing this function in the crossover script, since, due to our representation and
# problem definition, we are assuming all crossover operations will happen per grid (i.e., for each 3x3
# matrix composed of only unique values). As such, we need to access each grid, and the representation of
# the individuals in done in the format of rows.
def get_grids(matrix):
    """ returns a 9x9 matrix,
    where each list is a grid (3x3 matrix) of
    self.representation (instead of a row) """
    grid = [[] for i in range(9)]
    for i in range(9):
        for j in range(9):
            if i < 3 and j < 3:
                grid[0].append(matrix[i][j])
            elif i < 3 and 2 < j < 6:
                grid[1].append(matrix[i][j])
            elif i < 3 and 5 < j:
                grid[2].append(matrix[i][j])
            elif 2 < i < 6 and j < 3:
                grid[3].append(matrix[i][j])
            elif 2 < i < 6 and 2 < j < 6:
                grid[4].append(matrix[i][j])
            elif 2 < i < 6 and 5 < j:
                grid[5].append(matrix[i][j])
            elif 5 < i and j < 3:
                grid[6].append(matrix[i][j])
            elif 5 < i and 2 < j < 6:
                grid[7].append(matrix[i][j])
            elif 5 < i and 5 < j:
                grid[8].append(matrix[i][j])
    return grid


"""def template_co(p1, p2):
    [summary]

    Args:
        p1 ([type]): [description]
        p2 ([type]): [description]

    Returns:
        [type]: [description]
    

    return offspring1, offspring2"""


def single_point_co(rep1, rep2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring_rep1 = []
    offspring_rep2 = []

    for i in range(len(rep1)):
        # get the grid in which the crossover is taking place (1 of 9)
        p1 = rep1.get_item_grid(i)
        p2 = rep2.get_item_grid(i)
        # Offspring placeholders - None values make it easy to debug for errors
        offspring1 = [None] * len(p1)
        offspring2 = [None] * len(p1)
        # While there are still None values in offspring, get the first index of
        # None and start a "cycle" according to the cycle crossover method
        while None in offspring1:
            co_point = randint(1, len(p1) - 2)

            offspring1 = p1[:co_point] + p2[co_point:]
            offspring2 = p2[:co_point] + p1[co_point:]

        offspring_rep1 += [offspring1]
        offspring_rep2 += [offspring2]

    # Transforming the list of elements from offsprings to grids
    a = get_grids(offspring_rep1)
    rep1.set_representation(a)
    b = get_grids(offspring_rep2)
    rep2.set_representation(b)

    return rep1, rep2


def cycle_co(rep1, rep2):
    """Implementation of cycle crossover.

    Args:
        rep1 (Individual): First parent for crossover.
        rep2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    offspring_rep1 = []
    offspring_rep2 = []

    for i in range(len(rep1)):
        # get the grid in which the crossover is taking place (1 of 9)
        p1 = rep1.get_item_grid(i)
        p2 = rep2.get_item_grid(i)
        # Offspring placeholders - None values make it easy to debug for errors
        offspring1 = [None] * len(p1)
        offspring2 = [None] * len(p1)
        # While there are still None values in offspring, get the first index of
        # None and start a "cycle" according to the cycle crossover method
        while None in offspring1:
            index = offspring1.index(None)
            # alternate parents between cycles beginning on second cycle
            if index != 0:
                p1, p2 = p2, p1
            val1 = p1[index]
            val2 = p2[index]

            while val1 != val2:
                offspring1[index] = p1[index]
                offspring2[index] = p2[index]
                val2 = p2[index]
                index = p1.index(val2)

            for element in offspring1:
                if element is None:
                    index = offspring1.index(None)
                    if offspring1[index] is None:
                        offspring1[index] = p2[index]
                        offspring2[index] = p1[index]

        offspring_rep1 += [offspring1]
        offspring_rep2 += [offspring2]

    # transforming the list of elements from offsprings to grids
    a = get_grids(offspring_rep1)
    rep1.set_representation(a)
    b = get_grids(offspring_rep2)
    rep2.set_representation(b)

    return rep1, rep2


def new_PMX(x, y, co_points):
    o = [None] * len(x)

    o[co_points[0]:co_points[1]] = x[co_points[0]:co_points[1]]

    z = set(y[co_points[0]:co_points[1]]) - set(x[co_points[0]:co_points[1]])

    for i in z:
        temp = i
        index = y.index(x[y.index(temp)])
        while o[index] is not None:
            temp = index
            index = y.index(x[temp])
        o[index] = i

    while None in o:
        index = o.index(None)
        o[index] = y[index]
    return o


def pmx_co(rep1, rep2, window_size=4):
    offspring_rep1 = []
    offspring_rep2 = []
    for i in range(len(rep1)):
        p1 = rep1.get_item_grid(i)
        p2 = rep2.get_item_grid(i)

        co_points = sample(range(len(p1)), 2)
        co_points.sort()
        # to make sure we have diversity
        while co_points[1] - co_points[0] < window_size:
            co_points = sample(range(len(p1)), 2)
            co_points.sort()

        o1, o2 = new_PMX(p1, p2, co_points), new_PMX(p2, p1, co_points)
        offspring_rep1 += [o1]
        offspring_rep2 += [o2]

    a = get_grids(offspring_rep1)
    rep1.set_representation(a)
    b = get_grids(offspring_rep2)
    rep2.set_representation(b)

    return rep1, rep2


# This crossover method will not be applied to our problem
def arithmetic_co(p1, p2):
    """Implementation of arithmetic crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)
    # Set a value for alpha between 0 and 1
    alpha = uniform(0, 1)
    # Take weighted sum of two parents, invert alpha for second offspring
    for i in range(len(p1)):
        offspring1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        offspring2[i] = p2[i] * alpha + (1 - alpha) * p1[i]

    return offspring1, offspring2

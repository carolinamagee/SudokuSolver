from copy import deepcopy
from random import shuffle, choice, sample, random, randint, uniform
from operator import attrgetter


class Individual:
    def __init__(
            self,
            init_sol,
            representation=None,
            size=81,
            valid_set=range(0, 10),
            replacement=True):
        self.init_sol = init_sol

        if representation is None:
            self.representation = self.get_representation()
        else:
            self.representation = representation

        self.fitness = self.get_fitness()

        self.size = size

        self.valid_set = valid_set

    def get_columns(self, matrix):
        """ returns a 9x9 matrix,
        where each list is a column of
        self.representation (instead of a row) """
        columns = [[0 for i in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                columns[i][j] = matrix[j][i]
        return columns

    def get_grids(self, matrix):
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

    def get_fixed_values(self):
        """ returns the count of values that are different than 0 in the initial solution,
         i.e., counts all cells initially filled """
        count = 0
        for i in range(9):
            for j in range(9):
                if self.init_sol[i][j] != 0:
                    if self.init_sol[i][j] != self.representation[i][j]:
                        count += 1
        return count

    def set_representation(self, matrix):
        self.representation = matrix

    def get_possible_values(self, grid):
        """ for each value in a 3x3 matrix (grid) returns the possible values (from 1 to 9)
        according to the ones that were already there, assuming no repetitions are allowed """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for e in grid:
            if e != 0:
                values.remove(e)
        return values

    def get_representation(self):
        """ returns the representation of an individual, according to an initial solution """
        # Getting a 9x9 matrix with only zeros
        grids_matrix = self.get_grids(self.init_sol)
        # The representation will be a list of 9 lists, meaning it will have a total of 81 elements
        representation = [[0 for i in range(9)] for i in range(9)]
        # Possible values range from 1 to 9
        for i in range(9):
            # We are maintaining the fixed values in the initial solution
            possible_values = self.get_possible_values(grids_matrix[i])
            for j in range(9):
                # If the value in the initial solution is 0, randomly assign a number between 1 and 9
                if grids_matrix[i][j] == 0:
                    value = choice(possible_values)
                    representation[i][j] = value
                    possible_values.remove(value)
                # Else keep that number
                else:
                    representation[i][j] = grids_matrix[i][j]
        return self.get_grids(representation)

    def get_fitness(self, extra=None):
        """ counts the number of duplicates in each row and column, and counts the number of numbers whose
         fixed values do not match the solution (multiplied by 10) and returns their product """
        # Initializing fitness at 1
        fitness = 1
        # Accessing all rows and columns
        rows = self.representation
        columns = self.get_columns(self.representation)

        # Counting the number of duplicates for each row
        row_dups = self.count_total_duplicates(rows)
        # Counting the number of duplicates for each column
        column_dups = self.count_total_duplicates(columns)
        # Counting the numbers of values where the fixed value (i.e., different from 0), in the initial
        # solution, is different from the one in the individual
        fix_values = self.get_fixed_values()

        # For all the cases where the previous counts is different than 0, multiply the already initialized
        # fitness by row_dups, column_dups, and fix_values * 10
        if row_dups > 0:
            fitness *= row_dups
        if column_dups > 0:
            fitness *= column_dups
        if fix_values > 0:
            fitness *= fix_values * 10
        # Forcing the global optimum to be 0, otherwise a fitness of 1 could have different meanings
        if row_dups == 0 and column_dups == 0 and fix_values == 0:
            fitness = 0
        self.fitness = fitness

        return fitness

    def get_total_duplicates(self):
        """ counts the number of duplicates in each row,
        column and returns their sum """
        dups = 0
        rows = self.representation
        columns = self.get_columns(self.representation)

        row_dups = self.count_total_duplicates(rows)
        column_dups = self.count_total_duplicates(columns)

        dups += row_dups
        dups += column_dups

        print("Duplicates in rows: " + str(row_dups))
        print("Duplicates in columns: " + str(column_dups))

        return dups

    def print_rep(self):
        """ print the representation of an individual in a matrix form, for visualization purposes"""
        str_final = '\t----------+---------+----------'

        for i in range(9):
            str_final += '\n'
            if i == 3 or i == 6:
                str_final += '\t----------+---------+----------\n'
            string_1 = "\t|  "
            for j in range(9):
                string_1 += str(self.representation[i][j]) + ' '
                if j == 2 or j == 5:
                    string_1 += ' |  '
            str_final += string_1 + ' |'
        str_final += '\n\t----------+---------+----------'
        return str_final

    def print_init_sol(self):
        """ prints the initial solution in a matrix form, for visualization purposes """
        str_final = '\t----------+---------+----------'

        for i in range(9):
            str_final += '\n'
            if i == 3 or i == 6:
                str_final += '\t----------+---------+----------\n'
            string_1 = "\t|  "
            for j in range(9):
                a = "-" if self.init_sol[i][j] == 0 else self.init_sol[i][j]
                string_1 += str(a) + ' '
                if j == 2 or j == 5:
                    string_1 += ' |  '
            str_final += string_1 + ' |'
        str_final += '\n\t----------+---------+----------'
        print(str_final)

    def count_total_duplicates(self, matrix):
        duplicates = 0
        for l in matrix:
            duplicates += 9 - len(set(l))
        return duplicates

    def get_item_grid(self, position):
        """ given a position (index in the list of grids) returns the corresponding grid """
        grids = self.get_grids(self.representation)
        return grids[position]

    def set_item_grid(self, position, value):
        """ given a position (index in the list of grids) assign the value to that position """
        grids = self.get_grids(self.representation)
        grids[position] = value
        self.representation = self.get_grids(grids)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={self.size}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.size = size
        self.individuals = []
        self.sol_size = kwargs["sol_size"]
        self.sol_replacement = kwargs["replacement"]
        self.valid_set = kwargs["valid_set"]
        self.init_sol = kwargs["init_sol"]
        self.optim = optim
        self.init_pop()

    # Initializing a new population
    def init_pop(self):
        for _ in range(self.size):
            self.individuals.append(
                Individual(
                    size=self.sol_size,
                    replacement=self.sol_replacement,
                    valid_set=self.valid_set,
                    init_sol=self.init_sol
                )
            )

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism, init_sol, global_optimum, n_elite=10,
               max_same_fitness=89):
        best_individual = None
        same_fitness_counter = 0
        old_fitness = None

        for gen in range(gens):
            new_pop = []

            # Copying the n_elite best individuals in the initial population for each generation
            if elitism:
                if self.optim == "max":
                    elite = deepcopy(sorted(self.individuals, key=attrgetter("fitness"), reverse=True))[:n_elite]
                elif self.optim == "min":
                    elite = deepcopy(sorted(self.individuals, key=attrgetter("fitness")))[:n_elite]

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2
                # Mutation
                if random() < mu_p:
                    offspring1 = mutate(offspring1)
                if random() < mu_p:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1, init_sol=init_sol))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2, init_sol=init_sol))

            # Replacing the n_elite worst individuals in the population by the n_elite best from the
            # previous population
            if elitism:
                if self.optim == "max":
                    least = sorted(new_pop, key=attrgetter("fitness"))[:n_elite]
                elif self.optim == "min":
                    least = sorted(new_pop, key=attrgetter("fitness"), reverse=True)[:n_elite]
                for i in range(n_elite):
                    new_pop.pop(new_pop.index(least[i]))
                    new_pop.append(elite[i])

            self.individuals = new_pop

            # Returning the best individual in each population
            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
                new_best_individual = deepcopy(max(self, key=attrgetter("fitness")))
                if best_individual is None or new_best_individual.fitness > best_individual.fitness:
                    best_individual = deepcopy(new_best_individual)
                    fitness = best_individual.get_fitness()
                    if fitness == global_optimum:
                        break
            elif self.optim == "min":
                print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
                new_best_individual = deepcopy(min(self, key=attrgetter("fitness")))
                if best_individual is None or new_best_individual.fitness < best_individual.fitness:
                    best_individual = deepcopy(new_best_individual)
                    fitness = best_individual.get_fitness()
                    if fitness == global_optimum:
                        break

            print(f"Generation " + str(gen + 1) + " out of " + str(gens))

            # Comparing fitness values to see if the new one is better than the previous one
            if old_fitness == new_best_individual.fitness:
                same_fitness_counter += 1
            else:
                same_fitness_counter = 0
                old_fitness = new_best_individual.fitness

            # For cases where the program gets stuck in the same fitness value for max_same_fitness
            # iterations, re-initialize the population
            if same_fitness_counter > max_same_fitness:
                print("Population renewed\n\n")
                self.individuals = []
                self.init_pop()
                same_fitness_counter = 0
                old_fitness = None

        # Returning the fitness of the best individual in all generations, its representation, and the
        # total number of duplicates per column and row
        print("Final best individual: " + str(best_individual.fitness))
        print(best_individual.print_rep())
        print("Number of duplicates of final solution: " + str(best_individual.get_total_duplicates()))

    def get_individuals(self):
        return self.individuals

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"

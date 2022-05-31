from charles import Population
from selection import ranking_sel, fps, tournament
from mutation import swap_mutation, inversion_mutation
from crossover import pmx_co, cycle_co
from data import very_easy_sol, easy_sol, intermediate_sol, hard_sol

pop = Population(
    size=1000, optim="min", sol_size=81, valid_set=range(1, 10), replacement=True, init_sol=very_easy_sol)

pop.evolve(gens=600,
           select=tournament,
           crossover=pmx_co,
           mutate=inversion_mutation,
           co_p=0.95, mu_p=0.05,
           elitism=True,
           init_sol=very_easy_sol,
           global_optimum=0)


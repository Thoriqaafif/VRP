import random

alpha = 1  # pheromone influence
beta = 2   # visibility influence
rho = 0.1  # pheromone evaporation rate
gamma = 0.1  # global pheromone decay rate
q0 = 0.9  # exploration vs exploitation threshold
num_ants = 4  # number of ants
max_iter = 100  # max iterations
N = 5  # number of nodes
LNN = 100  # some total travel time value from clustering

tau0 = 1 / (N * LNN)  # initial pheromone value
pheromone = [[tau0 for _ in range(N)] for _ in range(N)]

distances = [
    [0, 2, 9, 10, 7],
    [2, 0, 6, 4, 3],
    [9, 6, 0, 8, 5],
    [10, 4, 8, 0, 1],
    [7, 3, 5, 1, 0]
]

def calculate_visibility():
    visibility = [[0 if i == j else 1/distances[i][j] for j in range(N)] for i in range(N)]
    return visibility

visibility = calculate_visibility()

def state_transition(pheromone, visibility, current_node, unvisited):
    q = random.random()
    unvisited_list = list(unvisited)
    if q <= q0:  # Exploitation
        next_node = max(unvisited_list, key=lambda j: (pheromone[current_node][j] ** alpha) * (visibility[current_node][j] ** beta))
    else:  # Exploration
        probabilities = [(pheromone[current_node][j] ** alpha) * (visibility[current_node][j] ** beta) for j in unvisited]
        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]
        next_node = random.choices(unvisited_list, probabilities)[0]
    return next_node

def local_pheromone_update(pheromone, i, j):
    pheromone[i][j] = (1 - rho) * pheromone[i][j] + rho * tau0

def global_pheromone_update(pheromone, best_solution, best_cost, iteration_best_cost, third_best_cost):
    A = third_best_cost
    B = best_cost  # Best overall cost across all iterations
    C = iteration_best_cost  # Best cost within the current iteration

    delta_tau = ((A - B) + (A - C)) / A

    for i, j in best_solution:
        pheromone[i][j] = (1 - gamma) * pheromone[i][j] + gamma * delta_tau
        
def acs():
    best_solution = None
    best_cost = float('inf')
    third_best_cost = float('inf')

    for iteration in range(max_iter):
        all_solutions = []
        all_costs = []

        for ant in range(num_ants):
            current_node = random.randint(0, N-1)
            unvisited = set(range(N)) - {current_node}
            tour = [current_node]
            cost = 0

            while unvisited:
                next_node = state_transition(pheromone, visibility, current_node, unvisited)
                tour.append(next_node)
                cost += distances[current_node][next_node]
                local_pheromone_update(pheromone, current_node, next_node)
                current_node = next_node
                unvisited.remove(next_node)

            all_solutions.append(tour)
            all_costs.append(cost)

        # Sort costs to get best and third-best solutions in the current iteration
        sorted_costs = sorted(all_costs)
        iteration_best_cost = sorted_costs[0]  # Best solution in this iteration
        third_best_cost = sorted_costs[2] if len(sorted_costs) >= 3 else third_best_cost  # 3rd best in current iteration

        if iteration_best_cost < best_cost:
            best_cost = iteration_best_cost

        best_solution = all_solutions[all_costs.index(best_cost)]

        # Global pheromone update
        global_pheromone_update(pheromone, zip(best_solution[:-1], best_solution[1:]), best_cost, iteration_best_cost, third_best_cost)

        print(f"Iteration {iteration+1}: Best cost = {best_cost}")

    return best_solution, best_cost

# Run the ACS algorithm
best_solution, best_cost = acs()
print(f"Best solution found: {best_solution} with cost {best_cost}")
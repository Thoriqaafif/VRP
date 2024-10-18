import random

alpha = 1  # pheromone influence
beta = 2   # visibility influence
rho = 0.1  # pheromone evaporation rate
gamma = 0.1  # global pheromone decay rate
q0 = 0.9  # exploration vs exploitation threshold
num_ants = 4  # number of ants
max_iter = 100  # max iterations
nodes = [66, 277, 322] 


node_connections = {
    66: [62, 1, 101, 60, 141, 189, 174, 113, 81, 7, 12, 44, 21, 46, 28, 4, 355, 256, 235, 104],
    277: [296, 135, 106, 175, 181, 161, 205, 95, 244, 242, 39, 408, 292, 399],
    322: [376, 221, 144, 210, 264, 289, 248, 140, 400, 386, 298, 177, 333, 315, 254, 402]
}


inf = float('inf')
N = len(node_connections)
distances = [[inf for _ in range(N)] for _ in range(N)]
node_to_index = {node: i for i, node in enumerate(node_connections.keys())}


for node, connections in node_connections.items():
    for connected_node in connections:
        if connected_node in node_to_index:
            i, j = node_to_index[node], node_to_index[connected_node]
            distances[i][j] = 1  

# Initialize pheromone
LNN = 100  
tau0 = 1 / (N * LNN)  
pheromone = [[tau0 for _ in range(N)] for _ in range(N)]

def calculate_visibility():
    visibility = [[0 if i == j else 1/distances[i][j] if distances[i][j] != inf else 0 for j in range(N)] for i in range(N)]
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
    B = best_cost  
    C = iteration_best_cost 

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

        sorted_costs = sorted(all_costs)
        iteration_best_cost = sorted_costs[0] 
        third_best_cost = sorted_costs[2] if len(sorted_costs) >= 3 else third_best_cost  # 3rd best in current iteration

        if iteration_best_cost < best_cost:
            best_cost = iteration_best_cost

        best_solution = all_solutions[all_costs.index(best_cost)]

        global_pheromone_update(pheromone, zip(best_solution[:-1], best_solution[1:]), best_cost, iteration_best_cost, third_best_cost)

        print(f"Iteration {iteration+1}: Best cost = {best_cost}")

    return best_solution, best_cost


best_solution, best_cost = acs()
print(f"Best solution found: {best_solution} with cost {best_cost}")

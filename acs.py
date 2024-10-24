import random

alpha = 1  # pheromone influence
beta = 2   # visibility influence
rho = 0.1  # pheromone evaporation rate
gamma = 0.1  # global pheromone decay rate
q0 = 0.9  # exploration vs exploitation threshold
num_ants = 4  # number of ants
max_iter = 100  # max iterations

# Node untuk Depo 1 dan konsumennya
node_connections = {
    66: [189, 174, 113, 46, 62, 60, 141, 81, 44, 39, 28, 140, 101, 4, 21, 254, 12, 7, 235, 144, 1, 104],  # Depo 1 connections
    277: [408, 95, 399, 296, 135, 292, 242, 205, 244, 161, 181, 175, 106],       # Depo 2 connections
    322: [210, 386, 248, 289, 298, 264, 221, 355, 256, 315, 402, 400, 333, 177, 376],      # Depo 3 connections
    # Add other nodes based on clusters
}

inf = float('inf')
nodes = list(node_connections.keys()) + list(node_connections["Depo 1"])
N = len(nodes)






# Initialize distances with infinity (inf) as before
distances = [[inf for _ in range(N)] for _ in range(N)]

# Mengaitkan node dengan indeks
node_to_index = {node: i for i, node in enumerate(nodes)}

# Loop through the predefined distance data
for (node1, node2), distance in predefined_distances.items():
    i, j = node_to_index[node1], node_to_index[node2]
    distances[i][j] = distance  # Set the distance
    distances[j][i] = distance  # Ensure symmetry for undirected connections

# Optionally, set distance from a node to itself as 0 (if needed)
for i in range(N):
    distances[i][i] = 0



# Initialize pheromone
LNN = 100  # some constant representing average tour length
tau0 = 1 / (N * LNN)  # initial pheromone value
pheromone = [[tau0 for _ in range(N)] for _ in range(N)]

# Visibility calculation (inverse of distance)
def calculate_visibility():
    visibility = [[0 if i == j else 1/distances[i][j] if distances[i][j] != inf else 0 for j in range(N)] for i in range(N)]
    return visibility

visibility = calculate_visibility()

# State transition rule with error handling for zero probabilities
def state_transition(pheromone, visibility, current_node, unvisited):
    q = random.random()
    unvisited_list = list(unvisited)
    if q <= q0:  # Exploitation
        next_node = max(unvisited_list, key=lambda j: (pheromone[current_node][j] ** alpha) * (visibility[current_node][j] ** beta))
    else:  # Exploration
        probabilities = [(pheromone[current_node][j] ** alpha) * (visibility[current_node][j] ** beta) for j in unvisited]
        total_prob = sum(probabilities)

        if total_prob == 0:
            # Jika total_prob 0, pilih node secara acak
            next_node = random.choice(unvisited_list)
        else:
            probabilities = [p / total_prob for p in probabilities]
            next_node = random.choices(unvisited_list, probabilities)[0]

    return next_node


# Local pheromone update
def local_pheromone_update(pheromone, i, j):
    pheromone[i][j] = (1 - rho) * pheromone[i][j] + rho * tau0

# Global pheromone update
def global_pheromone_update(pheromone, best_solution, best_cost, iteration_best_cost, third_best_cost):
    A = third_best_cost
    B = best_cost  
    C = iteration_best_cost 

    delta_tau = ((A - B) + (A - C)) / A

    for i, j in best_solution:
        pheromone[i][j] = (1 - gamma) * pheromone[i][j] + gamma * delta_tau

# Ant Colony System
def acs():
    best_solution = None
    best_cost = float('inf')
    third_best_cost = float('inf')

    for iteration in range(max_iter):
        all_solutions = []
        all_costs = []

        for ant in range(num_ants):
            current_node = random.randint(0, N-1)  # Starting point
            unvisited = set(range(N)) - {current_node}  # Remaining nodes to visit
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
        
        # Sorting to find the best and third best solutions
        sorted_costs = sorted(all_costs)
        iteration_best_cost = sorted_costs[0] 
        third_best_cost = sorted_costs[2] if len(sorted_costs) >= 3 else third_best_cost

        if iteration_best_cost < best_cost:
            best_cost = iteration_best_cost
            best_solution = all_solutions[all_costs.index(best_cost)]

        global_pheromone_update(pheromone, zip(best_solution[:-1], best_solution[1:]), best_cost, iteration_best_cost, third_best_cost)

        print(f"Iteration {iteration+1}: Best cost = {best_cost}")

    return best_solution, best_cost


# Jalankan ACS untuk Depo 1
best_solution, best_cost = acs()
print(f"Best solution found: {best_solution} with cost {best_cost}")

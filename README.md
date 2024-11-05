# VRP

## How to run
install all dependency for python:
```
pip install pandas networkx matplotlib numpy
```
run python Cluster
```
python cluster.py
```
We can get `klaster.json` as a result of **simplified parallel assignment** in every depot.

### ACS (Ant Colony System)

After we got the cluster result. We can move on to ACS program.
Here are some steps to do:

1. Save the clustering result with the name `klaster.json`
2. Run `acs.ipynb` program
3. For Depo 1, here are some parameters that can be changed (if needed)

```py
alpha = 0.7  # pheromone influence
beta = 0.7   # visibility influence
rho = 0.3  # pheromone evaporation rate
gamma = 0.7  # global pheromone decay rate
q0 = 0.95  # exploration vs exploitation threshold
num_ants = 300  # number of ants
max_iter = 100  # max iterations
```

4. When the program already run successfully, you can see the result for each Depo which provides best solution, destination cost, time cost, and travel path. Here is an example of the output

```py
DEPO 1
Best solution found: [7, 12, 21, 4, 1, 60, 113, 189, 174, 141, 101, 62, 81, 39, 333, 256, 235] with distance cost 61.53822179999999 KM and time cost 1.2376871223741353 hours
Travel path: [7, 13, 12, 15, 21, 14, 8, 4, 5, 3, 2, 1, 6, 9, 20, 25, 60, 82, 84, 95, 106, 102, 97, 111, 108, 116, 113, 134, 173, 198, 189, 174, 164, 152, 141, 132, 123, 121, 118, 110, 117, 107, 101, 381, 77, 66, 62, 75, 81, 58, 56, 49, 39, 129, 157, 380, 234, 254, 390, 268, 289, 314, 383, 313, 315, 339, 333, 319, 305, 279, 256, 304, 322, 345, 346, 245, 251, 378, 377, 235]
```

5. Check also for Depo 2 and Depo 3, with similar step 3 and 4.

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import pandas as pd
import json
import numpy as np
import time as tm

# Start the timer
start_time = tm.time()

df = pd.read_excel('./dataset/Data SC ACO.xlsx', sheet_name='Sheet1')
depot_df = pd.read_csv('./dataset/depot.csv')
customer_df = pd.read_csv('./dataset/customer.csv')
df['TV'] = df['Jarak (KM)'] / df['Kecepatan']

with open('./dataset/distances.json', 'r') as f:
    distance = json.load(f)
with open('./dataset/time.json', 'r') as f:
    time = json.load(f)

def time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60

depot_df['Time Begin'] = depot_df['Time Begin'].apply(time_to_decimal)
depot_df['Time End'] = depot_df['Time End'].apply(time_to_decimal)
customer_df['Time Begin'] = customer_df['Time Begin'].apply(time_to_decimal)
customer_df['Time End'] = customer_df['Time End'].apply(time_to_decimal)

time_windows = {row['Node']: (row['Time Begin'], row['Time End']) for _, row in depot_df.iterrows()}
time_windows.update({row['Node']: (row['Time Begin'], row['Time End']) for _, row in customer_df.iterrows()})
depots = depot_df['Node'].tolist()
customers = customer_df['Node'].tolist()
G = nx.DiGraph()

for idx, row in df.iterrows():
    G.add_edge(row['Node From'], row['Node To'], 
               distance=row['Jarak (KM)'], speed=row['Kecepatan'], TV = row['TV'])

def find_two_nearest_depots(customer, depots):
    dis = []
    for i in depots:
        dis.append((distance[str(customer)][str(i)], i))
    dis.sort(key=lambda x: x[0])
    # print(dis)
    return [dis[0][1], dis[1][1]]

def find_init_customers(depots, customers):
    C = {}
    for i in depots:
        mn = (float('inf'), None)
        for j in customers:
            if distance[str(i)][str(j)] < mn[0]:
                mn = (distance[str(i)][str(j)], j)
        C[i] = [mn[1]]
    return C

def calculate_dtw(i, j, time_windows):
    li , ei = time_windows[i]
    lj, ej = time_windows[j]
    if li < ej:
        return ej - li
    elif lj < ei:
        return ei - lj
    else:
        return 0
    
def calculate_affinity(i, depots, customer_to_depot, time_windows):
    affinities = {}
    for d in depots:
        associated_customers = customer_to_depot[d]
        affinity_sum = 0
        for j in associated_customers:
            dtw = calculate_dtw(i, j, time_windows)
            tij = time[str(i)][str(j)]
            affinity_sum += np.exp(-(dtw + tij))
        affinities[d] = affinity_sum / len(associated_customers) if associated_customers else 0
    return affinities

def calculate_closeness(i, j, affinity):
    return distance[str(i)][str(j)] / affinity

def determine_urgency(customers, depots,customer_to_depot):
    urgencies = {}
    for c in customers:
        nearest_two_depots = find_two_nearest_depots(c, depots)
        # print(nearest_two_depots)
        # print(distance[str(nearest_two_depots[0])][str(c)], distance[str(nearest_two_depots[1])][str(c)])
        if len(nearest_two_depots) >= 2:
            affiniti = calculate_affinity(c,depots=depots,customer_to_depot=customer_to_depot,time_windows=time_windows)    
            urgencies[c] = calculate_closeness(nearest_two_depots[0],c, affiniti[nearest_two_depots[0]]) - calculate_closeness(nearest_two_depots[1],c, affiniti[nearest_two_depots[1]])
        # break
    sorted_dict = dict(sorted(urgencies.items(), key=lambda item: item[1],reverse=True))

    print(sorted_dict)
    max_urgent = max(urgencies, key=urgencies.get)
    return (max_urgent,urgencies[max_urgent])

C = find_init_customers(depots,customers=customers)

temp_customer=customers.copy()

persediaan = {row['Node']: row['Persediaan'] for _, row in depot_df.iterrows()}

for key, value in C.items():
    temp_customer.remove(value[0])
while temp_customer:
    # temp_depots =depots.copy()
    indx , max_urgensi_values = determine_urgency(customers=temp_customer, depots=depots,customer_to_depot=C)
    print(indx,max_urgensi_values)
    first, second = find_two_nearest_depots(indx,depots)
    print(first,second)
    permintaan =  int(customer_df[customer_df['Node'] == indx]['Permintaan'].iloc[0])

    if persediaan[first] >= permintaan:
        C[first].append(indx)
        persediaan[first] -= permintaan
    elif persediaan[second] >= permintaan:
        C[second].append(indx)
        persediaan[second] -= permintaan
    else:
        for i in depots:
            if i != first and i != second:
                C[i].append(indx)
        
    print("Permintaan : ", permintaan)
    for i in persediaan:
        print(persediaan[i],type(persediaan[i]))
    print(temp_customer)
    temp_customer.remove(indx)
    print(temp_customer)

end_time = tm.time()
elapsed_time = end_time - start_time
print(f"Computation Time: {elapsed_time:.2f} seconds")
print("C", C)



with open("klaster.json", "w") as json_file:
    json.dump(C, json_file, indent=4)
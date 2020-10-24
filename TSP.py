from ortools.linear_solver import pywraplp
import numpy as np

"""
The program takes the input data, which is a m x m matrix that store the distance between each pair of nodes
(data[i,j] = distance from node i to node j), and returns the optimal solution to travel from one node through
every other nodes (each node is visited only once) and then return to the first node with minimum travel distance.

Since there is no point in traveling from one node to itself, data[i,i] should be a very big positive number for 
all i.
"""

def TSP(data: np.array):
    #Create subsets:
    nodes = len(data)
    sub = []
    for i in range(2**nodes):
        bina = bin(i)[2:].zfill(nodes)
        bina = bina[::-1]
        sub.append([t for t in range(nodes) if bina[t] == '1'])

    #Creat solver:
    solver = pywraplp.Solver.CreateSolver('TSP', 'CBC')
    inf = solver.infinity()

    #Create variables:
    var = {}
    for i in range(nodes):
        for j in range(nodes):
            var[i,j]= solver.IntVar(0, inf, 'a' + str(i) + str(j))

    #Set constraints for going through all nodes:
    for i in range(nodes):
        constraint = solver.Constraint(1, inf)
        for j in range(len(data[0])):
            constraint.SetCoefficient(var[i,j],1)

    #Set constraints for not looping throughout the journey:
    for k in sub:
        if len(k) == 0:
            continue
        for j in range(len(k)):
            constraint = solver.Constraint(0, 1)
            for i in range(len(k)):
                constraint.SetCoefficient(var[i, j], 1)

    #Set objective:
    objective = solver.Objective()
    for i in range(nodes):
        for j in range(len(data[0])):
            objective.SetCoefficient(var[i,j], float(data[i,j]))
    objective.SetMinimization()

    #Solve it:
    solver.Solve()

    #Print solution:
    sol = np.zeros(data.shape)
    exac = []
    for i in range(nodes):
        for j in range(len(data[0])):
            sol[i,j] = var[i,j].solution_value()
            if sol[i,j] == 1:
                exac.append(str(i) + ' -> ' + str(j))
    solstr = exac.pop(0)
    while exac:
        for connection in exac:
            if solstr[-1] == connection[0]:
                solstr += connection[1:]
                exac.remove(connection)
    print()
    print('The optimal solution is:')
    print(sol)
    print()
    print('To be exact:')
    print(solstr)
    print()
    print('The shortest path is:')
    print(objective.Value())


TSP(np.array([[9999,34,12,13],[23,9999,34,98],[45,12,9999,23],[23,45,23,9999]]))

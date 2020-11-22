import numpy as np
from ortools.sat.python import cp_model

def tsp_time(N, time_windows, time, distance):
    """

    :param N: number of customers
    :param time_windows: list of tuples (early, late, d) for each customer
    :param time: time cost matrix
    :param distance: distance cost matrix
    :return:
    """
    #Create model:
    model = cp_model.CpModel()

    # Create variables:
    var = []
    for i in range(N+1):
        var.append([])
        for j in range(N+1):
            var[i].append(model.NewBoolVar('x' + str(i) + str(j)))
    var = np.array(var)

    #Create subtours:
    sub = []
    for i in range(2 ** (N)):
        bina = bin(i)[2:].zfill(N+1)
        bina = bina[::-1]
        sub.append([t+1 for t in range(N) if bina[t] == '1'])
    # sub.pop()
    # sub.pop(0)

    # Set constraints for going through all nodes:
    for i in range(N+1):
        model.Add(np.sum(var[i, :]) == 1)

    #Set constraints for not looping:
    for i in range(N+1):
        model.Add(np.sum(var[:, i]) == 1)

    #Set constraints for not containing subtours
    for s in sub:
        subvar = []
        if len(s) >= 2:
            for i in s:
                for j in s:
                    subvar.append(var[i,j])
            model.Add(0 <= sum(subvar) <= len(s)-1)

    #Set time windows constraints:



    #Minimize the distance cost:
    model.Minimize(np.sum(var*distance))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        #Print the solution:
        sol = np.zeros((N+1, N+1))
        exac = []
        for i in range(N+1):
            for j in range(N+1):
                sol[i, j] = solver.Value(var[i,j])
                if sol[i, j] == 1:
                    exac.append(str(i) + ' -> ' + str(j))
        solstr = exac.pop(0)
        while exac:
            for connection in exac:
                if solstr[-1] == connection[0]:
                    solstr += connection[1:]
                    exac.remove(connection)
        print('The shortest path is:')
        print(solstr)
        print('Minimum of objective function:', solver.ObjectiveValue())
    elif status == cp_model.INFEASIBLE:
        print("No feasible solution found.")

if __name__ == '__main__':
    data = open('data_samples_mini_projects/miniproject-14/data.txt', 'r')
    N = int(data.readline())
    time_constraints = [[0,0,0]]
    time_cost = []
    distance_cost = []
    for i in range(N):
        time_constraints.append(data.readline().replace('\n', '').replace('\t', ' ').split())
    time_constraints = np.array(time_constraints, dtype = 'int')
    for i in range(N+1):
        time_cost.append(data.readline().replace('\n', '').replace('\t', ' ').split())
    time_cost = np.array(time_cost, dtype = 'int')
    for i in range(N+1):
        distance_cost.append(data.readline().replace('\n', '').replace('\t', ' ').split())
    for i in range(N+1):
        for j in range(N+1):
            if i == j:
                distance_cost[i][j] = 99999
    distance_cost = np.array(distance_cost, dtype = 'int')

    tsp_time(N, time_constraints, time_cost, distance_cost)
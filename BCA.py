import numpy as np
from ortools.linear_solver import pywraplp
N = 13
T = 3
slots = np.array([3,3,4,3,4,3,3,3,4,3,3,4,4])
pref = np.array([[1,0,1,1,1,0,0,0,1,0,1,0,0],[1,1,0,1,0,1,1,1,1,0,0,0,0],[0,1,1,1,0,0,0,1,0,1,0,1,1]])
conflict = np.array([[0,2],[0,4],[0,8],[1,4],[1,10],[3,7],[3,9],[5,11],[5,12],[6,8],[6,12]])

# for t in range(T):
# 	print('teacher ',t)
# 	for i in range(N):
# 		if pref[t,i]==1:
# 			print(i)
# 	print('--------')

def BCA(slots, pref, conflict, T):
	N = len(slots)
	solver = pywraplp.Solver.CreateSolver('BCA', 'CBC')
	inf = solver.infinity()

	#Initiate variables:
	var = {}
	for i in range(T):
		for j in range(N):
			var[i,j] = solver.IntVar(0, 1, 'x' + str(i) + str(j))
	Y = solver.IntVar(0, int(np.sum(slots)), 'Y')

	#Create constraints:

	#Exactly one teacher for each course:
	for j in range(N):
		constraint1 = solver.Constraint(1,1)
		for t in range(T):
			constraint1.SetCoefficient(var[t,j], 1)

	#No conflicting course:
	for k in conflict:
		for t in range(T):
			constraint2 = solver.Constraint(0,1)
			for kc in range(2):
				constraint2.SetCoefficient(var[t, k[kc]], 1)

	#Preference:
	for t in range(T):
		for j in range(N):
			constraint3 = solver.Constraint(0, int(pref[t,j]))
			constraint3.SetCoefficient(var[t, j], 1)

	#That one constraint:
	for t in range(T):
		constraint4 = solver.Constraint(-inf, 0)
		for j in range(N):
			constraint4.SetCoefficient(var[t,j], float(slots[j]))
		constraint4.SetCoefficient(Y, -1)

	#Create Objective:
	objective = solver.Objective()
	objective.SetCoefficient(Y, 1)
	objective.SetMinimization()

	#Solve it:
	solver.Solve()

	#Print solution:
	sol = np.zeros((T,N))
	for i in range(T):
		for j in range(N):
			sol[i, j] = var[i, j].solution_value()
	assignment = {}
	for t in range(T):
		assignment['teacher' + str(t+1)] = []
		for j in range(N):
			if int(sol[t,j]) == 1:
				assignment['teacher' + str(t+1)].append(j+1)

	return (sol, np.sum(sol*slots, axis = 1, keepdims = True), assignment, objective.Value())
	

solution = BCA(slots, pref, conflict, T)
print()
print('The BCA should be:')
print(solution[0])
print()
print('The load is')
print(solution[1])
print()
print('The exact assignment is:')
for t in solution[2].keys():
	print(t + ' teaches courses number ' + str(solution[2][t]).replace('[', '').replace(']', ''))
print()
print('The average teaching load of a teacher is', solution[3])
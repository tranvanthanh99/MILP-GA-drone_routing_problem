from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
import math
from utils import print_solution

tour= [0]
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['locations'] = [
        {
            "node": 0,
            "coordinate": (0, 0),
            "label": "D",
            "demand": 0
        },
        {
            "node": 1,
            "coordinate": (15, 28),
            "label": "R",
            "demand": 0
        },
        {
            "node": 2,
            "coordinate": (0, 15),
            "label": "P",
            "demand": 2
        },
        {
            "node": 3,
            "coordinate": (7, 20),
            "label": "P",
            "demand": 5
        },
        {
            "node": 4,
            "coordinate": (25, 20),
            "label": "P",
            "demand": 4
        },
        {
            "node": 5,
            "coordinate": (25, 39),
            "label": "P",
            "demand": 3
        },
        {
            "node": 6,
            "coordinate": (11, 41),
            "label": "P",
            "demand": 1
        },
        {
            "node": 7,
            "coordinate": (17, 9),
            "label": "P",
            "demand": 3
        },
        {
            "node": 8,
            "coordinate": (10, 21),
            "label": "P",
            "demand": 2
        },
        {
            "node": 9,
            "coordinate": (4, 27),
            "label": "P",
            "demand": 2
        },
        {
            "node": 10,
            "coordinate": (26, 0),
            "label": "P",
            "demand": 2
        },
    ]
    data['num_locations'] = 11
    data['max_payload'] = 8
    data['max_energy'] = 60
    data['gamma0'] = 2   # energy for takeoff and landing
    data['gamma'] = 1     # energy for takeoff and landing with w package
    data['p0'] = 1       # energy to fly one distance unit
    data['p'] = 1         # energy to fly one distance unit with 1 pakage

    return data

def get_distance(v1, v2):
    return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)

def get_energy_consumsed(data, i, j, w):
    gamma0 = 0.95   # energy for takeoff and landing
    gamma = 0.1     # energy for takeoff and landing with w package
    p0 = 0.95       # enery to fly one distance unit
    p = 0.2         # energy to fly one distance unit with 1 pakage
    sigma_ij = get_distance(data['locations'][i]['coordinate'], data['locations'][j]['coordinate']) # distance i -> j
    return gamma0 + (gamma * w) + sigma_ij * (p0 + (p * w))

def print_route(x, start, num_locations):
    if  type(x[0][0]) != float:
        for i in range (num_locations):
            for j in range(num_locations):
                x[i][j] = x[i][j].solution_value()
    last = True
    for i in range(num_locations):
        for j in range(num_locations):
            if x[i][j] > 0:
                last = False
                break
    if last: 
        print("-> 0")
    for i in range(num_locations):
        if x[start][i] > 0:
            tour.append(i)
            print(f"\n{start} " if start == 0 else f"-> {start} ", end="")
            x[start][i] = x[start][i] - 1
            print_route(x, i, num_locations,)

def MILP():
    solver = pywraplp.Solver("lp", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # solver = pywraplp.Solver.CreateSolver('SCIP')
    data = create_data_model()

    # initial 2D array to store vars
    # number of times when drone moves from i -> j
    x = [[0 for i in range(data['num_locations'])]
         for j in range(data['num_locations'])]
    # energy of drone when drone moves from i -> j
    e = [[0 for i in range(data['num_locations'])]
         for j in range(data['num_locations'])]
    # number of packages when drone moves from i -> j 
    w = [[0 for i in range(data['num_locations'])]
         for j in range(data['num_locations'])]

    # init variables
    # intvar
    for i in range(data['num_locations']):
        for j in range(data['num_locations']):
            x[i][j] = solver.IntVar(0, solver.Infinity(), f'x[{i}][{j}]')
            e[i][j] = solver.IntVar(0, solver.Infinity(), f'e[{i}][{j}]')
            w[i][j] = solver.IntVar(0, solver.Infinity(), f'w[{i}][{j}]')

    ### degree constraints
    for i in range(2, data['num_locations']):
        degreeConstraint = solver.Constraint(1, 1)
        for j in range(data['num_locations']):
            if i != j:
                degreeConstraint.SetCoefficient(x[j][i], 1)

    for i in range(data['num_locations']):
        degreeConstraint = solver.Constraint(0, 0)
        for j in range(data['num_locations']):
            if i != j:
                degreeConstraint.SetCoefficient(x[j][i], 1)
                degreeConstraint.SetCoefficient(x[i][j], -1)

    degreeConstraint = solver.Constraint(-solver.Infinity(), 1)
    for j in range(1, data['num_locations']):
        degreeConstraint.SetCoefficient(x[0][j], -1)

    ### demand constraints
    demandConstraint = solver.Constraint(0, 0)
    for i in range(1, data['num_locations']):
        if i != 0:
            demandConstraint.SetCoefficient(w[i][0], 1)

    for i in range(2, data['num_locations']):
        demandConstraint = solver.Constraint(data['locations'][i]['demand'], data['locations'][i]['demand'])
        for j in range(data['num_locations']):
            if i != j:
                demandConstraint.SetCoefficient(w[j][i], 1)
                demandConstraint.SetCoefficient(w[i][j], -1)

    demandConstraint = solver.Constraint(0, 0)
    for i in range(data['num_locations']):
        if i != 1:
            demandConstraint.SetCoefficient(w[i][1], 1)
            demandConstraint.SetCoefficient(w[1][i], -1)

    for i in range(data['num_locations']):
        for j in range(data['num_locations']):
            if i != j:
                demandConstraint = solver.Constraint(-solver.Infinity(), 0)
                demandConstraint.SetCoefficient(w[i][j], 1)
                demandConstraint.SetCoefficient(x[i][j], -data['max_payload'])

    ### energy constraints
    # for i in range(0, 1):
    #     for j in range(data['num_locations']):
    #         if i != j:
    #             energyConstraint = solver.Constraint(0, 0)
    #             energyConstraint.SetCoefficient(e[i][j], 1)
    #             energyConstraint.SetCoefficient(x[i][j], -data['max_energy'])

    # for i in range(2, data['num_locations']):
    #     for j in range(data['num_locations']):
    #         if i != j:
    #             energyConstraint = solver.Constraint(-solver.Infinity(), 0)
    #             energyConstraint.SetCoefficient(e[i][j], 1)
    #             energyConstraint.SetCoefficient(x[i][j], -data['max_energy'])

    # for i in range(2, data['num_locations']):
    #     energyConstraint = solver.Constraint(0, 0)
    #     for j in range(data['num_locations']):
    #         if i != j:
    #             energyConstraint.SetCoefficient(e[j][i], -1)
    #             energyConstraint.SetCoefficient(e[i][j], 1)
    #             energyConstraint.SetCoefficient(x[j][i], data['gamma0'])
    #             energyConstraint.SetCoefficient(w[j][i], data['gamma'])
    #             energyConstraint.SetCoefficient(x[j][i], (data['p0'] * get_distance(data['locations'][j]['coordinate'], data['locations'][i]['coordinate'])))
    #             energyConstraint.SetCoefficient(w[j][i], (data['p'] * get_distance(data['locations'][j]['coordinate'], data['locations'][i]['coordinate'])))

    # for i in range(data['num_locations']):
    #     for j in range(data['num_locations']):
    #         if i != j:
    #             energyConstraint = solver.Constraint(-solver.Infinity(), 0)
    #             energyConstraint.SetCoefficient(e[i][j], -1)
    #             energyConstraint.SetCoefficient(x[i][j], data['gamma0'])
    #             energyConstraint.SetCoefficient(w[i][j], data['gamma'])
    #             energyConstraint.SetCoefficient(x[i][j], (data['p0'] * get_distance(data['locations'][i]['coordinate'], data['locations'][j]['coordinate'])))
    #             energyConstraint.SetCoefficient(w[i][j], (data['p'] * get_distance(data['locations'][i]['coordinate'], data['locations'][j]['coordinate'])))




    ### objective
    objective = solver.Objective()
    for i in range(data['num_locations']):
        for j in range(data['num_locations']):
            if i != j:
                objective.SetCoefficient(x[i][j], get_distance(data['locations'][i]['coordinate'], data['locations'][j]['coordinate']))
            # print(get_distance(data['locations'][i]['coordinate'], data['locations'][j]['coordinate']), f"d[{i}][{j}]")
    objective.SetMinimization()

    ### get value
    status = solver.Solve()
    print("Problem solved in %f milliseconds" % solver.wall_time())
    print("Problem solved in %d iterations" % solver.iterations())

    ### print solution
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution: ")
        print("Objective value =", solver.Objective().Value())
        print("\nAdvange usage:")
        for i in range(data['num_locations']):
            for j in range(data['num_locations']):
                if x[i][j].solution_value() != 0:
                    print(f"{x[i][j].name()} = {x[i][j].solution_value()}")
        # for i in range(data['num_locations']):
        #     for j in range(data['num_locations']):
        #         if e[i][j].solution_value() != 0:
        #             print(f"{e[i][j].name()} = {e[i][j].solution_value()}")

        tol = 0
        for i in range(data['num_locations']):
            for j in range(data['num_locations']):
                if x[i][j].solution_value() != 0:
                    tol = tol + get_distance(data['locations'][i]['coordinate'], data['locations'][j]['coordinate'])
        print(f"total distance: {tol}")
        print_route(x, 0, data['num_locations'])
        print_solution(data['locations'], tour, title = "MILP")
    else:
        print("Not have optimal solution")


if __name__ == "__main__":
    MILP()

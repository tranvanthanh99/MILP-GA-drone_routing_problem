# encoding: utf-8
import sys
import random
import math
from utils import print_solution

vrp = {}

vrp['capacity'] = 8.00
vrp['nodes'] = [
	{'label' : 'depot', 'demand' : 0, "coordinate": (0, 0)},
	{'label' : 'node1', 'demand' : 2.00, "coordinate": (0, 15)},
	{'label' : 'node2', 'demand' : 5.00, "coordinate": (7, 20)},
	{'label' : 'node3', 'demand' : 4.00, "coordinate": (25, 20)},
	{'label' : 'node4', 'demand' : 3.00, "coordinate": (25, 39)},
	{'label' : 'node5', 'demand' : 1.00, "coordinate": (11, 41)},
	{'label' : 'node6', 'demand' : 3.00, "coordinate": (17, 9)},
	{'label' : 'node7', 'demand' : 2.00, "coordinate": (10, 21)},
	{'label' : 'node8', 'demand' : 2.00, "coordinate": (4, 27)},
	{'label' : 'node9', 'demand' : 2.00, "coordinate": (26, 0)},
]


def distance(n1, n2):
	dx = n2['coordinate'][0] - n1['coordinate'][0]
	dy = n2['coordinate'][1] - n1['coordinate'][1]
	return math.sqrt(dx * dx + dy * dy)

def fitness(p):
	# The first distance is from depot to the first node of the first route
	s = distance(vrp['nodes'][0], vrp['nodes'][p[0]])
	# Then calculating the distances between the nodes
	for i in range(len(p) - 1):
		prev = vrp['nodes'][p[i]]
		next = vrp['nodes'][p[i + 1]]
		s += distance(prev, next)
	# The last distance is from the last node of the last route to the depot
	s += distance(vrp['nodes'][p[len(p) - 1]], vrp['nodes'][0])
	return s

def adjust(p):
	# Adjust repeated
	repeated = True
	while repeated:
		repeated = False
		for i1 in range(len(p)):
			for i2 in range(i1):
				if p[i1] == p[i2]:
					haveAll = True
					for nodeId in range(len(vrp['nodes'])):
						if nodeId not in p:
							p[i1] = nodeId
							haveAll = False
							break
					if haveAll:
						del p[i1]
					repeated = True
				if repeated: break
			if repeated: break
	# Adjust capacity exceed
	i = 0
	s = 0.0
	cap = vrp['capacity']
	while i < len(p):
		s += vrp['nodes'][p[i]]['demand']
		if s > cap:
			p.insert(i, 0)
			s = 0.0
		i += 1
	i = len(p) - 2
	# Adjust two consective depots
	while i >= 0:
		if p[i] == 0 and p[i + 1] == 0:
			del p[i]
		i -= 1

def GA():
	popsize = int(sys.argv[1])
	iterations = int(sys.argv[2])

	pop = []

	# Generating random initial population
	for i in range(popsize):
		p = list(range(1, len(vrp['nodes'])))
		random.shuffle(p)
		pop.append(p)

	for p in pop:
		adjust(p)


	# Running the genetic algorithm
	for i in range(iterations):
		nextPop = []
		# Each one of this iteration will generate two descendants individuals
		# to guarantee same population size, this will iterate half population size times
		for j in range(int(len(pop) / 2)):
			# Selecting randomly 4 individuals to select 2 parents by a binary tournament
			parentIds = set()
			while len(parentIds) < 4:
				parentIds |= {random.randint(0, len(pop) - 1)}
			parentIds = list(parentIds)
			# Selecting 2 parents with the binary tournament
			parent1 = pop[parentIds[0]] if fitness(pop[parentIds[0]]) < fitness(pop[parentIds[1]]) else pop[parentIds[1]]
			parent2 = pop[parentIds[2]] if fitness(pop[parentIds[2]]) < fitness(pop[parentIds[3]]) else pop[parentIds[3]]
			# Selecting two random cutting points for crossover, with the same points (indexes) for both parents, based on the shortest parent
			cutIdx1, cutIdx2 = random.randint(1, min(len(parent1), len(parent2)) - 1), random.randint(1, min(len(parent1), len(parent2)) - 1)
			cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)
			# Doing crossover and generating two children
			child1 = parent1[:cutIdx1] + parent2[cutIdx1:cutIdx2] + parent1[cutIdx2:]
			child2 = parent2[:cutIdx1] + parent1[cutIdx1:cutIdx2] + parent2[cutIdx2:]
			nextPop += [child1, child2]
		# Doing mutation: swapping two positions in one of the individuals, with 1:15 probability
		for i in range(int(len(nextPop) / 8)):
			if random.randint(1, 15) == 1:
				randIdx = random.randint(0, len(nextPop) - 1)
				ptomutate = nextPop[randIdx]
				i1 = random.randint(0, len(ptomutate) - 1)
				i2 = random.randint(0, len(ptomutate) - 1)
				ptomutate[i1], ptomutate[i2] = ptomutate[i2], ptomutate[i1]
		# Adjusting individuals
		for p in nextPop:
			adjust(p)
		# Updating population generation
		pop = nextPop

		# print average cost of population
		f = 0
		for p in pop:
			f = f + fitness(p)
		print(f'COST: {f / len(pop)}')


	# Selecting the best individual, which is the final solution
	better = None
	bf = float('inf')
	for p in pop:
		f = fitness(p)
		if f < bf:
			bf = f
			better = p


	# Printing the solution
	print('\nROUTE:')
	print('depot', end="")
	for nodeIdx in better:
		print(" ->", vrp['nodes'][nodeIdx]['label'], end="")
	print('-> depot')
	print(f'COST: {bf}')

	tour = [0] + better + [0]
	print_solution(vrp['nodes'], tour, title="GA")



if __name__ == "__main__":
	GA()
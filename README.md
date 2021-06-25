# MILP-GA-drone_routing_problem

### Bibliography

This repository contains python code of a MILP model and genetic algorithm to solve the Drone Routing Problem with capacity and energy constraints. The MILP model was implemented from this paper: 
```Rabta, Boualem; Wankmüller, Christian; Reiner, Gerald  (2018). A drone fleet model for last-mile distribution in disaster relief operations. International Journal of Disaster Risk Reduction. https://sci-hub.mksa.top/10.1016/j.ijdrr.2018.02.020```

## Running the program

### Genetic algorithm

1. drone_GA1.py: genetic algorithm to solve problem with capacity constraints only.
2. drone_GA2.py: genetic algorithm to solve problem with capacity and energy constraints.


```bash
python drone_GA1.py [population-size] [number-of-iterations] 
```

```bash
python drone_GA2.py [population-size] [number-of-iterations] 
```

Required params:

1. ```[population-size]``` is an integer positive number that specifies the number of individuals of each generation in the genetic algorithm;
2. ```[number-of-iterations]``` is an integer positive number that specifies the number of iterations (population generations) of the genetic algorithm.

### MILP

```bash
python drone_MILP.py
```

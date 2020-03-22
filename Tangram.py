# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:50:07 2020

@author: Admin
"""
from typing import List, Tuple
from itertools import combinations_with_replacement, permutations, product
from collections import defaultdict as ddict
from Quadratic import Quadratic
import numpy as np
import matplotlib.pyplot as plt
import time

def angle_combinations(angles: List[int]) -> List[Tuple[int]]:
    """
    Generate all combinations of angles 45, 90, 135 which can create an n-gon
    with n <= 8.
    """
    combinations = set()
    angle_sum = 180*6       # Sum of angles 180*(n-2), n=8
    for combination in combinations_with_replacement(angles, 8):
        if sum(combination) == angle_sum:
            combination = tuple(sorted(filter(lambda x: x != 180, combination)))
            combinations.add(combination)
    return sorted(list(combinations), key=lambda x: len(x))     # Sort by n

def angle_unique_cycles(combination: Tuple[int]) -> List[Tuple[int]]:
    """
    Generate all permutations and remove extra cycles
    Note: Inefficient algorithm, but ok since small size
    """
    cycles = []
    for permutation in permutations(map(str, combination)):
        # Check for cyclity
        for cycle in cycles:
            if "".join(permutation) in "".join(3*cycle):
                break
        else:
            # Rotate cycle so that 90 angle is first if possible
            if "90" in permutation:
                index = permutation.index("90")
                permutation = permutation[index:] + permutation[:index]
            cycles.append(permutation)
    return [tuple(map(int, cycle)) for cycle in cycles]  # Cast back to ints

def polygon_area(x: Quadratic, y: Quadratic) -> Quadratic:
    """
    Returns the area of a polygon
    """
    area = Quadratic(0)
    for i in range(len(x)-1):
        area += x[i]*y[i+1]
        area -= x[i+1]*y[i]
    return Quadratic(0.5)*abs(area)
    
def simulation(cycle: Tuple[int], dist: List[Quadratic]) -> List[List[Quadratic]]:
    """
    Runs the simulation on a specific cycle. All possible distances between 
    angles (given in dist) are tested. Could be improved quite a lot by using 
    a backtracking approach, but we can get away with an inefficient approach
    since n is quite small.
    """
    # Generate sin and cos functions
    sin = { 0: Quadratic(0),     45: Quadratic(0, 0.5),
            90: Quadratic(1),    135: Quadratic(0, 0.5),
            180: Quadratic(0),   225: Quadratic(0, -0.5),
            270: Quadratic(-1),  315: Quadratic(0, -0.5)}
    cos = {}
    for key, val in sin.items():
        cos[(key+270)%360] = val
    
    # Run the simulation
    res = []
    for d in product(dist, repeat=len(cycle)):
        for rational in [True, False]:
            simulation_step(res, sin, cos, d, rational)
    return res

def simulation_step(res, sin, cos, d, rational) -> None:
    """
    Runs the simulation for one step.
    """
    # Define starting point
    x, y = Quadratic(1), Quadratic(0)
    cur_angle = 0
    # Generate shape
    X, Y = [x], [y]
    for i, angle in enumerate(cycle):
        if angle in [45, 135]:
            rational = not rational
        if rational:
            dst = Quadratic(d[i])
        else:
            dst = Quadratic(0, 0.5*d[i])
        x += dst*cos[(cur_angle+180-angle)%360]
        y += dst*sin[(cur_angle+180-angle)%360]
        
        # Terminate early by convexity
        if y < Quadratic(0):
            break
        
        X.append(x)
        Y.append(y)
        cur_angle += 180-angle
    # Valid shape will have area = 1, and will end where we started!    
    if polygon_area(X, Y) == Quadratic(1) and x == Quadratic(1)  \
                                                and y == Quadratic(0):
        res.append([X, Y])

def graph_results():
    """
    Graph results to a suitable grid whilst preserving scale. Settings are just
    hardcoded to suit the results
    """
    res = np.load('data.npy')
    fig, axis = plt.subplots(6, 4, sharex=True, sharey=True, figsize=[25.6,19.2])
    fig.subplots_adjust(wspace=-0.7, hspace=0.1)
    for i in range(len(res)):
        axis[i//4, i%4].plot(*res[i])
    for ax in fig.get_axes():
        ax.label_outer()
        ax.axis('scaled')
    fig.show()

if __name__ == "__main__":
    # Find possible combinations on angles which still form a valid n-gon
    angles = [45, 90, 135, 180]
    combinations = angle_combinations(angles)
    
    # Generate possible cycles of angles
    size = 0
    counter = 0
    all_cycles = ddict(list)
    print("Possible combinations of angles:")
    for combination in combinations:
        if len(combination) > size:
            size = len(combination)
            print("\nn = {}:\n".format(size))
        print("Angles = {}".format(combination))
        cycles = angle_unique_cycles(combination)
        all_cycles[size] += cycles
        counter += len(cycles)
        print("Unique cycles = {}\n".format(cycles))
    print("Total number of unique cycles to check = {}\n".format(counter))
    
    # List of possible distances, same list used for edges of form c*sqrt(2), 
    # but multiplied by sqrt(2)/2.
    dist = [0.5, 1, 1.5, 2, 2.5, 3]
    
    # Run the simulation for n-gons with n <= n_max. n_max <= 8 
    t1 = time.time()
    res = []
    n_max = 8
    for key in range(3, n_max+1):
        print("Starting on {}".format(key))
        for cycle in all_cycles[key]:
            if key > 4:
                res += simulation(cycle, dist[:len(dist)-2])
            else:
                res += simulation(cycle, dist)
    res = np.array(res)
    print("Found {} possible polygons!".format(len(res)))
    np.save('data', res) # Save the data
    t2 = time.time()
    graph_results()
    
    print("Took {} to complete!".format(t2-t1))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
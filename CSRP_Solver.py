#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 23:18:25 2022

@author: alejandroguzman
"""

import time
import sys
import numpy as np
import random

def initialize():
    size = 0
    depot = 1
    matrix_cost = np.zeros([size, size])
    matrix_demand = np.zeros([size, size])
    capacity = 0
    count = 0
    list = []
    file_name = "gdb1.dat"
    time_limit = 90
    seed = random.randint(1, 10)
    f = open('gdb1.dat', 'r')
    for line in f:
      line.split()
      list.append(line)
      count = count + 1
    vertice = list[1]
    size = int(vertice[11:]) + 1
    matrix_cost = np.zeros([size, size])
    matrix_demand = np.zeros([size, size])
    i = list[2]
    depot = int(i[8])
    re = list[3]
    RE = int(re[17:])
    nre = list[4]
    NRE = int(nre[21:])
    c = list[6]
    capacity=int(c[11:])

    for j in range(9, count - 1):
      data = list[j]
      x = int(data.split()[0])
      y = int(data.split()[1])
      cost = int(data.split()[2])
      demand = int(data.split()[3])
      matrix_cost[y][x] = cost
      matrix_cost[x][y] = cost
      matrix_demand[x][y] = demand
      matrix_demand[y][x] = demand

    for i in range(1, size):
      for j in range(1, size):
        if i!=j and matrix_cost[i][j] == 0:
          matrix_cost[i][j] = np.inf
    return matrix_cost, matrix_demand, depot, size, capacity

def floyd():
    init_response = initialize()
    min_cost_matrix = init_response[0]
    size = init_response[3]
    for k in range(1, size):
      for i in range(1, size):
        for j in range(1, size):
          if (min_cost_matrix[i][j] > min_cost_matrix[i][k] + min_cost_matrix[k][j]):
            min_cost_matrix[i][j] = min_cost_matrix[i][k] + min_cost_matrix[k][j]
    return min_cost_matrix

def demand_cost():
    init_response = initialize()
    size = init_response[3]
    original_cost = init_response[0]
    matrix_demand = init_response[1]
    matrix_cost = floyd()
    for i in range(1, size):
      for j in range(1, size):
        if matrix_demand[i][j] != 0:
          matrix_cost[i][j] = original_cost[i][j]
    return matrix_cost

def path_scan():
    orgnl_cost = demand_cost()
    init_response = initialize()
    matrix_demand = init_response[1]
    depot = init_response[2]
    size = init_response[3]
    Capacity = init_response[4]
    test = floyd()
    rev_arc = []
    arc = []
    Route = []
    Sum = 0
    S = []
    tS = []
    tRoute = []
    tCost = []
    Cost = []
    tLoad = []
    Load = []

    for i in range(1, size):
      for j in range(i, size):
        if i != j and matrix_demand[i][j] != 0:
          arc.append([i, j])
          rev_arc.append([j, i])
    task = arc + rev_arc
    
    while True:
        s = []
        route = []
        load = 0
        cost = 0
        i = depot
        
        while True:
            d = np.inf

            if not task: 
              break

            for u in task:
              if load + matrix_demand[u[0]][u[1]] < Capacity:             
                if test[i][u[0]] < d:
                  nu = u
                  d = test[i][u[0]]
                                 
            if d != np.inf:
                smallk=(nu[0], nu[1])
                s.append(smallk)
                route.append(nu)
                task.remove(nu)
                task.remove(nu[::-1])
                load = load + matrix_demand[nu[0]][nu[1]]
                cost = cost + orgnl_cost[nu[0]][nu[1]] + d              
                i = nu[1]
                
            if d == np.inf or not task: 
              break

        # Si la ruta no arranca en 1, agregar arco que simboliza ir desde 1 al punto inicial y sumar costo mínimo 
        if s[0][0] != 1: 
          s.insert(0, (str('1...'), s[0][0]))
          cost = cost + test[depot][int(s[0][1])]
        # Si la ruta no finaliza en 1, agregar arco que simboliza ir desde el punto final a 1 y sumar costo minimo 
        cost = cost + test[i][depot]
        if nu[1] != depot:
          sRollback = (str(nu[1]) + '...', depot)
          s.append(sRollback)
        S.append(s)
        Route.append(route)
        Load.append(load)
        Cost.append(cost)

        if not task:
           break

    if sum(Cost) <= sum(tCost) or sum(tCost) == 0:
      tCost = Cost
      tLoad = Load
      tRoute = Route
      tS = S
    for k in tCost:
      Sum = k + Sum
    TOTAL_COST = Sum
    return tS, Sum

def s_format():
    s, q = path_scan()
    for route in s:
       print("Ruta", s.index(route) + 1, ":", (",".join(str(d) for d in route).replace(" ", "")))
    print("Costo total:", int(q))

s_format()
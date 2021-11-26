#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 14:49:03 2021

@author: Jonathan
"""
from mpi4py import MPI
import numpy as np
import time

start_time = time.time()
pe = MPI.COMM_WORLD.Get_rank()
comm = MPI.COMM_WORLD
rows, columns = 250, 1000
max_temp_error = 0.01
temp = np.empty((rows + 2,columns + 2))
temp_last = np.empty((rows + 2,columns + 2))
cores = comm.Get_size()

def initialize_temperature(tm, pe):
    tm[:,:] = 0

    #Set right side boundery condition
    for i in range(rows + 1):
        tm[i,columns + 1] = (100/columns) * i + pe * (100/cores)

    #Set bottom boundery condition
    if pe == (cores - 1):
        for i in range(columns + 1):
             tm[rows + 1,i] = (100/columns) * i


def output(data):
    if pe == 0:
       data.tofile("comb_plate.out")


initialize_temperature(temp_last,pe)

max_iter = 0
if pe == 0:
    max_iter = int(input("Maximum iterations:"))
    
    
max_iter = comm.bcast(max_iter, root = 0)

dt = 100
max_dt = 100
iter = 1

while (max_dt > max_temp_error) and (iter < max_iter):
    if pe == 0:
        comm.Send(temp_last[-2,:], dest = pe + 1)
        comm.Recv(temp_last[-1,:], source = pe + 1)
    elif pe < cores - 1:
        comm.Send(temp_last[1,:], dest = pe - 1)
        comm.Recv(temp_last[0,:], source = pe - 1)
        comm.Send(temp_last[-2,:], dest = pe + 1)
        comm.Recv(temp_last[-1,:], source = pe + 1)
    elif pe == cores - 1:
        comm.Send(temp_last[1,:], dest = pe - 1)
        comm.Recv(temp_last[0,:], source = pe - 1)

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            temp[i,j] = 0.25 * (temp_last[i + 1,j] + temp_last[i - 1,j] +
                                           temp_last[i,j+1] + temp_last[i,j-1])


    dt = 0
    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            dt = max(dt,(temp[i,j] - temp_last[i,j]))
            temp_last[i,j] = temp [i,j]
    comm.barrier()
    max_dt = comm.allreduce(dt, op=MPI.MAX)
    iter += 1    
    
    
print("Converged at", iter, "iterations")
temp_last = temp_last[1:-1,1:-1]
temp_last = np.array(comm.gather(temp_last, root = 0))
comm.barrier()
output(temp_last)

end_time = time.time()
print(end_time - start_time)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
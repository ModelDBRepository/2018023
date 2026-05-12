"""write_vec(filename, neuron_vec)
Writes the neuron_vec to filename in an igorpro and matlab compatible format (text)
"""
import numpy as np
from neuron import h

def write_vec(filename, neuron_vec):
    vec = np.array(neuron_vec)
    with open(filename, "w") as f:
        for i in range(len(vec)):
            f.write(f"{vec[i]}\n")

def read_vec(filename):
    """vec = read_vec(filename)"""
    with open(filename, "r") as f:
        data=f.readlines()
    vec_string = np.array(data)
    vec = vec_string.astype(float)
    return vec

def save_clipboard(filename, delimiter=','):
    vec_x = np.array(h.hoc_obj_[1])
    vec_y = np.array(h.hoc_obj_[0])
    with open(filename, "w") as f:
        for i in range(len(vec_x)): # assume x and y same length
            f.write(f"{vec_x[i]}{delimiter}{vec_y[i]}\n")

    
        


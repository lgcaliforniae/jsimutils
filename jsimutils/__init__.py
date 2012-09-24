# Copyright (C) 2012 Joseph Swisher <jaswish@berkeley.edu>
#
#

"""
A set of utilities for dealing with porous material simulations.

This module contains some functions and scripts for preparing and
analyzing simulations of porous materials, mainly with the simulation
package COTA.
"""

__version__ = '0.1'
__author__ = 'Joseph Swisher'
__email__ = 'jaswish@berkeley.edu'

import os.path
import json
from math import sqrt
modpath = os.path.dirname(__file__)

atomic_masses = {"H": 1.008, "He": 4.002602, "Li": 6.94, "Be": 9.012182, "B": 10.81, "C": 12.011, 
                 "N": 14.007, "O": 15.999, "F": 18.9984032, "Ne": 20.1797, "Na": 22.98976928, 
                 "Mg": 24.3050, "Al": 26.9815386, "Si": 28.085, "P": 30.973762, "S": 32.06, 
                 "Cl": 35.45, "Ar": 39.948, "K": 39.0983, "Ca": 40.078, "Sc": 44.955912, 
                 "Ti": 47.867, "V": 50.9415, "Cr": 51.9961, "Mn": 54.938045, "Fe": 55.845, 
                 "Co": 58.933195, "Ni": 58.6934, "Cu": 63.546, "Zn": 65.38, "Ga": 69.723, 
                 "Ge": 72.63, "As": 74.92160, "Se": 78.96, "Br": 79.904, "Kr": 83.798, 
                 "Rb": 85.4678, "Sr": 87.62, "Y": 88.90585, "Zr": 91.224, "Nb": 92.90638, 
                 "Mo": 95.96, "Tc": 98, "Ru": 101.07, "Rh": 102.90550, "Pd": 106.42, 
                 "Ag": 107.8682, "Cd": 112.411, "In": 114.818, "Sn": 118.710, "Sb": 121.760, 
                 "Te": 127.60, "I": 126.90447, "Xe": 131.293, "Cs": 132.9054519, "Ba": 137.327, 
                 "La": 138.90547, "Ce": 140.116, "Pr": 140.90765, "Nd": 144.242, "Pm": 145, 
                 "Sm": 150.36, "Eu": 151.964, "Gd": 157.25, "Tb": 158.92535, "Dy": 162.500, 
                 "Ho": 164.93032, "Er": 167.259, "Tm": 168.93421, "Yb": 173.054, "Lu": 174.9668, 
                 "Hf": 178.49, "Ta": 180.94788, "W": 183.84, "Re": 186.207, "Os": 190.23, 
                 "Ir": 192.217, "Pt": 195.084, "Au": 196.966569, "Hg": 200.59, "Tl": 204.38, 
                 "Pb": 207.2, "Bi": 208.98040, "Po": 209, "At": 210, "Rn": 222, 
                 "Fr": 223, "Ra": 226, "Ac": 227, "Th": 232.03806, "Pa": 231.03588, 
                 "U": 238.02891, "Np": 237, "Pu": 244, "Am": 243, "Cm": 247, 
                 "Bk": 247, "Cf": 251, "Es": 252, "Fm": 257, "Md": 258, 
                 "No": 259, "Lr": 262, "Rf": 265, "Db": 268, "Sg": 271, 
                 "Bh": 270, "Hs": 277, "Mt": 276, "Ds": 281, "Rg": 280, 
                 "Cn": 285, "Uut": 284, "Fl": 289, "Uup": 288, "Lv": 293, 
                 "Uus": 294, "Uuo": 294}

def load_charges(library_name):
    libname = '.'.join([library_name, 'json'])
    libpath = os.path.join(modpath, 'parameters', 'charges', libname)
    if os.path.isfile(libpath):
        with open(libpath, mode='r') as f:
            charges = json.load(f)
    else:
        print "charge library %s not found!" % libname
        charges = None
    try:
        charges.pop('_comment')
    except:
        pass
    return charges

def load_molecule(molecule_name):
    libname = '.'.join([molecule_name, 'json'])
    libpath = os.path.join(modpath, 'parameters', 'molecules', libname)
    if os.path.isfile(libpath):
        with open(libpath, mode='r') as f:
            molecule = json.load(f)
    else:
        print "molecule library %s not found!" % libname
        molecule = None
    try:
        molecule.pop('_comment')
    except:
        pass
    return molecule

def load_force_field(ff_name):
    libname = '.'.join([ff_name, 'json'])
    libpath = os.path.join(modpath, 'parameters', libname)
    if os.path.isfile(libpath):
        with open(libpath, mode='r') as f:
            ff = json.load(f)
    else:
        print "force field library %s not found!" % libname
        ff = None
    try:
        ff.pop('_comment')
    except:
        pass
    return ff

def mean(array):
    """Returns the arthimetic mean of a list of numbers.
    """
    return float(sum(array))/len(array)

def stddev(array):
    """Returns ths sample standard deviation of a list of numbers.
    """
    xbar = mean(array)
    xsq = sum([ (x-xbar)**2 for x in array])
    return sqrt(xsq/(len(array)-1))


    

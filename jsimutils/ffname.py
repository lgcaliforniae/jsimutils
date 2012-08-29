#!/usr/bin/env python

import sys
from optparse import OptionParser
import unitcell
import cssr
import pdb
from bonds import bondlengths

def main():
    
    parser = OptionParser(usage="usage %prog [options] filename", version="%prog 0.1")

    parser.add_option("-r", "--rcut", action="store",
                                        dest="rcut",
                                        type="float",
                                        default=3.0,
                                        help="rough filter cuf off [default: 3.0 Ang.]")

    parser.add_option("-p", "--prefix", action="store",
                                        dest="prefix",
                                        type="string",
                                        default="mof",
                                        help="material type prefix [default: mof]")

    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        print "please supply a structure file!"
        return 2
    
    structure_file = args[0]
    
    (root, ext) = structure_file.split('.')
      
    if ext == 'cssr':
        atoms, uc = cssr.load_cssr(structure_file)
        natoms = len(atoms)
        distance = unitcell.abc_distance_func(uc)
    else:
        print "Please provide a .cssr"
        return 2
    
    for i in range(0,natoms):
        atoms[i]['elem'] = atoms[i]['name']

    for i in range(0,natoms-1):
        for j in range(i+1,natoms):
            r = distance(atoms[i]['abc'], atoms[j]['abc'])
            try:
                atoms[i]['r'].append( (r,j) )
            except KeyError:
                atoms[i]['r'] = [ (r,j) ]
            try:
                atoms[j]['r'].append( (r,i) )
            except KeyError:
                atoms[j]['r'] = [ (r,i) ]

    for i in range(0,natoms):
        R = [ (r,atoms[j]['elem']) for (r,j) in atoms[i]['r'] if r < options.rcut ]
        bonded = [ elem for (r, elem) in R if r < bondlengths['%s-%s' % (atoms[i]['elem'], elem) ] ]
        bonded.sort()
        atoms[i]['name'] = '%s_%s_%s' % (options.prefix, atoms[i]['elem'], ''.join(bonded))

    cssr.write_cssr('named_%s.cssr' % root, atoms, uc)
    
    return 0


if __name__ == '__main__':
    r = main()
    sys.exit(r)


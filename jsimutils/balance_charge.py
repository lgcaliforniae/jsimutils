
import sys
import os.path
from optparse import OptionParser
import decimal
import cPickle
import cssr

def main():
    parser = OptionParser(usage="usage %prog [options] filename", version="%prog 0.1")

    parser.add_option("-p", "--precision", action="store",
                                           dest="precision",
                                           type="int",
                                           default=3,
                                           help="decimal places to balance charge at [default: 3]")

    parser.add_option("-L", "--library", action="store",
                                         dest="library",
                                         type="string",
                                         default="zif_charges.pkl",
                                         help="pickle library of charges")

    (options, args) = parser.parse_args()	
    
    structure_file = os.path.abspath(args[0])
    
    if not os.path.isfile(structure_file):
        print "please supply a structure file!"
        return 2
    
    # configure decimal math
    #decimal.getcontext().prec = options.precision
    decimal.getcontext().prec = 8
    
    # load charge library
    with open(options.library, mode='r') as f:
        master_charges = cPickle.load(f)
    
    # load the structure
    atoms, uc = cssr.load_cssr(structure_file)

    atom_names = [ atom['name'] for atom in atoms ]
    types = set(atom_names)
    
    stoichiometry = [ atom_names.count(key) for key in types ]
    charges = []
    for key in types:
        try:
            charges.append(decimal.Decimal(master_charges[key]['charge']))
        except KeyError:
            print 'atom type %s not found!' % key
            return 3
    
    total_charge = decimal.Decimal(0.0)
    print 'Original charges'
    for t,n,q in zip(types, stoichiometry, charges):
        total_charge += n*q
        print '%14s %8.4f x %4d = %12.4f' % (t,q,n,n*q)
    
    #decimal.getcontext().prec = options.precision+1
    
    delta = -total_charge/sum(stoichiometry)
    
    print '=============================================\ntotal charge: %31.4f' % total_charge
    
    print '\n\ndelta = %f\n\n' % delta
    print 'New charges'
    total_charge = decimal.Decimal(0.0)
    for t,n,q in zip(types, stoichiometry, charges):
        print '%14s %8.4f x %4d = %12.6f' % (t,q+delta,n,n*(q+delta))
        total_charge += n*(q+delta)
    
    print '=============================================\ntotal charge: %31.8f' % total_charge
    
    return 0

if __name__ == '__main__':
	r = main()
	sys.exit(r)




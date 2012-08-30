
import sys
import os.path
from optparse import OptionParser
import decimal
import jsimutils
import cssr

def balance(library, structure_file):
    """Balance the charge of a structure.
        
    Given a structure in COTA cssr format and a set of preliminary charges,
    adjust the charges by a small delta to ensure the structure is 
    electrically neutral.
    
    """    
    if not os.path.isfile(structure_file):
        print "please supply a structure file!"
        return 2
    
    # configure decimal math
    decimal.getcontext().prec = 8
    decimal_place = decimal.Decimal('1.000')
    
    # load charge library
    master_charges = jsimutils.load_charges(library)
    if master_charges is None:
        return 2
    
    # load the structure
    atoms, uc = cssr.load_cssr(structure_file)

    atom_names = [ atom['name'].split('_', 1)[-1] for atom in atoms ]
    types = set(atom_names)
    
    stoichiometry = [ atom_names.count(key) for key in types ]
    charges = []
    for key in types:
        try:
            charges.append(decimal.Decimal(master_charges[key]))
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
    
    # compute the residual charge when enforcing 3 decimal places
    residual = decimal.Decimal(0.0)
    for n,q in zip(stoichiometry, charges):
        qprime = decimal.Decimal(q+delta).quantize(decimal_place)
        residual += n*(qprime)
    
    resid_delta = [ decimal.Decimal(0.000) for t in types ]
    if decimal.Decimal('0').compare(residual) is not decimal.Decimal('0'):
        # check to see if the charge can be evenly divided by any particular pseudo atom type
        for (i,n) in enumerate(stoichiometry):
            x = residual/n
            if  x.same_quantum(decimal_place):
                resid_delta[i] = x                  
                break
            else:
                pass        
    
    # Print final summary
    total_charge = decimal.Decimal(0.0)
    final_charges = {}
    print 'New charges'
    for t,n,q,r in zip(types, stoichiometry, charges, resid_delta):
        qprime = decimal.Decimal(q + delta - r).quantize(decimal_place)
        print '%14s %8.4f x %4d = %12.6f' % (t,qprime,n,n*qprime)
        total_charge += n*qprime    
        final_charges[t] = qprime
    
    print '=============================================\ntotal charge: %31.6f' % total_charge
    
    return final_charges

if __name__ == '__main__':
    parser = OptionParser(usage="usage %prog [options] filename", version="%prog 0.1")
    parser.add_option("-L", "--library", action="store",
                                 dest="library",
                                 type="string",
                                 default="cbac",
                                 help="library of charges [default: cbac]")
    (options, args) = parser.parse_args()	
    r = balance(options.library, os.path.abspath(args[0]))
    if isinstance(r, {}):
        sys.exit(0)
    else:
        sys.exit(r)


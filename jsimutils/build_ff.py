
import sys
import os.path
from optparse import OptionParser
import cssr
import balance_charge

def build(lj_file, charge_file, structure_file):
    
    # load the structure
    atoms, uc = cssr.load_cssr(structure_file)
    atom_names = [ atom['name'] for atom in atoms ]
    types = set(atom_names)
    elements = [ x.split('_')[1] for x in types ]
    
    directory = True
    with open(pseudoatomf, mode='wt') as f:
        f.write('#number of pseudo atoms\n%d\n' % (len(types)+2))
        f.write('#type      print   as  scatt mass       charge  B-factor radii  connectivity\n')
        f.write('UNIT       yes      H     H  1.0        1.0     1.0      1.0    0\n')
        f.write('DUMMY      no       H     H  1.0        0.0     1.0      1.0    0\n')
        for t,e in zip(types, elements):
            f.write('%14s  yes  %6s  %4s  %.5f  %.5f  1.0   1.0   0\n' % (t, e, e, mass[e], charge[t]))
    
    with open(mixingrulef, mode='wt') as f:
        f.write('# general rule for shifted vs truncated\nshifted\n')
        f.write('# general rule tailcorrections\nno\n')
        f.write('# number of defined interactions\n%d\n' % len() )
        f.write('# type interaction\n')
        for t in fftypes:
            f.write('%14s   lennard-jones   %.4f  %.4f\n' % (t, parameters[t]['sigma'], parameters[t]['epsilon']))
        f.write('# general mixing rule for Lennard-Jones\nLorentz-Berthelot\n')
    
    return 0

if __name__ == '__main__':
    parser = OptionParser(usage="usage %prog [options] filename", version="%prog 0.1")
    parser.add_option("-q", "--charges", action="store",
                                        dest="charges",
                                        type="string",
                                        help="pickle library of charges")
    parser.add_option("-d", "--dispersive", action="store",
                                        dest="dispersive",
                                        type="string",
                                        help="pickle library of LJ parameters")
    (options, args) = parser.parse_args()
    r = balance(options.dispersive, options.charges, os.path.abspath(args[0]))
    sys.exit(r)


import sys
import os
from optparse import OptionParser
import jsimutils
import cssr
import balance_charge

def build(fwk_ff, fwk_charges, molecules, structure_file):
    """Build a force field directory for COTA
    
    Using a selection of standard options, build a force
    field directory for a given structure.
    
    """
    charges = balance_charge.balance(fwk_charges, structure_file)

    # load the structure
    atoms, uc = cssr.load_cssr(structure_file)
    atom_types = set([ atom['name'] for atom in atoms ])
    elements = [ t.split('_')[1] for t in atom_types ]
    
    ff = jsimutils.load_force_field(fwk_ff)
    if ff is None:
        return 2
    
    mol_ff = {}
    for m in molecules:
        v = jsimutils.load_molecule(m)
        if v is None:
            return 2
        mol_ff.update(v)
    
    (fwk, ext) = os.path.basename(structure_file).split('.')
    try:
        os.mkdir(fwk)
    except OSError:
        pass
    
    with open(os.path.join(fwk,'pseudo_atoms.def'), mode='wt') as f:
        f.write('#number of pseudo atoms\n%d\n' % (len(atom_types)+len(mol_ff)+2) )
        f.write('#type      print   as  scatt mass       charge  B-factor radii  connectivity\n')
        f.write('UNIT            yes      H     H  1.0        1.0     1.0      1.0    0\n')
        f.write('DUMMY           no       H     H  1.0        0.0     1.0      1.0    0\n')
        for t,elem in zip(atom_types, elements):
            mass = jsimutils.atomic_masses[elem]
            charge = charges[t.split('_', 1)[-1]]
            f.write('%-14s  yes  %6s  %4s  %.4f  %.4f  1.0   1.0   0\n' % (t, elem, elem, mass, charge))
        for (t,v) in mol_ff.items():
            f.write('%-14s  yes  %6s  %4s  %.4f  %.4f  1.0   1.0   0\n' % (t, v['element'], v['element'], v['mass'], v['charge']))
    
    for (t,v) in mol_ff.items():
        if "sigma" not in v or "epsilon" not in v:
            mol_ff.pop(t)
    
    with open(os.path.join(fwk,'force_field_mixing_rules.def'), mode='wt') as f:
        f.write('# general rule for shifted vs truncated\nshifted\n')
        f.write('# general rule tailcorrections\nno\n')
        f.write('# number of defined interactions\n%d\n' % (len(atom_types)+len(mol_ff)) )
        f.write('# type interaction\n')
        for t,e in zip(atom_types, elements):
            f.write('%-14s   lennard-jones   %.4f  %.4f\n' % (t, ff[e]['sigma'], ff[e]['epsilon']))
        for (t,v) in mol_ff.items():
            f.write('%-14s   lennard-jones   %.4f  %.4f\n' % (t, v['sigma'], v['epsilon']))
        f.write('# general mixing rule for Lennard-Jones\nLorentz-Berthelot\n')
    
    with open(os.path.join(fwk,'force_field.def'), mode='wt') as f:
        f.write('# rules to overwrite\n0\n')
        f.write('# number of defined interactions\n1\n')
        f.write('# type      type2       interaction\n')
        f.write('UNIT        UNIT        lennard-jones      1.0       1.0\n')
        f.write('# mixing rules to overwrite\n0\n')
    
    return 0

if __name__ == '__main__':
    parser = OptionParser(usage="usage %prog [options] filename", version="%prog 0.1")
    parser.add_option("-q", "--charges", action="store", dest="charges", type="string", default="cbac",
                      help="inital charges [default: cbac]")
    parser.add_option("-f", "--framework", action="store", dest="framework", type="string", default="uff",
                      help="model LJ parameters for framework atoms [default: uff]")
    parser.add_option("-m", "--molecule", action="append", dest="molecules", default=[],
                      help="molecule models [default: none]")
    (options, args) = parser.parse_args()
    r = build(options.framework, options.charges, options.molecules, os.path.abspath(args[0]))
    sys.exit(r)


from optparse import OptionParser
import unitcell

def load_cssr(cssrfile):
    with open(cssrfile, mode='rt') as f:
        lines = f.readlines()
    uc = {}
    uc['length'] = tuple([ float(x) for x in lines[0].rstrip('\n').split()[0:3] ])
    uc['angle']= tuple([ float(x) for x in lines[1].rstrip('\n').split()[0:3] ])
    atoms = []
    for line in lines[4:]:
        try:
            [n, elem, a, b, c, rest] = line.split(None, 5)
            new = {'name': elem, 'elem': None, 'abc': (float(a),float(b),float(c))}
            atoms.append(new)
        except:
            pass
    
    return atoms, uc

def convert_to_xyz(cssrfile):
    with open(cssrfile, mode='rt') as f:
        data = [ line.rstrip('\n').split() for line in f.readlines() ]
    data = [ x for x in data if len(x) > 0 ]
    uc = {}
    uc['length'] = tuple([ float(x) for x in data[0][0:3] ])
    uc['angle'] = tuple([ float(x) for x in data[1][0:3] ])
    abctoxyz = unitcell.abctoxyz_func(uc)
    fname = cssrfile.rstrip('cssr') + 'xyz'
    with open(fname, mode='wt') as f:
        f.write('%d\n' % len(data[4:]))
        f.write('%s\n' % cssrfile)
        for line in data[4:]:
            try:
                name = line[1]
                abc = [ float(x) for x in line[2:5] ]
                xyz = abctoxyz(abc)
                f.write('%s %6.5f %6.5f %6.5f\n' % (name, xyz[0], xyz[1], xyz[2]))
            except:
                pass

    return 0

def write_cssr(cssrfile, atoms, uc):
    lines = []
    lines.append('%38.3f %8.3f %8.3f\n' % uc['length'])
    lines.append('%24.3f %8.3f %8.3f  SPGR = 1 P 1        OPT = 1\n' % uc['angle'])
    lines.append('%d    0\n' % len(atoms))
    lines.append('0 named with ffname.py :  comment\n')
    for (n,atom) in enumerate(atoms, start=1):
        lines.append('%6d%16s%10.5f%10.5f%10.5f  0  0  0  0  0  0  0  0  0.00\n' % (n, atom['name'], atom['abc'][0], atom['abc'][1], atom['abc'][2]) )

    with open(cssrfile, mode='wt') as f:
        f.writelines(lines)

    return 0


if __name__ == '__main__':
    parser = OptionParser(usage="usage %prog [options] filename", version="%prog 0.1")
    parser.add_option("--convert", action="store_true", dest="convert", default=False,
                      help="library of charges [default: cbac]")
    (options, args) = parser.parse_args()
    if options.convert:
        convert_to_xyz(args[0])
    else:
        pass



def load_pdb(pdbfile):
    with open(pdbfile, mode='rt') as f:
        lines = f.readlines()
    
    unitcell = {}
    atoms = []
    
    for line in lines:
        fields = line.rstrip('\n').split()
        if fields[0] == 'CRYST1':
            unitcell['length'] = [ float(x) for x in fields[1:4] ]
            unitcell['angle'] = [ float(x) for x in fields[4:7] ]
        elif fields[0] == 'ATOM':
            new = {'name': fields[2], 'elem': None, 'abc': None, 'xyz': tuple([ float(x) for x in fields[5:8] ])}
            elem = new['name'][0].upper()
            new['elem'] = 'Zn' if elem == 'Z' else elem
            atoms.append(new)
        else:
            pass
    
    return atoms, unitcell


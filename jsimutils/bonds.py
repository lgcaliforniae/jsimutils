
bonds = [ ('C', 'C', 1.5),
          ('C', 'O', 1.5),
          ('C', 'N', 1.5),
          ('C', 'H', 1.2),
          ('C', 'Zn', 0.1),
          ('C', 'Cl', 1.8),
          ('C', 'Cd', 0.1),
          ('C', 'Co', 0.1),
          ('C', 'Cu', 0.1),
          ('C', 'Fe', 0.1),
          ('C', 'In', 0.1),
          ('O', 'O', 1.5),
          ('O', 'N', 0.1),
          ('O', 'H', 1.2),
          ('O', 'Zn', 0.1),
          ('O', 'Cl', 0.1),
          ('O', 'Cd', 0.1),
          ('O', 'Co', 0.1),
          ('O', 'Cu', 0.1),
          ('O', 'Fe', 0.1),
          ('O', 'In', 0.1),
          ('N', 'N', 1.5),
          ('N', 'H', 1.2),
          ('N', 'Zn', 2.3),
          ('N', 'Cl', 0.1),
          ('N', 'Cd', 2.3),
          ('N', 'Co', 2.3),
          ('N', 'Cu', 2.3),
          ('N', 'Fe', 2.3),
          ('N', 'In', 2.3),
          ('H', 'H', 0.1),
          ('H', 'Zn', 0.1),
          ('H', 'Cl', 0.1),
          ('H', 'Cd', 0.1),
          ('H', 'Co', 0.1),
          ('H', 'Cu', 0.1),
          ('H', 'Fe', 0.1),
          ('H', 'In', 0.1),
          ('Zn', 'Zn', 0.1),
          ('Zn', 'Cl', 0.1),
          ('Zn', 'Cd', 0.1),
          ('Zn', 'Co', 0.1),
          ('Zn', 'Cu', 0.1),
          ('Zn', 'Fe', 0.1),
          ('Zn', 'In', 0.1),
          ('Cl', 'Cl', 0.1),
          ('Cl', 'Cd', 0.1),
          ('Cl', 'Co', 0.1),
          ('Cl', 'Cu', 0.1),
          ('Cl', 'Fe', 0.1),
          ('Cl', 'In', 0.1),
          ('Cd', 'Cd', 0.1),
          ('Cd', 'Co', 0.1),
          ('Cd', 'Cu', 0.1),
          ('Cd', 'Fe', 0.1),
          ('Cd', 'In', 0.1),
          ('Co', 'Co', 0.1),
          ('Co', 'Cu', 0.1),
          ('Co', 'Fe', 0.1),
          ('Co', 'In', 0.1),
          ('Cu', 'Cu', 0.1),
          ('Cu', 'Fe', 0.1),
          ('Cu', 'In', 0.1),
          ('Fe', 'Fe', 0.1),
          ('Fe', 'In', 0.1),
          ('Si', 'H',  0.1),
          ('Si', 'C',  1.9) ]

bondlengths = {}
for pair in bonds:
    bondlengths['%s-%s' % (pair[0],pair[1])] = pair[2]
    bondlengths['%s-%s' % (pair[1],pair[0])] = pair[2]


* Usage of jsimutils *

** Convert a cssr file to xyz **

Operate on a single file at a time.
    
    python -m jsimutils.cssr --convert {structure.cssr}


** Give the atoms in a structure a force field name **

The name has the basic structure *prefix*-*element*-*bonded atoms*. The 
program will determine the bonding based on a distance search.

    python -m jsimutils.ffname --prefix {code} {structure.cssr}
    
It should results in a file with the prefix *named_* appended to the
provided filename.


** Generate a force field for a structure **

Given a cssr file, the program can balance the charges to ensure
a neutral simulation cell and generate a COTA-compatible force field.

    python -m jsimutils.build_ff -f {framework parameters} -c {framework charges} -m {molecule 1} -m {molecule 2} {structure.cssr}
    
Framework parameters are based on the element. Available force fields: *uff*. 
The charges will be adjusted to provide a neutral framework, and the set provided will serve
as the starting point. Available charges: *cbac*. Any number of molecules can be specified,
each after it's own *-m* flag. The structure provided must already have the appropriate
force field naming.


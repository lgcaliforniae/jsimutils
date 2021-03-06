
from math import cos, sin, sqrt, radians

def abctoxyz_func(uc):
    [a,b,c] = uc['length']
    [al,be,ga] = [ radians(x) for x in uc['angle'] ]
    
    nu = sqrt(1 - cos(al)**2 - cos(be)**2 - cos(ga)**2
                    + 2*cos(al)*cos(be)*cos(ga))
    
    xtv = [ a, b*cos(ga), c*cos(be) ]
    ytv = [ 0.0, b*sin(ga), c*(cos(al)-cos(be)*cos(ga))/sin(ga) ]
    ztv = [ 0.0, 0.0, c*nu/sin(ga) ]
    
    def f(xyz):
        [x,y,z] = xyz
        xt = a*x + b*cos(ga)*y + c*cos(be)*z
        yt = b*sin(ga)*y + c*((cos(al)-cos(be)*cos(ga))/sin(ga))*z
        zt = ((c*nu)/sin(ga))*z
        return (xt, yt, zt)

    return f

def xyztoabc_func(uc):
    [a,b,c] = uc['length']
    [al,be,ga] = [ radians(x) for x in uc['angle'] ]
        
    nu = sqrt(1 - cos(al)**2 - cos(be)**2 - cos(ga)**2
                    + 2*cos(al)*cos(be)*cos(ga))
    
    atv = [ 1.0/a, -cos(ga)/(a*sin(ga)), (cos(al)*cos(ga)-cos(be))/(a*nu*sin(ga)) ]
    btv = [ 0.0, 1/(b*sin(ga)), (cos(be)*cos(ga)-cos(al))/(b*nu*sin(ga)) ]
    ctv = [ 0.0, 0.0, sin(ga)/(c*nu) ]
    
    def f(xyz):
        x = sum(map(lambda x,y: x*y, atv, xyz))
        y = sum(map(lambda x,y: x*y, btv, xyz))
        z = sum(map(lambda x,y: x*y, ctv, xyz))
        return (x, y, z)

    return f

def xyz_distance_func(uc):
    xyztoabc = xyztoabc_func(uc)
    abctoxyz = abctoxyz_func(uc)
    
    def f(p1, p2):
        dr = [ x-y for x,y in zip(p1,p2)]
        abc = xyztoabc(dr)
        dabc = [ x-nint(x) for x in abc ]
        dxyz = abctoxyz(dabc)
        return sqrt(sum([ x*x for x in dxyz ]))

    return f

def abc_distance_func(uc):
    abctoxyz = abctoxyz_func(uc)
    
    def f(abc1, abc2):
        dabc = [ x-y for x,y in zip(abc1, abc2) ]
        nint = [ -int(0.5-x) if x < 0.0 else int(0.5+x) for x in dabc ]
        dabc = [ x-y for x,y in zip(dabc, nint) ]
        dxyz = abctoxyz(dabc)
        return sqrt(sum([ x*x for x in dxyz ]))

    return f

def nint(x):
    return -int(0.5-x) if x < 0.0 else int(0.5+x)


# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from numpy import linalg as LA

import pyparticles.geometry.dist as dist

def box_intersects_sphere( b_min , b_max , c , r ):
    """
    return True if the box defined by the opposite vertices *n_max*, *b max* intersect the sphere centred in *c* with a radius *r*
    """
    
    r2 = r**2.0
    dmin = 0.0
    
    if c[0] < b_min[0] :
        dmin += ( c[0] - b_min[0] )**2.0
    elif c[0] > b_max[0]:
        dmin += ( c[0] - b_max[0] )**2.0
    
    if c[1] < b_min[1] :
        dmin += ( c[1] - b_min[1] )**2.0
    elif c[1] > b_max[1]:
        dmin += ( c[1] - b_max[1] )**2.0
    
    if c[2] < b_min[2] :
        dmin += ( c[2] - b_min[2] )**2.0
    elif c[2] > b_max[2]:
        dmin += ( c[2] - b_max[2] )**2.0
    
    return dmin <= r2


def sphere_intersect_sphere( c1 , r1 , c2 , r2 ):
    """
    returns the average intersection point if the two spheres centred in *c1* and *c2* and radius *r1*, *r2* are intersecting, else it returns *None*
    """
    d = dist.distance( c1 , c2 )
    
    if r1 + r2 >= d :
        
        u = ( c2 - c1 ) / LA.norm( c2 - c1 )
        p = ( ( c1 + u*r1 ) + ( c2 - u*r2 ) ) / 2.0
        
        return p
    else :
        return None
    
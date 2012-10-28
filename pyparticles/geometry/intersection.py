# dr14_t.meter: compute the DR14 value of the given audiofiles
# Copyright (C) 2011  Simone Riva
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

def box_intersects_sphere( b_min , b_max , c , r ):
    """
    return True if the box defined by the opposite vertices *n_max*, *b max* intersect the sphere centred in *c* with a radius *r*
    """
    
    r2 = r**2.0
    dmin = 0.0
    
    for i in range(3):
        if c[i] < b_min[i] :
            dmin += ( c[i] - b_min[i] )**2.0
        elif c[i] > b_max[i]:
            dmin += ( c[i] - b_max[i] )**2.0
        
    return dmin <= r2 
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


import time

class MyTimeFormatter( object ):
    
    def __init__(self):
        pass

    
    def to_str( self , t  ):
        
        tf = [ "%4dy " , "%3dd " , "%02dh " , "%02dm " , "%02ds " , "%07.3fms " ]
        
        days_y = 365.256363004
        sec_y = days_y * 3600 * 24
        
        years = int( t / sec_y )
        days  = int( t / (3600*24) - years*days_y )
        hr    = int( t / 3600 - days*24 - days_y*years*24 )
        minu  = int( t / 60 - hr*60 - days*(24*60) - days_y*years*24*60 ) 
        sec   = int( t - minu*60 - hr*3600 - days*(24*3600) - days_y*years*24*60*60 )
        msec  = float( 1000 * ( t - int( t ) ) )
        
        res = ""
                
        i = 0
        f = False
        for tt in list( [ years , days , hr , minu , sec , msec ] ):
            if tt > 0 or f : 
                res = res +  tf[i] % tt
                f = True
            i+=1
            
        return res

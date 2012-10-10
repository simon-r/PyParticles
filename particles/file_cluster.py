# PyParticles : Particles simulation in python
#Copyright (C) 2012  Simone Riva
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the :
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import re


class FileCluster(object):
    def __init__(self):
        pass

    def open( self , cfile ):
        if type( cfile ) is str :
            self.__f = open( cfile )
        else :
            self.__f = cfile
            
        
            
    
    def close(self):
        self.__f.close()

    def insert3( self , pset ):
        rd = True
        i = -1
        
        size = 1
        dim = 3
        
        xi = np.zeros((3))
        vi = np.zeros((3))
        
        re_flags = ( re.IGNORECASE | re.UNICODE )
        
        while rd :
            line = self.__f.readline()
            
            print( line )
            
            if line == "" :
                rd = False
                continue
            if i == -1 :
                m = re.search( r"(\d+)\s+(\d+)" , line , re_flags )
                if m != None and m.lastindex == 2:
                    size = int( m.group(1) )
                    dim  = int( m.group(2) )
                else:
                    raise
                
                reg_str = r""
                
                for j in range( 2*dim + 1 ):
                    reg_str = reg_str + "(\d*\.{0,1}\d+)\s+"
                    
                #reg_str.append( "([\w|\d|\s]+)$" )
                        
                pset.realloc( size , dim )
                    
            else :
                
                m = re.search( reg_str , line , re_flags )
                
                xi[0] = float( m.group(1) )
                xi[1] = float( m.group(2) )
                xi[2] = float( m.group(3) )
                
                pset.X[i,:] = xi
                
                
                vi[0] = float( m.group(4) )
                vi[1] = float( m.group(5) ) 
                vi[2] = float( m.group(6) )
                
                pset.V[i,:] = vi
                
                pset.M[i] = float( m.group(7) )
            
            i += 1
        
        print( "--------------" )
        print( pset.X )
        print( "--------------" )
        print( pset.V )
        print( "--------------" )
        print( pset.M )
        
    def write_out( self , X , M=None ,V=None ):
        pass




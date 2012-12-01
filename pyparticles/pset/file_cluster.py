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
import csv
import re


class FileCluster(object):
    """
    Read the data from a csv formatted file:
    
    The first row of the csv contains the size and the dim of the particles set.
    
    The other rows are the data of the perticles in the order:
    """
    
    def __init__(self):
        pass

    def open( self , cfile , mode="r" ):
        """
        Open the csv file named cfile.
        
        :param cfile: The file name
        :param mode: file mode (default reading)
        """
            
        self.__cfile = cfile
            
            
    def close(self):
        """
        Close the file
        """
        pass
        #self.__f.close()


    def insert3( self , pset ):
        """
        Insert the particles described in the file in the ParticlesSet pset
        
        :param pset: A reference to the particles set   
        """
        ff = open( self.__cfile , 'rb')
        csv_w = csv.reader( ff , delimiter=' ')
        
        i = -1
        
        dim = 0
        size = 0
        print( self.__cfile )
        #print( csv_w )
        
        label = False
        
        for row in csv_w :
            #print( row )
            if i == -1 :
                size = int(row[0])
                dim = int(row[1])
                try:
                    il = row.index( "label" )
                    label = True
                except:
                    label = False
                    
                pset.realloc( size , dim , label=il)
                
            else :
                for j in range( dim ) :
                    pset.X[i,j] = float(row[j])
                    pset.V[i,j] = float(row[j+dim])
                
                pset.M[i] = float( row[dim*2] )
                
                if label :
                    pset.label[i] = row[dim*2+1] 
                
            i+=1
            
        #print( pset.label )
        ff.close()
        #exit()
        


    def write_out( self , pset ):
        """
        Write out in the csv file the particles described in pset.
        
        :param pset: A reference to the particles set
        """
        ff = open( self.__cfile , 'wb')
        csv_w = csv.writer( ff , delimiter=' ')
        
        head = [ str(pset.size) , str(pset.dim) ]
        
        try:
            foo = pset.Q
            head.append("Charge")
        except:
            pass
        
        if pset.label != None :
            head.append( "Label" )
        
        csv_w.writerow( head )
        
        for i in range( pset.size ):
            lst = pset.get_list( i , to=float )
            csv_w.writerow( lst )
            
        ff.close()




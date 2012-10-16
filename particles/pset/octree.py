# PyParticles : Particles simulation in python
# Copyright (C) 2012  Simone Riva simone.rva {at} gmail {dot} com
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

import particles.pset.particles_set as ps

import numpy as np

class TreeElement( object ):
    """
    The element of a tree node
    """
    def __init__( self ):
        
        self.__particle = None
        
        self.__M = 0.0
        self.__centre_of_mass = np.zeos((3,1))
        
        self.__part_cnt = 0 
        
        self.__tree = None
                    # Tree structure :
                    #list( [
                    #          None ,  # Up   - Near  - Left
                    #          None ,  # Up   - Near  - Right
                    #          None ,  # Up   - Far   - Left
                    #          None ,  # Up   - Far   - Right
                    #          None ,  # down - Near  - Left
                    #          None ,  # down - Near  - Right
                    #          None ,  # down - Far   - Left
                    #          None    # down - Far   - Right
                    #        ] )        

    def get_particle( self ) :
        return self.__particle
    

        
    particle = property( get_particle , doc="Get the particle index of the tree element" )


    def getM(self):
        return self.__M
    
    M = property( getM , doc="getter: return the total mass of the current element ")


    def get_centre_of_mass( self ):
        return self.__centre_of_mass
    
    centre_of_mass = property( get_centre_of_mass , doc="return the centre of mass of the particle" )
    

    def set_local_boundary( self , ref_vertex , edge_len ) :
        self.__ref_vertex = ref_vertex
        self.__ref_vertex = edge_len


    def add_sub_trees( self ):        
        self.__tree = list( TreeElement() for i in range(8) )

    def is_in( self , coord ):
        pass

    def insert_particle( self , pset , i ) :
        if self.particle == None :
            self.__particle = i
            self.__M = pset.M[part_index]
            self.__centre_of_mass = pset.X[i,:]
            return
        
        elif self.particle != None and self.__tree == None :
            self.add_sub_trees()
            self.__part_cnt += 1
            # update mass
            self.__M += pset.M[i]
            
            # update centre of mass
            # TODO
            for st in self.__tree :
                if st.is_in( pset.X[i,:] ) :
                    st.insert_particle( pset , i )
                    break
            return 
                
            


class OcTree ( object ):
    """
    OcTree particles container class
    """
    def __init__( self ):
        self.__tree = TreeElement()
        
    
    def set_global_boundary( self ,
                            ref_vertex = np.array([ 0.0 , 0.0 , 0.0 ]) ,
                            edge_len   = 1.0 ) :
        
        """
        Define the size of the octree cube
        Arguments:
            ref_vertex : the ( down , near , left ) vertex
            edge_len   : leght of the edge 
        """
        
        self.__ref_vertex = ref_vertex
        self.__ref_vertex = edge_len
      
        
    def build_tree( self , pset ) :
        """
        Build the octree with the given particles set
            Arguments:
            pset: a ParticlesSet object used to build the tree
        """
        for i in range( pset.size ):
            self.__insert_rec( self.__tree , pset , i )
    
    
    def __insert_rec( self , tree_el , pset , particle_indx ):
            pass
        
    
    def get_up(self):
        return ( 0.5 , 1.0 )
    
    def get_down(self):
        return ( 0.0 , 0.5 )
    
    def get_left(self):
        return ( 0.0 , 0.5 )
    
    def get_right(self):
        return ( 0.5 , 1.0 )
    
    def get_near(self):
        return ( 0.0 , 0.5 )
    
    def get_far(self):
        return ( 0.5 , 1.0 )
        
    up    = property( get_up    , doc="relative domanin for the up 'sub-space' " )
    down  = property( get_down  , doc="relative domanin for the down 'sub-space' " )
    left  = property( get_left  , doc="relative domanin for the left 'sub-space' " )
    right = property( get_right , doc="relative domanin for the right 'sub-space' " )
    near  = property( get_near  , doc="relative domanin for the near 'sub-space' " )
    far   = property( get_far   , doc="relative domanin for the far 'sub-space' " )
    
    
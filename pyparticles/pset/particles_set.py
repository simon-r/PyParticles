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
from collections import deque

class ParticlesSet(object):
    """
    The main class for storing the particles data set.
    
        ============= =============== =======================================================
        Arguments
        ============= =============== =======================================================
        size          (default 0)     Number of particles
        dim           (default 3)     dimensions of the system 2 or 3 ... 2D 3D
        mass          (dafault True)  if True the particles have a mass.
        label         (default False) if true it's possible to set a name for each particle
        velocity      (dafault True)  if true the particles has a velocity
        charge        (default False) if true the particles have an electric charge.
        log_X         (default False) if true it's possible to logging the position
        log_V         (default False) if true it's possible to logging the velocity
        log_max_size  (default 0) set the maximal size of the log queue
        ============= =============== =======================================================
        
       Note: The properties: position X and velocity V are mandatory.
    """
    def __init__( self , size=1 , dim=3 , boundary=None ,
                 label=False , mass=True , velocity=True , charge=False ,
                 log_X=False , log_V=False , log_max_size=0 ):
        
        if size < 0 :
            raise
        
        self.__X = np.zeros((size,dim))
        
        if velocity:
            self.__V = np.zeros((size,dim))
        else:
            self.__V = None
        
        if mass :
            self.__mass = np.zeros((size,1))
        else:
            self.__mass = None
        
        if charge :
            self.__Q = np.zeros(( size , 1 ))
        else:
            self.__Q = None
        
        if not label :
            self.__label = None
        else:
            self.__label = list( "" for i in range(size) )
        
        self.__size = int( size )
        self.__dim  = int( dim )
        self.__centre_mass = None
        
        self.__bound = boundary
        
        self.__unit = 1.0
        self.__mass_unit = 1.0
        
        if log_X == True :
            self.__log_X = deque([])
        else :
            self.__log_X = None
            
        if log_V == True :
            self.__log_V = deque([])
        else :
            self.__log_V = None
            
        self.__log_max_size = log_max_size
        self.__log_len = 0
        
        self.__property_dict = dict()
        self.__property_dict['X'] = self.__X
        self.__property_dict['V'] = self.__V
        
        if self.__mass  != None :
            self.__property_dict['M'] = self.__mass
        
        if self.__label != None :
            self.__property_dict['label'] = self.__label
            
        if self.__Q != None :
            self.__property_dict['Q'] = self.__Q
        
        self.__notify_set_changed = []
        
        
    def realloc( self , size , dim , boundary=None ,
                 label=False , mass=True , velocity=True , charge=False ,
                 log_X=False , log_V=False , log_max_size=0 ):
        """
        Realloc the particle set, it uses the same args of the constructor,
        
          **Attention!** this method remove the dictionary of the of the extra properties
        """
        del self.__X
        del self.__V
        del self.__mass
        del self.__label
        del self.__log_X
        del self.__log_V
        del self.__property_dict
        
        self.__init__( size , dim , boundary , label , mass , velocity , charge , log_X , log_V , log_max_size )
        
    
    def resize( self , new_size ):
        """
        Resize the particles set with the new_size.
        
        If the new size is bigger the old data are copied in the new particles, according to the function numpy.resize
        if it is smaller it cancels the data.
        
        If the property is a list, the new elements will be filled with 'None' or empty string for the labels
        
        The dim of the set will be not changed.
        """
        
        for k in self.__property_dict.keys() :
            if self.__property_dict[k] == None :
                continue 
            
            if k == "label" :
                lst = list( "" for i in range(new_size) )
                
                mn = min( [ self.size , new_size ] )
                lst[:mn] = self.__label[:mn]
                
                self.__property_dict[k] = list( lst )
                self.__label = lst
                
            elif isinstance( self.__property_dict[k] , list ) :
                lst = list( None for i in range(new_size) )
                
                mn = min( [ self.size , new_size ] )
                lst[:mn] = self.__property_dict[k][:mn]
                self.__property_dict[k] = lst
                
            else :
                NP = np.resize( self.__property_dict[k]  ,
                                ( new_size , self.__property_dict[k].shape[1] ) )
                self.__property_dict[k] = NP
                
                if k == "M" :
                    self.__mass = NP
                elif k == "X" :
                    self.__X = NP
                elif k == "V" :
                    self.__V = NP
                elif k == "Q" :
                    self.__Q = NP                    
        
        self.__size = int( new_size )


    def get_by_name( self , property_name ):
        """
        Return a property reference by name:
        for example 'X' , 'V' , 'M' ...
        ::
        
            # set to [1,2,3] the position of the 10th particle
            pset.get_by_name('X')[10,:] = [1,2,3]
        """
        return self.__property_dict[property_name]


    def add_property_by_name( self , property_name , dim=None , model="numpy_array" , to_type=np.float64 ):
        """
        Insert a new property by name. If the dim is not specified it uses the current dimension of the set.
        
        If the model of the property is 'list' the dim is forced to 1
        
            ===================  ==============================================================================
            Arguments
            ===================  ==============================================================================
             property_name       the name of the new property
             dim                 the dimension of the new property ( 2 = "2D  , 3 = 3D ... )
             model               'list' or 'numpy_array'
             to_type=np.float64  an array-numpy type for the model 'numpy_array' [ np.float64 , np.int64 ... ]
            ===================  ==============================================================================
            
        For example add 'friction' or 'radius':
        ::
        
            # Add the friction to the particles set 
            pset.add_property_by_name( "friction" , dim=1 , to_type=np.float32 )
        """
        
        if dim == None :
            dim = self.dim
        
        if model == "numpy_array" :
            self.__property_dict[property_name] = to_type( np.zeros(( self.size , dim ) ) )
        elif model == "list" :
            self.__property_dict[property_name] = list( None for i in range(self.size) )


    def get_properties_names(self):
        """
        Return a list of containig the names of all properties
        """
        return self.__property_dict.keys()


    def getX(self):
        return self.__X
    
    X = property( getX , doc="return the reference to the array of the positions" )

    
    def getM(self):
        return self.__mass
    
    M = property( getM , doc="return the reference to the array of the masses" )
    

    def getQ(self):
        return self.__Q
    
    Q = property( getQ , doc="return the reference to the array of the charges" )

    
    def getV(self):
        return self.__V
    
    V = property( getV , doc="return the reference to the velocities array" )


    def get_list( self , i , to=float ):
        """
        return a list containing all data of the i-th particle
            TODO: adapt to property by name
        """
        #
        #lst = []
        #for k in self.__property_dict.keys() :
        #    pass
                 
        lstX = []
        lstV = []
        lstM =  to( self.M[i] )
        
        for j in range(  self.dim ):
            lstX.append( to( self.X[i,j] ) )
            lstV.append( to( self.V[i,j] ) )
        
        lst = lstX + lstV
        lst.append( lstM )
        
        if self.__label != None :
            lst.append( self.__label[i] )
            
        return lst


    def get_label( self ):
        return self.__label
    
    label = property( get_label , doc="return the reference to the label list" )
    

    def append( self , p_dict ) :
        """
        Append the particle(s) described in the given dictionary
        
         If the particle don't contain every required data will be rejected.
         
         The dictionary *p_dict* must contains the name of the property and it's value, and it **must include all property**, also the user defined!
        """
        
        for k in p_dict.keys():
            if not self.__property_dict.has_key( k ) :
                raise ValueError
        
        for kpr in self.__property_dict.keys() :
            if isinstance( self.__property_dict[kpr] , list ):
                self.__property_dict[kpr].append( p_dict[kpr] )
            else :
                self.__property_dict[kpr] = np.append( self.__property_dict[kpr] , p_dict[kpr] , 0 )
                if kpr == "X" :
                    self.__X = self.__property_dict[kpr]
                elif kpr == "V" :
                    self.__V = self.__property_dict[kpr]
                elif kpr == "M" :
                    self.__mass = self.__property_dict[kpr]
                elif kpr == "Q" :
                    self.__Q = self.__property_dict[kpr]                    

        self.notify_set_changed()
    
    def notify_set_changed(self):
        """
        Call this methos when the particle set is modified.
        """
        for e in self.__notify_set_changed :
            e.particles_set_changed( self )

    def add_set_changed_listener( self , listener ) :
        """
        Add an object that contains a member methond called: *particles_set_changed( pset )* that there will be called if the particle set will be modified.
        """
        self.__notify_set_changed.append( listener )

    def update_boundary( self ):
        """
        Update the particle set according to the boudary rule
        """
        if self.__bound != None :
            self.__bound.boundary( self )
        
    def get_boundary( self ):
        return self.__bound
    
    def set_boundary( self , boundary):
        self.__bound = boundary

    boundary = property( get_boundary , set_boundary , doc="return the reference to the boudary, None if the boudary are not set or open")

    
    def get_log_max_size( self ):
        return self.__log_max_size
    
    def set_log_max_size( self , log_max_size ):
        self.__log_max_size = log_max_size
    
    log_max_size = property( get_log_max_size , set_log_max_size , doc="set and get the max allowed size of the log")
    
    
    def enable_log( self , log_X=True , log_V=False , log_max_size=0 ):
        """
        |Eanble the X and V logging:
        |args:
            #. log_X=True : log the positions
            #. log_V=False : log the velocity
            #. log_max_size: max size of the log queue
        """
        if ( not self.log_X_enabled ) and log_X :
            self.__log_X = deque([])
            
        if ( not self.log_V_enabled ) and log_V :
            self.__log_V = deque([])
            
        self.log_max_size = log_max_size
            
    
    def get_log_size(self):
        return self.__log_len
    
    log_size = property( get_log_size )

    def get_log_X_enabled(self):
        return ( self.__log_X != None )
    
    def get_log_V_enabled(self):
        return ( self.__log_V != None )

    def get_log_enabled(self):
        return ( self.log_V_enabled or self.log_X_enabled )

    log_V_enabled = property( get_log_V_enabled , doc="return true if the logging of the position is enabled")
    log_X_enabled = property( get_log_X_enabled , doc="return true if the logging of the velocity is enabled")
    
    log_enabled = property( get_log_enabled , doc="return true if the logging of position or velocity is enabled")

    

    def log(self):
        """
        if the log is enabled, save the current status in the log queue.
        
        The last element of the queue will be removed if we reach the max allowed size
        """
        delta_x = 0
        delta_v = 0
        
        if self.__log_X != None :
            lX = np.zeros(( self.size , self.dim ))
            lX[:] = self.X
            
            #print(lX)
            
            if self.log_size > self.log_max_size :
                self.__log_X.popleft()
                delta_x -= 1
            
            self.__log_X.append( lX )
            delta_x += 1
        
        if self.__log_V != None :
            lV = np.zeros(( self.size , self.dim ))
            lV[:] = self.V
            
            if self.log_size > self.log_max_size :
                self.__log_V.popleft()
                delta_v -= 1
            
            self.__log_V.append( lV )
            delta_v+=1
            
        #print( self.__log_X )
        self.__log_len += max( [ delta_x , delta_v ]  )
        
    def jump( self , indx ):
        pass        

    def get_logX( self ):
        return self.__log_X
        
    def get_logV( self , i ):
        return self.__log_V
    
    logX = property( get_logX , doc="return the log queue X: position" )
    logV = property( get_logV , doc="return the log queue V: velocity" )
    

    def set_unit( self , u ):
        self.__unit = u
        
    def get_unit(self):
        return self.__unit
    
    unit = property( get_unit , set_unit , doc="set the unit lenght")
    
    
    def set_mass_unit( self , u ):
        self.__mass_unit = u
        
    def get_mass_unit(self):
        return self.__mass_unit
    
    mass_unit = property( get_mass_unit , set_mass_unit , doc="set the unit mass" )
    
    
    def update_centre_of_mass(self):
        self.__centre_mass = np.sum( self.__X * self.__mass , axis=0 ) / np.float( self.__size )
        return self.__centre_mass
        
    def centre_of_mass(self):
        return self.__centre_mass
    
    def get_dim(self):
        return self.__dim
    
    def get_size( self ):
        return self.__size
    
    dim = property( get_dim )
    size = property( get_size )
    
    def add_clusters( self , Cs , n ):
        i = 0
        for c in Cs:
            self.__X[n[i]:n[i]+c.shape[0]] = c
            i = i + 1
            
    
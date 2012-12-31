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



import zlib

###########################
# Current version
v_major    = 0
v_minor    = 3
v_revision = 6
###########################

def py_particle_version( r='s' ):
    global v_major
    global v_minor
    global v_revision
    
    if r == 's' :
        return "%d.%d.%d" % ( v_major , v_minor , v_revision )
    else :
        return ( v_major , v_minor , v_revision )


def test_pyopencl():
    try :
        import pyopencl
    except :
        return False
    else :
        return True
    
def about():
    
    mail = zlib.decompress(b'x\x9c+\xce\xcc\xcd\xcfK\xd5+*KtH\xcfM\xcc\xcc\xd1K\xce\xcf\x05\x00R\x9c\x07\xba').decode('utf-8')
    
    message = """
    
    PyParticles is a particle simulation toolbox entirely written in python.

    The main objective of PyParticles is to provide a system API simple and fast to use. 
    Furthermore is to provide a basic application for the implementation of simple models.

    Visit: http://pyparticles.wordpress.com/ 
    Docs: http://simon-r.github.com/PyParticles/index.html 
    
    Copyright (C) %s  %s email: %s 

    --------------------------------------------------------------------

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
    """
    
    message = message % ( '2012' , 'Simone Riva' , mail )
    
    print( message )
    

    
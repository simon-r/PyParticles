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



import os
import shutil
import subprocess
import sys
import re
import sys

is_winows = sys.platform.startswith('linux')

from distutils.core import setup
from pyparticles.utils.pypart_global import py_particle_version
from distutils.command.install import install


class particles_install(install):
    user_options = install.user_options
 
    def run(self):
        
        install.run(self)
    
        # man ... Linux only    
        if sys.platform.startswith('linux'):
            
            man_dir = os.path.abspath("./man/")
    
            prefix = re.sub( r'^/' , '' , self.prefix )
    
            output = subprocess.Popen([os.path.join(man_dir, "install.sh")],
                    stdout=subprocess.PIPE,
                    cwd=man_dir,
                    env=dict({"PREFIX": os.path.join( self.root , prefix ) }, **dict(os.environ))).communicate()[0]
            
            print( output )




setup(name = "pyparticles",
    version = "%s" % py_particle_version() ,
    description = "Particles simulation toolbox for python, with some force model and integrations methods",
    author = "Simone Riva",
    author_email = "simone.rva [at] gmail.com",
    url = "https://github.com/simon-r/PyParticles",
    packages = ['pyparticles' ,
                'pyparticles.utils' ,
                'pyparticles.ode' ,
                'pyparticles.forces' ,
                'pyparticles.animation' ,
                'pyparticles.demo' ,
                'pyparticles.pset' ,
                'pyparticles.measures' ,
                'pyparticles.main' ,
                'pyparticles.geometry' ,
                'pyparticles.ogl' ],
    scripts = ["pyparticles_app"],
    long_description = "Particles simulation toolbox in python, with some force model and integrations methods. Particles includes an OpenGL GUI and an easy to use problem comfiguration" ,
    classifiers=[
        'Development Status :: %s Stable' % py_particle_version() ,
        'Topic :: Scientific/Engineering :: Physics' ,
        'Topic :: Scientific/Engineering :: Mathematics' ,
        'Environment :: Console' ,
        'Environment :: X11 Applications' ,
        'Environment :: Win32 (MS Windows)' ,
        'Intended Audience :: Users',
        'License :: OSI Approved :: GPL-3.0+' ,
        'Operating System :: Linux' ,
        'Programming Language :: Python' ] ,
    cmdclass={"install": particles_install }
) 

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


import argparse

def parse_args():
    desc = "PyParticles is a particle simulation tool box that support the most diffused numerical integration " 
    desc = desc + " and forces models "

    parser = argparse.ArgumentParser( description=desc )
    
    parser.add_argument("-m", "--config_model",
        action="store_true",
        dest="config_model",
        help="Write out the model of a config file and exit")
    
    parser.add_argument( "-d" , "--demo",
        action="store",
        choices=[ "springs" , 
                 "solar_system" , 
                 "gas_lj" , 
                 "bubble" , 
                 "cat_spri" , 
                 "el_static" , 
                 "elmag_field" ,
                 "fountain" ,
                 "galaxy"] ,
        dest="demo",
        default=None ,
        help="Execute the specified buildin demo"
        )

    parser.add_argument( "-t" , "--test",
        action="store",
        choices=[ "fall" , "harmonic" , "dharmonic" ] ,
        dest="test",
        default=None ,
        help="Execute the specified buildin test")

    parser.add_argument(
        dest="path_name",
        nargs='?',
        default=None
        )
    
    parser.add_argument( "-v" , "--version",
        action="store_true",
        dest="version",
        help="print the current version and exit"
        )
    
    parser.add_argument( "-a" , "--about",
        action="store_true",
        dest="about",
        help="print the about message and exit"
        )    
    
    return parser.parse_args()

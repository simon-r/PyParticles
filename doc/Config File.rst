Config file
===========

Config file description:
    
Section: pset_origin
--------------------

    **Define the origin of the particles data set.**

    **Varibles**

           =====================        ========================
           Variable                     Description
           =====================        ========================
           media_origin = [file]        Where data the is stored
           file_name = <file>           the dataset file name
           =====================        ========================
    
Section: set_config
-------------------
    **Particles data set configauration**

    **Varibles:**

           ===========================  ==========================================
           Variable                     Description
           ===========================  ==========================================
           len_unit  = <number>         How many meters is a unit,
           mass_unit = <number>         How many Kg is a unit
           boundary  = [open|periodic]  The boundary model used in the simulation
           ===========================  ==========================================

           Note: len_unit & mass_unit are used only for drawing the particles
    
Section: model
--------------
    **Simulation method and force model**

    **Varibles:**

           ==============================================================      =====================================
           Variable                                                            Description
           ==============================================================      =====================================
           force = [gravity|linear_spring|constant_force|midpoint]             Force type used
           ode_solver_name = [euler|runge_kutta|leap_frog|constant_force]      Integration method
           time_step = <number>                                                time step used for the integration
           force_const = <number>                                              Force constant, like G
           force_vector= <number>                                              Force vector, for the constant force
           ==============================================================      =====================================

    
Section: animation
------------------
    **Simulation control & graphic wiew**

    **Variables:**

           ==============================================================      =================================================
           Variable                                                            Description
           ==============================================================      =================================================
           animation_type = [opengl|matplotlib]                                Setup the output interface
           xlim = <number> <number>                                            define the limit of the picture (sometime unused)
           ylim = <number> <number> 
           zlim = <number> <number>
           ==============================================================      =================================================

    
Example:
--------
    ::

        [pset_origin]
        media_origin = from_file
        file_name = solar_sys.csv
        
        [set_config]
        len_unit = 149597870700.0
        mass_unit = 5.9736e24
        boundary = open
        
        [model]
        force = gravity
        ode_solver_name = euler
        time_step = 3600
        steps = 1000000
        force_const = 6.67384e-11
        force_vector = 0 0 0
        
        [animation]
        animation_type = opengl
        xlim = -5.0  5.0
        ylim = -5.0  5.0
        zlim = -5.0  5.0 


Problem Config file
===================

The config file is used to generate a simulation model that can be executed with the application *pyparticle_app*:
::

  pyparticle_app ma_simul.cfg

The config files are based on the sintax **rfc822** used by the python *configparser* module, very easy to read and edit and used in numerous applications.
  
Creating a simulation using the config file is quite easy, as first you must create a model file with the commands:
::
  
  pyparticle_app -m
  mv example_pyparticles_config.cfg my_sim.cfg

And after this you must edit the file according you criteria. 
Observe that the uneeded parameters are ignored; if there are an editing error normally is used the default value or the application exit with an exception.

Config file description:
------------------------   
Section: pset_origin
--------------------

    **Define the origin of the particles data set.**

    **Varibles**

           ==========================        ========================
           Variable                          Description
           ==========================        ========================
           media_origin = [file|rand]        Where data the is stored
           file_name = <file>                the dataset file name
           ==========================        ========================
    
Section: set_config
-------------------
    **Particles data set configauration**

    **Varibles:**

           ==================================== ==============================================
           Variable                             Description
           ==================================== ==============================================
           len_unit  = <number>                 How many meters is a unit
           mass_unit = <number>                 How many Kg is a unit
           boundary  = [open|periodic|rebound]  The boundary model used in the simulation
           boundary_lim = <#> <#>               Define the size of the boundary
           sim_log = <number>                   The size of the log queue (0 disable the log)
           sim_log_X = [True|False]             If sim_log is enabled log the position
           sim_log_V = [True|False]             If sim_log is enabled log the velocities
           rand_part_nr = <number>              The total number of particles for a rand set
           ==================================== ==============================================

           Note: len_unit & mass_unit are used only for drawing the particles
    
Section: model
--------------
    **Simulation method and force model**

    **Varibles:**

           ==============================================================      =====================================
           Variable                                                            Description
           ==============================================================      =====================================
           force = [gravity|linear_spring|constant_force]                      Force type used
           ode_solver_name = [euler|runge_kutta|leap_frog|midpoint]            Integration method
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
           draw_log = [True|False]                                             Draw the simulation log (if enabled)
           xlim = <number> <number>                                            define the limit of the picture (sometime unused)
           ylim = <number> <number> 
           zlim = <number> <number>
           ==============================================================      =================================================

    
Examples:
--------
*The solar system*:
    ::

        [pset_origin]
        media_origin = file
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


*Random cluster:*
    ::

	# this is a comment
	[pset_origin]
	media_origin = rand
        # Ignored !!!
	file_name = solar_sys.csv  

	[set_config]
	len_unit = 1
	mass_unit = 1
	boundary = open
	boundary_lim = -7 7 
	sim_log = 0
	sim_log_x = True
	sim_log_v = False
        # Attention: the total number of particles is here !!
	rand_part_nr = 350   

	[model]
	force = gravity
	ode_solver_name = runge_kutta
	time_step = 0.005
	steps = 1000000
	force_const = 0.001
	# ignored 
	force_vector = 0 0 -7  

	[animation]
	animation_type = opengl
	draw_trajectory = False
	trajectory_step = 15
	xlim = -5.0  5.0
	ylim = -5.0  5.0
	zlim = -5.0  5.0

	# Randon cluster definition
	[rand_cluster_bar]  
	rc_part_nr = 150
	rc_centre = 0 0 1
	rc_radius = 1.0
	rc_mass_rng = 0.5  1.0
	rc_vel_rng = 0.1 0.2
	rc_vel_mdl = no
	rc_vel_dir = 0 1 0

	[rand_cluster_foo]
	rc_part_nr = 150
	rc_centre = 0 0 -1
	rc_radius = 2.0
	rc_mass_rng = 0.5  2.0
	rc_vel_rng = 0.021 0.2
	rc_vel_mdl = const
	rc_vel_dir = 1 1 0

	[rand_cluster_foobar]
	rc_part_nr = 50
	rc_centre = 0 3 -3
	rc_radius = 2.0
	rc_mass_rng = 0.2  2.0
	rc_vel_rng = .1 .2
	rc_vel_mdl = bomb
	rc_vel_dir = 0 1 0


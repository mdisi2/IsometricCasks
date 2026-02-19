import openmc 
import numpy as np

from Function_Folder.material_init import S_316_borated, He
from Function_Folder.triso_pebble_treatment import Depleted_Triso_Universe

### This file constructs the cell for the fuel blanket and pebbles, with reflective boundary conditions to fill the mpc universe
### In units [cm]

### Bouding Box
z_top = openmc.ZPlane(z0= 11.006257/2)
z_bottom = openmc.ZPlane(z0= -11.006257/2)
x_1 = openmc.XPlane(x0 = -6.25 / 2)
x_2 = openmc.XPlane(x0 =  6.25 / 2)
y_1 = openmc.YPlane(y0 =  -6.25 / 2)
y_2 = openmc.YPlane(y0 =  6.25 / 2)

Boundary_Region = +z_bottom & -z_top & +x_1 & -x_2 & +y_1 & -y_2

def F_Blanket(blanket):

    """
    2D Polygonal surface of the frame that the pebble will sit in, along 
    with polygonal cuts. It is extended across the third axis to make the 
    Isometric, corrugated, 'blanket' for each of the pebbles to lay on.
    """

    frame_outer = np.array([(0.1,5.503),
                (-0.1,5.503),
                (-0.1,3.551),
                (-3.125,1.804),
                (-3.125,-1.804),
                (-0.1,-3.551),
                (-0.1,-5.503),
                (0.1,-5.503),
                (0.1,-3.551),
                (3.125,-1.804),
                (3.125,1.804),
                (0.1,3.551)])
    
    frame_cut = np.array([(0,3.493),
                 (3.025, 1.746),
                 (3.025,-1.746),
                 (0,-3.493),
                 (-3.025,-1.746),
                 (-3.025,1.764)])

    frame_xz = openmc.model.Polygon(points=frame_outer,basis='xz')
    cut_xz = openmc.model.Polygon(points=frame_cut,basis='xz')
    frame_region_xz = ~cut_xz.region & frame_xz.region 

    frame_yz = openmc.model.Polygon(points=frame_outer,basis='yz')
    cut_yz = openmc.model.Polygon(points=frame_cut,basis='yz')
    frame_region_yz = ~cut_yz.region & frame_yz.region


    frame = openmc.Cell(name='blanket',
                        region = (frame_region_yz | frame_region_xz) & Boundary_Region,
                        fill = blanket)
    
    return frame



def Triso_Pebbles():

    """
    Returns a list of cells containing the triso pebbles filled with the
    triso particles and graphite.

    Triso pebbles are each initialized in the center, and 8 corners, then
    filled by translating the trio region initialized in 
    triso_pebble_treatment.py to the respective coordinates.
    """

    #sphere in xy plane

    pebbles = [ 
        (openmc.Sphere(x0=0, y0=0, z0=0 , r =3.0) , (0,0,0)),
        
        (openmc.Sphere(x0=3.125, y0=3.125, z0= 5.503, r =3.0) , (3.125, 3.125, 5.503)),
        (openmc.Sphere(x0=-3.125, y0=3.125, z0= 5.503, r =3.0) , (-3.125, 3.125, 5.503)),
        (openmc.Sphere(x0=-3.125, y0=-3.125, z0= 5.503, r =3.0) , (-3.125, -3.125, 5.503)),
        (openmc.Sphere(x0=3.125, y0=-3.125, z0= 5.503, r =3.0) , (3.125, -3.125, 5.503)),

        (openmc.Sphere(x0=3.125, y0=3.125, z0= -5.503, r =3.0) , (3.125, 3.125, -5.503)),
        (openmc.Sphere(x0=-3.125, y0=3.125, z0= -5.503, r =3.0) , (-3.125, 3.125, -5.503)),
        (openmc.Sphere(x0=-3.125, y0=-3.125, z0= -5.503, r =3.0) , (-3.125, -3.125, -5.503)),
        (openmc.Sphere(x0=3.125, y0=-3.125, z0= -5.503, r =3.0) , (3.125, -3.125, -5.503))]
    
    cells = []

    for sphere, center in pebbles:
        c = openmc.Cell(fill=Depleted_Triso_Universe(), region= -sphere & Boundary_Region)
        c.translation = center

        cells.append(c)
    
    return cells 

def void_space(void_fill):

    """
    :input basket: the cell of the basket
    :type basket: 
    :input void_fill: the material that is not filled by a pebble or the basket, should be helium or water in accident scenario  
    """

    Centered = openmc.Sphere(x0=0, y0=0, z0=0 , r =3.0)
    
    t_1 = openmc.Sphere(x0=3.125, y0=3.125, z0= 5.503, r =3.0)
    t_2 = openmc.Sphere(x0=-3.125, y0=3.125, z0= 5.503, r =3.0)
    t_3 = openmc.Sphere(x0=-3.125, y0=-3.125, z0= 5.503, r =3.0)
    t_4 = openmc.Sphere(x0=3.125, y0=-3.125, z0= 5.503, r =3.0)

    b_1 = openmc.Sphere(x0=3.125, y0=3.125, z0= -5.503, r =3.0)
    b_2 = openmc.Sphere(x0=-3.125, y0=3.125, z0= -5.503, r =3.0)
    b_3 = openmc.Sphere(x0=-3.125, y0=-3.125, z0= -5.503, r =3.0)
    b_4 = openmc.Sphere(x0=3.125, y0=-3.125, z0= -5.503, r =3.0)
    
    region_pebbles = (-Centered | -t_1 | -t_2 | -t_3 | -t_4 | -b_1 | -b_2 | -b_3 | -b_4) & Boundary_Region

    region = ~(region_pebbles| F_Blanket().region)

    voidcel = openmc.Cell(name='void',
                          region=region,
                          fill=void_fill)

    return voidcel

def Blanket_and_Pebble_Universe(void_fill,blanket):
    """
    Returns the lattice universe of the blanket and the filled 
    triso pebbles
    
    :input coolant: this is what fills the voidspace
    :coolant type: openmc material
    """

    # MPC height = ~504.19 cm so at ~ 11 cell height = 46 to be safe
    # MPC diameter = 347.98 cm at  ~ 6.25 cell width = 57 to be safe

    pebbles = Triso_Pebbles()
    unit = openmc.Universe(name='unit cell',
                           cells=[F_Blanket(blanket), *pebbles, void_space(void_fill)])


    finite = openmc.RectLattice(name='Basket Lattice')
    finite.pitch = (6.25, 6.25, 11.006257)
    finite.lower_left = (-175, -175, 50)
    finite.universes = np.full((60, 60, 50),unit)

    #Bounding Box
    xmin = openmc.XPlane(x0=-175)
    xmax = openmc.XPlane(x0= 175)
    ymin = openmc.YPlane(y0= -175)
    ymax = openmc.YPlane(y0= 175)
    zmin = openmc.ZPlane(z0= 52.705)
    zmax = openmc.ZPlane(z0= 505 + 55)

    region = +xmin & -xmax & +ymin & -ymax & +zmin & -zmax

    lattice_cell = openmc.Cell(name='Pebble Lattice Cell',
                               fill=finite,
                               region=region)

    return openmc.Universe(name='Pebble Lattice Universe',
                           cells=[lattice_cell])


def plotter():
    
    geometry = openmc.Geometry([F_Blanket(), *Triso_Pebbles()]) #void_space(void_fill=He)])
    geometry.root_universe.bounding_region = Boundary_Region
    geometry.export_to_xml()

    # Plotting hehe

    plot1 = openmc.Plot()
    plot1.filename = 'basket_plot_origin_xz.png'
    plot1.basis = 'xz'
    plot1.origin = (0, 0, 0)
    plot1.width = (13, 13)
    plot1.pixels = (500, 500)
    plot1.color_by = 'cell'

    plot2 = openmc.Plot()
    plot2.filename = 'basklet_plot_far_xz.png'
    plot2.basis = 'xz'
    plot2.origin = (0, 3.1249, 0)
    plot2.width = (13, 13)
    plot2.pixels = (500, 500)
    plot2.color_by = 'cell'

    plot3 = openmc.Plot()
    plot3.filename = 'basklet_plot_close_xz.png'
    plot3.basis = 'xz'
    plot3.origin = (0, -3.124, 0)
    plot3.width = (13, 13)
    plot3.pixels = (500, 500)
    plot3.color_by = 'cell'

    ##YZ Plots

    plot4 = openmc.Plot()
    plot4.filename = 'basket_plot_origin_yz.png'
    plot4.basis = 'yz'
    plot4.origin = (0, 0, 0)
    plot4.width = (13, 13)
    plot4.pixels = (500, 500)
    plot4.color_by = 'cell'

    plot5 = openmc.Plot()
    plot5.filename = 'basklet_plot_far_yz.png'
    plot5.basis = 'yz'
    plot5.origin = (3.1249, 0, 0)
    plot5.width = (13, 13)
    plot5.pixels = (500, 500)
    plot5.color_by = 'cell'

    plot6 = openmc.Plot()
    plot6.filename = 'basklet_plot_close_yz.png'
    plot6.basis = 'yz'
    plot6.origin = (-3.125, 0, 0)
    plot6.width = (13, 13)
    plot6.pixels = (500, 500)
    plot6.color_by = 'cell'

    plots = openmc.Plots([plot1,plot2,plot3,plot4,plot5,plot6])
    plots.export_to_xml()

plotter()
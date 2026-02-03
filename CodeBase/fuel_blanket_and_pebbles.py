import openmc 

from Function_Folder.mats import S_316_borated, Concrete
from Function_Folder.utilities import extrude

### This file constructs the cell for the fuel blanket and pebbles, with reflective boundary conditions to fill the mpc universe
### In units [cm]

###bouding box
z_top = openmc.ZPlane(z0= 11.006257/2,boundary_type='reflective')
z_bottom = openmc.ZPlane(z0= -11.006257/2,boundary_type='reflective')
x_1 = openmc.XPlane(x0 = -6.25 / 2,boundary_type='reflective')
x_2 = openmc.XPlane(x0 =  6.25 / 2,boundary_type='reflective')
y_1 = openmc.YPlane(y0 =  -6.25 / 2,boundary_type='reflective')
y_2 = openmc.YPlane(y0 =  6.25 / 2,boundary_type='reflective')


Boundary_Region = +z_bottom & -z_top & +x_1 & -x_2 & +y_1 & -y_2

#Bounding Box for xz quad 1 
x_0 = openmc.XPlane(x0=0,boundary_type='reflective')
x_f = openmc.XPlane(x0=3.125,boundary_type='reflective')
z_t = openmc.ZPlane(z0=5.503,boundary_type='reflective')
z_b = openmc.ZPlane(z0=0,boundary_type='reflective')
y_0 = openmc.YPlane(y0=-3.125,boundary_type='reflective')
y_f = openmc.YPlane(y0=3.125,boundary_type='reflective')


bounding_box = +x_0 & -x_f & +z_b & -z_t & +y_0 & -y_f

def Fuel_Blanket():

    ## XZ plane 
    PXZ_1 = [(3.025,0),
             (3.125,0),
             (3.125,1.804),
             (0.1,3.551),
             (0.1,5.503),
             (0,5.503),
             (0,3.493),
             (3.025,1.746)]
    
    PXZ_1_hole = [(0,0),
                  (1.732,0),
                  (0.866,1.5),
                  (0,1.5)]
    
    PXZ_1_hole2 = [(3.125,4.003),
                  (3.125,5.503),
                  (1.393,5.503),
                  (2.259,4.003)]
    

    Region_1 = openmc.model.Polygon(points=PXZ_1, basis='xz').region
    Region_cut_1 = openmc.model.Polygon(points=PXZ_1_hole, basis='xz').region
    Region_cut_2 = openmc.model.Polygon(points=PXZ_1_hole2, basis='xz').region

    total_region = (Region_1 & ~Region_cut_1 & ~Region_cut_2) & bounding_box


    F_B = openmc.Cell(name='Fuel Blanket',
                      region = total_region,
                      fill = S_316_borated)

    return F_B


def Triso_Pebble():
    #sphere in xy plane

    Centered = openmc.Sphere(x0=0, y0=0, z0=0 , r =3.0)
    Top_far = openmc.Sphere(x0=3.125, y0=3.125, z0= 5.503, r =3.0)
    Top_close = openmc.Sphere(x0=3.125, y0=-3.125, z0= 5.503, r =3.0)
    region = -Centered | -Top_far | -Top_close

    Triso_Pebble = openmc.Cell(name='Pebbles',
                               region=region & bounding_box,
                               fill=Concrete) # TODO triso pebble fill

    return Triso_Pebble

def Triso_smeared():
    ## TODO

    return None

tester = openmc.Cell(name='ball',
                     region = -openmc.Sphere(r=3.0,y0=3.125),
                     fill = Concrete)

settings = openmc.Settings()
materials = openmc.Materials([S_316_borated, Concrete])
geometry = openmc.Geometry([Triso_Pebble()])
geometry.root_universe.bounding_region = Boundary_Region

materials.export_to_xml()
geometry.export_to_xml()
settings.export_to_xml()

# Plotting hehe

plot1 = openmc.Plot()
plot1.filename = 'basket_plot_origin.png'
plot1.basis = 'xz'
plot1.origin = (0, 0, 0)
plot1.width = (13, 13)
plot1.pixels = (100, 100)
plot1.color_by = 'cell'

plot2 = openmc.Plot()
plot2.filename = 'basklet_plot_far.png'
plot2.basis = 'xz'
plot2.origin = (0, 3.123999, 0)
plot2.width = (13, 13)
plot2.pixels = (100, 100)
plot2.color_by = 'cell'

plot3 = openmc.Plot()
plot3.filename = 'basklet_plot_close.png'
plot3.basis = 'xz'
plot3.origin = (0, -3.125, 0)
plot3.width = (13, 13)
plot3.pixels = (100, 100)
plot3.color_by = 'cell'

plots = openmc.Plots([plot1,plot2,plot3])
plots.export_to_xml()
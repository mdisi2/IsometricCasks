import openmc 

from Function_Folder.mats import S_316_borated
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

left = openmc.XPlane(x0=0,boundary_type='reflective')
right = openmc.XPlane(x0=3.125,boundary_type='reflective')
top = openmc.ZPlane(z0=5.503,boundary_type='reflective')
bottom = openmc.ZPlane(z0=0,boundary_type='reflective')

bounding_box = -left & +right & -top & +bottom

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
    

    Region_1 = openmc.model.Polygon(points=PXZ_1, basis='xz')
    Region_cut_1 = openmc.model.Polygon(points=PXZ_1_hole, basis='xz')
    Region_cut_2 = openmc.model.Polygon(points=PXZ_1_hole2, basis='xz')

    total_region = Region_1 & ~(Region_cut_1) & ~(Region_cut_2) & -bounding_box


    F_B = openmc.cell(name='Fuel Blanket',
                      region = total_region,
                      fill = S_316_borated)

    return F_B


def Triso_Pebble():
    #sphere in xy plane

    Centered = openmc.Sphere(x=0, y=0, z=0 , r =3.0)
    Top_close = openmc.Sphere(x=3.125, y=3.125, z= 5.503, r =3.0)
    Top_far = openmc.Sphere(x=3.125, y=-3.125, z= 5.503, r =3.0)

    region = (Centered | Top_close | Top_far) & -bounding_box

    Triso_Pebble = openmc.cell(name='Pebbles',
                               region=region,
                               fill=S_316_borated) # TODO triso pebble fill

    return Triso_Pebble

def Triso_smeared():
    ## TODO

    return None


settings = openmc.Settings()
materials = openmc.Materials([S_316_borated])
geometry = openmc.Geometry([Fuel_Blanket(),Triso_Pebble()])
geometry.root_universe.bounding_region = Boundary_Region

materials.export_to_xml()
geometry.export_to_xml()
settings.export_to_xml()

# Plotting hehe

plot1 = openmc.Plot()
plot1.name('basket_plot_origin.png')
plot1.basis = 'xz'
plot1.origin = (0, 0, 0)
plot1.width = (700, 700)
plot1.pixels = (700, 700)
plot1.color_by = 'cell'

plot2 = openmc.Plot()
plot2.name('basklet_plot_far.png')
plot2.basis = 'xz'
plot2.origin = (0, 3.125, 0)
plot2.width = (700, 700)
plot2.pixels = (700, 700)
plot2.color_by = 'cell'

plot3 = openmc.Plot()
plot3.name('basklet_plot_close.png')
plot3.basis = 'xz'
plot3.origin = (3.125, 0, 0)
plot3.width = (700, 700)
plot3.pixels = (700, 700)
plot3.color_by = 'cell'

plots = openmc.Plots([plot1,plot2,plot3])
plots.export_to_xml()
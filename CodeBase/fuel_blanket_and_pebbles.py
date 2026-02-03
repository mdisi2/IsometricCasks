import openmc 
import numpy as np

from Function_Folder.mats import S_316_borated, Concrete

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

def Fuel_Blanket():

    ## Main frame
    PXZ_1 = [(3.025,0),
             (3.125,0),
             (3.125,1.804),
             (0.1,3.551),
             (0.1,5.503),
             (0,5.503),
             (0,3.493),
             (3.025,1.746)]
    
    PXZ_2 = [(-3.025,0),
             (-3.125,0),
             (-3.125,1.804),
             (-0.1,3.551),
             (-0.1,5.503),
             (-0,5.503),
             (-0,3.493),
             (-3.025,1.746)]
    
    PXZ_3 = [(-3.025,-0),
             (-3.125,-0),
             (-3.125,-1.804),
             (-0.1,-3.551),
             (-0.1,-5.503),
             (-0,-5.503),
             (-0,-3.493),
             (-3.025,-1.746)]
    
    PXZ_4 = [(3.025,-0),
             (3.125,-0),
             (3.125,-1.804),
             (0.1,-3.551),
             (0.1,-5.503),
             (0,-5.503),
             (0,-3.493),
             (3.025,-1.746)]
    

    frame_outer = [(0.1,5.503),
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
                (0.1,3.551)]
    
    frame_cut = [(0,3.493),
                 (-3.025, 1.746),
                 (-3.025,-1.746),
                 (0,-3.493),
                 (3.025,-1.746),
                 (3.025,1.764)]
    
    ### Center cuts
    
    PXZ_1_hole = [(0,0),
                  (1.732,0),
                  (0.866,1.5),
                  (0,1.5)]
    
    PXZ_2_hole = [(0,0),
                  (-1.732,0),
                  (-0.866,1.5),
                  (-0,1.5)]
    
    PXZ_2_hole = [(0,0),
                  (-1.732,0),
                  (-0.866,-1.5),
                  (-0,-1.5)]
    
    PXZ_2_hole = [(0,0),
                  (1.732,0),
                  (0.866,-1.5),
                  (0,-1.5)]
    
    ### Corner cuts
    
    PXZ_1_hole2 = [(3.125,4.003),
                  (3.125,5.503),
                  (1.393,5.503),
                  (2.259,4.003)]
    
    PXZ_2_hole2 = [(-3.125,4.003),
                  (-3.125,5.503),
                  (-1.393,5.503),
                  (-2.259,4.003)]
    
    PXZ_3_hole2 = [(-3.125,-4.003),
                  (-3.125,-5.503),
                  (-1.393,-5.503),
                  (-2.259,-4.003)]
    
    PXZ_3_hole2 = [(3.125,-4.003),
                  (3.125,-5.503),
                  (1.393,-5.503),
                  (2.259,-4.003)]
    

    Region_1 = openmc.model.Polygon(points=PXZ_1, basis='xz').region
    Region_cut_1 = openmc.model.Polygon(points=PXZ_1_hole, basis='xz').region


    
    Region_cut_2 = openmc.model.Polygon(points=PXZ_1_hole2, basis='xz').region

    total_region = (Region_1 & ~Region_cut_1 & ~Region_cut_2) & Boundary_Region


    F_B = openmc.Cell(name='Fuel Blanket',
                      region = total_region,
                      fill = S_316_borated)

    return F_B


def basket():

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
                        region = frame_region_yz | frame_region_xz,
                        fill = Concrete)
    
    return frame



def Triso_Pebbles():
    #sphere in xy plane

    Centered = openmc.Sphere(x0=0, y0=0, z0=0 , r =3.0)
    
    t_1 = openmc.Sphere(x0=3.125, y0=3.125, z0= 5.503, r =3.0)
    t_2 = openmc.Sphere(x0=-3.125, y0=3.125, z0= 5.503, r =3.0)
    t_3 = openmc.Sphere(x0=-3.125, y0=-3.125, z0= 5.503, r =3.0)
    t_4 = openmc.Sphere(x0=3.125, y0=-3.125, z0= 5.503, r =3.0)

    b_1 = openmc.Sphere(x0=3.125, y0=3.125, z0= -5.503, r =3.0)
    b_2 = openmc.Sphere(x0=-3.125, y0=3.125, z0= -5.503, r =3.0)
    b_3 = openmc.Sphere(x0=-3.125, y0=-3.125, z0= -5.503, r =3.0)
    b_4 = openmc.Sphere(x0=3.125, y0=-3.125, z0= -5.503, r =3.0)
    
    region = -Centered | -t_1 | -t_2 | -t_3 | -t_4 | -b_1 | -b_2 | -b_3 | -b_4

    Triso_Pebble = openmc.Cell(name='Pebbles',
                               region=region & Boundary_Region,
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
geometry = openmc.Geometry([basket(), Triso_Pebbles()])
geometry.root_universe.bounding_region = Boundary_Region

materials.export_to_xml()
geometry.export_to_xml()
settings.export_to_xml()

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
plot3.origin = (0, -3.125, 0)
plot3.width = (13, 13)
plot3.pixels = (500, 500)
plot3.color_by = 'cell'

##Yz

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
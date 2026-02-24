import openmc
import os
from math import pi
import numpy as np
cm = 2.54 # 1-inch = 2.54cm

script_dir = os.path.dirname(os.path.abspath(__file__))
materials_path = os.path.join(script_dir, "materials_zoey.xml")
materials_zoey = openmc.Materials.from_xml(materials_path)

#### Importing Cross Sections
simga_path = '/home/matthewdisimone/Downloads/endfb80/endfb-viii.0-hdf5/cross_sections.xml'
openmc.config['cross_sections'] = simga_path


##########
### MPC Canister Stainless Steal S_316
##########

S_316 = openmc.Material(material_id=1, name='Stainless Steel 316')

# C Carbon - 0.08% maximum
# Mn Manganese - 2.00% maximum
# Si Silicon - 0.75% maximum
# Cr Chromium - 16.00 - 18.00%
# Ni Nickel - 10.00 - 14.00%
# Mo Molybdenum - 2.00 - 3.00%
# P Phosphorous - 0.045% max
# S Sulfur - 0.030% maximum
# N Nitrogen - 0.10% max
# Fe Iron - Balance

S_316.set_density('g/cm3',8.027)
S_316.add_element('C', 0.08 / 100 , percent_type='wo')
S_316.add_element('Mn', 2 / 100, percent_type='wo')
S_316.add_element('Si', 0.75 / 100, percent_type='wo')
S_316.add_element('Cr', 17 / 100, percent_type='wo')
S_316.add_element('Ni', 12 / 100, percent_type='wo')
S_316.add_element('Mo', 2.5 / 100, percent_type='wo')
S_316.add_element('P', 0.045 / 100, percent_type='wo')
S_316.add_element('S', 0.030 / 100, percent_type='wo')
S_316.add_element('N', 0.1 / 100, percent_type='wo')
S_316.add_element('Fe', 1 - (0.08 + 2 + 0.75 + 17 + 12 + 2.5 + 0.045 + 0.030 + 0.1) / 100 , percent_type='wo')

#############
# Fuel Basket
#############

#Dosed Stainless Steel

S_316_borated = openmc.Material(material_id=4, name='Fuel Basket')

# C Carbon - 0.08% maximum
# Mn Manganese - 2.00% maximum
# Si Silicon - 0.75% maximum
# Cr Chromium - 16.00 - 18.00%
# Ni Nickel - 10.00 - 14.00%
# Mo Molybdenum - 2.00 - 3.00%
# P Phosphorous - 0.045% max
# S Sulfur - 0.030% maximum
# N Nitrogen - 0.10% max
# Fe Iron - Balance

B_wo = 1.0 

S_316_borated.set_density('g/cm3',8.027)
S_316_borated.add_element('C', 0.08 / 100 , percent_type='wo')
S_316_borated.add_element('Mn', 2 / 100, percent_type='wo')
S_316_borated.add_element('Si', 0.75 / 100, percent_type='wo')
S_316_borated.add_element('Cr', 17 / 100, percent_type='wo')
S_316_borated.add_element('Ni', 12 / 100, percent_type='wo')
S_316_borated.add_element('Mo', 2.5 / 100, percent_type='wo')
S_316_borated.add_element('P', 0.045 / 100, percent_type='wo')
S_316_borated.add_element('S', 0.030 / 100, percent_type='wo')
S_316_borated.add_element('N', 0.1 / 100, percent_type='wo')


S_316_borated.add_element('B', B_wo/100, percent_type='wo')
S_316_borated.add_element('Fe', 1 - (0.08 + 2 + 0.75 + 17 + 12 + 2.5 + 0.045 + 0.030 + 0.1 + B_wo) / 100 , percent_type='wo')


#Ambient air
air = openmc.Material(material_id=5, name='Air')
air.set_density('g/cm3', 0.00120)
air.add_element('N', 78.1 / 100, percent_type='wo')
air.add_element('O', 20.95 / 100, percent_type='wo')
air.add_element('Ar', 0.95 / 100, percent_type='wo')


#helium for inside cask at normal conditions
He  = None
for m in materials_zoey:
    if m.name == 'He':
        He = m
        break

#accident case scenario where cask is submerged in water
water = openmc.Material(material_id=6, name='Water')
water.set_density('g/cm3' , 1.00)
water.add_element('H', 2, percent_type = 'ao')
water.add_element('O', 1, percent_type = 'ao')

# Undepleted fuel, enriched to 15 % U235
uco = openmc.Material(name='Fresh Fuel')
uco.set_density('g/cm3', 10.4)
uco.add_nuclide("U235", 0.1386, percent_type='wo')
uco.add_nuclide("U238",0.7559, percent_type='wo')
uco.add_element("O", 0.06025, percent_type='wo')
uco.add_element('C', 0.04523, percent_type='wo')

depleted_fuel = None
for m in materials_zoey:
    if m.name == 'depleted kernel':
        depleted_fuel = m
        break

graphite = None 
for m in materials_zoey:
    if m.name == 'graphite' :
        graphite = m
        break

buffer = None
for m in materials_zoey:
    if m.name == 'buffer':
        buffer = m
        break

SiC = None 
for m in materials_zoey:
    if m.name == 'SiC':
        SiC = m
        break

PyC = None 
for m in materials_zoey:
    if m.name == 'PyC' :
        PyC = m
        break

materials = openmc.Materials([S_316_borated, S_316, air, He, graphite, depleted_fuel, buffer, PyC, SiC,uco])

### This is appropriated from the OpenMC triso particle example page
# https://docs.openmc.org/en/v0.12.2/examples/triso.html 

# Pebble fuel region compositions are from Zoe Richter's 4th iteration
# depletion modeling for depleted pebbles in the Xe-100. 

spheres = [openmc.Sphere(r=r*1e-4) for r in [215.,315.,350.,385.]]

cells = [openmc.Cell(fill=depleted_fuel, region=-spheres[0]),
         openmc.Cell(fill=buffer, region=+spheres[0] & -spheres[1]),
         openmc.Cell(fill=PyC, region=+spheres[1] & -spheres[2]),
         openmc.Cell(fill=SiC, region=+spheres[2] & -spheres[3]),
         openmc.Cell(fill=PyC, region=+spheres[3])]

triso_univ = openmc.Universe(cells=cells)

outer_radius_particle = 0.0425

fuel_zone = openmc.Sphere(r=2.5)


centers = openmc.model.pack_spheres(radius=outer_radius_particle,
                                    region=-fuel_zone,
                                    pf=0.094,
                                    seed=621)

print("Number of TRISOs:", len(centers))

trisos = [openmc.model.TRISO(outer_radius = outer_radius_particle, 
                             fill = triso_univ, 
                             center = c) for c in centers]

lower_left = (-2.5,-2.5,-2.5)
upper_right = (2.5,2.5,2.5)
shape = (3,3,3)
pitch = (np.array(upper_right) - np.array(lower_left))/shape

lattice = openmc.model.create_triso_lattice(
        trisos=trisos,
        lower_left=lower_left,
        pitch=pitch,
        shape=shape,
        background=graphite)

fuel_zone_cell = openmc.Cell(region=-fuel_zone, fill=lattice)

### Graphite Zone
outer_rad = openmc.Sphere(r=3.0)
graphite_zone = openmc.Cell(fill=graphite,
                            region=-outer_rad & +fuel_zone)

def Depleted_Triso_Universe():
    root_univ = openmc.Universe(cells=[fuel_zone_cell,graphite_zone])
    return root_univ

def Periodic_BC():
    z_top = openmc.ZPlane(z0= 11.006257/2)
    z_bottom = openmc.ZPlane(z0= -11.006257/2)
    z_top.periodic_surface = z_bottom

    x_1 = openmc.XPlane(x0 = -6.25 / 2)
    x_2 = openmc.XPlane(x0 =  6.25 / 2)
    x_1.periodic_surface = x_2

    y_1 = openmc.YPlane(y0 =  -6.25 / 2)
    y_2 = openmc.YPlane(y0 =  6.25 / 2)
    y_1.periodic_surface = y_2

    Boundary_Region = +z_bottom & -z_top & +x_1 & -x_2 & +y_1 & -y_2

    return Boundary_Region

def F_Blanket(basket=S_316):

    """
    2D Polygonal surface of the frame that the pebble will sit in, along 
    with polygonal cuts. It is extended across the third axis to make the 
    Isometric, corrugated, 'basket' for each of the pebbles to lay on.
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


    frame = openmc.Cell(name='basket',
                        region = (frame_region_yz | frame_region_xz),
                        fill = basket)
    
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
        c = openmc.Cell(fill=Depleted_Triso_Universe(), region= -sphere)
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
    
    region_pebbles = (-Centered | -t_1 | -t_2 | -t_3 | -t_4 | -b_1 | -b_2 | -b_3 | -b_4)

    region = ~(region_pebbles| F_Blanket(S_316_borated).region)

    voidcell = openmc.Cell(name='void',
                          region=region,
                          fill=void_fill)

    return voidcell


cells = [F_Blanket(S_316),Triso_Pebbles(),void_space(He)]
root_universe = openmc.Universe(cells=[cells],region=Periodic_BC)

geometry = openmc.Geometry(root_universe)
geometry.export_to_xml()

settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.particles = 100000
settings.batches   = 1000
settings.inactive  = 300
settings.temperature = {'method': 'interpolation'}

#box around mpc
box = openmc.stats.Box(lower_left = (-6.25 / 2 * cm,-6.25 / 2 * cm, 
                                     -11.006257/2 * cm),
                       upper_right = (6.25 / 2 * cm,6.25 / 2 * cm, 
                                     11.006257/2 * cm),)

source = openmc.IndependentSource(space = box)
settings.source = source

mesh = openmc.RegularMesh()
mesh.dimension = (3, 3, 11)
mesh.lower_left = (-6.25 / 2 * cm,-6.25 / 2 * cm, -11.006257/2 * cm)
mesh.upper_right = (6.25 / 2 * cm, 6.25 / 2 * cm, 11.006257/2 * cm)

settings.entropy_mesh = mesh
settings.export_to_xml()

def plots():
    plot1 = openmc.Plot()
    plot1.basis = 'xz'
    plot1.origin = (0, 0, 0)
    plot1.width = (6.25 *cm, (11.006 * cm))
    plot1.pixels = (1250, 2200)
    plot1.color_by = 'material'
    plot1.type = 'slice'
    plot1.filename = 'xz-slice-BCC.png'

    plot2 = openmc.Plot()
    plot2.basis = 'xy'
    plot2.origin = (0, 0, 0)
    plot2.width = (6.25/2 * cm, 6.25/2 * cm)
    plot2.pixels = (1250, 1250)
    plot2.color_by = 'material'
    plot2.type = 'slice'
    plot2.filename = 'xy-slice-BCC.png'

    plots = openmc.Plots([plot1,plot2])
    plots.export_to_xml()
    openmc.plot_geometry()



plots()
# openmc.run()
# sp = openmc.StatePoint(f'statepoint.{settings.batches}.h5')
# print("k-effective =", sp.k_combined)
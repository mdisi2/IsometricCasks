import openmc
import os
from math import pi
import numpy as np
cm = 2.54 # 1-inch = 2.54cm

script_dir = os.path.dirname(os.path.abspath(__file__))
materials_path = os.path.join(script_dir, "materials_zoey.xml")
materials_zoey = openmc.Materials.from_xml(materials_path)

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


###Overpack

# Type II Portland Cement
Concrete = openmc.Material(material_id=2,name='Concrete')

# Atomic number | Fraction by weight
# 1 0.010000 
# 6 0.001000 
# 8 0.529107 
# 11 0.016000 
# 12 0.002000 
# 13 0.033872 
# 14 0.337021 
# 19 0.013000 
# 20 0.044000 
# 26 0.014000

Concrete.set_density('g/cm3',2.3)
Concrete.add_element('H', 0.010000, percent_type='wo')
Concrete.add_element('C', 0.001000, percent_type='wo')
Concrete.add_element('O', 0.529107, percent_type='wo')
Concrete.add_element('Na', 0.016000, percent_type='wo')
Concrete.add_element('Mg', 0.002000, percent_type='wo')
Concrete.add_element('Al', 0.033872, percent_type='wo')
Concrete.add_element('Si', 0.337021, percent_type='wo') 
Concrete.add_element('K', 0.013000, percent_type='wo')   
Concrete.add_element('Ca', 0.044000, percent_type='wo')  
Concrete.add_element('Fe', 1 - (0.010000 + 0.001000 + 0.529107 + 0.016000 + 0.002000 + 0.033872 + 0.337021 + 0.013000 + 0.044000), percent_type='wo')

#ASTM A516 Grade 70 / ASME SA516 Grade 70

A516_70 = openmc.Material(material_id=3, name='A516_70')
A516_70.set_density('g/cm3' , 7.85)

### https://www.azom.com/article.aspx?ArticleID=4787

A516_70.add_element('C',  0.1 /100, percent_type='wo')
A516_70.add_element('Si', 0.6 /100, percent_type='wo')
A516_70.add_element('Mn', 1 /100,   percent_type='wo')
A516_70.add_element('P',  0.03 /100,percent_type='wo')
A516_70.add_element('S',  0.03 /100,percent_type='wo')
A516_70.add_element('Al', 0.02 /100,percent_type='wo')
A516_70.add_element('Cr', 0.3 /100, percent_type='wo')
A516_70.add_element('Cu', 0.3 /100, percent_type='wo')
A516_70.add_element('Ni', 0.03 /100,percent_type='wo')
A516_70.add_element('Mo', 0.08 /100,percent_type='wo')
A516_70.add_element('Nb', 0.01 /100,percent_type='wo')
A516_70.add_element('Ti', 0.03 /100,percent_type='wo')
A516_70.add_element('V',  0.02 /100,percent_type='wo')
A516_70.add_element('Fe',1-(0.1 + 0.6 + 1 + 0.03 + 0.03 + 0.02 + 0.3 + 0.3 + 0.03 + 0.08 + 0.01 + 0.03 + 0.02)/100, percent_type='wo')

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

# B - whatever i want, but in practice around 1.5 w%o

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


# material_colors = {S_316.id : "#b71732",
#                    Concrete.id : '#aba596' , 
#                    He.id : '#ebab63',
#                    water.id : '#1F3A5F',
#                    AIR.id : '#B7D9F2',
#                    A516_70.id : '#22223b',
#                    S_316_borated.id : "#5c0110",
#                    graphite.id : "#2B2828"}

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

materials = openmc.Materials([S_316_borated, Concrete, A516_70, S_316, air, He, graphite, depleted_fuel, buffer, PyC, SiC,uco])

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

### This file constructs the cell for the fuel blanket and pebbles, with reflective boundary conditions to fill the mpc universe
### In units [cm]

### Bouding Box

def Triso_BCC_Region():
    z_top = openmc.ZPlane(z0= 11.006257/2)
    z_bottom = openmc.ZPlane(z0= -11.006257/2)
    x_1 = openmc.XPlane(x0 = -6.25 / 2)
    x_2 = openmc.XPlane(x0 =  6.25 / 2)
    y_1 = openmc.YPlane(y0 =  -6.25 / 2)
    y_2 = openmc.YPlane(y0 =  6.25 / 2)

    Boundary_Region = +z_bottom & -z_top & +x_1 & -x_2 & +y_1 & -y_2

    return Boundary_Region

def F_Blanket(basket=S_316): #defaults to stainless steel

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
                        region = (frame_region_yz | frame_region_xz) & Triso_BCC_Region(),
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
        c = openmc.Cell(fill=Depleted_Triso_Universe(), region= -sphere & Triso_BCC_Region())
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
    
    region_pebbles = (-Centered | -t_1 | -t_2 | -t_3 | -t_4 | -b_1 | -b_2 | -b_3 | -b_4) & Triso_BCC_Region

    region = ~(region_pebbles| F_Blanket(S_316_borated).region)

    voidcell = openmc.Cell(name='void',
                          region=region,
                          fill=void_fill)

    return voidcell

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


###Constructs the cask and the MPC of the holtec 100, inside mpc 'universe' to be filled later within a sim file
#everything will be in inches multipled by the conversion factor

def Outside_Cask(void_fill):

    """
    Space outside cask, fill with air or water
    """

    outer_cyl = openmc.ZCylinder(r=132.5/2 * cm)
    h0 = openmc.ZPlane(z0 = 0 * cm)
    hT = openmc.ZPlane(z0 = 231.75 * cm)

    Region_cyl = -outer_cyl & +h0 & -hT

    x1 = openmc.XPlane(x0 =-140/2 * cm)
    x2 = openmc.XPlane(x0 = 140/2 * cm)
    y1 = openmc.YPlane(y0 =-140/2 * cm)
    y2 = openmc.YPlane(y0 = 140/2 * cm)
    z0 = openmc.ZPlane(z0 =-10 * cm)
    zT = openmc.ZPlane(z0 = 240 * cm)

    Region_rec = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

    cell = openmc.Cell(name='Outside Cask Space', fill=void_fill, region=Region_rec & ~Region_cyl)

    return cell


def Overpack_Shell():

    """
    These shells hug the outer wall of the cask as well as the space 
    beteween the radial sheileds and the air annulus/MPC
    """

    outer_cyl_outer = openmc.ZCylinder(r=132.5/2 * cm)
    outer_cyl_inner = openmc.ZCylinder(r=131/2 * cm)

    inner_cyl_outer = openmc.ZCylinder(r=75/2 * cm)
    inner_cyl_inner = openmc.ZCylinder(r=73.5/2 *cm )

    h0 = openmc.ZPlane(z0=2 * cm)
    hT = openmc.ZPlane(z0 = (231.75-4) *cm)

    outer_shell_region = -outer_cyl_outer & +outer_cyl_inner & -hT & +h0
    inner_shell_region = -inner_cyl_outer & +inner_cyl_inner & -hT & +h0 

    Overpack_Region = outer_shell_region | inner_shell_region

    Overpack = openmc.Cell(name='Overpack Shells', fill=A516_70, region=Overpack_Region)

    return Overpack


def Radial_Shield_Concrete():

    """
    Primary neutron shield, thick concrete
    """

    #portland concrete ii

    concrete_outer = openmc.ZCylinder(r=131/2 * cm)
    concrete_inner = openmc.ZCylinder(r=(131/2 - 26.75) * cm) #26.75 in thick

    h0 = openmc.ZPlane(z0 = 2*cm)
    ht = openmc.ZPlane(z0 = (231.75-4) *cm)

    Concrete_Region = -concrete_outer & +concrete_inner & +h0 & -ht

    Concrete_Sheild = openmc.Cell(
        name = 'Radial Shield Concrete',
        region= Concrete_Region,
        fill= Concrete)
    
    return Concrete_Sheild

def Radial_Shield_Steel():

    """
    Gamma sheild, high Z metal
    """
    
    steel_outer = openmc.ZCylinder(r=(131/2 - 26.75) * cm)
    steel_inner = openmc.ZCylinder(r=75/2 * cm) #3.75 in thick

    h0 = openmc.ZPlane(z0 = 2*cm)
    ht = openmc.ZPlane(z0 = (231.75-4) *cm)

    Steel_Region = -steel_outer & +steel_inner & +h0 & -ht

    Steel_Shield = openmc.Cell(
        name = 'Radial Shield Steel',
        region= Steel_Region,
        fill= A516_70)

    return Steel_Shield
    
def Plates():

    """
    These plates sit at the top and base of the Cask
    """

    # carbon steel top and naseplate

    rad = openmc.ZCylinder(r=132.5/2 * cm)

    top_plate_top = openmc.ZPlane(z0 = 231.75 *cm)
    top_plate_bottom = openmc.ZPlane(z0 = (231.75-4) *cm)

    bot_plate_top = openmc.ZPlane(z0 = 2 *cm)
    bot_plate_bot = openmc.ZPlane(z0 = 0 *cm)

    top_region = -rad & +top_plate_bottom & -top_plate_top
    base_region = -rad & +bot_plate_bot & -bot_plate_top

    total_region = top_region | base_region

    Plates = openmc.Cell(
        name = 'Top and Bottom Plates',
        region= total_region,
        fill= S_316)

    return Plates

def MPC_Concrete():

    """
    This is the concrete of the same radial thickness as the MPC.
    
    [Plate]
    [MPC Concrete]
    [MPC Steel]
    [Air Annulus]
    [MPC]
    [MPC Steel]
    [MPC Concrete]
    [Plate] 
    """

    #portland concrete ii

    rad = openmc.ZCylinder(r=69.5/2 * cm)

    top_conc_top = openmc.ZPlane(z0 = (231.75-4) *cm)
    top_conc_bot = openmc.ZPlane(z0 = (231.75-4-10.75) *cm)

    base_conc_top = openmc.ZPlane(z0=17.5 * cm)
    base_conc_bot = openmc.ZPlane(z0=2*cm)

    top_region = -rad & +top_conc_bot & -top_conc_top
    base_region = -rad & +base_conc_bot & -base_conc_top

    total_region = top_region | base_region

    MPC_Outer_Concrete = openmc.Cell(
        name = 'MPC Outer Concrete',
        region= total_region,
        fill= Concrete)

    return MPC_Outer_Concrete

def MPC_Steel():
    
    """
    This is the steel of the same radial thickness as the MPC.
    
    [Plate]
    [MPC Concrete]
    [MPC Steel]
    [Air Annulus]
    [MPC]
    [MPC Steel]
    [MPC Concrete]
    [Plate] 
    """

    rad = openmc.ZCylinder(r=69.5/2 * cm)

    top_steel_top = openmc.ZPlane(z0 = (231.75-4-10.75) *cm)
    top_steel_bot = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75) * cm)

    base_steel_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 - 1 - 1- 190.5) * cm) #same as MPC base bottom
    base_steel_bot = openmc.ZPlane(z0=17.5 * cm) #same as base concrete top

    top_region = -rad & +top_steel_bot & -top_steel_top
    base_region = -rad & +base_steel_bot & -base_steel_top

    total_region = top_region | base_region

    MPC_Outer_Steel = openmc.Cell(
        name = 'MPC Outer Steel',
        region= total_region,
        fill= A516_70)

    return MPC_Outer_Steel

def MPC():

    """
    Defines the MPC shell. The void inside the MPC is defined and filled
    in another cell
    """


    mpc_outer = openmc.ZCylinder(r= 69.5/2 * cm)
    mpc_inner = openmc.ZCylinder(r= 68.5/2 * cm)

    mpc_toper_top =  openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1) * cm) #1 in air clearance
    mpc_toper_bot = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #1 in thick MPC shell

    mpc_base_top = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm)
    mpc_base_bot = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 - 1 - 1- 190.5) * cm)

    outer_wall = -mpc_outer & +mpc_inner & -mpc_toper_top & +mpc_base_bot
    top = -mpc_toper_top & +mpc_toper_bot & -mpc_outer
    base = -mpc_base_top & +mpc_base_bot & -mpc_outer

    MPC_region = outer_wall | top | base

    MPC = openmc.Cell(
        name = 'MPC',
        region= MPC_region,
        fill= S_316)

    return MPC

def MPC_Inside(mpc_void_fill=He, blanket_material=S_316_borated):

    """
    Defines the void space inside the MPC, should be filled
    with the BCC universe defined in fuel_blanket_and_pebbles.py
    """

    BCC = Blanket_and_Pebble_Universe(void_fill=mpc_void_fill,
                                      blanket=blanket_material)

    ### represents the cylindrical shape inside the MPC to be filled with the BCC

    void_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #same as mpc_top_bot
    void_base = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm) # Same as mpc_base_top

    void_cyl = openmc.ZCylinder(r= 68.5/2 * cm) # same as mpc_inner

    Void_Region = -void_cyl & -void_top & +void_base

    voidcell = openmc.Cell(name='Inside_MPC',
                          region=Void_Region,
                          fill = BCC)
    
    return voidcell

def MPC_Inside_Region():

    """
    Returns cylindical inside region of MPC
    """

    ### represents the cylindrical shape inside the MPC to be filled with the BCC

    void_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #same as mpc_top_bot
    void_base = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm) # Same as mpc_base_top

    void_cyl = openmc.ZCylinder(r= 68.5/2 * cm) # same as mpc_inner

    Void_Region = -void_cyl & -void_top & +void_base
    
    return Void_Region

def air_annulus(void_fill = air):

    """
    returns cell for the annulus between the MPC and overpack shells

    :input void_fill: fills annulus, should be air or water in accident scenario
    :type void_fill: openmc material
    """

    shell_inner_cyl_inner = openmc.ZCylinder(r=73.5/2 *cm )
    mpc_outer_cyl = openmc.ZCylinder(r= 69.5/2 * cm)

    top_plate_bottom = openmc.ZPlane(z0 = (231.75-4) *cm)
    bot_plate_top = openmc.ZPlane(z0 = 2 *cm)

    annulus_region = -shell_inner_cyl_inner & +mpc_outer_cyl & +bot_plate_top & -top_plate_bottom

    #weird gap between mpc and steel above it 

    air_gap_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75) * cm)
    air_gap_bot =  openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1) * cm)
    air_gap_rad = openmc.ZCylinder(r= 69.5/2 * cm)

    air_gap_region_above = -air_gap_rad & +air_gap_bot & -air_gap_top

    total_region = annulus_region | air_gap_region_above
    
    cell = openmc.Cell(name='Annulus', fill=void_fill, region=total_region)

    return cell


def Cask_and_MPC_Universe(mpc_cool_fill, annulus_fill, outside_fill, blanket_material):

    """
    Returns all the cells for the entire universe for the project import file, all the MPC cells, all the cask cells, all the void cells, every cell. 

    :input mpc_void_fill: material that fills the void space between pebbles and blanket
    :input annulus_fill: material that fills the cask annulus 
    :input outside_fill: material that fills space outside the cask 

    """

    universe = openmc.Universe(name='Cask and MPC Universe')

    universe.add_cells([MPC(), MPC_Concrete(), MPC_Steel(), 
                        Plates(),  Radial_Shield_Steel(), 
                        Radial_Shield_Concrete(), Overpack_Shell(), 
                        MPC_Inside(mpc_cool_fill), 
                        air_annulus(annulus_fill),
                        Outside_Cask(outside_fill)])
    
    return universe



### Meant to model the Cask under normal conditions
### MPC coolant is Hellium
### Annulus is filled with air
### Space outside cask is filled with air
### S_316 doped to 1.0%

cm = 2.54 # 1 inch = 2.54 cm

#### Importing Cross Sections
path = '/home/matthewdisimone/Downloads/endfb80/endfb-viii.0-hdf5/cross_sections.xml'
openmc.config['cross_sections'] = path


#### Defining boundary region inside 
# def Boundary_Region():

#     x1 = openmc.XPlane(x0 = -140/2 * cm, boundary_type='vacuum')
#     x2 = openmc.XPlane(x0 =  140/2* cm, boundary_type='vacuum')
#     y1 = openmc.YPlane(y0 = -140/2 * cm, boundary_type='vacuum')
#     y2 = openmc.YPlane(y0 =  140/2 * cm, boundary_type='vacuum')
#     z0 = openmc.ZPlane(z0 = -10  * cm, boundary_type='vacuum')
#     zT = openmc.ZPlane(z0 =  240 * cm, boundary_type='vacuum')

#     Region_rec = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

#     return Region_rec

def Boundary_Region_cyl():

    """
    Boundary region of a rectangle slightly larger than the cask
    """

    absolute_edge = openmc.ZCylinder(r=150/2 * cm,boundary_type ='vacuum')
    z0 = openmc.ZPlane(z0 =-10 * cm, boundary_type = 'vacuum')
    zT = openmc.ZPlane(z0 = 240 * cm, boundary_type = 'vacuum')

    Region_rec = (-absolute_edge & +z0 & -zT) 

    return Region_rec


#### Defining Cask Universe with fills with relevant materials
Cask_Universe = Cask_and_MPC_Universe(mpc_cool_fill    =  He, 
                                          annulus_fill     =  air,
                                          outside_fill     =  air,
                                          blanket_material = S_316_borated)


def Rectangle():
    """
    Returns the rectangular unverse surrounding the cask
    """
    x1 = openmc.XPlane(x0 = -140/2 * cm, boundary_type='vacuum')
    x2 = openmc.XPlane(x0 =  140/2* cm, boundary_type='vacuum')
    y1 = openmc.YPlane(y0 = -140/2 * cm, boundary_type='vacuum')
    y2 = openmc.YPlane(y0 =  140/2 * cm, boundary_type='vacuum')
    z0 = openmc.ZPlane(z0 = -10  * cm, boundary_type='vacuum')
    zT = openmc.ZPlane(z0 =  240 * cm, boundary_type='vacuum')

    boundary_region = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

    return boundary_region


root_cell = openmc.Cell(fill=Cask_Universe, region=Rectangle())
root_universe = openmc.Universe(cells=[root_cell])

geometry = openmc.Geometry(root_universe)
geometry.export_to_xml()

settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.particles = 100000
settings.batches   = 1000
settings.inactive  = 50
settings.temperature = {'method': 'interpolation'}

#box around mpc
box = openmc.stats.Box(lower_left = (-68.5*cm , -68.6*cm, 20.75 * cm),
                       upper_right = (68.5*cm, 68.5*cm, 211.25*cm))

source = openmc.IndependentSource(space = box)
settings.source = source

mesh = openmc.RegularMesh()
mesh.dimension = (7, 7, 25)
mesh.lower_left = (-140/2*cm, -140/2*cm, -10*cm)
mesh.upper_right = (140/2*cm, 140/2*cm, 240*cm)

settings.entropy_mesh = mesh
settings.export_to_xml()

def plots():
    plot1 = openmc.Plot()
    plot1.basis = 'xz'
    plot1.origin = (0, 2, 240 / 2 * cm)
    plot1.width = ((cm * 2 * 70), (cm * 240))
    plot1.pixels = (700*5, 1200*5)
    plot1.color_by = 'material'
    plot1.type = 'slice'
    plot1.filename = 'xz-slice-normal-cond.png'

    plot2 = openmc.Plot()
    plot2.basis = 'xy'
    plot2.origin = (0, 0, 240 / 2 * cm)
    plot2.width = ((cm * 70 * 2), (cm * 70 * 2))
    plot2.pixels = (1000*5, 1000*5)
    plot2.color_by = 'material'
    plot2.type = 'slice'
    plot2.filename = 'xy-slice-normal-cond.png'

    plots = openmc.Plots([plot1,plot2])
    plots.export_to_xml()
    openmc.plot_geometry()

openmc.run()
sp = openmc.StatePoint(f'statepoint.{settings.batches}.h5')
print("k-effective =", sp.k_combined)
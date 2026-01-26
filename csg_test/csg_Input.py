import openmc
import numpy as np

# CSG construction of isometric cask

###################
# Materials
###################

Outerpack_Shell = openmc.Material('Outer Shell')
Outerpack_Shell.set_density('g/cm3', XXXX)
Outerpack_Shell.add_nuclide(C12) ### Find compositions of carbon steel or astm a516 gr 70

Radial_Shield = openmc.Material('Radial Shield')
Radial_Shield.set_density('g/cm3', xxxx)
Radial_Shield.add_nuclide('Reinforced Concrete')

Overpack_Inner_Shell = openmc.Material('Inner Shell')
Overpack_Inner_Shell.set_density('g/cm3' , xxxx)
Overpack_Inner_Shell.add_nuclide('same data as outerpack shield')

Air = openmc.Material('Air')
Air.set_density(g/cm3)
Air.add_nuclide("brahhhhh air")

MPC = openmc.Material('MPC') #stainless steel
MPC.set_density('g/cm3', density of stainless steel)
MPC.add_nuclide('composition of stainless steel')

Fuel_Basket = openmc.Material('Fuel Basket') #Stainless steel with neutron absorbers (B4C, look up typical examples)
Fuel_Basket.set_density('g/cm3', xxxx)
Fuel_Basket.add_nuclide()

### This should be the entire pebble???
Depleted_Pebble = openmc.Material('DF')
Depleted_Pebble.set_density()
Depleted_Pebble.add_nuclide()

####################
# Cask Construction
####################

model.materials(Outerpack_Shell, Radial_Shield, Overpack_Shield_Plate, Air, MPC, Fuel_Basket)

### Radial Distances
# Outerpack Shell - (132.5 , 131) in
# Radial Sheild - (131 , 74.5) in
# Inner Shell - (74.5 , 73.5) in
# Air Annulus - (73.5 , 69.5) in
# MPC - (69.5 - 68.5)

### Heights
# Outerpack Base - (0 , 4) in
# Outerpack Shell (bottom) - (4 , 5.5) in
# Radial Sheild - (5.5 , 225.75) in
# Outerpack Shell (top) - (225.75 , 227.25)in
# Outerpack Top - (227.25, 231.25) in

#### MPC
# Concrete Top - (216.5, 227.25) in
# Air Annulus - (215.5, 216.5) in
# MPC_top - (214.5 , 215.5) in
# MPC_sides - (25.5, 214.5) in  ; effective MPC height 
# MPC_bottom - (24.5,25.5) in 
# Concrete Base - (4, 24.5) in

# Diam of triso_pebble = 2.3622 in ~ 6cm

#################
# Converted to CM
#################

### Radial Distances, Diameter
# Outerpack Shell - (336.55 , 332.74) cm
# Radial Sheild - (332.74 , 189.23) cm
# Inner Shell - (189.23 , 186.69) cm
# Air Annulus - (186.69 , 176.53) cm
# MPC (General thickness) - (176.53 - 173.99) cm or 1 in

### Heights
# Outerpack Base - (0 , 10.16) cm
# Outerpack Shell (bottom) - (10.16 , 13.97) cm
# Radial Sheild - (13.97 , 573.405) cm
# Outerpack Shell (top) - (573.405 , 578.485) cm
# Outerpack Top - (578.485, 587.375) cm

#### MPC
# Concrete Top - (549.91, 577.215) cm ; radial diameter 176.53 cm
# Air Annulus - (547.37, 549.91) cm
# MPC_top - (544.83 , 547.37) cm
# MPC_sides - (64.77, 544.83) cm  ; effective MPC height 
# MPC_bottom - (62.23 , 64.77) cm ; radial diameter 176.53 cm
# Concrete Base - (10.16, 62.23) cm

# Diam of triso_pebble - 6cm

###################
# Surfaces
###################

# Radial Surfaces

r_baseplate_o = openmc.ZCylinder(r=336.55/2)

r_outerpack_shell_o = openmc.ZCylinder(r=336.55/2, boundary_type='vacuum')
r_outerpack_shell_i = openmc.ZCylinder(r=332.74/2)

r_neutron_shield_o = openmc.ZCylinder(r=332.74/2)
r_neutron_shield_i = openmc.ZCylinder(r=191.83/2)

r_gamma_shield_o = openmc.ZCylinder(r=191.83/2)
r_gamma_sheild_i = openmc.ZCylinder(r=189.23/2)

r_inner_shell_o = openmc.ZCylinder(r=189.23/2)
r_inner_shell_i = openmc.ZCylinder(r=186.69/2)

r_air_annulus_0 = openmc.ZCylinder(r=186.69/2)
r_air_annulus_i = openmc.ZCylinder(r=176.53/2)

r_mpc_o = openmc.ZCylinder(r=176.53/2)
r_mpc_i = openmc.ZCylinder(r=173.99/2)


# Z Surface Heights

z_bottom = openmc.ZPlane(z0=0.0, boundary_type='vacuum')

z_steel_baseplate = openmc.ZPlane(z0=0)
z_steel_baseplate = openmc.ZPlane(z0=10.16)

z_bottom_shell_b = openmc.ZPlane(z0=10.16)
z_bottom_shell_t = openmc.ZPlane(z0=13.97)

z_radial_sheilds_b = openmc.ZPlane(z0=13.97)
z_radial_sheilds_t = openmc.ZPlane(z0=573.405)

z_top_shell_b = openmc.ZPlane(z0=573.405)
z_top_shell_t = openmc.ZPlane(z0=578.485)

z_steel_top_b = openmc.ZPlane(z0=578.485)
z_steel_top_t = openmc.ZPlane(z0=587.375)

z_top = openmc.ZPlane(z0=587.375, boundary_type='vacuum')

# MPC Construction

r_mpc_neutron_gamma_sheilds = openmc.ZCylinder(r=1776.53)

z_mpc_concrete_base_t = openmc.ZPlane(z0=52.07)
z_mpc_concrete_base_b = openmc.ZPlane(z0=10.16)

z_mpc_gamma_shield_b = openmc.ZPlane(z0=52.07)
z_mpc_gamma_shield_t = openmc.ZPlane(z0=62.23)

z_mpc_bottom_b = openmc.ZPlane(z0=62.23)
z_mpc_bottom_t = openmc.ZPlane(z0=64.77)

z_mpc_sides_b = openmc.ZPlane(z0=64.77)
z_mpc_sides_t = openmc.ZPlane(z0=544.83)

z_mpc_top_b = openmc.ZPlane(z0=544.83)
z_mpc_top_t = openmc.ZPlane(z0=547.37)

z_mpc_air_annulus_b = openmc.ZPlane(z0=547.37)
z_mpc_air_annulus_t = openmc.ZPlane(z0=548.91)

z_mpc_gamma_top_b = openmc.ZPlane(z0=548.91)
z_mpc_gamma_top_t = openmc.ZPlane(z0=551.18)

z_mpc_concrete_top_b = openmc.ZPlane(z0=551.18)
z_mpc_concrete_top_t = openmc.ZPlane(z0=578.485)

### Component Construction

outerpack_shell = openmc.Cell(name = 'Outerpack Shell',
                              fill = Outerpack_Shell ,
                              region = (
                                - r_outerpack_shell_i & 
                                + r_outerpack_shell_o &
                                - z_bottom_shell_b & 
                                + z_bottom_shell_t
                              ))

def unit_cell_constructor():
  Z_top = openmc.ZPlane(z=12.54)
  Z_bottom = openmc.ZPlane(z=0)
  X_back = openmc.XPlane(x=6.538)
  X_front = openmc.XPlane(x=0) # at origin
  Y_Left = openmc.YPlane(y=0) # at origin
  Y_Right = openmc.YPlane(y=6.538)

  # XZ Plane
  #Left half octogon big (X,Y,Z)
  Big_Left_Half_Octogon = {(0,     0 , 3.251),
               (1.51,  0 , 3.251),
               (3.019, 0 , 4.76),
               (3.019, 0 , 7.78),
               (1.51,  0 , 9.289)}
    
  Big_Bottom_Half_Octogon = {(0.25, 0 , 0),
                              (0.25, 0 , 1.51),
                              (1.759, 0 , 3.019),
                              (4.779, 0, 3.019),
                              (6.288, 0 , 1.51)}
    
  Big_Right_Half_Octogon = {(6.538, 0 , 3.251),
                              (5.028, 0 , 3.251),
                              (3.519, 0 , 4.76),
                              (3.519, 0 , 7.78),
                              (5.028, 0 , 9.289)}
    
  Big_Bottom_Half_Octogon = {(0.25, 0 , 12.54 - 0),
                              (0.25, 0 ,  12.54 - 1.51),
                              (1.759, 0 , 12.54 - 3.019),
                              (4.779, 0, 12.54 - 3.019),
                              (6.288, 0 , 12.54 - 1.51)}
    
  ## Holder thing XZ (X,Y,Z)

  XYZ_Holder = [(0,0),
                 (0.25,1.51),
                 (1.759,3.019),
                 (4.779,3.019),
                 (6.288,1.51),
                 (6.288,0),
                 (6.538,0),
                 (6.538,3.251),
                 (5.028,3.251),
                 (3.519,4.76),
                 (3.519,7.78),
                 (5.028,9.289),
                 (6.538,9.289),
                 (6.538,12.54),
                 (6.288,12.54),
                 (6.288,11.03),
                 (4.779,9.521),
                 (1.759,9.521),
                 (0.25,11.03),
                 (0.25,12.54),
                 (0,12.54),
                 (0,9.289),
                 (1.51, 9.289),
                 (3.019, 7.78),
                 (3.019, 4.76),
                 (1.51,3.251),
                 (0,1.51),
                 (0,0)]
    
  XZ_Plane = []

  for i in range(len(XYZ_Holder)):
    x1, z1 = XYZ_Holder[i]
    x2, z2 = XYZ_Holder[(i + 1) % len(XYZ_Holder)]

    a =  z2 - z1
    c = -(x2 - x1)
    d = -(a*x1 + c*z1)

    line = openmc.Plane(a=a, c=c, d=d)

    XZ_Plane.append(line) 

  XZ_Region = openmc.Region()

  for line in XZ_Plane:
       XY_region &= line

  XZ_Holder = XZ_Region & +Y_Left & -Y_Right
  YZ_Holder = XZ_Region & X_front & - X_back

  holder_cell = openmc.Cell(
    name = 'Unit Corr Cell'
    region=XZ_Holder & YZ_Holder,
    fill=Fuel_Basket)


  universe = openmc.Universe(cells=[holder_cell])
  geometry = openmc.Geometry(universe)
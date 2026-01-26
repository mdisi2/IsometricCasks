import openmc

###Constructs the cask and the MPC of the holtec 100, inside mpc 'universe' to be filled later

#everything will be in inches multipled by the conversion factor

cm = 2.54 # 1inch = 2.54cm

def Overpack_Shells():
    #carbon steel or astm a516 gr 70

    outer_cyl_outer = openmc.ZCylinder(r=132.5/2 * cm)
    outer_cyl_inner = openmc.ZCylinder(r=131/2 * cm)

    inner_cyl_outer = openmc.ZCylinder(r=75/2 * cm)
    inner_cyl_inner = openmc.ZCylinder(r=73.5/2 *cm )

    topper_outer = openmc.ZCylinder(r=131/2 * cm)
    topper_inner = openmc.ZCylinder(r=73.5/2 * cm)

    h0 = openmc.ZPlane(z0=2 * cm)
    hT = openmc.ZPlane(z0 = (213.25 - (6)) * cm)

    H = openmc.ZPlane(z0 = (213.25 - (6)) * cm)
    HB = openmc.ZPlane((213.25 - (7.5)) * cm)

    # outer_shell_region = 

def Radial_Shield():

    concrete_outer = openmc.ZCylinder(r=131/2 * cm)
    concrete_inner = openmc.ZCyliner(r=(131 - 26.75)/2 * cm) #26.75 in thick

    steel_outer = openmc.ZCyliner(r=((131/2) - 26.75) * cm)
    steel_inner = openmc.ZCylinder(r=75/2 * cm) #3.75 in thick

    h0 = openmc.ZPlane(z0 = 2*cm)
    ht = openmc.ZPlane((213.25 - (7.5)) * cm)

def Top_and_Bottom_Plates():

    rad = openmc.ZCylinder(r=132.5/2 * cm)

    top_plate_top = openmc.ZPlane(z0 = 231.75 *cm)
    top_plate_bottom = openmc.ZPlane(z0 = (231.75-4) *cm)

    bot_plate_top = openmc.ZPlane(z0 = 2 *cm)
    bot_plate_bot = openmc.ZPlane(z0 = 0 *cm)

def MPC_Concrete_Base_and_Top():

    rad = openmc.ZCylinder(r=69.2/2 * cm)

    top_conc_top = openmc.ZPlane(z0 = (231.75-4) *cm)
    top_conc_bot = openmc.ZPlane(z0 = (231.75-4-10.75) *cm)

    base_conc_top = openmc.ZPlane(z0=17.5 * cm)
    base_conc_bot = openmc.ZPlane(Z0=2*cm)

def MPC_Steel_Base_and_Top():

    rad = openmc.ZCylinder(r=69.2/2 * cm)

    top_steel_top = openmc.ZPlane(z0 = (231.75-4-10.75) *cm)
    top_steel_bot = openmc.ZPlane(Z0= (231.75-4-10.75 - 3.75) * cm)

    base_steel_top = openmc.ZPlane(z0 = openmc.ZPlane(Z0= (231.75-4-10.75 - 3.75 - 1 - 1 - 1- 190.5) * cm)) #same as MPC base bottom
    base_steel_bot = openmc.ZPlane(z0=17.5 * cm) #same as base concrete top


def MPC():

    mpc_outer = openmc.ZCylinder(r= 69.5/2 * cm)
    mpc_inner = openmc.ZCylinder(r= 68.5/2 * cm)

    mpc_toper_top =  openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1) * cm) #1 in air clearance
    mpc_toper_bot = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #1 in thick MPC shell

    mpc_base_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm)
    mpc_base_bot = openmc.ZPlane(z0 = openmc.ZPlane(Z0= (231.75-4-10.75 - 3.75 - 1 - 1 - 1- 190.5) * cm))


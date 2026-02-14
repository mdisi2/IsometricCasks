import openmc
from Function_Folder.mats import S_316_borated, Concrete, A516_70, S_316, air, He, graphite, depleted_fuel, buffer, PyC, SiC
from fuel_blanket_and_pebbles import Blanket_and_Pebble_Universe

###Constructs the cask and the MPC of the holtec 100, inside mpc 'universe' to be filled later within a sim file
#everything will be in inches multipled by the conversion factor

cm = 2.54 # 1-inch = 2.54cm

def Boudary_Region():

    outer_cyl = openmc.ZCylinder(r=133/2 * cm, boundary_type='vacuum')
    h0 = openmc.ZPlane(z0=0, boundary_type='vacuum')
    hT = openmc.ZPlane(z0=233 * cm, boundary_type='vacuum')

    Region = -outer_cyl & +h0 & -hT

    return Region


def Overpack_Shells():

    #carbon steel outer and inner cylindrical shells

    outer_cyl_outer = openmc.ZCylinder(r=132.5/2 * cm)
    outer_cyl_inner = openmc.ZCylinder(r=131/2 * cm)

    inner_cyl_outer = openmc.ZCylinder(r=75/2 * cm)
    inner_cyl_inner = openmc.ZCylinder(r=73.5/2 *cm )

    topper_outer = openmc.ZCylinder(r=131/2 * cm)
    topper_inner = openmc.ZCylinder(r=73.5/2 * cm)

    h0 = openmc.ZPlane(z0=2 * cm)
    hT = openmc.ZPlane(z0 = (231.25 - (6)) * cm)

    H = openmc.ZPlane(z0 = (231.25 - (6)) * cm)
    HB = openmc.ZPlane(z0 = (231.25 - (7.5)) * cm)

    outer_shell_region = -outer_cyl_outer & +outer_cyl_inner & -hT & +h0
    inner_shell_region = -inner_cyl_outer & +inner_cyl_inner & -hT & +h0 
    topper_region = -topper_outer & +topper_inner & -H & +HB

    Overpack_Region = outer_shell_region | inner_shell_region | topper_region

    Overpack = openmc.cell.Cell(name='Overpack Shells', fill=A516_70, region=Overpack_Region)

    return Overpack


def Radial_Shield_Concrete():
    #portland concrete ii

    concrete_outer = openmc.ZCylinder(r=131/2 * cm)
    concrete_inner = openmc.ZCylinder(r=(131/2 - 26.75) * cm) #26.75 in thick

    h0 = openmc.ZPlane(z0 = 2*cm)
    ht = openmc.ZPlane(z0 = (231.25 - (7.5)) * cm)

    Concrete_Region = -concrete_outer & +concrete_inner & +h0 & -ht

    Concrete_Sheild = openmc.Cell(
        name = 'Radial Shield Concrete',
        region= Concrete_Region,
        fill= Concrete)
    
    return Concrete_Sheild

def Radial_Shield_Steel():

    # not sure yet
    
    steel_outer = openmc.ZCylinder(r=(131/2 - 26.75) * cm)
    steel_inner = openmc.ZCylinder(r=75/2 * cm) #3.75 in thick

    h0 = openmc.ZPlane(z0 = 2*cm)
    ht = openmc.ZPlane((231.25 - (7.5)) * cm)

    Steel_Region = -steel_outer & +steel_inner & +h0 & -ht

    Steel_Shield = openmc.Cell(
        name = 'Radial Shield Steel',
        region= Steel_Region,
        fill= A516_70)

    return Steel_Shield
    
def Plates():

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

    #portland concrete ii

    rad = openmc.ZCylinder(r=69.2/2 * cm)

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

    rad = openmc.ZCylinder(r=69.2/2 * cm)

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

def MPC_Void():

    BCC = Blanket_and_Pebble_Universe(coolant=He)

    ### represents the cylindrical shape inside the MPC to be filled

    void_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #same as mpc_top_bot
    void_base = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm) # Same as mpc_base_top

    void_cyl = openmc.ZCylinder(r= 68.5/2 * cm) # same as mpc_inner

    Void_Region = -void_cyl & -void_top & +void_base

    voidcel = openmc.Cell(name='Inside_MPC',
                          region=Void_Region,
                          fill = BCC)
    
    return voidcel

def Cask_and_MPC_universe(ex_mpc=air, en_mpc=He):

    """
    Universe for the project impot file

    ex_mpc : openmc material that fills the void space outside the MPC but inside the cask in the annuls and such

    en_mpc : openmc material that fills the inside of the MPC, helium, seawater, etc

    """

    universe = openmc.Universe(name='Cask and MPC Universe')
    universe.add_cells([MPC(), MPC_Concrete(), MPC_Steel(), 
                                     Plates(),  Radial_Shield_Steel(), 
                                     Radial_Shield_Concrete(), Overpack_Shells(), 
                                     MPC_Void()])
    
    return universe


### TODO make void airspace outside cask

settings = openmc.Settings()


geometry = openmc.Geometry([MPC(), MPC_Concrete(), MPC_Steel(), Plates(),  Radial_Shield_Steel(), Radial_Shield_Concrete(), Overpack_Shells(),MPC_Void()])
geometry.root_universe.bounding_region = Boudary_Region()

geometry.export_to_xml()
settings.export_to_xml()

# Plotting hehe

plot1 = openmc.Plot()
plot1.basis = 'xz'
plot1.origin = (0, 2, 240 / 2 * cm)
plot1.width = (400, 700)
plot1.pixels = (1600, 1400*2)
plot1.color_by = 'cell'
plot1.type = 'slice'
plot1.filename = 'cask_xsection_yz_filled_stag.png'

plot2 = openmc.Plot()
plot2.basis = 'xy'
plot2.origin = (0, 0, 248.9 / 2 * cm)
plot2.width = (400, 400)
plot2.pixels = (1200*3, 1200*3)
plot2.color_by = 'cell'
plot2.type = 'slice'
plot2.filename = 'cask_xsection_xy_filled_stag.png'

plots = openmc.Plots([plot1,plot2])
plots.export_to_xml()
openmc.plot_geometry()
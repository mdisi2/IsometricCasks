import openmc
from Function_Folder.material_init import S_316_borated, Concrete, A516_70, S_316, air, He, graphite, depleted_fuel, buffer, PyC, SiC
from fuel_blanket_and_pebbles import Blanket_and_Pebble_Universe

###Constructs the cask and the MPC of the holtec 100, inside mpc 'universe' to be filled later within a sim file
#everything will be in inches multipled by the conversion factor

cm = 2.54 # 1-inch = 2.54cm

def Boundary_Region():

    outer_cyl = openmc.ZCylinder(r=133/2 * cm, boundary_type='vacuum')
    h0 = openmc.ZPlane(z0=0 * cm, boundary_type='vacuum')
    hT = openmc.ZPlane(z0 = 231.75 *cm)

    Region_cyl = -outer_cyl & +h0 & -hT

    x1 = openmc.XPlane(x0 = -240 * cm, boundary_type='vacuum')
    x2 = openmc.XPlane(x0 = 240 * cm, boundary_type='vacuum')
    y1 = openmc.YPlane(y0 = -240 * cm, boundary_type='vacuum')
    y2 = openmc.YPlane(y0 = 240 * cm, boundary_type='vacuum')
    z0 = openmc.ZPlane(z0=-10 * cm, boundary_type='vacuum')
    zT = openmc.ZPlane(z0=240 * cm, boundary_type='vacuum')

    Region_rec = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

    return Region_rec

def Space_Outside_Cask(void_fill):
    
    outer_cyl = openmc.ZCylinder(r=132.5/2 * cm)
    h0 = openmc.ZPlane(z0 = 0 * cm)
    hT = openmc.ZPlane(z0 = 231.75 * cm)

    Region_cyl = -outer_cyl & +h0 & -hT

    x1 = openmc.XPlane(x0 =-140 * cm)
    x2 = openmc.XPlane(x0 = 140 * cm)
    y1 = openmc.YPlane(y0 =-140 * cm)
    y2 = openmc.YPlane(y0 = 140 * cm)
    z0 = openmc.ZPlane(z0 =-10 * cm)
    zT = openmc.ZPlane(z0 = 240 * cm)

    Region_rec = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

    cell = openmc.Cell(name='Outside Cask Space', fill=void_fill, region=Region_rec & ~Region_cyl)

    return cell


def Overpack_Shells():

    #carbon steel outer and inner cylindrical shells

    outer_cyl_outer = openmc.ZCylinder(r=132.5/2 * cm)
    outer_cyl_inner = openmc.ZCylinder(r=131/2 * cm)

    inner_cyl_outer = openmc.ZCylinder(r=75/2 * cm)
    inner_cyl_inner = openmc.ZCylinder(r=73.5/2 *cm )

    h0 = openmc.ZPlane(z0=2 * cm)
    hT = openmc.ZPlane(z0 = (231.75-4) *cm)

    outer_shell_region = -outer_cyl_outer & +outer_cyl_inner & -hT & +h0
    inner_shell_region = -inner_cyl_outer & +inner_cyl_inner & -hT & +h0 

    Overpack_Region = outer_shell_region | inner_shell_region

    Overpack = openmc.cell.Cell(name='Overpack Shells', fill=A516_70, region=Overpack_Region)

    return Overpack


def Radial_Shield_Concrete():
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

    #gamma sheild 
    
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

def MPC_Inside(mpc_void_fill=He):

    BCC = Blanket_and_Pebble_Universe(void_fill=mpc_void_fill)

    ### represents the cylindrical shape inside the MPC to be filled

    void_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #same as mpc_top_bot
    void_base = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm) # Same as mpc_base_top

    void_cyl = openmc.ZCylinder(r= 68.5/2 * cm) # same as mpc_inner

    Void_Region = -void_cyl & -void_top & +void_base

    voidcel = openmc.Cell(name='Inside_MPC',
                          region=Void_Region,
                          fill = BCC)
    
    return voidcel

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


def Cask_and_MPC_Universe(mpc_cool_fill, annulus_fill, outside_fill):

    """
    Universe for the project import file

    :input mpc_void_fill: material that fills the void space between pebbles and blanket
    :input annulus_fill: material that fills the cask annulus 
    :input outside_fill: material that fills space outside the cask 

    """

    universe = openmc.Universe(name='Cask and MPC Universe')

    universe.add_cells([MPC(), MPC_Concrete(), MPC_Steel(), 
                        Plates(),  Radial_Shield_Steel(), 
                        Radial_Shield_Concrete(), Overpack_Shells(), 
                        MPC_Inside(mpc_cool_fill), 
                        air_annulus(annulus_fill),
                        Space_Outside_Cask(outside_fill)])
    
    return universe



def xml():
    settings = openmc.Settings()


    geometry = openmc.Geometry([MPC(), MPC_Concrete(), MPC_Steel(), Plates(),  Radial_Shield_Steel(), Radial_Shield_Concrete(), Overpack_Shells(), MPC_Inside(), air_annulus(air), Space_Outside_Cask(air)])
    geometry.root_universe.bounding_region = Boundary_Region()

    geometry.export_to_xml()
    settings.export_to_xml()

# Plotting hehe

def plotter():

    plot1 = openmc.Plot()
    plot1.basis = 'xz'
    plot1.origin = (0, 2, 240 / 2 * cm)
    plot1.width = (400, 700)
    plot1.pixels = (1600, 1400*2)
    plot1.color_by = 'material'
    plot1.type = 'slice'
    plot1.filename = 'cask_xsection_yz_filled_stag.png'

    plot2 = openmc.Plot()
    plot2.basis = 'xy'
    plot2.origin = (0, 0, 248.9 / 2 * cm)
    plot2.width = (400, 400)
    plot2.pixels = (1200*2, 1200*2)
    plot2.color_by = 'material'
    plot2.type = 'slice'
    plot2.filename = 'cask_xsection_xy_filled_stag.png'

    plots = openmc.Plots([plot1,plot2])
    plots.export_to_xml()
    openmc.plot_geometry()
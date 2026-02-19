import openmc
import cask_and_mpc as cam
from Function_Folder.material_init import air, He, S_316_borated

### Meant to model the Cask under normal conditions
### MPC coolant is Hellium
### Annulus is filled with air
### Space outside cask is filled with air
### S_316 doped to 1.0%

# openmc.config['cross_sections'] = 

cm = 2.54 # 1 inch = 2.54 cm

def Boundary_Region():

    x1 = openmc.XPlane(x0 = -140/2 * cm, boundary_type='vacuum')
    x2 = openmc.XPlane(x0 =  140/2* cm, boundary_type='vacuum')
    y1 = openmc.YPlane(y0 = -140/2 * cm, boundary_type='vacuum')
    y2 = openmc.YPlane(y0 =  140/2 * cm, boundary_type='vacuum')
    z0 = openmc.ZPlane(z0 = -10  * cm, boundary_type='vacuum')
    zT = openmc.ZPlane(z0 =  240 * cm, boundary_type='vacuum')

    Region_rec = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

    return Region_rec

def MPC_Inside_Region():

    """represents the cylindrical shape inside the MPC to be filled with the BCC"""

    void_top = openmc.ZPlane(z0= (231.75-4-10.75 - 3.75 - 1 -1) * cm) #same as mpc_top_bot
    void_base = openmc.ZPlane(z0 = (231.75-4-10.75 - 3.75 - 1 -1 - 190.5) * cm) # Same as mpc_base_top

    void_cyl = openmc.ZCylinder(r= 68.5/2 * cm) # same as mpc_inner

    Void_Region = -void_cyl & -void_top & +void_base

    return Void_Region

Cask_Universe = cam.Cask_and_MPC_Universe(mpc_cool_fill    =  He, 
                                          annulus_fill     =  air,
                                          outside_fill     =  air,
                                          blanket_material = S_316_borated)

geometry = openmc.Geometry(Cask_Universe)
geometry.root_universe.bounding_region = Boundary_Region()
geometry.export_to_xml()

settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.particles = 1000
settings.batches   = 20
settings.inactive  = 30

source = openmc.Source()
source.space = openmc.CylindricalIndependent(r=(0,86.995), origin=(0,0,0))
source.angle = openmc.stats.Isotropic()
settings.source = source

mesh = openmc.RegularMesh()
mesh.dimension = (7, 7, 25)
mesh.lower_left = (-140/2*cm, -140/2*cm, -10*cm)
mesh.upper_right = (140/2*cm, 140/2*cm, 240*cm)

settings.entropy_mesh = mesh
settings.export_to_xml()

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
plot2.pixels = (700*5, 1000*5)
plot2.color_by = 'material'
plot2.type = 'slice'
plot2.filename = 'xy-slice-normal-cond.png'

plots = openmc.Plots([plot1,plot2])
plots.export_to_xml()
openmc.plot_geometry()
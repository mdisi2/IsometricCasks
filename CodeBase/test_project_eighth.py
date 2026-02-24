import openmc
import cask_and_mpc as cam
from Function_Folder.material_init import air, He, S_316, fresh_fuel

### Meant to model the Cask under normal conditions
### MPC coolant is Hellium
### Annulus is filled with air
### Space outside cask is filled with air
### S 316 normal
### 1/8th of the cask with parabolic boundry coditions

cm = 2.54 # 1 inch = 2.54 cm

#### Importing Cross Sections
path = '/home/matthewdisimone/Downloads/endfb80/endfb-viii.0-hdf5/cross_sections.xml'
openmc.config['cross_sections'] = path

#### Defining boundary region inside 
def Boundary_Region():

    """
    Boundary region of a cylander slightly larger than the cask
    """

    absolute_edge = openmc.ZCylinder(r=150/2 * cm,boundary_type ='vacuum')
    z0 = openmc.ZPlane(z0 =-10 * cm, boundary_type = 'vacuum')
    zT = openmc.ZPlane(z0 = 240 * cm, boundary_type = 'vacuum')

    x_axis = openmc.XPlane(x0=0,boundary_type='reflective')
    s1 = openmc.Plane(a=1,b=-2,c=0,d=0,boundary_type='reflective')

    Region_rec = (-absolute_edge & +z0 & -zT) & (-s1 & +x_axis) 

    return Region_rec


#### Defining Cask Universe with fills with relevant materials
Cask_Universe = cam.Cask_and_MPC_Universe(mpc_cool_fill    =  He, 
                                          annulus_fill     =  air,
                                          outside_fill     =  air,
                                          blanket_material = S_316)


root_cell = openmc.Cell(fill=Cask_Universe, region=Boundary_Region())
root_universe = openmc.Universe(cells=[root_cell])

geometry = openmc.Geometry(root_universe)
geometry.export_to_xml()

settings = openmc.Settings()
settings.run_mode = 'eigenvalue'
settings.particles = 50000
settings.batches   = 300
settings.inactive  = 50
settings.temperature = {'method': 'interpolation'}

#box around mpc slice
box_slice = openmc.stats.Box(lower_left = (0*cm , 0*cm, 20.75 * cm),
                       upper_right = (68.5*cm, 68.5*cm, 211.25*cm))

source = openmc.IndependentSource(space = box_slice)
settings.source = source

mesh = openmc.RegularMesh()
mesh.dimension = (14, 14,  50)
mesh.lower_left = (0, 0, -10*cm)
mesh.upper_right = (140/2*cm, 140/2*cm, 240*cm)

settings.entropy_mesh = mesh
settings.export_to_xml()

def plots():
    plot1 = openmc.Plot()
    plot1.basis = 'xz'
    plot1.origin = (70*cm, cm, 240 / 2 * cm)
    plot1.width = ((cm * 2 * 70), (cm * 240))
    plot1.pixels = (700*5, 1200*5)
    plot1.color_by = 'material'
    plot1.type = 'slice'
    plot1.filename = 'xz-slice-eight.png'

    plot2 = openmc.Plot()
    plot2.basis = 'xy'
    plot2.origin = (35*cm, 35*cm, 120 * cm)
    plot2.width = ((cm * 90 * 2), (cm * 75 * 2))
    plot2.pixels = (1000*3, 1000*3)
    plot2.color_by = 'material'
    plot2.type = 'slice'
    plot2.filename = 'xy-slice-eight.png'

    plots = openmc.Plots([plot1,plot2])
    plots.export_to_xml()
    openmc.plot_geometry()

openmc.run()
sp = openmc.StatePoint(f'statepoint.{settings.batches}.h5')
print("k-effective =", sp.k_combined)


### At 100,000 particle batches, shannon entorpy might converge at like 50 batches the way its looking

### Do one w/o doped stainless steel to more neutons
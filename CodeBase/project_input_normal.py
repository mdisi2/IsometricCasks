import openmc
import cask_and_mpc as cam
from Function_Folder.material_init import air, He

### Meant to model the Cask under normal conditions
### MPC coolant is Hellium
### Annulus is filled with air
### Space outside cask is filled with air

cm = 2.54 # 1 inch = 2.54 cm

def Region_Outside_Cask():
    
    outer_cyl = openmc.ZCylinder(r=133/2 * cm)
    h0 = openmc.ZPlane(z0=0 * cm)
    hT = openmc.ZPlane(z0=233 * cm)

    Region_cyl = -outer_cyl & +h0 & -hT

    x1 = openmc.XPlane(x0 = -240 * cm)
    x2 = openmc.XPlane(x0 = 240 * cm)
    y1 = openmc.YPlane(y0 = -240 * cm)
    y2 = openmc.YPlane(y0 = 240 * cm)
    z0 = openmc.ZPlane(z0=-10 * cm)
    zT = openmc.ZPlane(z0=240 * cm)

    Region_rec = +x1 & -x2 & +y1 & -y2 & +z0 & -zT

    return Region_rec & ~Region_cyl

Cask_Universe = cam.Cask_and_MPC_Universe(mpc_cool_fill  =  He, 
                                          annulus_fill   =  air,
                                          outside_fill   =  air)

geometry = openmc.Geometry(Cask_Universe)
geometry.root_universe.bounding_region = Region_Outside_Cask()
geometry.export_to_xml()


plot1 = openmc.Plot()
plot1.basis = 'xz'
plot1.origin = (0, 2, 240 / 2 * cm)
plot1.width = (400, 700)
plot1.pixels = (1600, 1400*2)
plot1.color_by = 'material'
plot1.type = 'slice'
plot1.filename = 'project_input_normal.png'

plots = openmc.Plots([plot1])
plots.export_to_xml()
openmc.plot_geometry()
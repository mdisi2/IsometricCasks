from math import pi
import numpy as np
import matplotlib.pyplot as plt
import openmc
import openmc.model

fuel = openmc.Material(name='Fuel')
fuel.set_density('g/cm3', 10.5)
fuel.add_nuclide('U235', 4.6716e-02)
fuel.add_nuclide('U238', 2.8697e-01)
fuel.add_nuclide('O16',  5.0000e-01)
fuel.add_element('C', 1.6667e-01)

buff = openmc.Material(name='Buffer')
buff.set_density('g/cm3', 1.0)
buff.add_element('C', 1.0)
buff.add_s_alpha_beta('c_Graphite')

PyC1 = openmc.Material(name='PyC1')
PyC1.set_density('g/cm3', 1.9)
PyC1.add_element('C', 1.0)
PyC1.add_s_alpha_beta('c_Graphite')

PyC2 = openmc.Material(name='PyC2')
PyC2.set_density('g/cm3', 1.87)
PyC2.add_element('C', 1.0)
PyC2.add_s_alpha_beta('c_Graphite')

SiC = openmc.Material(name='SiC')
SiC.set_density('g/cm3', 3.2)
SiC.add_element('C', 0.5)
SiC.add_element('Si', 0.5)

graphite = openmc.Material()
graphite.set_density('g/cm3', 1.1995)
graphite.add_element('C', 1.0)
graphite.add_s_alpha_beta('c_Graphite')

# Create TRISO universe
spheres = [openmc.Sphere(r=1e-4*r)
           for r in [215., 315., 350., 385.]]
cells = [openmc.Cell(fill=fuel, region=-spheres[0]),
         openmc.Cell(fill=buff, region=+spheres[0] & -spheres[1]),
         openmc.Cell(fill=PyC1, region=+spheres[1] & -spheres[2]),
         openmc.Cell(fill=SiC, region=+spheres[2] & -spheres[3]),
         openmc.Cell(fill=PyC2, region=+spheres[3])]
triso_univ = openmc.Universe(cells=cells)

Sphere_Where_Trisos_Exist = openmc.Sphere(r=2.5,boundary_type='transmission') # out of the 3cm r, only 0.5 thickness region on edge with no fuel
region = -Sphere_Where_Trisos_Exist


outer_radius = 425.*1e-4
centers = openmc.model.pack_spheres(radius=outer_radius, region=region, pf=0.3)
trisos = [openmc.model.TRISO(outer_radius, triso_univ, center) for center in centers]

centers = np.vstack([triso.center for triso in trisos])
print(centers.min(axis=0))
print(centers.max(axis=0))

box = openmc.Cell(region=region)
lower_left, upper_right = box.region.bounding_box
shape = (3, 3, 3)
pitch = (upper_right - lower_left)/shape
lattice = openmc.model.create_triso_lattice(
    trisos, lower_left, pitch, shape, graphite)

box = openmc.Cell(region=region, fill=lattice)

universe = openmc.Universe(cells=[box])
geometry = openmc.Geometry(universe)
geometry.export_to_xml()

materials = list(geometry.get_all_materials().values())
openmc.Materials(materials).export_to_xml()

plot = openmc.Plot()
plot.origin = (0,0,0)
plot.width = (6,6)
plot.pixels = (1000,1000)
plot.color_by = 'material'
plot.colors = {graphite: 'gray'}

plots = openmc.Plots([plot])
plots.export_to_xml()
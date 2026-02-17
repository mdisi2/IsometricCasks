from math import pi
import numpy as np
import openmc
from .material_init import SiC, PyC, buffer, depleted_fuel, graphite

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

root_univ = openmc.Universe(cells=[fuel_zone_cell,graphite_zone])
geom = openmc.Geometry(root_univ)
geom.export_to_xml()


def Depleted_Triso_Universe():
    return root_univ



### This file does everything it should, please do not touch!!! 
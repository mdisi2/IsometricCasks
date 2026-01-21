import openmc

Fuel_Basket = openmc.Material(name='Fuel Basket') #Stainless steel with neutron absorbers (B4C, look up typical examples)
Fuel_Basket.set_density('g/cm3', 10.0)
Fuel_Basket.add_element('Fe', 0.70)

materials = openmc.Materials([Fuel_Basket])

### CSG

Z_top = openmc.ZPlane(z0=12.54)
Z_bottom = openmc.ZPlane(z0=0)
X_back = openmc.XPlane(x0=6.538)
X_front = openmc.XPlane(x0=0) # at origin
Y_Left = openmc.YPlane(y0=0) # at origin
Y_Right = openmc.YPlane(y0=6.538)
  
    
## Holder thing XZ (X,Y,Z)

XYZ_Points =    [(0,0),
                 (0.25,0),
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
                 (0,3.251),
                 (0,1.51)]

x_distance = 6.538

XZ_left_octogon_pts = [(0,8.769),
                       (1.51,8.769),
                       (2.499,7.78),
                       (2.499,4.76),
                       (1.51,3.771),
                       (0,3.771)]

XZ_right_octogon_pts = [(x_distance - 0,8.769),
                       (x_distance - 1.51,8.769),
                       (x_distance - 2.499,7.78),
                       (x_distance -2.499,4.76),
                       (x_distance - 1.51, 3.771),
                       (x_distance - 0, 3.771)]

XZ_bottom_pts = [(0.77,0),
                 (0.77,1.51),
                 (1.759,2.499),
                 (4.779,2.499),
                 (5.768,1.51),
                 (5.768,0)]

XZ_top_pts = [(0.77,12.54 - 0),
                 (0.77,12.54 - 1.51),
                 (1.759,12.54 - 2.499),
                 (4.779,12.54 - 2.499),
                 (5.768,12.54 - 1.51),
                 (5.768,12.54 - 0)]


XZ_Polygon = openmc.model.Polygon(basis='xz', points=XYZ_Points)
XZ_LOctogon = openmc.model.Polygon(basis='xz', points=XZ_left_octogon_pts)
XZ_ROctogon = openmc.model.Polygon(basis='xz', points=XZ_right_octogon_pts)
XZ_BOctogon = openmc.model.Polygon(basis='xz', points=XZ_bottom_pts)
XZ_TOctogon = openmc.model.Polygon(basis='xz', points=XZ_top_pts)

YZ_Polygon = openmc.model.Polygon(basis='yz', points=XYZ_Points)
YZ_LOctogon = openmc.model.Polygon(basis='yz', points=XZ_left_octogon_pts)
YZ_ROctogon = openmc.model.Polygon(basis='yz', points=XZ_right_octogon_pts)
YZ_BOctogon = openmc.model.Polygon(basis='yz', points=XZ_bottom_pts)
YZ_TOctogon = openmc.model.Polygon(basis='yz', points=XZ_top_pts)

xy_region  = -XZ_Polygon & +Y_Left & -Y_Right & +YZ_TOctogon & +YZ_BOctogon & +YZ_LOctogon & +YZ_ROctogon

yz_region  = -YZ_Polygon & +X_front & -X_back  & +XZ_TOctogon & +XZ_BOctogon & +XZ_LOctogon & +XZ_ROctogon

holder_cell = openmc.Cell(
    name = 'Unit Corr Cell',
    region= xy_region,
    fill= Fuel_Basket)

holder_cell2 = openmc.Cell(
    name = 'Unit Corr Cell',
    region= yz_region,
    fill= Fuel_Basket)

geometry = openmc.Geometry([holder_cell, holder_cell2])

settings = openmc.Settings()

materials.export_to_xml()
geometry.export_to_xml()
settings.export_to_xml()

plotxz = openmc.Plot()
plotxz.basis = 'xz'
plotxz.origin = (6.538/2, 0, 12.54/2)
plotxz.width = (10, 15)
plotxz.pixels = (100, 150)
plotxz.color_by = 'cell'

plotyz = openmc.Plot()
plotyz.basis = 'yz'
plotyz.origin = (0, 6.538/2, 12.54/2)
plotyz.width = (10, 15)
plotyz.pixels = (100, 150)
plotyz.color_by = 'cell'

plotxy = openmc.Plot()
plotxy.basis = 'xy'
plotxy.origin = (6.538/2, 6.538/2, 9.3)
plotxy.width = (10, 15)
plotxy.pixels = (100, 150)
plotxy.color_by = 'cell'


plots = openmc.Plots([plotxz,plotxy,plotyz,])
plots.export_to_xml()
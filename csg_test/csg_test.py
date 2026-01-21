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

XZ_Polygon = openmc.model.Polygon(basis='xz', points=XYZ_Points)
xy_region  = -XZ_Polygon & +Y_Left & -Y_Right

YZ_Polygon = openmc.model.Polygon(basis='yz', points=XYZ_Points)
yz_region  = -YZ_Polygon & +X_front & -X_back

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
plotxz.origin = (6.538/2, 6.538/2, 12.54/2)
plotxz.width = (10, 15)
plotxz.pixels = (100, 150)
plotxz.color_by = 'cell'

plotyz = openmc.Plot()
plotyz.basis = 'yz'
plotyz.origin = (6.538/2, 6.538/2, 12.54/2)
plotyz.width = (10, 15)
plotyz.pixels = (100, 150)
plotyz.color_by = 'cell'

plotxy = openmc.Plot()
plotxy.basis = 'xy'
plotxy.origin = (6.538/2, 6.538/2, 12.54/2)
plotxy.width = (10, 15)
plotxy.pixels = (100, 150)
plotxy.color_by = 'cell'


plots = openmc.Plots([plotxz,plotxy,plotyz,])
plots.export_to_xml()
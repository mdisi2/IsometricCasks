import openmc

Fuel_Basket = openmc.Material('Fuel Basket') #Stainless steel with neutron absorbers (B4C, look up typical examples)
Fuel_Basket.set_density('g/cm3', 10)


### CSG

Z_top = openmc.ZPlane(z=12.54)
Z_bottom = openmc.ZPlane(z=0)
X_back = openmc.XPlane(x=6.538)
X_front = openmc.XPlane(x=0) # at origin
Y_Left = openmc.YPlane(y=0) # at origin
Y_Right = openmc.YPlane(y=6.538)
  
# XZ Plane
# #Left half octogon big (X,Z)
Big_Left_Half_Octogon = {(0,     0 , 3.251),
               (1.51,  0 , 3.251),
               (3.019, 0 , 4.76),
               (3.019, 0 , 7.78),
               (1.51,  0 , 9.289)}
    
Big_Bottom_Half_Octogon = {(0.25, 0 , 0),
                              (0.25, 0 , 1.51),
                              (1.759, 0 , 3.019),
                              (4.779, 0, 3.019),
                              (6.288, 0 , 1.51)}
    
Big_Right_Half_Octogon = {(6.538, 0 , 3.251),
                              (5.028, 0 , 3.251),
                              (3.519, 0 , 4.76),
                              (3.519, 0 , 7.78),
                              (5.028, 0 , 9.289)}
    
Big_Bottom_Half_Octogon = {(0.25, 0 , 12.54 - 0),
                              (0.25, 0 ,  12.54 - 1.51),
                              (1.759, 0 , 12.54 - 3.019),
                              (4.779, 0, 12.54 - 3.019),
                              (6.288, 0 , 12.54 - 1.51)}
    
## Holder thing XZ (X,Y,Z)

XYZ_Holder = [(0,0),
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
                 (0,1.51),
                 (0,0)]
    
XZ_Plane = []

for i in range(len(XYZ_Holder)):
    x1, z1 = XYZ_Holder[i]
    x2, z2 = XYZ_Holder[(i + 1) % len(XYZ_Holder)]

    a =  z2 - z1
    c = -(x2 - x1)
    d = -(a*x1 + c*z1)

    line = openmc.Plane(a=a, c=c, d=d)

    XZ_Plane.append(line) 

XZ_Region = openmc.Region()

for line in XZ_Plane:
    XZ_Region &= line

XZ_Holder = XZ_Region & +Y_Left & -Y_Right
YZ_Holder = XZ_Region & X_front & - X_back

holder_cell = openmc.Cell(
    name = 'Unit Corr Cell',
    region=XZ_Holder & YZ_Holder,
    fill=Fuel_Basket)


materials.export_to_xml()
geometry.export_to_xml()
settings.export_to_xml()


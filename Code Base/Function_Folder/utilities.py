### Holds helpful functions for more readable code within sim files

import openmc 

def extrude(coords,start,plane1,plane2):
    """
    extrudes a 2D face accross a third dimension.
    
    :param coords: The 2D face points
    :cords type: list of tuples
    :param start: staring 2D plane dimensions (xy, yz, xz)
    :type start: string
    :param plane1: starting plane of third dimension
    :plane1 type: openmc plane
    :param plane2: ending plane of third dimension
    :plane2 type: openmc plane
    """
    
    if start == 'xy':
        
        XY = []
        for i in range(len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[(i + 1) % len(coords)]

            a =  y2 - y1
            c = -(x2 - x1)
            d = -(a*x1 + c*y1)

            line = openmc.Plane(a=a, c=c, d=d)

            XY.append(line) 

        XY_Region = openmc.Region()

        for line in XY:
            XY &= line

        ret = XY_Region & +plane1 & -plane2
        return ret
    
    if start == "xz":
        
        XZ = []
        for i in range(len(coords)):
            x1, z1 = coords[i]
            x2, z2 = coords[(i + 1) % len(coords)]

            a =  z2 - z1
            c = -(x2 - x1)
            d = -(a*x1 + c*z1)

            line = openmc.Plane(a=a, c=c, d=d)

            XZ.append(line) 

        XZ_Region = openmc.Region()

        for line in XZ:
            XZ &= line

        ret = XZ_Region & +plane1 & -plane2
        return ret
    
    if start == "yz":
        
        YZ = []
        for i in range(len(coords)):
            y1, z1 = coords[i]
            y2, z2 = coords[(i + 1) % len(coords)]

            a =  y2 - y1
            c = -(y2 - y1)
            d = -(a*y1 + c*z1)

            line = openmc.Plane(a=a, c=c, d=d)

            YZ.append(line) 

        YZ_Region = openmc.Region()

        for line in YZ:
            YZ &= line

        ret = YZ_Region & +plane1 & -plane2
        return ret
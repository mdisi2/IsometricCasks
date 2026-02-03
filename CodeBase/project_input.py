import openmc
from CodeBase.cask_and_mpc import MPC, MPC_Concrete, MPC_Steel, Plates,  Radial_Shield_Steel, Radial_Shield_Concrete, Overpack_Shells
from CodeBase.Function_Folder.mats import S_316_borated, Concrete, A516_70, S_316
from CodeBase.fuel_blanket_and_pebbles import basket, Triso_Pebbles
import numpy as np

#geometry = openmc.Geometry([MPC(), MPC_Concrete(), MPC_Steel(), Plates(),  Radial_Shield_Steel(), Radial_Shield_Concrete(), Overpack_Shells()])
#geometry = openmc.Geometry([basket(), Triso_Pebbles()])

## create a universe of the basket and pebbles
## create a lattice of this universe
## fill the region inisde the MPC with this lattice 

import openmc
from CodeBase.cask_and_mpc import Cask_and_MPC_universe
from CodeBase.Function_Folder.mats import S_316_borated, Concrete, A516_70, S_316, air, He, graphite, depleted_fuel
from CodeBase.fuel_blanket_and_pebbles import finite_universe
import numpy as np


basket_universe = finite_universe(en_mpc=He)
cask_mpc_universe = Cask_and_MPC_universe(ex_mpc=air, en_mpc=He)
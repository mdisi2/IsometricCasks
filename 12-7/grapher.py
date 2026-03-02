import openmc 
import matplotlib.pyplot as plt
import numpy as np

path = '12-7/statepoint.100boratedwater.h5'

sp = openmc.StatePoint(path)
t = sp.get_tally(name='neutron_spectrum')

t = sp.get_tally(name='neutron_spectrum')

flux = t.mean.flatten()

energy_filter = [f for f in t.filters if isinstance(f, openmc.EnergyFilter)][0]
bins = np.array(energy_filter.bins)

E_bins = np.concatenate(([bins[0,0]], bins[:,1]))

E_mid = 0.5 * (E_bins[:-1] + E_bins[1:])
dlnE  = np.log(E_bins[1:] / E_bins[:-1])

flux_lethargy = flux / dlnE
flux_lethargy /= np.sum(flux_lethargy * dlnE)

plt.figure(figsize=(12,7))
plt.loglog(E_mid, flux, color='black')
plt.xlabel("Energy [eV]")
plt.ylabel("Normalized Flux / lethargy")
plt.xscale('log')
plt.yscale('log')
plt.title("Neutron Spectrum | Water Submersion (HAC) | Borated Blanket")
plt.grid(True, alpha=0.5)
plt.axvline(1,linestyle='--',color='red')
plt.axvline(10e3,linestyle='--',color='red')
plt.tight_layout()
plt.savefig('flux_spectrum_HAC_B.png', dpi=600)
plt.show()
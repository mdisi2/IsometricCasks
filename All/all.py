import openmc 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Serif'

# for f in fm.findSystemFonts(fontpaths=None):
#     print(fm.FontProperties(fname=f).get_name())

plt.figure(figsize=(465/46.5,240/46.5))

path1 = 'All/statepoint.100.h5'
path2 = 'All/statepoint.100borated.h5'
path3 = 'All/statepoint.100w.h5'
path4 = 'All/statepoint.100boratedwater.h5'


path = [path1,path2,path3,path4]

Names = ["NC | Helium" , "NC | Borated Blanket" , 'HAC | Water' , "HAC | Borated Blanket"]

Color = ['#FC8403','#FC8403','blue','blue']

Style = ['-','--','-','--']

for i in range(len(Names)):
    sp = openmc.StatePoint(path[i])
    t = sp.get_tally(name='neutron_spectrum')
    flux = t.mean.flatten()

    energy_filter = [f for f in t.filters if isinstance(f, openmc.EnergyFilter)][0]
    bins = np.array(energy_filter.bins)

    E_bins = np.concatenate(([bins[0,0]], bins[:,1]))

    E_mid = 0.5 * (E_bins[:-1] + E_bins[1:])
    dlnE  = np.log(E_bins[1:] / E_bins[:-1])

    flux_lethargy = flux / dlnE
    flux_lethargy /= np.sum(flux_lethargy * dlnE)

    plt.loglog(E_mid, flux_lethargy,label=Names[i],color=Color[i],linestyle=Style[i])


plt.xlabel(r"Energy [eV]")
plt.ylabel(r"Normalized Flux / Lethargy")
plt.ylim(10**(-7))
#plt.title(r"Neutron Spectra" , fontsize=20) 
plt.grid(True, alpha=0.5)
plt.axvline(1,linestyle=':',color='black',lw=0.5)
plt.axvline(10e3,linestyle=':',color='black',lw=0.5)
plt.legend()
plt.tight_layout()
plt.savefig('flux_spectrum_combined222.png', dpi=600)
plt.show()
print('\nLoading packages...\n')
import os                  
import numpy as np
import uproot
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import trange
import pandas as pd
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

font = {'family' : 'serif', 'size' : 12 }
mpl.rc('font', **font)
mpl.rcParams['mathtext.fontset'] = 'cm'  # Set the math font to Computer Modern
mpl.rcParams['legend.fontsize'] = 1
mpl.rcParams['figure.figsize'] = (5, 4)  # Default figure size


# *********************************************************************************** #
# An example of a XS plot showcasing contribution from different interactions for NC  #
# *********************************************************************************** #

# The spline data have the energies given in GeV and the cross sections given in in 10−38cm2

# GENIE spline file
file_path = 'xsec_graphs.root'

# we are going to access the XS information for nu_mu on Oxygen
# given NC is flavor-independent, we can pull the XS info from just one of the flavors

# TGraphs within the root file are given as total (on Oxygen), and split into proton/neutron

qel_nc_p = []; qel_nc_n = []  # Quasielastic (n/p)
res_nc_p = []; res_nc_n = []  # Resonant (n/p)
coh_nc = []                   # coherent pion production
mec_nc = []                   # meson-exchange (2p2h)
tot_nc = []                   # total NC
dis_nc_p = []; dis_nc_n = []  # deep inelastic scattering
ve_nc = []                    # nu_e interaction (very tiny % --> I guess GENIE likes to keep the flavors separate. We can subtract this from the total XS)

x_vals = []                   # energy values [GeV]


# extract the data
print('Extracting XS data...\n')
with uproot.open(file_path) as root:
    
    all_keys = [name for name in root.keys()]

    # (nu_mu only - the other flavors should be the same for NC!)
    desired_folders = [
        'nu_mu_O16'
    ]
    desired_graphs = [
        'qel_nc_p', 'qel_nc_n',      # per-nucleon cross section
        'res_nc_p', 'res_nc_n',
        'coh_nc', 'mec_nc',
        'tot_nc',
        'dis_nc_p', 'dis_nc_n',
        've_nc'
    ]

    # filter the keys to find the desired graphs within the folders
    selected_graphs = {}
    for folder in desired_folders:
        selected_graphs[folder] = {}
        for graph in desired_graphs:
            graph_name = f'{folder}/{graph};1'
            if graph_name in all_keys:
                selected_graphs[folder][graph] = root[graph_name]
    
    for folder, graphs in selected_graphs.items():
        print(f'Folder: {folder}')
        for graph_name, graph_obj in graphs.items():
            print(f'  Graph: {graph_name}')
            x_values = graph_obj.values()[0]  # x values [Gev]
            y_values = graph_obj.values()[1]  # y values [XS, 10^-38 cm^2]
            #print(f'    x values: {x_values}')
            #print(f'    y values: {y_values}')
            
            # all flavors should be the same for NC
            if folder == 'nu_mu_O16':
                if graph_name == 'qel_nc_p':
                    qel_nc_p.append(y_values)
                    x_vals.append(x_values)
                elif graph_name == 'qel_nc_n':
                    qel_nc_n.append(y_values)
                
                elif graph_name == 'res_nc_p':
                    res_nc_p.append(y_values)
                elif graph_name == 'res_nc_n':
                    res_nc_n.append(y_values)
                    
                elif graph_name == 'coh_nc':
                    coh_nc.append(y_values)
                    
                elif graph_name == 'mec_nc':
                    mec_nc.append(y_values)
                    
                elif graph_name == 'tot_nc':
                    tot_nc.append(y_values)
                    
                elif graph_name == 'dis_nc_p':
                    dis_nc_p.append(y_values)
                elif graph_name == 'dis_nc_n':
                    dis_nc_n.append(y_values)
                    
                elif graph_name == 've_nc':
                    ve_nc.append(y_values)

                # grab any other information you want...


# we must combine n + p for an O16 cross section
# let's also re-structure the arrays to make it easier to plot

total_qel = []; total_res = []; total_mec = []; total_coh = []; total_dis = []
total_ve = []; total_nc = [];

GeV_vals = []

for i in range(len(x_vals[0])):

    # total O16 XS (no need to multiply by 8 as GENIE XS is calculated per 016 nucleus, not per nucleon)
    total_qel.append( qel_nc_p[0][i] + qel_nc_n[0][i] )
    total_res.append( res_nc_p[0][i] + res_nc_n[0][i] )
    total_dis.append( dis_nc_p[0][i] + dis_nc_n[0][i] )
    total_mec.append( mec_nc[0][i] )
    total_coh.append( coh_nc[0][i] )
    
    total_ve.append( ve_nc[0][i] )   # nu_e contribution
    
    total_nc.append( tot_nc[0][i] )

    # re-structure the x-data array
    GeV_vals.append(x_vals[0][i])


print('XS information loaded! Plotting...\n')

# *********************************************************************************** #
# Plotting

# JUST AN EXAMPLE: plot all XS's as a function of Energy

# subtract out nu_e contribution (just for the plot)
total_nc_minus_nue = [total_nc[i] - total_ve[i] for i in range(len(total_nc))]

fig, ax = plt.subplots(figsize=(5, 4))
plt.plot(GeV_vals, total_qel, color = 'blue', linewidth = 1, label = 'NCQE', zorder = 6)
plt.plot(GeV_vals, total_mec, color = 'purple', linewidth = 1, label = 'NC 2p2h (MEC)', zorder = 5)
plt.plot(GeV_vals, total_res, color = 'red', linewidth = 1, label = 'NC1' + r'$\pi$' + ' resonance', zorder = 3)
plt.plot(GeV_vals, total_coh, color = 'orange', linewidth = 1, label = 'NC1' + r'$\pi$' + ' coherent', zorder = 4)
plt.plot(GeV_vals, total_dis, color = 'cyan', linewidth = 1, label = 'NC DIS', zorder = 2)

plt.xlabel(r'$E_\nu$' + ' [GeV]', loc = 'right', fontsize = 16)
plt.ylabel(r'$\sigma$' + ' [' r'$10^{-38} cm^{2}$'+ ']', loc = 'top', fontsize = 16)
plt.xlim([0,3]); plt.ylim([0,6])
ax.tick_params(axis='x', which = 'both', direction= 'in', top = True,)
ax.tick_params(axis='y', which = 'both', direction= 'in', right = True)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_minor_locator(MultipleLocator(0.2))
plt.legend(fontsize = 11, frameon = False)
ax.text(0.45, 1.02, 'GENIE v3.0.6 G18_10a_02_11a', color='black', fontsize=9, weight = 'bold', transform=ax.transAxes) 
plt.tight_layout()
plt.savefig('neutrino NC XS vs E _ GENIE v3.0.6 G18_10a_02_11a.png',
            dpi=300,bbox_inches='tight',pad_inches=.3,facecolor = 'w')

plt.show()


# *********************************************************************************** #

print('\ndone\n')

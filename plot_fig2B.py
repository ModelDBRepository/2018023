"""plot_fig2B.py
Reads data written from sensitivity_depol_iclamp.py and creates a
figure like Figure 2B in the paper"""

# This script was modified from a matplotlib example of plotting with
# a colormap

import numpy as np
import matplotlib.pyplot as plt
plt.ion() # interactive display on
import glob

# 1. Generate some 2D scalar data (e.g., a sample gradient)
# A false color image is an image that depicts an object in colors that differ from those a photograph would show.
# data = np.random.rand(10, 10) # 10x10 array of random values

folders="20260123vShift_0_LVA_0p6IClamp_amp_index"
template=folders+"*/ca_suppr/delta_ca_total_mean.txt"
files=glob.glob(template)
locations=np.loadtxt(folders+"0/ca_suppr/v.txt") # v.txt contains dendritic locs
v_per_index=[v for v in range(-70,-58, 2)]

data=np.zeros((len(v_per_index), len(locations)))

for file in files:
    index=int(file.split('index')[1].split('/')[0]) # finds the amp_index
    data[index,:]=np.loadtxt(file)

# Alternatively, a sample gradient:
# x = np.linspace(0, 10, 100)
# y = np.linspace(0, 10, 100)
# X, Y = np.meshgrid(x, y)
# data = np.sin(X) * np.cos(Y)

# 2. Display the data as a false color image
plt.figure(figsize=(7, 5))
# Use 'viridis' colormap as an example. Matplotlib has many other options.
# The input is 2D scalar data, which will be rendered as a pseudocolor image.
plt.imshow(data, cmap='YlOrRd', interpolation='nearest') # 'nearest' avoids int

# 3. Add a colorbar to show the value-color mapping

plt.colorbar(label='$\Delta{Ca}^{2+}(\%\ Baseline)$')
# 4. Add titles and labels
plt.title('Figure 2B')
plt.xlabel('Apical Location ($\mu$m)')
plt.ylabel('Vm (mV)')

ax=plt.gca()

loc_indicies=[3, 7, 11]
ax.set_xticks(loc_indicies, [int(locations[i]) for i in loc_indicies])

v_index=[1, 3, 5]
ax.set_yticks(v_index, [int(v_per_index[i]) for i in v_index])

ax.invert_yaxis()

# 5. Show the plot
plt.show()

#######
if 0: # can reveal higher resolution of intermediate values if desired
    import matplotlib.colors as mcolors
    colors=['white', 'yellow', 'red', 'darkred']
    nodes=[0, .5, 0.75, 1 ]
    custom_cmap=mcolors.LinearSegmentedColormap.from_list("YellowDarkred", list(zip(nodes,colors)))
    plt.imshow(data, cmap=custom_cmap, interpolation='nearest') # 'nearest' avoids i
    ax.invert_yaxis()

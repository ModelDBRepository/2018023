"""calc_ca_suppr.py stores the data (delta Ca2+) and
some images (delta Ca2+) from running tonic_GABAAR_distal.py"""

import sys # sys is likely no longer used
from pathlib import Path
from tonic_GABAAR_gbar import tonic_GABAAR_gbar

# form the folder name

from base_dir_name import base_dir_name
folder_name = base_dir_name  # name used to have pS/um2 for pas and
# gbar_exGABALeak (tonic GABAAR (tGAR)) supplied however now a date
folder_name += f"ca_suppr/"

# create the folder
Path(folder_name).mkdir(parents=True, exist_ok=True)

# run the tonic_GABAAR_distal.py script

from solo_ap import *
from tonic_GABAAR_distal import *
print("len(ica_hva_session_record)=",len(ica_hva_session_record))
# create the integrated charge figure and data
v, delta_ca_hva_mean, delta_ca_hva_std, delta_ca_lva_mean, delta_ca_lva_std, \
    hva_ca_num_denom, lva_ca_num_denom, \
    delta_ca_total_mean, delta_ca_total_std = \
    integrated_charge(send=True,
                      record_keys=['blocked',
                                   'control'])

save_suppression(folder_name, v, delta_ca_hva_mean, delta_ca_hva_std,
                 delta_ca_lva_mean, delta_ca_lva_std,
                 hva_ca_num_denom, lva_ca_num_denom,
                 delta_ca_total_mean, delta_ca_total_std)

# last figure created was delta ca
plt.savefig(folder_name+f'ca_suppr') # writes a png by default
plt.savefig(folder_name+f'ca_suppr.pdf') # also save pdf


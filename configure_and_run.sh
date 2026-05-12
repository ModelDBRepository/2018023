nrnivmodl mod_files
# recreate pkl's in case mech's changed
rm -r -f data/*.pkl
python3 configure_sim.py
python3 figs_incl_suppl.py
python3 calc_ca_suppr.py
python3 plot_states_times.py

******************************************************************************************
*README by DR 2012. Illustrates usage of simulations in this folder on glutamatecad2kca
******************************************************************************************


This folder should contain all the .dat files created by the simulations. It should be 
possible to run them simply by clicking on the .hoc file. If they don't work it might be 
because of a .dat file not w+ opening. If that happens check values of strings tragetDir, 
simRef and simDir. These strings should all be empty. If not, delete what is in them.

All simulations replicate the stimulation done by the glutamate200 point process in the 
original Larkum et al. 2009 model, but under different conditions. The point process 
glutamatecad2kca is a combination of the cad2 calcium shell, the kca channel mechanism
using Larkum's original settings, and the glutamate synapse point process. Ca influx 
through a single instant of glutamatecad2kca was fitted to exactly match the Ca entry 
produced by 20 synapses into apic[63] in the original model. This is evident by comparing 
Ca_cad2kca_4pulse.dat to Ca_glutnoinact_4pulse.dat. All .dat files should be plotted 
against time.dat in this folder. The .dat files show variable recorded and the location of
the recording. KCa_gk_noKCa_SCa_2pulse.dat shows the potassium conductance through 
glutamatecad2kca during 2 pulses of stimulation, the second one triggering an NMDA spike.

The names of the hocfiles indicate what they do:


*Original means the original model, with Ca pooling and all channels.

*glutnoinact means that glutnoinact is used for stimulation, i.e. no Ca inactivation of
 gNMDA.
 
*kca_point means kca_point is being used instead of KCa. This is an intermediate for the
 development of glutamatecad2kca.

*glutnoinact_4pulse means that glutnoinact was used, but without SCa and KCa. 
 glutnoinact is the only source of Ca entry in the stimulated compartment.
 
*cad2kca means glutamatecad2kca was used in this simulation, but without SCa and no KCa.
 cad2kca is the only source of Ca entry in the stimulated compartment.

*2pulse or 4 pulse indicates number of pulses, if different from the standard 3.

*noKCa_noSCa or KCa_SCa or any combination of those means that glutamatecad2kca was used,
 and that KCa or SCa conductance was switched ON or OFF.
 
 
 
 
 
 
 


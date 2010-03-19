************************************************************************
*Documentation for modified VS granule cell with F-I, I-V and f-F plots*
************************************************************************

This folder contains a modified version of the Saviane&Steuber model of a cerebellar granule cell,
which was modified by Paidreg Gleeson and Dan Ruedt.

The model has an added tonic conductance with a reversal potential of -75 mV and a conductance of 438pS.

There are 3 python scripts in the folder, which create F-I, I-V and f-F plots respectively.

A list of all conductances present can be found in the neuroConstruct project.

The sim config "Test Tonic" has 438 pS of tonic inhibitory conductance (implemented as a leak current).
The sim config "Cells pulse 500ms" has the same conductances but misses the tonic inhibitory current.

***********
*F-I plots*
***********

To create an F-I plot using this model, run neuroConstruct with the -python argument to get to the
jython command line. From there type execfile("F_I_plot.py"), which runs the simulations and opens a 
neuroConstruct. Plotted is input current (Current Clamp) on the X-axis versus output firing rate on the Y-axis.

The script itself comprises two files, F_I_plot.py and GenerateF_ICurve.py, the latter containing the actual code.
This code is just an adaptation of the F_I_script from Paidreg Gleeson which is available in 
\neuroConstruct\pythonNeuroML\Examples. 

The file F_I_plot.py contains all the main parameters for the F-I plot. These are the range of current injected
(stimAmpLow and stimAmpHigh, respectively, in nA) the increment per iteration (i.e. the number of data points in
the range), as well as the delay and duration of the current step (to reach a steady state).

The file also allows for the time window for data analysis to be changed, which is not really necessary. The start 
time should always be a few 100 ms after the onset of the current step, to ensure the cell is firing at a steady
rate.

***********
*I-V plots*
***********

The I-V plot plots the current that is flowing when the granule cell is clamped to a given potential relative to
the surroundings. This plot visualizes the voltage dependences of membrane conductances, as well as of the input
resistance (slope of the curve). To run, start neuroConstruct with the -python argument to reach the jython command 
line. Type execfile("V_I_plot.py") to run the script from the jython shell. 

The script itself is in GenerateV_ICurve.py and V_I_plot.py allows the setting of all the main parameters. These
are stimAmpLow and stimAmpHigh, which specify the voltage range, in addition to stimAmpInc, which sets the increment
step and thus the number of data points. This script utelizes the normal voltage clamp function in neuron and 
current through the voltage clamp is measured at one point in time in the middle of the simulation (so everything 
is in a steady state). 

NOTE: This script has changed. It now produces a series of TXT files in the simulations folder which represent a
current trace each at the indicated holding potential. There are three distinct holding potentials, one pre and one
post the indicated holding potential. Pre and post holding potentials last 150ms each. Please check 
GenerateV_ICurve.py for the amplitudes of pre and post holding potentials. The trace is recorded from the very start
to the very end of the simulation. Only the indicated holding potential is varied across simulations. Dt is 0.01 ms 
and all values are in nano Amps. Please use Igor to view data. The plot generated in neuroConstruct now simply shows
a series of zeros and has nothing to do with the actual traces.

***********
*f-F plots*
***********

The f-F plot plots the output firing rate of the granule cell in response to an input train that reflects 
stimulation of a single mossy fibre at a given input frequency (X-axis). The current is injected by playing
a time varying conductance into the cell that reflects activation of AMPA receptors exclusively. All trains
at the input frequencies used were obtained from actual recordings in voltage clamp mode, and the AMPA conductnance
calculated from the measured current flow. NMDA receptors were blocked for the recordings and all input trains were 
obtained under two conditions: with and without 5 nS of tonic inhibitory conductance (E = -75mV). 

To execute, start neuronConstruct in jython mode using "nc -python" in the neuroConstruct folder. Run via
"execfile("f-F_plot.py")". The actual script is located in "Generate_fF_Curve". You can set the main 
parameters for the script in f-F_plot.py: The simulation configuration (i.e. with or without tonic inhibition),
the number of conductance trains available for playing into the model (currently 8) and the duration of the
simulation, which should be longer than the longest available train. 

The number of trains should be set to the number of data files read in by the script into the hoc files created.
They are stored in the /gTrains_nS/ subfolder. The values are conductances in nS and the time step is 0.03 ms per
value. The files have the form gAMPA_*.txt, where * is a placeholder for the number of the train (counting starts
at 1). The file with index 0 is just for testing purposes. If you have more files to read in, increase nTrains in
f-F_plot.py. 

Importantly, the folder also contains the file gAMPA_traininfo.txt. This file contains information on the 
stimulation frequencies used to generate the conductance trains, where the first value is assigned to train number 
1 and so on. These frequencies are used for the x-coordinates of the data points in the plot (the y-coordinates
being measured by the script). If you add more trains or change the trains, you need to modify the values in this
file as well, otherwise the data won't make any sense.







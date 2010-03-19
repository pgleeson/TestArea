#
#
#   A file which generates an input frequency vs output frequency curve for various cells
#
#   Author: Dan Ruedt
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

from sys import *

from java.io import File
from Generate_fF_Curve import fFplot

from math import *

simConfig="TestTonic" 



nTrains = 8    # enter how many trains you have as files


simDuration = 3000   #set this to a reasonable value higher than duration of your longest train


analyseStartTime = 0
analyseStopTime = simDuration
analyseThreshold = -20 # mV

# Change this number to the number of processors you wish to use on your local machine
maxNumSimultaneousSims = 4



# Load neuroConstruct project

projFile = File("VSCSGranCell.neuro.XML")

gen = fFplot()

gen.make_fF_Curve(projFile,
                 "NEURON",
                 simConfig,
                 nTrains,
                 simDuration,
                 analyseStartTime, analyseStopTime,
                 analyseThreshold,
                 maxNumSimultaneousSims)




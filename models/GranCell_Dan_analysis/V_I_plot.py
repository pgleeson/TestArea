#
#
#   Trying to create V-I plot
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
from GenerateV_ICurve import VoltageVsCurrentGenerator

from math import *

simConfig="TestTonic" 


stimAmpLow = -100.0
stimAmpInc = 5.0
stimAmpHigh = -40.0


stimDur = 300

simDuration = stimDur + 300# ms


# Change this number to the number of processors you wish to use on your local machine
maxNumSimultaneousSims = 4



# Load neuroConstruct project

projFile = File("GranCell_Dan_analysis.ncx")

gen = VoltageVsCurrentGenerator()

gen.generateV_ICurve(projFile,
                 "NEURON",
                 simConfig,
                 stimAmpLow, stimAmpInc, stimAmpHigh,
                 stimDur,
                 simDuration,
                 maxNumSimultaneousSims)



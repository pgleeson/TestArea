#
#
#   A file which generates a frequency vs current curve for various cells
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

from sys import *

from java.io import File
from GenerateF_ICurve import FreqVsCurrentGenerator

from math import *

simConfig="TestTonic" 


preStimAmp = -0.05
preStimDel = 0
preStimDur = 200

stimAmpLow = 0.0
stimAmpInc = 0.002
stimAmpHigh = 0.1

stimDel = preStimDur
stimDur = 1000

simDuration = preStimDur + stimDur # ms

analyseStartTime = stimDel + 300 # So it's firing at a steady rate...
analyseStopTime = simDuration
analyseThreshold = -20 # mV

# Change this number to the number of processors you wish to use on your local machine
maxNumSimultaneousSims = 4



# Load neuroConstruct project

projFile = File("VSCSGranCell.neuro.XML")

gen = FreqVsCurrentGenerator()

gen.generateF_ICurve(projFile,
                 "NEURON",
                 simConfig,
                 preStimAmp, preStimDel, preStimDur,
                 stimAmpLow, stimAmpInc, stimAmpHigh,
                 stimDel, stimDur,
                 simDuration,
                 analyseStartTime, analyseStopTime,
                 analyseThreshold,
                 maxNumSimultaneousSims)




#
#
#   A file which generates a frequency vs current curve for the Granule cell
#   
#   To execute this file, type '..\..\..\nC.bat -python XXX.py' (Windows)
#   or '../../../nC.sh -python XXX.py' (Linux/Mac)
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

import sys
import os

from java.io import File

from math import *

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc

simConfig="CellsPulse500ms"


preStimDel = 0
preStimDur = 200

stimAmpLow =  0.000
stimAmpInc =  0.001
stimAmpHigh = 0.03

stimDel = preStimDur
stimDur = 1500

simDuration = preStimDur + stimDur # ms

analyseStartTime = stimDel + 100 # So it's firing at a steady rate...
analyseStopTime = simDuration
analyseThreshold = -20 # mV

# Change this number to the number of processors you wish to use on your local machine
numConcurrentSims = 4



# Load neuroConstruct project

projFile = File("../VSCSGranCell.neuro.xml")


simManager = nc.SimulationManager(projFile,
                                  numConcurrentSims)

simManager.generateFICurve("NEURON",
                           simConfig,
                           stimAmpLow,
                           stimAmpInc,
                           stimAmpHigh,
                           stimDel,
                           stimDur,
                           simDuration,
                           analyseStartTime,
                           analyseStopTime,
                           analyseThreshold)

             

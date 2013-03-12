#
#
#   File to test current configuration of CA1Pyramidal cell project. 
#
#   To execute this type of file, type '..\..\..\nC.bat -python XXX.py' (Windows)
#   or '../../../nC.sh -python XXX.py' (Linux/Mac). Note: you may have to update the
#   NC_HOME and NC_MAX_MEMORY variables in nC.bat/nC.sh
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

try:
    from java.io import File
except ImportError:
    print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc # Many useful functions such as SimManager.runMultipleSims found here

projFile = File(os.getcwd(), "../LarkumEtAl2009.ncx")

##############  Main settings  ##################

simConfigs = []

simConfigs.append("test_IClamp")
#simConfigs.append("CA1Cell")

simDt =                 0.025

simulators =            ["NEURON"]

numConcurrentSims =     1

varTimestepNeuron =     False

plotSims =              True
plotVoltageOnly =       True
runInBackground =       True
analyseSims =           True

verbose = True

#############################################


def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      numConcurrentSims = numConcurrentSims,
                                      verbose = verbose)

    simManager.runMultipleSims(simConfigs =           simConfigs,
                               simDt =                simDt,
                               simulators =           simulators,
                               runInBackground =      runInBackground,
                               varTimestepNeuron =    varTimestepNeuron)

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)

    # Times from ModelDB version at dt 0.025...
    spikeTimesToCheck = {'pyr_group_0': [61.6, 71.05, 84.675, 133.475, 143.975, 190.625, 200.825, 251.75, 262.35, 310.975, 321.675, 369.125, 379.9, 426.275, 437.125]}

    spikeTimeAccuracy = 0.1

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy)

    print report

    # Times recorded from nC mod based impl
    times = [61.625, 71.075, 84.7, 133.5, 144.0, 190.65, 200.85, 251.775, 262.4, 311.0, 321.7, 369.15, 379.925, 426.3, 437.15]
    spikeTimesToCheck = {'pyr_group_0': times,
                         'pyrCML_group_0': times}

    spikeTimeAccuracy = 0.1

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy)

    print report
    

    return report


if __name__ == "__main__":
    testAll()
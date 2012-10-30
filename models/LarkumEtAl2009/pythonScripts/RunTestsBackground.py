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

simConfigs.append("background activity")

simDt =                 0.025
neuroConstructSeed =    12443                                   ##
simulatorSeed =         234434                                   ##

simulators =            ["NEURON"]

numConcurrentSims =     1

varTimestepNeuron =     False

plotSims =              True
plotVoltageOnly =       True
runInBackground =       False
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
                               varTimestepNeuron =    varTimestepNeuron,
                               neuroConstructSeed =   neuroConstructSeed,
                               simulatorSeed =        simulatorSeed)

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)


    # Times recorded from nC mod based impl
    times = [21.95, 213.025, 310.225, 645.4, 733.4, 891.425, 989.7]
    spikeTimesToCheck = {'pyr_group_0': times}

    spikeTimeAccuracy = 0.1

    report = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
                                  spikeTimeAccuracy = spikeTimeAccuracy,
                                  threshold = -61)

    print report
    

    return report


if __name__ == "__main__":
    testAll()
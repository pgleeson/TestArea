#
#
#   File to generate network for execution on parallel NEURON
#   Note this script has only been tested with UCL's cluster!
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

from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings

import ncutils as nc # Many useful functions such as SimManager.runMultipleSims found here

projFile = File("../Parallel.ncx")

simConfig="SmallNetwork"

###########  Main settings  ###########
simDuration =           500 # ms
simDt =                 0.025 # ms
neuroConstructSeed =    1234
simulatorSeed =         1111
simulators =            ["NEURON"]
simConfigs = []
simConfigs.append("Default Simulation Configuration")

mpiConfig =               MpiSettings.LEGION_4PROC
mpiConfig =               MpiSettings.MATLEM_8PROC
mpiConfig =               MpiSettings.LOCAL_SERIAL

suggestedRemoteRunTime = 2   # mins

varTimestepNeuron =     False

analyseSims =           True
plotSims =              True
plotVoltageOnly =       True

simAllPrefix =          "Py_"   # Adds a prefix to simulation reference

runInBackground =       mpiConfig == MpiSettings.LOCAL_SERIAL

verbose =               True

#######################################

def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      verbose = verbose)

    simManager.runMultipleSims(simConfigs =           simConfigs,
                               simDt =                simDt,
                               simulators =           simulators,
                               runInBackground =      runInBackground,
                               varTimestepNeuron =    varTimestepNeuron,
                               mpiConfig =                mpiConfig,
                               suggestedRemoteRunTime =   suggestedRemoteRunTime)


if __name__ == "__main__":
    testAll()
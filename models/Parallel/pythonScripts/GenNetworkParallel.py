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
from ucl.physiol.neuroconstruct.simulation import SimulationData

import ncutils as nc # Many useful functions such as SimManager.runMultipleSims found here

projFile = File("../Parallel.ncx")

simConfig="SmallNetwork"

###########  Main settings  ###########
simDuration =           200 # ms
simDt =                 0.025 # ms
neuroConstructSeed =    1234
simulatorSeed =         1111
simulators =            ["NEURON"]
simConfigs = []
simConfigs.append("Default Simulation Configuration")


mpiConfigs =              [MpiSettings.MATLEM_1PROC, MpiSettings.MATLEM_2PROC, MpiSettings.MATLEM_4PROC, MpiSettings.MATLEM_8PROC, MpiSettings.MATLEM_16PROC] #, MpiSettings.MATLEM_4PROC, MpiSettings.MATLEM_8PROC, MpiSettings.MATLEM_16PROC
#mpiConfigs =              [MpiSettings.LOCAL_SERIAL]

suggestedRemoteRunTime = 2   # mins

varTimestepNeuron =     False

analyseSims =           True
plotSims =              True
plotVoltageOnly =       True

simAllPrefix =          "Py_"   # Adds a prefix to simulation reference

runInBackground =       mpiConfigs == [MpiSettings.LOCAL_SERIAL]

verbose =               True
runSims =               False

#######################################

def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      verbose = verbose)

    allSims = simManager.runMultipleSims(simConfigs =             simConfigs,
                               simDt =                   simDt,
                               simDuration =             simDuration,
                               simulators =              simulators,
                               runInBackground =         runInBackground,
                               varTimestepNeuron =       varTimestepNeuron,
                               mpiConfigs =              mpiConfigs,
                               suggestedRemoteRunTime =  suggestedRemoteRunTime,
                               simRefGlobalPrefix =      simAllPrefix,
                               runSims =                 runSims)

    for sim in allSims:
        simDir = File(projFile.getParentFile(), "/simulations/"+sim)

        try:
            simData = SimulationData(simDir)
            simData.initialise()
            simTime = simData.getSimulationProperties().getProperty("RealSimulationTime")
            print "Simulation: %s took %s seconds"%(sim, simTime)

        except:
            self.printver("Error analysing simulation data from: %s"%simDir.getCanonicalPath())

if __name__ == "__main__":
    testAll()
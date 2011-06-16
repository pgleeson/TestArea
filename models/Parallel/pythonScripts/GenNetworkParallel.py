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

from sys import *
from time import *

from java.io import File

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo


projFile = File("../Parallel.neuro.xml")

simConfig="SmallNetwork"

###########  Main settings  ###########
simDuration =           500 # ms
simDt =                 0.025 # ms
neuroConstructSeed =    1234
simulatorSeed =         1111
simRefPrefix =          "SB_"
defaultSynapticDelay =  1
mpiConf =               MpiSettings.LEGION_4PROC
mpiConf =               MpiSettings.MATLEM_8PROC
#######################################


# Load neuroConstruct project

print "Loading project from "+ projFile.getCanonicalPath()


pm = ProjectManager()
myProject = pm.loadProject(projFile)

myProject.simulationParameters.setDt(simDt)
index = 0

while File( "%s/simulations/%s%i"%(myProject.getProjectMainDirectory().getCanonicalPath(), simRefPrefix,index)).exists():
    index = index+1

simRef = "%s%i"%(simRefPrefix,index)
myProject.simulationParameters.setReference(simRef)

# Use this so defaultSynapticDelay will be recorded in simulation.props and listed in SimulationBrowser GUI
SimulationsInfo.addExtraSimProperty("defaultSynapticDelay", str(defaultSynapticDelay))

simConfig = myProject.simConfigInfo.getSimConfig(simConfig)

simConfig.setSimDuration(simDuration)


mpiSettings = MpiSettings()
simConfig.setMpiConf(mpiSettings.getMpiConfiguration(mpiConf))

print "Parallel configuration: "+ str(simConfig.getMpiConf())

for netConnName in simConfig.getNetConns():
    if netConnName.count("gap")==0:
        print "Changing synaptic delay in %s to %i"%(netConnName, defaultSynapticDelay)
        delayGen = NumberGenerator(defaultSynapticDelay)
        for synProps in myProject.morphNetworkConnectionsInfo.getSynapseList(netConnName):
            synProps.setDelayGenerator(delayGen)


pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(1)

numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

print "Number of cells generated: " + str(numGenerated)

myProject.neuronFileManager.generateTheNeuronFiles(simConfig,
                                                    None,
                                                    NeuronFileManager.RUN_HOC,
                                                    simulatorSeed)

print "Generated NEURON files for: "+simRef

compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())

compileSuccess = compileProcess.compileFileWithNeuron(0,0)

print "Compiled NEURON files for: "+simRef

if compileSuccess:
    pm.doRunNeuron(simConfig)
    print "Set running simulation: "+simRef


exit()

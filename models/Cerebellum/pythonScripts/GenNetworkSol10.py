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
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from ucl.physiol.neuroconstruct.simulation import SimulationsInfo
from ucl.physiol.neuroconstruct.neuron import NeuronSettings

path.append(environ["NC_HOME"]+"/pythonNeuroML/nCUtils")
import ncutils as nc

projFile = File("../Cerebellum.ncx")


###########  Main settings  ###########

simConfig=              "SolinasEtAl2010Net"
simDuration =           500 # ms
simDt =                 0.025 # ms
neuroConstructSeed =    12345
simulatorSeed =         12345

simulators =             ["NEURON"]

simRefPrefix =          "Sol10_"

defaultSynapticDelay =  1

#mpiConf =               MpiSettings.CLUSTER_4PROC
#mpiConf =               MpiSettings.LEGION_8PROC
#mpiConf =               MpiSettings.LEGION_16PROC
#mpiConf =               MpiSettings.LOCAL_SERIAL
#mpiConf =               MpiSettings.LEGION_1PROC
#mpiConf =               MpiSettings.LEGION_16PROC
mpiConf =               MpiSettings.MATLEM_8PROC
#mpiConf =               MpiSettings.LEGION_256PROC
#mpiConf =               'Matthau_6_8PROCS'
#mpiConf =               'Matthau_Lemmon_Test_56'
#mpiConf =                'Matthau_Lemmon_Test_ALL'


saveDataAsHdf5 =        False


varTimestepNeuron =     False
verbose =               True
runInBackground=        False

suggestedRemoteRunTime = 120


#######################################


### Load neuroConstruct project

print "Loading project from "+ projFile.getCanonicalPath()

pm = ProjectManager()
project = pm.loadProject(projFile)


### Set duration & timestep & simulation configuration

project.simulationParameters.setDt(simDt)
simConfig = project.simConfigInfo.getSimConfig(simConfig)
simConfig.setSimDuration(simDuration)

if saveDataAsHdf5:
    project.neuronSettings.setDataSaveFormat(NeuronSettings.DataSaveFormat.HDF5_NC)


### Set simulation reference

index = 0
simRef = "%s%i"%(simRefPrefix,index)


while File( "%s/simulations/%s_N"%(project.getProjectMainDirectory().getCanonicalPath(), simRef)).exists():
    simRef = "%s%i"%(simRefPrefix,index)
    index = index+1

project.simulationParameters.setReference(simRef)


### Change parallel configuration

mpiSettings = MpiSettings()
simConfig.setMpiConf(mpiSettings.getMpiConfiguration(mpiConf))
print "Parallel configuration: "+ str(simConfig.getMpiConf())

if suggestedRemoteRunTime > 0:
    project.neuronFileManager.setSuggestedRemoteRunTime(suggestedRemoteRunTime)
    project.genesisFileManager.setSuggestedRemoteRunTime(suggestedRemoteRunTime)


### Change synaptic delay associated with each net conn

for netConnName in simConfig.getNetConns():
    if netConnName.count("gap")==0:
        print "Changing synaptic delay in %s to %f"%(netConnName, defaultSynapticDelay)
        delayGen = NumberGenerator(defaultSynapticDelay)
        for synProps in project.morphNetworkConnectionsInfo.getSynapseList(netConnName):
            synProps.setDelayGenerator(delayGen)

# defaultSynapticDelay will be recorded in simulation.props and listed in SimulationBrowser GUI
SimulationsInfo.addExtraSimProperty("defaultSynapticDelay", str(defaultSynapticDelay))


### Generate network structure in neuroConstruct

pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(2)


print "Number of cells generated: " + str(project.generatedCellPositions.getNumberInAllCellGroups())
print "Number of network connections generated: " + str(project.generatedNetworkConnections.getNumAllSynConns())


myNetworkMLFile = File("../generatedNeuroML/Network_"+simRef+".nml")

pm.saveNetworkStructureXML(project, myNetworkMLFile, 0, 0, simConfig.getName(), "Physiological Units")

print "Network structure saved to file: "+ myNetworkMLFile.getCanonicalPath()

#exit()

if simulators.count("NEURON")>0:
    
    simRefN = simRef+"_N"
    project.simulationParameters.setReference(simRefN)

    nc.generateAndRunNeuron(project,
                            pm,
                            simConfig,
                            simRefN,
                            simulatorSeed,
                            verbose=verbose,
                            runInBackground=runInBackground,
                            varTimestep=varTimestepNeuron)
        
    sleep(2) # wait a while before running GENESIS...
    
if simulators.count("GENESIS")>0:
    
    simRefG = simRef+"_G"
    project.simulationParameters.setReference(simRefG)

    nc.generateAndRunGenesis(project,
                            pm,
                            simConfig,
                            simRefG,
                            simulatorSeed,
                            verbose=verbose,
                            runInBackground=runInBackground)
                            
    sleep(2) # wait a while before running MOOSE...


if simulators.count("MOOSE")>0:

    simRefM = simRef+"_M"
    project.simulationParameters.setReference(simRefM)

    nc.generateAndRunMoose(project,
                            pm,
                            simConfig,
                            simRefM,
                            simulatorSeed,
                            verbose=verbose,
                            runInBackground=runInBackground)
                            
    sleep(2) # wait a while before running GENESIS...


print "Finished running all sims, shutting down..."
sleep(5)
exit()

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
from java.util import Vector

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
from ucl.physiol.neuroconstruct.cell.utils import CellTopologyHelper
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager
from ucl.physiol.neuroconstruct.cell import *


projFile = File("../IonTest.ncx")

simConfig="Default Simulation Configuration"

###########  Main settings  ###########
simDuration =          100 # ms
simDt =                0.005 # ms
neuroConstructSeed =   1234
simulatorSeed =        1111
simRef =               "TestSim1"
#######################################


# Load neuroConstruct project

print "Loading project from "+ projFile.getCanonicalPath()


pm = ProjectManager()
myProject = pm.loadProject(projFile)

myProject.simulationParameters.setDt(simDt)
myProject.simulationParameters.setReference(simRef)


cell = myProject.cellManager.getCell("SampleCell")

spVg = cell.getSpeciesVsGroups()

sp1 = Species("k")
sp1.setProperty("e", "-77.7")
grps1 =  Vector()
grps1.add(Section.ALL)
spVg.put(sp1, grps1)

sp2 = Species("na")
sp2.setProperty("e", "55.5")
grps2 =  Vector()
grps2.add(Section.ALL)
spVg.put(sp2, grps2)

print "Spec vs groups: " + str(spVg)

print CellTopologyHelper.printDetails(cell, myProject)

simConfig = myProject.simConfigInfo.getSimConfig(simConfig)

myProject.markProjectAsEdited()
print "Saving project..."
myProject.saveProject()
print "Project saved"

exit()
simConfig.setSimDuration(simDuration)

pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
        print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
        sleep(1)

numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

print "Number of cells generated: " + str(numGenerated)

print "Parallel configuration: "+ str(simConfig.getMpiConf())

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



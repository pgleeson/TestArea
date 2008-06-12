import os
import time

from java.io import *

from ucl.physiol.neuroconstruct.cell.utils import *
from ucl.physiol.neuroconstruct.project import *
from ucl.physiol.neuroconstruct.neuron import *
from ucl.physiol.neuroconstruct.simulation import *
from ucl.physiol.neuroconstruct.gui.plotter import *
from ucl.physiol.neuroconstruct.dataset import *
from ucl.physiol.neuroconstruct.nmodleditor.processes import *


neuroConstructSeed = 1234
simulatorSeed = 4321

projName = 'Ex7-GranuleCell.neuro.xml'
projDir = 'examples/Ex7-GranuleCell/'

file = File(projDir+projName)

print 'Loading project file: ', file

myProject = Project.loadProject(file,  Project.getDummyProjectEventListener())


pm = ProjectManager(None, None)

pm.setCurrentProject(myProject)

print "Loaded project: " + myProject.getProjectName() 

simConfig = myProject.simConfigInfo.getSimConfig("OnlyVoltage")


pm.doGenerate(simConfig.getName(), neuroConstructSeed)

while pm.isGenerating():
    print "Waiting for the project to be generated..."
    time.sleep(2)
    
numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

print "Number of cells generated: " + str(numGenerated)

#allSimulations = {'PySim_8':0.01, 'PySim_9':0.011}
allSimulations = {}

if numGenerated > 0:

    print "Generating NEURON scripts..."
    
    myProject.neuronSettings.setCopySimFiles(1)
    
    for i in range(0, 20):
    
        simRef = "PySim_"+str(i)
        
        allSimulations[simRef] = i
        
        stim = myProject.elecInputInfo.getStim(0)
        
        print "First stim: "+ str(stim)
        
        stim.setAmplitude(i/1000.0)
        
        myProject.elecInputInfo.updateStim(stim)
    
        myProject.simulationParameters.setReference(simRef)
        
        myProject.neuronFileManager.setQuitAfterRun(1)
    
        myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, neuroConstructSeed)
    
        compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())
    
        compileSuccess = compileProcess.compileFileWithNeuron(0)
    
        if compileSuccess:
            pm.doRunNeuron(simConfig)
            time.sleep(4)
      

frame = PlotManager.getPlotterFrame("All voltage traces")
frame2 = PlotManager.getPlotterFrame("Frequency versus stimulus curve")
fiCurve = DataSet("F/I curve", "F/I curve", "", "", "", "")

for sim in allSimulations.keys():


    simDir = File(projDir+"simulations/"+sim)

    print "Reloading simulation: "+ sim +" from directory: "+ simDir.getAbsolutePath()

    simData = SimulationData(simDir)
    simData.initialise()
    
    dataSet = simData.getDataSet("Gran_0", "VOLTAGE", 0)
    
    print "Got data: "+ dataSet.toString()
    
    frame.addDataSet(dataSet)
    
    threshold = -20
    
    stim = myProject.elecInputInfo.getStim(0)
    start = stim.getDelay().getStart()
    stop = stim.getDuration().getStart() + start
    
    spikeTimes = SpikeAnalyser.getSpikeTimes(dataSet.getYValues(),
                                             dataSet.getXValues(),
                                             threshold,
                                             start,
                                             stop)
                                             
                                                 
    
    print "Number of spikes: "+ str(len(spikeTimes))
    fiCurve.addPoint(allSimulations[sim], len(spikeTimes)/stim.getDuration().getStart())
    
    
frame2.addDataSet(fiCurve)
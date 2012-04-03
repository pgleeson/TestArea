#
#   A file that opens the neuroConstruct project LarkumEtAl2009 run the cell model LarkumPyr (used by the teststim.py script)
#
#   Author: Matteo Farinella

from sys import *
from java.io import File
from java.lang import System
from java.util import ArrayList 
from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.gui import SimulationRerunFrame
from ucl.physiol.neuroconstruct.gui.plotter import PlotManager
from ucl.physiol.neuroconstruct.gui.plotter import PlotCanvas
from ucl.physiol.neuroconstruct.dataset import DataSet
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser
from math import *
import random
import time
import shutil
import os
import subprocess

print "============================"
print "run neuroConstruct model"
print "============================"

projName = "LarkumEtAl2009"
projFile = File("/home/matteo/neuroConstruct/models/"+projName+"/"+projName+".ncx")

print "Loading project from file: " + projFile.getAbsolutePath()+", exists: "+ str(projFile.exists())
pm = ProjectManager()
myProject = pm.loadProject(projFile)
myProject.neuronSettings.setNoConsole() # Calling this means no console/terminal is opened when each simula
simConfig = myProject.simConfigInfo.getSimConfig("test_IClamp")# configuration aimed to reproduce the IClamp from modelDB
randomseed = random.randint(1000,5000)
pm.doGenerate(simConfig.getName(),  randomseed)
while pm.isGenerating():
    print "Waiting for the project to be generated..."
    time.sleep(2)    

numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()
simRef = "testsim"
myProject.simulationParameters.setReference(simRef)
          
myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
print "Generated NEURON files for: "+simRef	
compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
print "Compiled NEURON files for: "+simRef

if compileSuccess:
   pm.doRunNeuron(simConfig)
print "Set running simulation: "+simRef

print "allow 3 mins for simulation to finish..."
	  
time.sleep(180)
            
# get values from NEURON-vector format into Python format
times_nC = [] # Use list to add another trace later.
linestring = open('models/LarkumEtAl2009/simulations/testsim/time.dat', 'r').read()
times_nC = map(float, linestring.split())

voltages_nC = []
linestring = open('models/LarkumEtAl2009/simulations/testsim/pyr_group_0.dat', 'r').read()
voltages_nC = map(float, linestring.split())
            
print "================================="
print "load original modelDB spike times"
print "================================="

print "opening file .../ModelDB/IClamp_somaV.txt"

# the file IClamp_somaV.txt contains the somatic recording from the original ModelDB model
# run with a time step of 0.025 ms, Ra = 85 Mohm, eK = -87mV (as in the paper)

# get values from NEURON-vector format into Python format
times_original = []
voltages_original = []
for line in open ('models/LarkumEtAl2009/ModelDB/IClamp_somaV.txt', 'rt'):
   t, v = [float (x) for x in line.split()]
   times_original.append (t)
   voltages_original.append (v)

print "============================"
print "plot and compare spike times"
print "============================"

analyseStartTime = 0 # ms
analyseStopTime = 600
analyseThreshold = -20 # mV

spikeTimes_nC = SpikeAnalyser.getSpikeTimes(voltages_nC, times_nC, analyseThreshold, analyseStartTime, analyseStopTime)
print "neuroConcsturct spike times:"
print spikeTimes_nC

spikeTimes_original = SpikeAnalyser.getSpikeTimes(voltages_original, times_original, analyseThreshold, analyseStartTime, analyseStopTime)
print "modelDB spike times:"
print spikeTimes_original

plotFrame = PlotManager.getPlotterFrame("test model: "+str(myProject.getProjectFile()) , 1, 1)
plotFrame.setViewMode(PlotCanvas.INCLUDE_ORIGIN_VIEW)
info = "modelDB vs nC: "+str(simConfig)

dataSet_nC = DataSet(info, info, "ms", "nC", "time", "nC")
dataSet_nC.setGraphFormat(PlotCanvas.USE_CIRCLES_FOR_PLOT)   
for t1 in spikeTimes_nC:
   dataSet_nC.addPoint(t1,1)
 
dataSet_original = DataSet(info, info, "ms", "modelDB", "time", "modelDB")
dataSet_original.setGraphFormat(PlotCanvas.USE_CIRCLES_FOR_PLOT)   
for t2 in spikeTimes_original:
   dataSet_original.addPoint(t2,1)
   
plotFrame.addDataSet(dataSet_nC)
plotFrame.addDataSet(dataSet_original)

test = 0
if len(spikeTimes_nC) == len(spikeTimes_original):
   test = 1
   for x in range(len(spikeTimes_nC)):
      if (abs(spikeTimes_nC[x] - spikeTimes_original[x]) > 1): # 1 ms precision
	 test = 0
	 
if test == 0 :
  print "**************** TEST FAILED ****************"
else:
  print "================ TEST PASSED ================"
   
 

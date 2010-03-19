#
#
#   A file which generates a frequency vs current curve for various cells
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

from sys import *

from java.io import File

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.gui.plotter import PlotManager
from ucl.physiol.neuroconstruct.gui.plotter import PlotCanvas
from ucl.physiol.neuroconstruct.dataset import DataSet
from ucl.physiol.neuroconstruct.neuron import NeuronFileManager
from ucl.physiol.neuroconstruct.cell.compartmentalisation import GenesisCompartmentalisation
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager

from math import *
import time
import sys

class FreqVsCurrentGenerator:

	neuroConstructSeed = 1234
	simulatorSeed = 4321

	simsRunning = []
	myProject = None
	simulator = None

	def generateF_ICurve(self,
                         projFile,
                         simulator,
                         simConfig,
                         preStimAmp, preStimDel, preStimDur,
                         stimAmpLow, stimAmpInc, stimAmpHigh,
                         stimDel, stimDur,
                         simDuration,
                         analyseStartTime, analyseStopTime,
                         analyseThreshold,
                         maxNumSimultaneousSims = 4):

			# Load neuroConstruct project

			print "Loading project from file: " + projFile.getAbsolutePath()+", exists: "+ str(projFile.exists())

			pm = ProjectManager()
			self.myProject = pm.loadProject(projFile)
			self.simulator = simulator

			simConfig = self.myProject.simConfigInfo.getSimConfig(simConfig)

			simConfig.setSimDuration(simDuration)

			pm.doGenerate(simConfig.getName(), self.neuroConstructSeed)

			while pm.isGenerating():
					print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
					time.sleep(2)

			numGenerated = self.myProject.generatedCellPositions.getNumberInAllCellGroups()

			print "Number of cells generated: " + str(numGenerated)

			simReferences = {}


			if numGenerated > 0:

					print "Generating scripts for simulator: %s..."%simulator

					if simulator == 'NEURON':
						self.myProject.neuronFileManager.setQuitAfterRun(1) # Remove this line to leave the NEURON sim windows open after finishing
						self.myProject.neuronSettings.setCopySimFiles(1) # 1 copies hoc/mod files to PySim_0 etc. and will allow multiple sims to run at once
						self.myProject.neuronSettings.setGraphicsMode(0) # 0 hides graphs during execution
                        
					if simulator == 'GENESIS':
						self.myProject.genesisFileManager.setQuitAfterRun(1) # Remove this line to leave the NEURON sim windows open after finishing
						self.myProject.genesisSettings.setCopySimFiles(1) # 1 copies hoc/mod files to PySim_0 etc. and will allow multiple sims to run at once
						self.myProject.genesisSettings.setGraphicsMode(0) # 0 hides graphs during execution


					stimAmp = stimAmpLow

					while stimAmp <= stimAmpHigh:

							while (len(self.simsRunning)>=maxNumSimultaneousSims):
									print "Sims currently running: "+str(self.simsRunning)
									print "Waiting..."
									time.sleep(3) # wait a while...
									self.updateSimsRunning()


							simRef = "PySim_"+str(float(stimAmp))

							print "Going to run simulation: "+simRef

							########  Adjusting the amplitude of the current clamp ###############

                                                        # preStim = self.myProject.elecInputInfo.getStim(simConfig.getInputs().get(0))
							preStim = self.myProject.elecInputInfo.getStim("Input_3")

							preStim.setAmp(NumberGenerator(preStimAmp))
							preStim.setDel(NumberGenerator(preStimDel))
							preStim.setDur(NumberGenerator(preStimDur))
							self.myProject.elecInputInfo.updateStim(preStim)


							# stim = self.myProject.elecInputInfo.getStim(simConfig.getInputs().get(1))
							stim = self.myProject.elecInputInfo.getStim("Input_4")
							

							stim.setAmp(NumberGenerator(stimAmp))
							stim.setDel(NumberGenerator(stimDel))
							stim.setDur(NumberGenerator(stimDur))
							self.myProject.elecInputInfo.updateStim(stim)

							print "Next stim: "+ str(stim)

							self.myProject.simulationParameters.setReference(simRef)

							if simulator == "NEURON":
									self.myProject.neuronFileManager.generateTheNeuronFiles(simConfig,
																							None,
																							NeuronFileManager.RUN_HOC,
																							self.simulatorSeed)

									print "Generated NEURON files for: "+simRef

									compileProcess = ProcessManager(self.myProject.neuronFileManager.getMainHocFile())

									compileSuccess = compileProcess.compileFileWithNeuron(0,0)

									print "Compiled NEURON files for: "+simRef

									if compileSuccess:
													pm.doRunNeuron(simConfig)
													print "Set running simulation: "+simRef
													self.simsRunning.append(simRef)

							if simulator == "GENESIS":
									compartmentalisation = GenesisCompartmentalisation()

									self.myProject.genesisFileManager.generateTheGenesisFiles(simConfig,
																							None,
																							compartmentalisation,
																							self.simulatorSeed)
									print "Generated GENESIS files for: "+simRef

									pm.doRunGenesis(simConfig)
									print "Set running simulation: "+simRef
									self.simsRunning.append(simRef)

							time.sleep(1) # Wait for sim to be kicked off
							simReferences[simRef] = stimAmp
							stimAmp = stimAmp +stimAmpInc

					print
					print "Finished running "+str(len(simReferences))+" simulations for project "+ projFile.getAbsolutePath()
					print "These can be loaded and replayed in the previous simulation browser in the GUI"
					print

			while (len(self.simsRunning)>0):
					print "Sims currently running: "+str(self.simsRunning)
					print "Waiting..."
					time.sleep(4) # wait a while...
					self.updateSimsRunning()

			#simReferences = {'PySim_0.3':0.3,'PySim_0.4':0.4,'PySim_0.5':0.5}

			plotFrameFI = PlotManager.getPlotterFrame("F-I curve from project: "+str(self.myProject.getProjectFile())+" on "+simulator , 1, 1)
			plotFrameVolts = PlotManager.getPlotterFrame("VoltageTraces from project: "+str(self.myProject.getProjectFile())+" on "+simulator , 1, 1)

			plotFrameFI.setViewMode(PlotCanvas.INCLUDE_ORIGIN_VIEW)

			info = "F-I curve for Simulation Configuration: "+str(simConfig)

			dataSet = DataSet(info, info, "nA", "Hz", "Current injected", "Firing frequency")
			dataSet.setGraphFormat(PlotCanvas.USE_CIRCLES_FOR_PLOT)

			simList = simReferences.keys()
			simList.sort()

			for sim in simList:

					simDir = File(projFile.getParentFile(), "/neuroConstruct/models/Dan_GranCell/simulations/"+sim)
					print
					print "--- Reloading data from simulation in directory: %s"%simDir.getCanonicalPath()
					try:
							simData = SimulationData(simDir)
							simData.initialise()
							print "Data loaded: "
							print simData.getAllLoadedDataStores()
							times = simData.getAllTimes()
							cellSegmentRef = simConfig.getCellGroups().get(0)+"_0"
							volts = simData.getVoltageAtAllTimes(cellSegmentRef)

							traceInfo = "Voltage at: %s in simulation: %s"%(cellSegmentRef, sim)

							dataSetV = DataSet(traceInfo, traceInfo, "mV", "ms", "Membrane potential", "Time")
							for i in range(len(times)):
									dataSetV.addPoint(times[i], volts[i])

							plotFrameVolts.addDataSet(dataSetV)

							spikeTimes = SpikeAnalyser.getSpikeTimes(volts, times, analyseThreshold, analyseStartTime, analyseStopTime)
							stimAmp = simReferences[sim]
							print "Number of spikes at %f nA in sim %s: %i"%(stimAmp, sim, len(spikeTimes))
							avgFreq = 0
							if len(spikeTimes)>1:
									avgFreq = len(spikeTimes)/ ((analyseStopTime - analyseStartTime)/1000.0)
									dataSet.addPoint(stimAmp,avgFreq)
					except:
							print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
							print sys.exc_info()[0]


			plotFrameFI.addDataSet(dataSet)


	def updateSimsRunning(self):

			simsFinished = []

			for sim in self.simsRunning:
					timeFile = File(self.myProject.getProjectMainDirectory(), "simulations/"+sim+"/time.dat")
					finishedFile = File(self.myProject.getProjectMainDirectory(), "simulations/"+sim+"/finished")
					#print "Checking file: "+timeFile.getAbsolutePath() +", exists: "+ str(timeFile.exists())
					if (((self.simulator == "NEURON") and timeFile.exists()) or 
                        ((self.simulator == "GENESIS") and finishedFile.exists())):
							simsFinished.append(sim)

			if(len(simsFinished)>0):
					for sim in simsFinished:
							self.simsRunning.remove(sim)

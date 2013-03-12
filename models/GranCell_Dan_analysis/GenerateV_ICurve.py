#
#
#   Trying to generate V-I curve
#
#   Author: Dan Ruedt
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
from ucl.physiol.neuroconstruct.neuron import NativeCodeLocation
from ucl.physiol.neuroconstruct.cell.compartmentalisation import GenesisCompartmentalisation
from ucl.physiol.neuroconstruct.utils import NumberGenerator
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser
from ucl.physiol.neuroconstruct.nmodleditor.processes import ProcessManager

from math import *
import time
import sys

class VoltageVsCurrentGenerator:

	neuroConstructSeed = 1234
	simulatorSeed = 4321

	simsRunning = []
	myProject = None
	simulator = None

	def generateV_ICurve(self,
                         projFile,
                         simulator,
                         simConfig,
                         stimAmpLow, stimAmpInc, stimAmpHigh,
                         stimDur,
                         simDuration,
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

					ADD_TO_BEFORE_INIT = self.myProject.neuronSettings.getNativeBlock(NativeCodeLocation.BEFORE_INITIAL)
					ADD_TO_RECORD_I = self.myProject.neuronSettings.getNativeBlock(NativeCodeLocation.AFTER_SIMULATION)
					ADD_TO_START_FINITIALIZE = self.myProject.neuronSettings.getNativeBlock(NativeCodeLocation.START_FINITIALIZE)

					while stimAmp <= stimAmpHigh:

							while (len(self.simsRunning)>=maxNumSimultaneousSims):
									print "Sims currently running: "+str(self.simsRunning)
									print "Waiting..."
									time.sleep(3) # wait a while...
									self.updateSimsRunning()


							simRef = "PySim_"+str(float(stimAmp))

							print "Going to run simulation: "+simRef

							########  Adjusting the amplitude of the Voltage clamp ###############

                                                        TEXT_BEFORE_CREATION = "objref clampobj" + "\n" + "objref record_current" + "\n" + "objref data_save" + "\n"

                                                        # TEXT_BEFORE_INIT = "GranuleCell_mod_tonic[0].Soma {\n" + "clampobj = new SEClamp(0.5)\n" + "clampobj.dur1 = 150.0" + "\n" + "clampobj.amp1 = -100.0" + "\n" + "clampobj.dur2 = " + str(stimDur) + "\n" + "clampobj.amp2 = " + str(stimAmp) + "\n" + "clampobj.dur3 = 150.0" + "\n" + "clampobj.amp3 = -100.0" + "\n" + "clampobj.rs = 0.00001\n " + "}\n" # This should do the trick

                                                        # TEXT_BEFORE_INIT = TEXT_BEFORE_INIT + ADD_TO_BEFORE_INIT

                                                        TEXT_START_FINITIALIZE = "GranuleCell_mod_tonic[0].Soma {\n" + "clampobj = new SEClamp(0.5)\n" + "clampobj.dur1 = 150.0" + "\n" + "clampobj.amp1 = -100.0" + "\n" + "clampobj.dur2 = " + str(stimDur) + "\n" + "clampobj.amp2 = " + str(stimAmp) + "\n" + "clampobj.dur3 = 150.0" + "\n" + "clampobj.amp3 = -40.0" + "\n" + "clampobj.rs = 0.00001\n" + "record_current = new Vector()" + "\n" + "record_current.record(&clampobj.i)" + "\n" + "}\n" #This should do the trick

                                                        TEXT_START_FINITIALIZE = TEXT_START_FINITIALIZE + ADD_TO_START_FINITIALIZE

                                                        TEXT_TO_RECORD_I = """data_save = new File() \n""" + """strdef filename \n""" + """sprint(filename, """" + self.myProject.getProjectMainDirectory().getAbsolutePath() + """/simulations/current%.3f.txt", clampobj.amp2) \n""" + """data_save.wopen(filename) \n""" + """record_current.printf(data_save) \n""" + """data_save.close() \n"""

                                                        TEXT_TO_RECORD_I = TEXT_TO_RECORD_I + ADD_TO_RECORD_I

                                                        self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.BEFORE_CELL_CREATION, TEXT_BEFORE_CREATION)
                                                        # self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.BEFORE_INITIAL, TEXT_BEFORE_INIT)
                                                        self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.START_FINITIALIZE, TEXT_START_FINITIALIZE)
                                                        self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.AFTER_SIMULATION, TEXT_TO_RECORD_I)

					
							print "Next stim: "+ str(stimAmp)

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

			plotFrameVI = PlotManager.getPlotterFrame("V-I curve from project: "+str(self.myProject.getProjectFile())+" on "+simulator , 1, 1)


			plotFrameVI.setViewMode(PlotCanvas.INCLUDE_ORIGIN_VIEW)

			info = "V-I curve for Simulation Configuration: "+str(simConfig)

			dataSet = DataSet(info, info, "mV", "nA", "Voltage", "Current")
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

							cfilename = "E:/neuroConstruct/models/Dan_GranCell/simulations/" + sim + "/current.txt"
							trace = "E:/neuroConstruct/models/Dan_GranCell/simulations/" + sim + ".txt"
							# cFILE = open(cfilename, "r")
							
							
							strom = 0.0
							
							volts = simData.getVoltageAtAllTimes(cellSegmentRef)
							

							traceInfo = "Voltage at: %s in simulation: %s"%(cellSegmentRef, sim)

							stimAmp = simReferences[sim]
							print "Current at %f mV in sim %s: %f"%(stimAmp, sim, float(strom))
							
							dataSet.addPoint(stimAmp,float(strom))
					except:
							print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
							print sys.exc_info()[0]


			plotFrameVI.addDataSet(dataSet)


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

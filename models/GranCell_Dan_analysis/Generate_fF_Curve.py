#
#
#   Trying to generate f-F curve
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

class fFplot:

	neuroConstructSeed = 1234
	simulatorSeed = 4321

	simsRunning = []
	myProject = None
	simulator = None

	def make_fF_Curve(self,
                          projFile,
                          simulator,
                          simConfig,
                          nTrains,
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


					currentTrain = 0

					ADD_TO_START_FINITIALIZE = self.myProject.neuronSettings.getNativeBlock(NativeCodeLocation.START_FINITIALIZE)
					ADD_TO_RECORD_I = self.myProject.neuronSettings.getNativeBlock(NativeCodeLocation.AFTER_SIMULATION)

					while currentTrain <= nTrains:

							while (len(self.simsRunning)>=maxNumSimultaneousSims):
									print "Sims currently running: "+str(self.simsRunning)
									print "Waiting..."
									time.sleep(3) # wait a while...
									self.updateSimsRunning()


							simRef = "PySim_"+str(currentTrain)

							print "Going to run simulation: "+simRef

							########  Adjusting the amplitude of the Voltage clamp ###############

                                                        TEXT_BEFORE_CREATION = """objref vector, gTrainFile\n""" + "objectvar clamp\n"

                                                        ### TEXT_BEFORE_INIT = "GranuleCell_mod_tonic[0].Soma {\n" + "clampobj = new VClamp(0.5)\n" + "clampobj.dur[0] = " + str(stimDur) + "\n" + "clampobj.amp[0] = " + str(stimAmp) + "\n" +  "}\n" # This should do the trick

                                                        TEXT_START_FINITIALIZE = "\n" + "gTrainFile = new File() \n" + "vector = new Vector(100000) \n" + "access GranuleCell_mod_tonic[0].Soma \n" + "clamp = new SEClamp(0.5) \n" + "clamp.amp1 = 0 \n" + "clamp.dur1 = 1e9 \n" + """gTrainFile.ropen("E:/neuroConstruct/models/Dan_GranCell/gTrains_nS/gAMPA_""" + str(currentTrain) + """.txt") \n""" + "vector.scanf(gTrainFile) \n" + "gTrainFile.close \n" + "for i = 0, vector.size() -1 { \n" + "     if (vector.x[i] <= 0) { \n" + "          vector.x[i] = 1e-20 \n" + "              } \n" + "        } \n" + "for i = 0, vector.size() -1 { \n" + "    vector.x[i] = ( 1 / vector.x[i] ) * 1000 \n" + "    } \n" + "vector.play(&clamp.rs, 0.03) \n" # This

                                                        TEXT_START_FINITIALIZE = TEXT_START_FINITIALIZE + ADD_TO_START_FINITIALIZE

                                                        TEXT_TO_RECORD_I = """// currently not used \n"""

                                                        TEXT_TO_RECORD_I = TEXT_TO_RECORD_I + ADD_TO_RECORD_I

                                                        self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.BEFORE_CELL_CREATION, TEXT_BEFORE_CREATION)
                                                        self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.START_FINITIALIZE, TEXT_START_FINITIALIZE)
                                                        self.myProject.neuronSettings.setNativeBlock(NativeCodeLocation.AFTER_SIMULATION, TEXT_TO_RECORD_I)

					
							print "Next Train: "+ str(currentTrain)

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
							simReferences[simRef] = currentTrain
							currentTrain = currentTrain + 1

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

			plotFrameFf = PlotManager.getPlotterFrame("F-f curve from project: "+str(self.myProject.getProjectFile())+" on "+simulator , 1, 1)

			plotFrameVolts = PlotManager.getPlotterFrame("VoltageTraces from project: "+str(self.myProject.getProjectFile())+" on "+simulator , 1, 1)

			plotFrameFf.setViewMode(PlotCanvas.INCLUDE_ORIGIN_VIEW)

			info = "F-f curve for Simulation Configuration: "+str(simConfig)

			dataSet = DataSet(info, info, "Hz", "Hz", "Input_Freq", "Output_Freq")
			dataSet.setGraphFormat(PlotCanvas.USE_CIRCLES_FOR_PLOT)

			simList = simReferences.keys()
			simList.sort()
			
		        traininfos = open("E:/neuroConstruct/models/Dan_GranCell/gAMPA_traininfo.txt")
			train_info_list = traininfos.readlines()
			currentTrain = 0

			for sim in simList:

					simDir = File(projFile.getParentFile(), "E:/neuroConstruct/models/Dan_GranCell/simulations/"+sim)
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

							time.sleep(2)

							traceInfo = "Voltage at: %s in simulation: %s"%(cellSegmentRef, sim)

							dataSetV = DataSet(traceInfo, traceInfo, "ms", "mV", "Time", "Membrane Potential")

                                                        
                                                        Spike_List = []

                                                        Spike_List.append(0.00)

							for i in range(len(times)):
								dataSetV.addPoint(times[i], volts[i])

							for i in range(len(times)):
								if (volts[i] > 0.0):
                                                                        if (times[i] - Spike_List[len(Spike_List)-1] > 0.50):
                                                                                Spike_List.append(times[i])

                                                                                
                                                        Spike_List.remove(0.00)
        

							plotFrameVolts.addDataSet(dataSetV)

							spikeTimes = SpikeAnalyser.getSpikeTimes(volts, times, analyseThreshold, analyseStartTime, analyseStopTime)

							currentTrain_Freq = float(train_info_list[currentTrain-1])

							
							print "Number of spikes in sim %s: %i"%(sim, len(spikeTimes))
							avgFreq = 0
							if len(Spike_List)>0:
									avgFreq = 1000.0 / ((Spike_List[len(Spike_List)-1] - Spike_List[0]) / (len(Spike_List) -1))
									dataSet.addPoint(currentTrain_Freq,avgFreq)
							currentTrain = currentTrain + 1

							
					except:
							print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
							print sys.exc_info()[0]


			plotFrameFf.addDataSet(dataSet)


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

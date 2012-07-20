#
#   A file that opens the neuroConstruct project LarkumEtAl2009 and run multiple simulations stimulating ech terminal apical branch with varying number of synapses.
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
from math import *
import time
import shutil
import random
import os
import subprocess

# Load the original project
projName = "LarkumEtAl2009"
projFile = File("/home/matteo/neuroConstruct/models/"+projName+"/"+projName+".ncx")

print "Loading project from file: " + projFile.getAbsolutePath()+", exists: "+ str(projFile.exists())
pm = ProjectManager()
myProject = pm.loadProject(projFile)
simConfig = myProject.simConfigInfo.getSimConfig("Default Simulation Configuration")#
randomseed = random.randint(1000,5000)
pm.doGenerate(simConfig.getName(),  randomseed)
while pm.isGenerating():
    print "Waiting for the project to be generated..."
    time.sleep(2)    
numGenerated = myProject.generatedCellPositions.getNumberInAllCellGroups()

simsRunning = []
def updateSimsRunning():
    simsFinished = []
    for sim in simsRunning:
        timeFile = File(myProject.getProjectMainDirectory(), "simulations/"+sim+"/time.dat")
        #print "Checking file: "+timeFile.getAbsolutePath() +", exists: "+ str(timeFile.exists())
        if (timeFile.exists()):
            simsFinished.append(sim)
    if(len(simsFinished)>0):
        for sim in simsFinished:
            simsRunning.remove(sim)            

if numGenerated > 0:

    print "Generating NEURON scripts..."
    myProject.neuronFileManager.setQuitAfterRun(1) # Remove this line to leave the NEURON sim windows open after finishing
    myProject.neuronSettings.setCopySimFiles(1) # 1 copies hoc/mod files to PySim_0 etc. and will allow multiple sims to run at once
    myProject.neuronSettings.setGraphicsMode(False) # Run NEURON without GUI
    # Note same network structure will be used for each!  
    # Change this number to the number of processors you wish to use on your local machine
    maxNumSimultaneousSims = 100

    #multiple simulation settings:    
    prefix = "" #string that will be added to the name of the simulations to identify the simulation set    
    trials = 1
    Nbranches = 28
    Configuration = ["NMDAspike input"]

    apical_branch = ["apical17","apical18","apical21","apical23","apical24","apical25","apical27","apical28","apical31","apical34","apical35","apical37","apical38","apical44","apical46","apical52","apical53","apical54","apical56","apical57","apical61","apical62","apical65","apical67","apical68","apical69","apical72","apical73"]

    apical_stim = ["NMDAs_17","NMDAs_18","NMDAs_21","NMDAs_23","NMDAs_24","NMDAs_25","NMDAs_27","NMDAs_28","NMDAs_31","NMDAs_34","NMDAs_35","NMDAs_37","NMDAs_38","NMDAs_44","NMDAs_46","NMDAs_52","NMDAs_53","NMDAs_54","NMDAs_56","NMDAs_57","NMDAs_61","NMDAs_62","NMDAs_65","NMDAs_67","NMDAs_68","NMDAs_69","NMDAs_72","NMDAs_73"]

    apical_ID =[4460,4571,4793,4961,4994,5225,5477,5526,5990,6221,6274,6523,6542,6972,7462,8026,8044,8088,8324,8468,8685,8800,8966,9137,9160,9186,9592,9639]
    
    apical_lenght = [98,69,78,26,34,166,161,49,143,55,87,25,38,73,194,19,22,26,25,129,138,95,42,89,21,62,26,18]  
 
    apical_plot = ["pyrCML_apical17_V","pyrCML_apical18_V","pyrCML_apical21_V","pyrCML_apical23_V","pyrCML_apical24_V","pyrCML_apical25_V","pyrCML_apical27_V","pyrCML_apical28_V","pyrCML_apical31_V","pyrCML_apical34_V","pyrCML_apical35_V","pyrCML_apical37_V","pyrCML_apical38_V","pyrCML_apical44_V","pyrCML_apical46_V","pyrCML_apical52_V","pyrCML_apical53_V","pyrCML_apical54_V","pyrCML_apical56_V","pyrCML_apical57_V","pyrCML_apical61_V","pyrCML_apical62_V","pyrCML_apical65_V","pyrCML_apical67_V","pyrCML_apical68_V","pyrCML_apical69_V","pyrCML_apical72_V","pyrCML_apical73_V"]
    
    print "Going to run " +str(int(trials*Nbranches)) + " simulations"
   
    refStored = []
    simGroups = ArrayList()
    simInputs = ArrayList()
    simPlots = ArrayList()

    stringConfig = Configuration[0]
    print "nConstruct using SIMULATION CONFIGURATION: " +stringConfig
    simConfig = myProject.simConfigInfo.getSimConfig(stringConfig) 
       
    for y in range(0, Nbranches):
       
       j=y+1
       
       selectedBranches = []

       prefix = "b"+str(j) #number of branches stimulated
       
       print
       print "-----------------------------------------------------------------------"
       print str(trials)+" trials, stimulating " +str(int(j))+" branches"
       print "reference name: " + prefix +"..."
       print "-----------------------------------------------------------------------"
       print
       
       for i in range(0, trials):
          
          print ""
          selectedBranches = []

          #empty vectors
	  simGroups = ArrayList()
	  simInputs = ArrayList()
	  simPlots = ArrayList()

          '''########  Selecting j random different apical branches, to Input and Plot ###############
          for r in range(0,j):

             randomApicalBranch = random.randint(0,int(len(apical_branch))-1)
             while randomApicalBranch in selectedBranches:
                randomApicalBranch = random.randint(0,int(len(apical_branch))-1)             
             selectedBranches.append(randomApicalBranch)
             print "selected branch  "+apical_branch[randomApicalBranch]
             simInputs.add(apical_stim[randomApicalBranch])
             
             prefix = str(apical_ID[randomApicalBranch])
	     for p in range(0, int(len(apical_plot))):
	       simPlots.add(apical_plot[p])
	  '''
	       
	  simInputs.add(apical_stim[y])
	  prefix = "b"+str(apical_ID[y])
	  for p in range(0, int(len(apical_plot))):
	     simPlots.add(apical_plot[p])

	  simGroups.add("pyrCML_group")          
	  simPlots.add("pyrCML_soma_V")
	  simPlots.add("pyrCML_CaZone_V")
	  
	  simConfig.setCellGroups(simGroups)
	  simConfig.setInputs(simInputs)
	  simConfig.setPlots(simPlots)

          ###################################### control #########################################
	  
	  simRef = prefix+"t"+str(i)+"_control"
	  print "Simref: "+simRef
	  myProject.simulationParameters.setReference(simRef)
	  refStored.append(simRef)
	  
	  randomseed = random.randint(1000,5000)

	  '''##### RUN BLOCK control #####	  

	  pm.doGenerate(simConfig.getName(), randomseed)
	  while pm.isGenerating():
	    print "Waiting for the project to be generated..."
	    time.sleep(2)
		    
	  myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
	  myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
	
	  print "Generated NEURON files for: "+simRef	
	  compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
	  compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
	  print "Compiled NEURON files for: "+simRef

	  if compileSuccess:
	    pm.doRunNeuron(simConfig)
	    print "Set running simulation: "+simRef
	  
	  time.sleep(5) # Wait for sim to be kicked off

	  #####################'''
	  
	  '''########  Running the same configuration + background exc 1500 ###############

	  simInputs.add("backgroundExc")
	  
	  simConfig.setInputs(simInputs)

	  print "group generated: "+simConfig.getCellGroups().toString()
	  print "going to stimulate: "+simConfig.getInputs().toString()
	  print "going to record: "+simConfig.getPlots().toString()
          
          ##########################################################################################
	  
	  simRef = prefix+"t"+str(i)+"_exc1500"
	  print "Simref: "+simRef
	  myProject.simulationParameters.setReference(simRef)
	  refStored.append(simRef)

	  ##### RUN BLOCK background exc #####

	  randomseed = random.randint(1000,5000)

	  pm.doGenerate(simConfig.getName(), randomseed)
	  while pm.isGenerating():
	    print "Waiting for the project to be generated..."
	    time.sleep(2)
		    
	  myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
	  myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
	
	  print "Generated NEURON files for: "+simRef	
	  compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
	  compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
	  print "Compiled NEURON files for: "+simRef

	  if compileSuccess:
	    pm.doRunNeuron(simConfig)
	    print "Set running simulation: "+simRef
	  
	  time.sleep(30)
	  simInputs.remove("backgroundExc")

	  #####################'''
	  
	  '''########  Running the same configuration + background exc/inh ###############

	  simInputs.add("backgroundExc")
	  simInputs.add("backgroundInh")

	  
	  simConfig.setInputs(simInputs)

	  print "group generated: "+simConfig.getCellGroups().toString()
	  print "going to stimulate: "+simConfig.getInputs().toString()
	  print "going to record: "+simConfig.getPlots().toString()
          
          ##########################################################################################
	  
	  simRef = prefix+"t"+str(i)+"_excinh"
	  print "Simref: "+simRef
	  myProject.simulationParameters.setReference(simRef)
	  refStored.append(simRef)

	  ##### RUN BLOCK background exc #####

	  randomseed = random.randint(1000,5000)

	  pm.doGenerate(simConfig.getName(), randomseed)
	  while pm.isGenerating():
	    print "Waiting for the project to be generated..."
	    time.sleep(2)
		    
	  myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
	  myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
	
	  print "Generated NEURON files for: "+simRef	
	  compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
	  compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
	  print "Compiled NEURON files for: "+simRef

	  if compileSuccess:
	    pm.doRunNeuron(simConfig)
	    print "Set running simulation: "+simRef
	  
	  time.sleep(30)
	  simInputs.remove("backgroundExc")
	  simInputs.remove("backgroundInh")


	  #####################'''
	  
	  ########  Running the same configuration + background exc 1500 + inh 150% ###############

	  simInputs.add("backgroundExc")
	  simInputs.add("backgroundInh150")

	  
	  simConfig.setInputs(simInputs)

	  print "group generated: "+simConfig.getCellGroups().toString()
	  print "going to stimulate: "+simConfig.getInputs().toString()
	  print "going to record: "+simConfig.getPlots().toString()
          
          ##########################################################################################
	  
	  simRef = prefix+"t"+str(i)+"_EI150pc"
	  print "Simref: "+simRef
	  myProject.simulationParameters.setReference(simRef)
	  refStored.append(simRef)

	  '''##### RUN BLOCK background exc #####

	  randomseed = random.randint(1000,5000)

	  pm.doGenerate(simConfig.getName(), randomseed)
	  while pm.isGenerating():
	    print "Waiting for the project to be generated..."
	    time.sleep(2)
		    
	  myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
	  myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
	
	  print "Generated NEURON files for: "+simRef	
	  compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
	  compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
	  print "Compiled NEURON files for: "+simRef

	  if compileSuccess:
	    pm.doRunNeuron(simConfig)
	    print "Set running simulation: "+simRef
	  
	  time.sleep(5)
	  simInputs.remove("backgroundExc")
	  simInputs.remove("backgroundInh150")


	  #####################'''

          '''########  Running the same configuration + background exc 1200 ###############

	  simInputs.add("backgroundExc1200")
	  
	  simConfig.setInputs(simInputs)

	  print "group generated: "+simConfig.getCellGroups().toString()
	  print "going to stimulate: "+simConfig.getInputs().toString()
	  print "going to record: "+simConfig.getPlots().toString()
          
          ##########################################################################################
	  
	  simRef = prefix+"t"+str(i)+"_exc1200"
	  print "Simref: "+simRef
	  myProject.simulationParameters.setReference(simRef)
	  refStored.append(simRef)

	  ##### RUN BLOCK background exc #####

	  randomseed = random.randint(1000,5000)

	  pm.doGenerate(simConfig.getName(), randomseed)
	  while pm.isGenerating():
	    print "Waiting for the project to be generated..."
	    time.sleep(2)
		    
	  myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
	  myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
	
	  print "Generated NEURON files for: "+simRef	
	  compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
	  compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
	  print "Compiled NEURON files for: "+simRef

	  if compileSuccess:
	    pm.doRunNeuron(simConfig)
	    print "Set running simulation: "+simRef
	  
	  time.sleep(10) # Wait for sim to be kicked off
	  
	  simInputs.remove("backgroundExc1200")

	  #####################'''
	  
	  '''########  Running the same configuration + background exc 900 ###############

	  simInputs.add("backgroundExc900")
	  
	  simConfig.setInputs(simInputs)

	  print "group generated: "+simConfig.getCellGroups().toString()
	  print "going to stimulate: "+simConfig.getInputs().toString()
	  print "going to record: "+simConfig.getPlots().toString()
          
          ##########################################################################################
	  
	  simRef = prefix+"t"+str(i)+"_exc900"
	  print "Simref: "+simRef
	  myProject.simulationParameters.setReference(simRef)
	  refStored.append(simRef)

	  ##### RUN BLOCK background exc #####

	  randomseed = random.randint(1000,5000)

	  pm.doGenerate(simConfig.getName(), randomseed)
	  while pm.isGenerating():
	    print "Waiting for the project to be generated..."
	    time.sleep(2)
		    
	  myProject.neuronFileManager.setSuggestedRemoteRunTime(10)
	  myProject.neuronFileManager.generateTheNeuronFiles(simConfig, None, NeuronFileManager.RUN_HOC, randomseed)
	
	  print "Generated NEURON files for: "+simRef	
	  compileProcess = ProcessManager(myProject.neuronFileManager.getMainHocFile())	
	  compileSuccess = compileProcess.compileFileWithNeuron(0,0)	
	  print "Compiled NEURON files for: "+simRef

	  if compileSuccess:
	    pm.doRunNeuron(simConfig)
	    print "Set running simulation: "+simRef
	  
	  time.sleep(10) # Wait for sim to be kicked off
	  
	  simInputs.remove("backgroundExc900")

	  #####################'''
	  
        ### end for i (trials)

    ### end for j (noise)
   
########  Extracting simulations results ###############    
time.sleep(60) 

y=-1
for sim in refStored:
    y=y+1
    pullSimFilename = "pullsim.sh"
    path = "/home/matteo/neuroConstruct/models/"+projName
    print "\n------   Checking directory: " + path +"/simulations"+"/"+sim
    pullsimFile = path+"/simulations/"+sim+"/"+pullSimFilename

    if os.path.isfile(pullsimFile):
       print pullSimFilename+" exists and will be executed..."
       process = subprocess.Popen("cd "+path+"/simulations/"+sim+"/"+";./"+pullSimFilename, shell=True, stdout=subprocess.PIPE)
       stdout_value = process.communicate()[0]
       process.wait()       
    else:
       print "Simulation not finished"

    if os.path.isfile(path+"/simulations/"+sim+"/pyrCML_group_0.dat"):
      print "Simulation results recovered from remote cluster."
      simDir = File(path+"/simulations/"+sim)
      newFileSoma = path+"/recordings/"+sim+".soma"
      shutil.copyfile(path+"/simulations/"+sim+"/pyrCML_group_0.dat" , newFileSoma)
      
      for ID in apical_ID:
	  if os.path.isfile(path+"/simulations/"+sim+"/pyrCML_group_0."+str(ID)+".dat"):
            newFileApical = path+"/recordings/"+sim+"_ID"+str(ID)+".apical"
	    shutil.copyfile(path+"/simulations/"+sim+"/pyrCML_group_0."+str(ID)+".dat" , newFileApical)

      print "Simulation was successful. "
      print "Results saved."
      print 
    else:
      print "Simulation failed!"
    

### '''  

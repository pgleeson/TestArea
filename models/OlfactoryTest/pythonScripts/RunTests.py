#
#
#   File to test current configuration of CA1Pyramidal cell project. 
#
#   To execute this type of file, type '..\nC.bat -python XXX.py' (Windows)
#   or '../nC.sh -python XXX.py' (Linux/Mac). Note: you may have to update the
#   NC_HOME and NC_MAX_MEMORY variables in nC.bat/nC.sh
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
import time

from java.io import File

from ucl.physiol.neuroconstruct.project import ProjectManager
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.gui.plotter import PlotManager
from ucl.physiol.neuroconstruct.project import SimPlot
from ucl.physiol.neuroconstruct.cell.utils import CellTopologyHelper


sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc

projFile = File("../OlfactoryTest.ncx")



##############  Main settings  ##################

simConfigs = []

simConfigs.append("Default Simulation Configuration")
#simConfigs.append("SC_nax")
#simConfigs.append("SC_kamt")
#simConfigs.append("SC_kdrmt")


simDt =                 0.002

neuroConstructSeed =    12345
simulatorSeed =         11111

#simulators =            ["NEURON", "GENESIS", "MOOSE", "PSICS"]
#simulators =            ["NEURON"]
simulators =            ["NEURON", "GENESIS", "MOOSE"]
#simulators =            ["PSICS"]

temperatures =          [35]

mpiConf =               MpiSettings.LOCAL_SERIAL

maxElecLens =           [-1]

numConcurrentSims =     3

varTimestepNeuron =     False

runSims =               True
analyseSims =           True
plotSims =              True
plotVoltageOnly =       True

runInBackground =       True

verbose = True

#############################################

print "Loading project from "+ projFile.getCanonicalPath()

pm = ProjectManager()
project = pm.loadProject(projFile)

allRunningSims = []
allFinishedSims = []

def updateSimsRunning():

    for sim in allRunningSims:
            timeFile = File(project.getProjectMainDirectory(), "simulations/"+sim+"/time.dat")
            timeFile2 = File(project.getProjectMainDirectory(), "simulations/"+sim+"/time.txt") # for PSICS...

            print "Checking file: "+timeFile.getAbsolutePath() +", exists: "+ str(timeFile.exists())

            if (timeFile.exists()):
                    allFinishedSims.append(sim)
                    allRunningSims.remove(sim)
            else:
                print "Checking file: "+timeFile2.getAbsolutePath() +", exists: "+ str(timeFile2.exists())
                if (timeFile2.exists()):
                    allFinishedSims.append(sim)
                    allRunningSims.remove(sim)

    print "allFinishedSims: "+str(allFinishedSims)
    print "allRunningSims: "+str(allRunningSims)


def reloadSims(waitForSimsToFinish):


    print "Trying to reload sims: "+str(allFinishedSims)

    plottedSims = []

    for simRef in allFinishedSims:

        simDir = File(projFile.getParentFile(), "/simulations/"+simRef)
        timeFile = File(simDir, "time.dat")
        timeFile2 = File(simDir,"time.txt") # for PSICS...


        if timeFile.exists() or timeFile2.exists():
            if verbose: print "--- Reloading data from simulation in directory: %s"%simDir.getCanonicalPath()
            time.sleep(1) # wait a while...

            try:
                simData = SimulationData(simDir)
                simData.initialise()
                times = simData.getAllTimes()

                if analyseSims:
                    '''
                    volts = simData.getVoltageAtAllTimes(cellSegmentRef)

                    if verbose: print "Got "+str(len(volts))+" data points on cell seg ref: "+cellSegmentRef

                    analyseStartTime = 0
                    analyseStopTime = simConfig.getSimDuration()
                    analyseThreshold = -20 # mV

                    spikeTimes = SpikeAnalyser.getSpikeTimes(volts, times, analyseThreshold, analyseStartTime, analyseStopTime)

                    print "Spike times in %s for sim %s: %s"%(cellSegmentRef, simRef, str(spikeTimes))
                    '''

                if plotSims:

                    simConfigName = simData.getSimulationProperties().getProperty("Sim Config")
                    temp = simData.getSimulationProperties().getProperty("Simulation temp")

                    if simConfigName.find('(')>=0:
                        simConfigName = simConfigName[0:simConfigName.find('(')]

                    for dataStore in simData.getAllLoadedDataStores():

                        ds = simData.getDataSet(dataStore.getCellSegRef(), dataStore.getVariable(), False)

                        if not plotVoltageOnly or dataStore.getVariable() == SimPlot.VOLTAGE:

                            plotFrame = PlotManager.getPlotterFrame("Behaviour of "+dataStore.getVariable() \
                                +" on: %s for sim config: %s at temperature: %s"%(str(simulators), simConfigName, temp))

                            plotFrame.addDataSet(ds)


                    plottedSims.append(simRef)


            except:
                print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
                print sys.exc_info()

    for simRef in plottedSims:
        allFinishedSims.remove(simRef)


    if waitForSimsToFinish and len(allRunningSims)>0:

        if verbose: print "Waiting for sims: %s to finish..."%str(allRunningSims)

        time.sleep(2) # wait a while...
        updateSimsRunning()
        reloadSims(True)


def doCheckNumberSims():

    print "Sims currently running: "+str(allRunningSims)

    while (len(allRunningSims)>=numConcurrentSims):
        print "Waiting..."
        time.sleep(4) # wait a while...
        updateSimsRunning()


for simConfigName in simConfigs:

  for maxElecLen in maxElecLens:
   for temp in temperatures:

    simTempStr = ""
    if temp >=0:
        project.simulationParameters.setTemperature(temp)
        simTempStr = "_%i"%temp

    project.simulationParameters.setDt(simDt)

    simConfig = project.simConfigInfo.getSimConfig(simConfigName)

    recompSuffix = ""
    
    if maxElecLen > 0:
        cellGroup = simConfig.getCellGroups().get(0)
        cell = project.cellManager.getCell(project.cellGroupsInfo.getCellType(cellGroup))
        print "Recomp cell in: "+cellGroup+" which is: "+str(cell)
        info = CellTopologyHelper.recompartmentaliseCell(cell, maxElecLen, project)
        print "*** Recompartmentalised cell: "+info
        recompSuffix = "_"+str(maxElecLen)

    pm.doGenerate(simConfig.getName(), neuroConstructSeed)

    while pm.isGenerating():
            if verbose: print "Waiting for the project to be generated with Simulation Configuration: "+str(simConfig)
            time.sleep(1)


    print "Generated network with %i cell(s)" % project.generatedCellPositions.getNumberInAllCellGroups()


    simRefPrefix = (simConfigName+"_").replace(' ', '')+simTempStr

    doCheckNumberSims()

    if simulators.count("NEURON")>0:

        simRef = simRefPrefix+"_N"+recompSuffix
        project.simulationParameters.setReference(simRef)

        if runSims:
            nc.generateAndRunNeuron(project,
                             pm,
                             simConfig,
                             simRef,
                             simulatorSeed,
                             verbose=verbose,
                             runInBackground=runInBackground,
                             varTimestep=varTimestepNeuron)

        allRunningSims.append(simRef)


    doCheckNumberSims()

    if simulators.count("PSICS")>0:

        simRef = simRefPrefix+"_P"+recompSuffix
        project.simulationParameters.setReference(simRef)

        if runSims:
            nc.generateAndRunPsics(project,
                             pm,
                             simConfig,
                             simRef,
                             simulatorSeed,
                             verbose=verbose,
                             runInBackground=runInBackground)

        allRunningSims.append(simRef)


    doCheckNumberSims()

    if simulators.count("MOOSE")>0:

        simRef = simRefPrefix+"_M"+recompSuffix
        project.simulationParameters.setReference(simRef)

        if runSims:
            nc.generateAndRunMoose(project,
                             pm,
                             simConfig,
                             simRef,
                             simulatorSeed,
                             verbose=verbose,
                             quitAfterRun=runInBackground,
                             runInBackground=runInBackground)

        allRunningSims.append(simRef)

        time.sleep(2) # wait a while before running GENESIS...

    doCheckNumberSims()

    if simulators.count("GENESIS")>0:

        simRef = simRefPrefix+"_G"+recompSuffix
        project.simulationParameters.setReference(simRef)

        if runSims:
            nc.generateAndRunGenesis(project,
                             pm,
                             simConfig,
                             simRef,
                             simulatorSeed,
                             verbose=verbose,
                             quitAfterRun=runInBackground,
                             runInBackground=runInBackground,
                             symmetricComps=False)

        allRunningSims.append(simRef)

        time.sleep(2) # wait a while before running GENESISsym...
        
    doCheckNumberSims()

    if simulators.count("GENESISsym")>0:

        simRef = simRefPrefix+"_Gs"+recompSuffix
        project.simulationParameters.setReference(simRef)

        if runSims:
            nc.generateAndRunGenesis(project,
                             pm,
                             simConfig,
                             simRef,
                             simulatorSeed,
                             verbose=verbose,
                             quitAfterRun=runInBackground,
                             runInBackground=runInBackground,
                             symmetricComps=True)

        allRunningSims.append(simRef)


    updateSimsRunning()
    reloadSims(waitForSimsToFinish=False)


reloadSims(waitForSimsToFinish=True)
    


if not plotSims:
    sys.exit()



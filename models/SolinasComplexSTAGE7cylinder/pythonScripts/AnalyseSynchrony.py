#
#
#   File to analyse across multiple simulations
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Wellcome Trust and the Medical
#   Research Council
#
#

from sys import *
from time import *

from java.io import File
from java.util import ArrayList

from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser
from ucl.physiol.neuroconstruct.gui.plotter import PlotManager
from ucl.physiol.neuroconstruct.project import SimPlot
from ucl.physiol.neuroconstruct.utils import GeneralUtils

#################################################

projFile = File("../SolinasComplexSTAGE7cylinder.ncx")
simRefs = ["Sim_2296", "Sim_2299", "Sim_2302", "Sim_2308", "Sim_2315"]

threshold = -20
slideSize = 20

#################################################

from ucl.physiol.neuroconstruct.project import ProjectManager

print 'Loading project file: ', projFile.getAbsolutePath()

pm = ProjectManager()
project = pm.loadProject(projFile)

print 'Successfully loaded project: ', project.getProjectName()


generatedCellPositions = None
inputCells = []

plotFrame = PlotManager.getPlotterFrame("Analysis of synchrony from: "+project.getProjectName(), False)

for simRef in simRefs:

    try:
        
        GeneralUtils.timeCheck("Before load sim", True)

        simData = pm.reloadSimulation(simRef)

        print
        print "--- Reloading data from simulation: %s"%simRef


        for input in project.generatedElecInputs.getInputLocations("Input_0"):
            if input.getCellNumber() not in inputCells:
                inputCells.append(input.getCellNumber())

        print "Inputs: "+str(inputCells)

        GeneralUtils.timeCheck("After load sim", True)
        spikeLists = ArrayList()

        times = simData.getAllTimes()


        for input in inputCells:
            cellSegRef = SimulationData.getCellRef("CellGroup_1", input)
            volts = simData.getVoltageAtAllTimes(cellSegRef)
            spikes = SpikeAnalyser.getSpikeTimes(volts,
                                                 times,
                                                 threshold,
                                                 0,
                                                 times[-1])
            spikeLists.add(spikes)
            #ds = simData.getDataSet(cellSegRef, SimPlot.VOLTAGE, False)
            #plotFrame.addDataSet(ds)

        ds = SpikeAnalyser.getSlidingSpikeSynchrony(spikeLists,
                                                    times,
                                                    slideSize,
                                                    0,
                                                    times[-1])

        plotFrame.addDataSet(ds)




    except:
        print "Error analysing simulation data from: %s"%simRef
        print exc_info()


plotFrame.setVisible(True)






                                        
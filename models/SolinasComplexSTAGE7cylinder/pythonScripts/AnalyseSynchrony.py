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

from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser
from ucl.physiol.neuroconstruct.gui.plotter import PlotManager
from ucl.physiol.neuroconstruct.project import SimPlot

#################################################

projFile = File("../SolinasComplexSTAGE7cylinder.ncx")
simRefs = ["Sim_2296"]

#################################################

from ucl.physiol.neuroconstruct.project import ProjectManager

print 'Loading project file: ', projFile.getAbsolutePath()

pm = ProjectManager()
project = pm.loadProject(projFile)

print 'Successfully loaded project: ', project.getProjectName()

inputCells = []

for simRef in simRefs:

    simDir = File(projFile.getParentFile(), "/simulations/"+simRef)
    print
    print "--- Reloading data from simulation in directory: %s"%simDir.getCanonicalPath()

    plotFrame = PlotManager.getPlotterFrame("All voltage traces from simulation: "+simRef, False)

    try:
        simData = SimulationData(simDir)
        simData.initialise()

        volt_traces = simData.getCellSegRefs(True)
        for trace in volt_traces:
            #print "Plotting data from: ", trace
            ds = simData.getDataSet(trace, SimPlot.VOLTAGE, False)
            plotFrame.addDataSet(ds)



    except:
        print "Error analysing simulation data from: %s"%simDir.getCanonicalPath()
        print exc_info()

    plotFrame.setVisible(True)






                                        
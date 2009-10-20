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

from javax.vecmath import Point3f;

from ucl.physiol.neuroconstruct.simulation import SimulationData
from ucl.physiol.neuroconstruct.simulation import SpikeAnalyser
from ucl.physiol.neuroconstruct.gui.plotter import PlotManager
from ucl.physiol.neuroconstruct.gui.plotter import PlotCanvas
from ucl.physiol.neuroconstruct.utils import GeneralUtils
from ucl.physiol.neuroconstruct.dataset import DataSet

#################################################

projFile = File("../SolinasComplexSTAGE7cylinder.ncx")

simRefs = ["Sim_2296", "Sim_2299", "Sim_2302", "Sim_2308", "Sim_2315"]
#simRefs = ["Sim_2296"]

threshold = -20  # above which constitutes a spike
slideSize = 20   # for initial synchrony graphs

peakThreshold = 3   # In synchrony, what constitutes a peak

maxRadius = 300

radiusRing = 50

cellGroupName = "CellGroup_1"
inputStimRef = "Input_0"

#################################################

from ucl.physiol.neuroconstruct.project import ProjectManager

print 'Loading project file: ', projFile.getAbsolutePath()

pm = ProjectManager()
project = pm.loadProject(projFile)

print 'Successfully loaded project: ', project.getProjectName()



innerRadius = 0
outerRadius = radiusRing*2

while innerRadius < maxRadius:


    plotFrame = PlotManager.getPlotterFrame("Analysis of synchrony in ring %f -> %f"%(innerRadius,outerRadius), False)
    plotFrame2 = PlotManager.getPlotterFrame("Peak times in ring %f -> %f"%(innerRadius,outerRadius), False)

    peaks_wave = {}


    cellsToUse = []
    centre = None

    for simRef in simRefs:
    
        info = "Peaks of synchrony for sim: "+simRef
    
        peaks_wave[simRef] = DataSet(info, info, "Time", "Peak", "ms", "")
    
        try:
            
            GeneralUtils.timeCheck("Before load sim", True)
    
            simData = pm.reloadSimulation(simRef)
    
            print
            print "--- Reloading data from simulation: %s"%simRef

            if centre is None:
                centre = Point3f(0,0,0)
                numInputs = len(project.generatedElecInputs.getInputLocations(inputStimRef))

                for input in project.generatedElecInputs.getInputLocations(inputStimRef):
                    print input
                    pos = project.generatedCellPositions.getOneCellPosition(cellGroupName, input.getCellNumber())
                    print pos
                    centre.x += pos.x/numInputs
                    centre.y += pos.y/numInputs
                    centre.z += pos.z/numInputs
    
            if len(cellsToUse) == 0:
                for pos in project.generatedCellPositions.getPositionRecords(cellGroupName):
                    #centre = Point3f(0,40,0)
                    dist = pos.getPoint().distance(centre)
                    #print "Cell %i at %s is %f away from centre %s"%(pos.cellNumber, str(pos.getPoint()), dist, str(centre))

                    if dist >= innerRadius and dist < outerRadius:
                        cellsToUse.append(pos.cellNumber)

    
            GeneralUtils.timeCheck("After load sim", True)
            spikeLists = ArrayList()
    
            times = simData.getAllTimes()
    
    
            for cellNum in cellsToUse:
                cellSegRef = SimulationData.getCellRef(cellGroupName, cellNum)
                volts = simData.getVoltageAtAllTimes(cellSegRef)
    
                spikes = SpikeAnalyser.getSpikeTimes(volts,
                                                    times,
                                                    threshold,
                                                    0,
                                                    times[-1])
                spikeLists.add(spikes)
                
    
            ds = SpikeAnalyser.getSlidingSpikeSynchrony(spikeLists,
                                                        times,
                                                        slideSize,
                                                        0,
                                                        times[-1])

            ds.setDescription(str(cellsToUse))
    
            peak_vals = []
            peak_times = []
    
            peak_index = 0
            t_index = 0
            first_peak = -1
            
            while t_index < ds.getNumberPoints():
    
                if(ds.getPoint(t_index)[1] > peakThreshold):
                    #print "Peak at point num: "+str(t_index)
                    if first_peak < 0:
                        first_peak = ds.getPoint(t_index)[0]
    
                    peak_vals.append(0)
                    peak_times.append(0)
                    
                    for cnt2 in xrange(t_index, t_index + 1000):
    
                        if cnt2 < ds.getNumberPoints():
                            if (ds.getPoint(cnt2)[1] > peak_vals[peak_index]):
                                #print "Peak 2 at point num: "+str(cnt2)
    
                                peak_vals[peak_index] = ds.getPoint(cnt2)[1]
    
                                ##### Exact peak times:
                                peak_times[peak_index] = ds.getPoint(cnt2)[0]
    
                                ##### Centred peak times:
                                #peak_times[peak_index] = first_peak + (peak_index*125)
    
        
                    peak_index = peak_index + 1
    
                    t_index = t_index + 2500
                    #print "Jumping to: "+str(t_index)
                    
                t_index = t_index + 1
    
            for i in xrange(len(peak_times)):
    
                peaks_wave[simRef].addPoint(i, peak_vals[i])
    
    
    
            plotFrame.addDataSet(ds)
            plotFrame2.addDataSet(peaks_wave[simRef])
    
    
    
    
        except:
            print "Error analysing simulation data from: %s"%simRef
            print exc_info()
    
    num_peaks = 1e9
    
    for ds in peaks_wave.values():
        if ds.getNumberPoints() < num_peaks:
            num_peaks = ds.getNumberPoints()
    
    
    info = "Averaged peak trace"
    
    avg = DataSet(info, info, "Time", "Peak", "ms", "")
    avg.setGraphFormat(PlotCanvas.USE_THICK_LINES_FOR_PLOT)
    
    for i in xrange(num_peaks):
        tot_val = 0
        for ds in peaks_wave.values():
            tot_val += ds.getPoint(i)[1]
        avg.addPoint(i, tot_val/len(peaks_wave))
    
    plotFrame2.addDataSet(avg)
    
    
    plotFrame.setVisible(True)
    plotFrame2.setVisible(True)

    innerRadius = outerRadius
    outerRadius += radiusRing
    





                                        
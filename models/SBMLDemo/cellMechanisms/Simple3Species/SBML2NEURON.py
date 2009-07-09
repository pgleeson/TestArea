#!/usr/bin/env python

#
#
#   A file which can be used to generate NEURON mod files (and hoc files to test them) 
#   from **SIMPLE** SBML files. The only SBML elements which are currently supported are:
#     listOfCompartments
#     listOfSpecies
#     listOfReactions
#         
# 
#   For usage options type 'python SBML2NEURON.py'
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct & NeuroML projects
#
#   This work has been funded by the Wellcome Trust and the Medical Research Council
#   
#
#


import sys
import os.path
import libsbml
 
def main (args):

  if len(args) != 2 and len(args) != 4:
    print "Usage examples: \n    python SBML2NEURON.py ex.xml \n        (to create a mod file ex.mod from the SBML file)"
    print "\n    python SBML2NEURON.py ex.xml 100 0.01\n        (to create a mod file ex.mod from the SBML file, plus a test hoc file to run the simulation for 100ms, timestep 0.01ms)"
    sys.exit(1)

  infile = args[1]
  modfile = infile[0:infile.rfind('.')]+".mod"
  
  generateModFromSBML(infile, modfile)
  
  
  if len(args) == 4:
  
    compileMod()
  
    hocfile = infile[0:infile.rfind('.')]+"_test.hoc"
    dur = float(args[2])
    dt = float(args[3])
    generateTestHocFromSBML(infile, hocfile, dur, dt)
    
    
def compileMod():

 

  cmdToCompileMod = 'nrnivmodl'               # Assumes command is on PATH for Linux/Mac

  if sys.platform.count('win') >0:
      nrnDir = 'C:/nrn62'                     # NOTE forward slash is preferred by Python
      cmdToCompileMod = "\""+nrnDir+"/bin/rxvt.exe\" -e \""+nrnDir+"/bin/sh\" \""+nrnDir+"/lib/mknrndll.sh\" \""+ nrnDir+"\""
  
  print "Compiling the mod files using: "+ cmdToCompileMod

  import subprocess 
  subprocess.Popen(cmdToCompileMod)

  
  
def generateTestHocFromSBML(sbmlFile, hocfile, dur, dt):
      
  print "Going to read SBML from file: %s and create hoc file: %s" % (sbmlFile, hocfile)
  
  reader  = libsbml.SBMLReader()
  writer  = libsbml.SBMLWriter()
  sbmldoc = reader.readSBML(sbmlFile)
    
  hoc = file(hocfile, mode='w')
  
  hoc.write("load_file(\"nrngui.hoc\")\n\n")
  
  
  hoc.write("print \"Testing mapping of SBML file %s on NEURON\"\n\n"%sbmlFile)
  
  hoc.write("create soma\n")
  hoc.write("access soma\n")
  hoc.write("L = 1\n")
  hoc.write("diam = 1\n\n")
  
  hoc.write("insert pas  \n\n")
  
  modelId = getModelId(sbmldoc.getModel())
  
  hoc.write("insert %s\n\n"%modelId)
  
  hoc.write("psection()\n\n")
  
  
  hoc.write("tstop = %s\n"%dur)
  hoc.write("dt = %s\n"%dt)
  hoc.write("steps_per_ms = %f\n\n"%(1/dt))
  
  hoc.write("objref SampleGraph\n")
  hoc.write("SampleGraph = new Graph(0)\n\n")
  
  hoc.write("minVal = 0\n")
  hoc.write("maxVal = 10\n\n")
  
  hoc.write("{SampleGraph.size(0,tstop,minVal,maxVal)}\n")
  
  hoc.write("{SampleGraph.view(0, minVal, tstop, (maxVal-minVal), 100, 500, 500, 300)}\n")
  
  hoc.write("{\n")
  
  colIndex = 1
  for species in sbmldoc.getModel().getListOfSpecies():
  
    print "Looking at: "+str(species.getId())
    
    hoc.write("    SampleGraph.addexpr(\"soma.%s_%s(0.5)\", %i, 1)\n" % (species.getId(), modelId, colIndex))
    colIndex+=1

  
  hoc.write("    graphList[0].append(SampleGraph)\n")
  hoc.write("}\n\n")
  
  
  hoc.write("print \"Starting simulation!\"\n")
  
  hoc.write("{run()}\n")
  
  hoc.write("print \"Finished simulation!\"\n")
  
  print "Hoc file written to %s" % (hocfile) 


def getModelId(model):

  modelId = model.getId()
  if len(modelId)>=16:
    modelId = modelId[0:16]
    
  return modelId
  
def generateModFromSBML(sbmlFile, modFile):
    
  print "Going to read SBML from file: %s and create mod file: %s" % (sbmlFile, modFile)


  reader  = libsbml.SBMLReader()
  writer  = libsbml.SBMLWriter()
  sbmldoc = reader.readSBML(sbmlFile)
  
  mod = file(modFile, mode='w')
  
  modelId = getModelId(sbmldoc.getModel())
  
  mod.write("TITLE SBML model: %s generated from file: %s\n\n" % (modelId, sbmlFile) )
  
  mod.write("UNITS {\n")
  mod.write("  (mA) = (milliamp)\n")
  mod.write("  (mV) = (millivolt)\n")
  
  mod.write("}\n\n")
  
  
  rangeVariables = ""
  params = ""
  derivs = ""
  
  states = ""
  initial = ""
  stateNames = []
  stateInc = {}
  
  
  for species in sbmldoc.getModel().getListOfSpecies():

    states = "%s  %s\n" % (states, species.getId())
    stateNames.append(species.getId())
    
    initVal = species.getInitialAmount()
    if initVal == 0 and species.getInitialConcentration() >0:
      initVal = species.getInitialConcentration()
    
    initial = "%s  %s = %s\n" % (initial, species.getId(), initVal)
  
  print "States found: %s"%stateNames
  
  for compartment in sbmldoc.getModel().getListOfCompartments():
  
    rangeVariables = "%s  RANGE %s\n" % (rangeVariables, compartment.getId())
    params = "%s  %s = %f\n" % (params, compartment.getId(), compartment.getSize())
    
  
  for state in stateNames:
    stateInc[state] = ""
  
  translatedParams = {}
  infoString = ""
    
  for reaction in sbmldoc.getModel().getListOfReactions():
    rid = reaction.getId()
    print "Looking at reaction %s with formula: (%s)"%(rid, reaction.getKineticLaw().getFormula())
    
    for parameter in reaction.getKineticLaw().getListOfParameters():
      localParamName = "%s_%s" % (rid,parameter.getId())
      translatedParams[parameter.getId()] = localParamName
      rangeVariables = "%s  RANGE %s\n" % (rangeVariables, localParamName)
      params = "%s  %s = %f\n" % (params, localParamName, parameter.getValue())
      
      
    formula = reaction.getKineticLaw().getFormula()

    for parameter in reaction.getKineticLaw().getListOfParameters():
      if translatedParams.has_key(parameter.getId()):
        formula = formula.replace(parameter.getId(), translatedParams[parameter.getId()])
      
    prodString = ""
    reacString = ""
      
    for product in reaction.getListOfProducts():

      stoichiometryFactor = ""
      if product.getStoichiometry() != 1:
        stoichiometryFactor = "%f * "%product.getStoichiometry()
        
      if stateInc[product.getSpecies()] != "":
        stateInc[product.getSpecies()] = stateInc[product.getSpecies()] + " +"

      stateInc[product.getSpecies()] = "%s (%s%s)" % (stateInc[product.getSpecies()], stoichiometryFactor, formula)
      
      if len(prodString) > 0: prodString = prodString +", "
      prodString = prodString+ product.getSpecies()
      
    for reactant in reaction.getListOfReactants():
      stoichiometryFactor = ""
      if reactant.getStoichiometry() != 1:
        stoichiometryFactor = "%f * "%reactant.getStoichiometry()
      
      stateInc[reactant.getSpecies()] = "%s - (%s%s) " % (stateInc[reactant.getSpecies()], stoichiometryFactor, formula)
      
      if len(reacString) > 0: reacString = reacString +", "
      reacString = reacString+ reactant.getSpecies()
      
    
    infoString = infoString +"  :  ("+reacString+") -> ("+ prodString+") with formula : "+ formula+"\n"


  for state in stateNames:  
  
    if stateInc[state] != "":
      derivs = "%s  %s\' = %s \n" % (derivs, state, stateInc[state])
  

  mod.write("NEURON {\n")
  mod.write("  SUFFIX %s\n" % modelId)

  mod.write(rangeVariables)
  mod.write("}\n\n")


  mod.write("PARAMETER {\n")
  mod.write(params)
  mod.write("}\n\n")
  
  
  print "Num species: "+str(sbmldoc.getModel().getListOfSpecies().size())
  
    
  mod.write("STATE {\n")
  mod.write(states)
  mod.write("}\n\n")
  
  mod.write("INITIAL {\n")
  mod.write(initial)
  mod.write("}\n\n")
  

  mod.write("BREAKPOINT {\n")
  mod.write("  SOLVE states METHOD cnexp\n")
  mod.write("}\n\n")
  
  
  mod.write("DERIVATIVE states {\n")
  mod.write(infoString)      
  mod.write(derivs)      
  mod.write("}\n")


  print "Mod file written to %s" % (modFile) 
  


if __name__ == '__main__':
  main(sys.argv)  

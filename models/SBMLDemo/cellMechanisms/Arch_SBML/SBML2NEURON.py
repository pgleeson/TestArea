import os.path
#!/usr/bin/env python

#
#
#   A file which can be used to generate NEURON mod files (and hoc files to test them) 
#   from **SIMPLE** SBML files. The only SBML elements which are currently supported are:
#
#     listOfCompartments
#     listOfSpecies
#     listOfParameters
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
import os
import libsbml

import subprocess


voltageSBOTerm = 'SBO:0000259'   # To indicate a parameter refers to voltage/membrane potential
currentSBOTerm = 'SBO:0000999'   # *DUMMY* SBO term to indicate a parameter refers to transmembrane current

specialSBOTerms = [voltageSBOTerm, currentSBOTerm]

functionDefs = {}

functionDefs["gt"] =  "FUNCTION gt(A, B) {\n    if (A > B) {gt = 1}\n    else {gt = 0}\n}\n\n"
functionDefs["geq"] =  "FUNCTION geq(A, B) {\n    if (A >= B) {geq = 1}\n    else {geq = 0}\n}\n\n"
functionDefs["lt"] =  "FUNCTION lt(A, B) {\n    if (A < B) {lt = 1}\n    else {lt = 0}\n}\n\n"
functionDefs["leq"] =  "FUNCTION leq(A, B) {\n    if (A <= B) {leq = 1}\n    else {leq = 0}\n}\n\n"
functionDefs["power"] = "FUNCTION power(A, B) {\n    power\n}\n\n"
#TODO: more functions to add from here: http://sbml.org/Software/libSBML/docs/python-api/libsbml-python-math.html


class Species:

    def __init__(self, realName, index):
        self.realName = realName
        self.index = index
        self.increase = "" # Hoe the state variable will change

    def getRealName(self):
        return self.realName

    def getLocalName(self):
        localName = self.realName

        if self.realName[0]=='_':
            localName = "U%s"%self.realName
        return localName

    def getShortName(self):
        return "SP_%i"%self.index

    def setStateIncrease(self, inc):
        self.increase = inc

    def getStateIncrease(self):
        return self.increase

    def __str__(self):
        return self.getRealName()


class Parameter:

    def __init__(self, realName, value, index):
        self.realName = realName
        self.localName = realName
        self.value = value
        self.scope = 'GLOBAL'
        self.sboTerm = ''
        self.index = index
        self.hasRateRule = False

    def isGlobalScope(self):
        return self.scope == 'GLOBAL'


    def getRealName(self):
        return self.realName

    def getLocalName(self):
        return self.localName

    def setLocalName(self, localName):
        self.localName = localName

    def getSBOTerm(self):
        return self.sboTerm

    def setSBOTerm(self, sboTerm):
        self.sboTerm = sboTerm

    def getScope(self):
        return self.scope

    def setScope(self, scope):
        self.scope = scope

    def getShortName(self):
        return "p%s"%hex(self.index)[2:]

    def getValue(self):
        return self.value

    def getHasRateRule(self):
        return self.hasRateRule

    def setHasRateRule(self, rr):
        self.hasRateRule = rr

    def __str__(self):
        return self.getRealName()




def main (args):

  testMode = False
  if "-test" in args:
      testMode = True
      args.remove("-test")


  if len(args) != 2 and len(args) != 4 and len(args) != 6:
    print "Usage examples: \n    python SBML2NEURON.py ex.xml \n        (to create a mod file ex.mod from the SBML file)"
    print "\n    python SBML2NEURON.py ex.xml 100 0.01\n        (to create a mod file ex.mod from the SBML file, plus a test hoc file to run the simulation for 100ms, timestep 0.01ms)"
    print "\n    python SBML2NEURON.py ex.xml 100 0.01 -1 12\n        (to files as above, with y axis from -1 to 12)"
    sys.exit(1)

  infile = args[1]
  modfile = infile[0:infile.rfind('.')]+".mod"
  
  generateModFromSBML(infile, modfile)
  
  
  if len(args) == 4 or len(args) == 6:
  
    rv = compileMod(modfile)

    if rv != 0:
        raise Exception('Problem compiling the mod file: %s'%modfile)
        return

  
    hocfile = infile[0:infile.rfind('.')]+"_test.hoc"
    dur = float(args[2])
    dt = float(args[3])
    ymin = 0
    ymax = 10
    if len(args) == 6:
        ymin = float(args[4])
        ymax = float(args[5])
        
    generateTestHocFromSBML(infile, hocfile, dur, dt, ymin, ymax, testMode)




    
def compileMod(infile):

  modToCompile = os.path.realpath(infile)
  dirToCompile = os.path.split(modToCompile)[0]
  cmdToCompileMod = 'nrnivmodl'              # Assumes command is on PATH for Linux/Mac

  if sys.platform.count('win') >0:
      nrnDir = 'C:/nrn62'                     # NOTE forward slash is preferred by Python
      cmdToCompileMod = "\""+nrnDir+"/bin/rxvt.exe\" -e \""+nrnDir+"/bin/sh\" \""+nrnDir+"/lib/mknrndll.sh\" \""+ nrnDir+"\" "
  
  print "Compiling the mod files using: ("+ cmdToCompileMod +") in dir: ("+ dirToCompile+")"

  process = None
  if sys.platform.count('win') >0:
    process = subprocess.Popen(cmdToCompileMod, cwd=dirToCompile)
  else:
    process = subprocess.Popen(cmdToCompileMod, cwd=dirToCompile, shell=True)

  rv = process.wait()
  print "Compilation has finished with return val: %s"%rv
  return rv
      

  
  
def generateTestHocFromSBML(sbmlFile, hocfile, dur, dt, ymin, ymax, testMode):
      
  print "Going to read SBML from file: %s and create hoc file: %s" % (sbmlFile, hocfile)
  
  reader  = libsbml.SBMLReader()
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
  
  hoc.write("minVal = %s\n"%ymin)
  hoc.write("maxVal = %s\n\n"%ymax)
  
  hoc.write("{SampleGraph.size(0,tstop,minVal,maxVal)}\n")
  
  hoc.write("{SampleGraph.view(0, minVal, tstop, (maxVal-minVal), 100, 500, 500, 300)}\n")
  
  hoc.write("{\n")
  
  colIndex = 1

  for species in sbmldoc.getModel().getListOfSpecies():
  
    print "Looking at: "+str(species.getId())

    speciesName = species.getId()

    if speciesName[0] == '_':
        speciesName = 'U'+speciesName
    
    hoc.write("    SampleGraph.addexpr(\"soma.%s_%s(0.5)\", %i, 1)\n" % (speciesName, modelId, colIndex))
    colIndex+=1


  for param in sbmldoc.getModel().getListOfParameters():

    if not param.getConstant():
        print "Looking at: "+str(param.getId())

        paramName = param.getId()

        hoc.write("    SampleGraph.addexpr(\"soma.%s_%s(0.5)\", %i, 1)\n" % (paramName, modelId, colIndex))
        colIndex+=1

  
  hoc.write("    graphList[0].append(SampleGraph)\n")
  hoc.write("}\n\n")
  
  
  hoc.write("print \"Starting simulation!\"\n")
  
  hoc.write("{run()}\n")
  
  hoc.write("print \"Finished simulation!\"\n")

  print "Hoc file written to %s\n" % (hocfile)

  if testMode:

      hoc.write("\nobjref testResultFile\n")
      hoc.write("{testResultFile = new File()}\n")
      hoc.write("{testResultFile.wopen(\"%s.finished\")}\n" % (os.path.basename(hocfile) ))
      #{testResultFile.printf("numPassed=%g\n", numTestsPassed)}

      hoc.write("{testResultFile.close()}\n")


def getModelId(model):

  modelId = model.getId()
  if len(modelId)>=28:
    modelId = modelId[0:28]
    
  return modelId


# This assumes the formulas are generated with spaces, brackets or commas around the values
def replaceInFormula(formula, oldTerm, newTerm):

    if formula.startswith(oldTerm):
        formula = newTerm + formula[len(oldTerm):]

    if formula.endswith(oldTerm):
        formula = formula[:-1*len(oldTerm)]+newTerm

    formula = formula.replace(" "+oldTerm+" ", " "+newTerm+" ")
    formula = formula.replace(" "+oldTerm+")", " "+newTerm+")")
    formula = formula.replace(","+oldTerm+")", ","+newTerm+")")
    formula = formula.replace("("+oldTerm+" ", "("+newTerm+" ")
    formula = formula.replace("("+oldTerm+",", "("+newTerm+",")
    formula = formula.replace(" "+oldTerm+",", " "+newTerm+",")
    return formula

  
def generateModFromSBML(sbmlFile, modFile):
    
  print "Going to read SBML from file: %s and create mod file: %s" % (sbmlFile, modFile)


  reader  = libsbml.SBMLReader()
  sbmldoc = reader.readSBML(sbmlFile)
  
  mod = file(modFile, mode='w')
  
  modelId = getModelId(sbmldoc.getModel())
  
  mod.write("TITLE SBML model: %s generated from file: %s\n\n" % (modelId, sbmlFile) )
  
  mod.write("UNITS {\n")
  mod.write("  (mA) = (milliamp)\n")
  mod.write("  (mV) = (millivolt)\n")
  
  mod.write("}\n\n")
  
  derivs = ""
  initial = ""

  substituteSpeciesNames = False

  speciesInfo = []  # List of Species objects
  parameterInfo = []  # List of Parameter objects

  for species in sbmldoc.getModel().getListOfSpecies():

    s = Species(species.getId(), len(speciesInfo))
    speciesInfo.append(s)
    
    initVal = species.getInitialAmount()
    if initVal == 0 and species.getInitialConcentration() >0:
      initVal = species.getInitialConcentration()
    
    initial = "%s  %s = %s\n" % (initial, s.getLocalName(), initVal)


  if len(speciesInfo)>=5:
      print "There are %i species. Using shortened names in DERIVATIVE statement"%len(speciesInfo)
      substituteSpeciesNames = True

  
  print "States/species found: "+ str(speciesInfo)
  
  for compartment in sbmldoc.getModel().getListOfCompartments():

    p = Parameter(compartment.getId(), compartment.getSize(), len(parameterInfo))
    parameterInfo.append(p)


  for parameter in sbmldoc.getModel().getListOfParameters():

    p = Parameter(parameter.getId(), parameter.getValue(), len(parameterInfo))
    p.setSBOTerm(parameter.getSBOTermID())

    if parameter.getSBOTermID() in specialSBOTerms:
        print "SBOTerm of %s (%s) is special..." % (parameter.getId(), parameter.getSBOTermID() )
        if parameter.getSBOTermID() == voltageSBOTerm:
            p.setLocalName('v')
            
    parameterInfo.append(p)

  for rule in sbmldoc.getModel().getListOfRules():

    if rule.getType() == libsbml.RULE_TYPE_RATE:
        for p in parameterInfo:
            if p.getRealName() == rule.getVariable():
                p.setHasRateRule(True)


  '''
  # Reordering by longest name first so that parameter par1 doesn't get substituted for par10, etc.
  sortedParamNames = []
  for param in parameterInfo:
      sortedParamNames.append(param.getRealName())

  sortedParamNames.sort(key=len, reverse=True)
  print sortedParamNames
  sortedParams = []
  for paramName in sortedParamNames:
    for param in parameterInfo:
        if param.getRealName()==paramName:
            sortedParams.append(param)
  parameterInfo = sortedParams

  for param in parameterInfo: print param
  '''



  infoString = ""

  extraFunctions = ""

  for rule in sbmldoc.getModel().getListOfRules():
    print "Looking at rule: %s of type: %s"%(rule, rule.getType())

    if rule.getType() == libsbml.RULE_TYPE_RATE:
        print "Rate rule: d(%s)/dt = %s"%(rule.getVariable(), rule.getFormula())

        derivs = "%s  %s' = %s\n"%(derivs, rule.getVariable(), rule.getFormula())


    
  for reaction in sbmldoc.getModel().getListOfReactions():
    rid = reaction.getId()
    
    formula = reaction.getKineticLaw().getFormula()
    origFormula = str(formula)
    
    print "Looking at reaction %s with formula: (%s)"%(rid, reaction.getKineticLaw().getFormula())
    
    for parameter in reaction.getKineticLaw().getListOfParameters():
      localParamName = "%s_%s" % (rid,parameter.getId())

      p = Parameter(parameter.getId(), parameter.getValue(), len(parameterInfo))
      p.setLocalName(localParamName)
      p.setScope(rid)
      parameterInfo.append(p)


    for param in parameterInfo:

      if substituteSpeciesNames:
        if param.getRealName() in formula:
            print "Substituting %s for %s in:  %s"%(param.getRealName(), param.getShortName(), formula)
            formula = replaceInFormula(formula, param.getRealName(), param.getShortName())

      else:
        if param.isGlobalScope() or param.getScope()==rid:
            formula = replaceInFormula(formula, param.getRealName(), param.getLocalName())


    for species in speciesInfo:
        formula = replaceInFormula(formula, species.getRealName(), species.getLocalName())

    '''if substituteSpeciesNames:
        for species in speciesInfo:
            formula = replaceInFormula(formula, species.getRealName(), species.getShortName())'''

    if substituteSpeciesNames:
        formula = formula.replace(" * ", "*")
        formula = formula.replace(" + ", "+")
      
    prodString = ""
    reacString = ""
      
    for product in reaction.getListOfProducts():

      stoichiometryFactor = ""
      if product.getStoichiometry() != 1:
        stoichiometryFactor = "%f * "%product.getStoichiometry()

      prodSpecies = None
      for species in speciesInfo:
        if species.getRealName() == product.getSpecies():
            prodSpecies = species 
        
      if prodSpecies.getStateIncrease() != "":
        prodSpecies.setStateIncrease(prodSpecies.getStateIncrease() + " +")

      prodSpecies.setStateIncrease("%s (%s%s)" % (prodSpecies.getStateIncrease(), stoichiometryFactor, formula))

      
      if len(prodString) > 0: prodString = prodString +", "
      prodString = prodString+ product.getSpecies()
      
    for reactant in reaction.getListOfReactants():
      stoichiometryFactor = ""
      if reactant.getStoichiometry() != 1:
        stoichiometryFactor = "%f * "%reactant.getStoichiometry()

      reactantSpecies = None
      for species in speciesInfo:
        if species.getRealName() == reactant.getSpecies():
            reactantSpecies = species

      reactantSpecies.setStateIncrease("%s - (%s%s)" % (reactantSpecies.getStateIncrease(), stoichiometryFactor, formula))
      
      if len(reacString) > 0: reacString = reacString +", "
      reacString = reacString+ reactant.getSpecies()
      
    
    infoString = "%s  : Reaction %s (%s) -> (%s) with formula : %s (ORIGINALLY: %s)\n" % (infoString, rid, reacString, prodString, formula, origFormula)


  for species in speciesInfo:
  
    if species.getStateIncrease() != "":
      derivs = "%s  %s\' = %s \n" % (derivs, species.getLocalName(), species.getStateIncrease())

  assigned = ''

  mod.write("NEURON {\n")
  mod.write("  SUFFIX %s\n" % modelId)

  for param in parameterInfo:
    if param.getSBOTerm() != voltageSBOTerm and param.getSBOTerm() != currentSBOTerm and not param.getHasRateRule():
        mod.write("  RANGE %s\n" % param.getLocalName())
    if param.getSBOTerm() == currentSBOTerm:
        mod.write("  NONSPECIFIC_CURRENT %s\n" % param.getLocalName())
        #assigned = "%s\n  %s (nanoamp)\n"%(assigned, param.getLocalName())
    
  mod.write("}\n\n")

  
  mod.write("PARAMETER {\n")
  
  
  for param in parameterInfo:
    if not param.getHasRateRule():
      if param.getSBOTerm() == voltageSBOTerm:
        mod.write("  v (mV)\n")
      elif param.getSBOTerm() == currentSBOTerm:
        assigned = "%s  %s (nanoamp)\n"%(assigned, param.getLocalName())
      else:
        mod.write("  %s = %s\n"%(param.getLocalName(), param.getValue()))

  
  mod.write("}\n\n")
  
  if len(assigned) > 0:
    mod.write("ASSIGNED {\n")
    mod.write(assigned)
    mod.write("}\n\n")
  
  
  print "Num species: "+str(sbmldoc.getModel().getListOfSpecies().size())
  
    
  mod.write("STATE {\n")
  for species in speciesInfo:
    mod.write("  %s\n"%species.getLocalName())
  for param in parameterInfo:
    if param.getHasRateRule():
        mod.write("  %s\n"%param.getLocalName())
  mod.write("}\n\n")
  
  mod.write("INITIAL {\n")
  mod.write(initial)

  #for param in parameterInfo:
  #  mod.write("  %s = %s\n"%(param.getLocalName(), param.getValue()))


  for param in parameterInfo:
    if param.getHasRateRule():
        mod.write("  %s = %s\n"%(param.getLocalName(), param.getValue()))

  mod.write("}\n\n")
  

  mod.write("BREAKPOINT {\n")
  mod.write("  SOLVE states METHOD derivimplicit\n")

  mod.write("  ? Need to check order in which assignments/event assignments should be updated!!!\n")

  for rule in sbmldoc.getModel().getListOfRules():

    if rule.getType() == libsbml.RULE_TYPE_SCALAR:
        ruleString = "%s = %s"%(rule.getVariable(), rule.getFormula())
        mod.write("\n  ? Assignment rule here: %s\n"%ruleString)
        mod.write("  %s\n"%ruleString)

  for event in sbmldoc.getModel().getListOfEvents():

    trigger = libsbml.formulaToString((event.getTrigger().getMath()))
    trigger = replaceInFormula(trigger, "time", "t")
    print "Adding info on event with trigger: %s"%(trigger)

    mod.write("  if (%s) {\n" % trigger)

    for ea in event.getListOfEventAssignments():
        print "Event assi: %s = %s"%(ea.getVariable(), libsbml.formulaToString(ea.getMath()))
        var = ea.getVariable()

        if var == "time":
            var = "t"

        formula = libsbml.formulaToString(ea.getMath())
        formula = replaceInFormula(formula, "time", "t")
        formula = replaceInFormula(formula, "pow", "power")

        for function in functionDefs.keys():
            if function in formula or function in trigger:
                replaceWith = functionDefs[function]
                if not replaceWith in extraFunctions:
                    extraFunctions = extraFunctions+replaceWith

        mod.write("    %s = %s\n"%(var, libsbml.formulaToString(ea.getMath())))


    mod.write("  }\n\n")



  mod.write("}\n\n")
  
  
  mod.write("DERIVATIVE states {\n")

  if substituteSpeciesNames:

      mod.write("  LOCAL dummy ")
      '''for speciesInd in range(0, len(speciesInfo)):
        if speciesInd>0:  mod.write(",")
        mod.write("%s"%speciesInfo[speciesInd].getShortName())'''
        
      for param in parameterInfo:
        mod.write(",%s"%param.getShortName())
      mod.write("\n")


      '''for species in speciesInfo:
        mod.write("  %s = %s\n"%(species.getShortName(), species.getLocalName()))
      mod.write("\n")'''

      for param in parameterInfo:
        mod.write("  %s = %s\n"%(param.getShortName(), param.getLocalName()))
      mod.write("\n")


  mod.write(infoString)
  mod.write(derivs)
  mod.write("}\n\n")


  mod.write(extraFunctions)


  print "Mod file written to %s" % (modFile)


'''
  formula = "(a+b) * (c-d)"
  ast    = libsbml.parseFormula(formula)


  print libsbml.formulaToString(ast)

def convertASTNode(astNode):

    if astNode is not None:
        print "Converting : %s"%astNode
        print "To : %s"%libsbml.formulaToString(astNode)
        
        print "Curr node: %s, %s, children: %i" %(astNode.getName(), astNode.getType(), astNode.getNumChildren())
        if astNode.getNumChildren() == 2:
            convertASTNode(astNode.getChild(0))
            convertASTNode(astNode.getChild(1))
'''

if __name__ == '__main__':
    main(sys.argv)



#
#
#  A simple example of loading a neuroConstruct project using the Jython scripting interface
#
#  To use type 'run.bat -python test.py' or './run.sh -python test.py'.
#  
#  Get in contact directly with PG for more info and the latest status...
#
#


import os

from java.io import *

from ucl.physiol.neuroconstruct.cell.examples import *
from ucl.physiol.neuroconstruct.cell.utils import *
from ucl.physiol.neuroconstruct.project import *


file = File("examples/Ex1-Simple/Ex1-Simple.neuro.xml")

print 'Loading project file: ', file

pm = ProjectManager()

myProject = pm.loadProject(file)

print pm.status()

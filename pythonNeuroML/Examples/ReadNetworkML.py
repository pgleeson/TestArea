#
#   A simple example of reading in and printing the contents of a NetworkML file
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council
#
#

 
import sys
import os
import math
import xml
import xml.sax

import logging
 
sys.path.append("../NeuroMLUtils")

from NetworkHandler import NetworkHandler
from NetworkMLSaxHandler import NetworkMLSaxHandler

file_name = 'small.nml'
#file_name = 'Pre1.7.1.nml'

logging.basicConfig(level=logging.DEBUG, format="%(name)-19s %(levelname)-5s - %(message)s")


print("Going to read contents of a NetworkML file: "+str(file_name))


parser = xml.sax.make_parser()   # A parser for any XML file

nmlHandler = NetworkHandler()	# The base NetworkHandler class just prints out details of the network

curHandler = NetworkMLSaxHandler(nmlHandler) # The SAX handler knows of the structure of NetworkML and calls appropriate functions in NetworkHandler

curHandler.setNodeId(-1) 	# Flags to handle cell info for all nodes, as opposed to only cells with a single nodeId >=0

parser.setContentHandler(curHandler) # Tells the parser to invoke the NetworkMLSaxHandler when elements, characters etc. parsed

parser.parse(open(file_name)) # The parser opens the file and ultimately the appropriate functions in NetworkHandler get called








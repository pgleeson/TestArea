COMMENT

   **************************************************
   File automatically generated by: neuroConstruct 
   **************************************************

   This file holds the implementation in NEURON of the Cell Process:
   LeakConductance (Type: Channel mechanism, Model: Template based ChannelML file)

   with parameters: 
   /channelml/@xsi:schemaLocation = http://morphml.org/channelml/schema     ../../Schemata/v1.1/Level2/ChannelML_v1.1.xsd 
   /channelml/@units = Physiological Units 
   /channelml/notes/. = null 
   /channelml/ion/@name = non_specific 
   /channelml/ion/@charge = 1 
   /channelml/ion/@default_erev = -54.3 
   /channelml/channel_type/@name = LeakConductance 
   /channelml/channel_type/@density = yes 
   /channelml/channel_type/notes/. = null 
   /channelml/channel_type/notes/. = null 
   /channelml/channel_type/current_voltage_relation/ohmic/@ion = non_specific 
   /channelml/channel_type/current_voltage_relation/ohmic/conductance/@default_gmax = 0.3 

ENDCOMMENT


?  This is a NEURON mod file generated from a v1.1 ChannelML file

?  Unit system of ChannelML file: Physiological Units


COMMENT
    ChannelML file containing a single Channel description
ENDCOMMENT

TITLE Channel: LeakConductance

COMMENT
    Simple example of a leak/passive conductance. Note: for GENESIS cells with a single leak conductance,
        it is better to use the Rm and Em variables for a passive current
ENDCOMMENT


UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}


    
NEURON {
    SUFFIX LeakConductance
    ? A non specific current is present
    RANGE e
    NONSPECIFIC_CURRENT i
    
    RANGE gmax, gion
    
}

PARAMETER { 
    gmax = 0.0003 (S/cm2) 
    
    e = -54.3 (mV)
    
}



ASSIGNED {
    v (mV)
        
    i (mA/cm2)
        
}

BREAKPOINT {
    
    i = gmax*(v - e) 
        
}
    

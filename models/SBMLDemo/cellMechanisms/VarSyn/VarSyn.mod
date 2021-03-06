COMMENT

   **************************************************
   File generated by: neuroConstruct v1.3.4 
   **************************************************

   This file holds the implementation in NEURON of the Cell Mechanism:
   DoubExpSyn (Type: Synaptic mechanism, Model: Template based ChannelML file)

   with parameters: 
   /channelml/@units = Physiological Units 
   /channelml/notes = ChannelML file describing a synaptic mechanism 
   /channelml/synapse_type/@name = DoubExpSyn 
   /channelml/synapse_type/status/@value = stable 
   /channelml/synapse_type/notes = Simple example of a synaptic mechanism, which consists of a postsynaptic conductance which changes as          double exponential function of time 
   /channelml/synapse_type/authorList/modelTranslator/name = Padraig Gleeson 
   /channelml/synapse_type/authorList/modelTranslator/institution = UCL 
   /channelml/synapse_type/authorList/modelTranslator/email = p.gleeson - at - ucl.ac.uk 
   /channelml/synapse_type/neuronDBref/modelName = Receptor properties 
   /channelml/synapse_type/neuronDBref/uri = http://senselab.med.yale.edu/senselab/NeuronDB/receptors2.asp 
   /channelml/synapse_type/doub_exp_syn/@max_conductance = 1.0E-5 
   /channelml/synapse_type/doub_exp_syn/@rise_time = 1 
   /channelml/synapse_type/doub_exp_syn/@decay_time = 2 
   /channelml/synapse_type/doub_exp_syn/@reversal_potential = 0 

// File from which this was generated: C:\neuroConstruct\nCexamples\Ex5_Networks\cellMechanisms\DoubExpSyn\DoubExpSyn.xml

// XSL file with mapping to simulator: C:\neuroConstruct\nCexamples\Ex5_Networks\cellMechanisms\DoubExpSyn\ChannelML_v1.8.0_NEURONmod.xsl

ENDCOMMENT


?  This is a NEURON mod file generated from a ChannelML file

?  Unit system of original ChannelML file: Physiological Units

COMMENT
    ChannelML file describing a synaptic mechanism
ENDCOMMENT

? Creating synaptic mechanism, based on NEURON source impl of Exp2Syn
    

TITLE Channel: DoubExpSyn

COMMENT
    Simple example of a synaptic mechanism, which consists of a postsynaptic conductance which changes as 
        double exponential function of time
ENDCOMMENT


UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

    
NEURON {
    POINT_PROCESS %Name%
    RANGE tau_rise, tau_decay 
    GLOBAL total
    
    
    POINTER g_scaling    


    RANGE i, e, gmax
    NONSPECIFIC_CURRENT i
    RANGE g, factor

}

PARAMETER {
    gmax = 0.001
    tau_rise = 3 (ms) <1e-9,1e9>
    tau_decay = 13 (ms) <1e-9,1e9>
    e = 0  (mV)
    
    g_scaling = 1 (1)

}


ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor 
    total (uS)

}

STATE {
    A (uS)
    B (uS)
}

INITIAL {
    LOCAL tp
    total = 0
    
    if (tau_rise == 0) {
        tau_rise = 1e-9  : will effectively give a single exponential timecourse synapse
    }
    
    if (tau_rise/tau_decay > .999999) {
        tau_rise = .999999*tau_decay : will result in an "alpha" synapse waveform
    }
    A = 0
    B = 0
    tp = (tau_rise*tau_decay)/(tau_decay - tau_rise) * log(tau_decay/tau_rise)
    factor = -exp(-tp/tau_rise) + exp(-tp/tau_decay)
    factor = 1/factor
}

BREAKPOINT {
    SOLVE state METHOD cnexp
    g = g_scaling * gmax * (B - A)
    i = g*(v - e)
    
    
}


DERIVATIVE state {
    A' = -A/tau_rise
    B' = -B/tau_decay 
}

NET_RECEIVE(weight (uS)) {
    
    state_discontinuity(A, A + weight*factor
)
    state_discontinuity(B, B + weight*factor
)

    
    
}


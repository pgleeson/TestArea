 
NEURON {
      

    SUFFIX tonic
     
    NONSPECIFIC_CURRENT i
    
    RANGE i
    GLOBAL gtonic,etonic
    
}


UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (pS) = (picosiemens)
    (um) = (micrometer)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (l) = (liter)
}


PARAMETER { 

    gtonic = 5 (pS/um2)
    
    etonic = -60 (mV)
    
}


ASSIGNED {
      

    v (mV)
        
    i (mA/cm2)
        
}


BREAKPOINT { 
    i = (1e-4)*gtonic*(v - etonic) 
        

}



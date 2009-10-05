




UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
    (um) = (micrometer)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (l) = (liter)
}


    
NEURON {
      

    SUFFIX %Name%
              
        
    RANGE a, b, scale
    RANGE val
    
}

PARAMETER { 
      

    a = 2 (1) 
    b = 1 (1) 
    scale = 10 (1) 
    
}



ASSIGNED {
      

    v (mV)

    val (1)
    
    
    
}

BREAKPOINT { 
                        
 

    val = a+b*(t/scale)
            

}



INITIAL {
    
    val = 0
    
}
    




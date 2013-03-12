




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
              
    
    USEION IP3 WRITE IP3i VALENCE 0    
        
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
    
    IP3i (1)
    
    
    
}

BREAKPOINT { 
                        
 
    if(t>5 && t<10) {
    
        IP3i = a*2+b*(t/scale)
    }
    else {
        IP3i = a+b*(t/scale)
    }
            

}



INITIAL {
    
    IP3i = a
    
}
    




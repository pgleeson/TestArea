COMMENT

   Test file to help simulate diffusion

ENDCOMMENT

TITLE Diffusive substance dependent conductance
 


UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S) = (siemens)
} 

NEURON {
	SUFFIX SubstanceSource
	NONSPECIFIC_CURRENT i
	RANGE gmax, e, start, stop, strength, x,y,z
}

PARAMETER {
	gmax = 3.0E-6	(S/cm2)	<0,1e9>
	e = -20.0	(mV)
    start = 20
    stop = 50
    maxstrength = 1
    minstrength = 0.05
    x = 0
    y = 0
    z = 0
}

ASSIGNED {
    v (mV)  
    i (mA/cm2)
    strength
}

BREAKPOINT {

    if (t>start && t<stop) {    
        strength = maxstrength
    } else {
        strength = minstrength
    }

        i = gmax * strength *(v - e) 
}

COMMENT

   Test file to help simulate diffusion

ENDCOMMENT

TITLE Diffusive substance dependent synapse
 

UNITS {
	(mV) = (millivolt)
	(mA) = (milliamp)
	(S) = (siemens)
} 


NEURON {
    POINT_PROCESS PFPCSyn
    NONSPECIFIC_CURRENT i

    RANGE tau1, tau2 
    GLOBAL total

    RANGE i, e, gmax
    NONSPECIFIC_CURRENT i
    RANGE g, x,y,z, source_x, source_y, source_z

    POINTER emitting_NO

    RANGE local_conc_NO, releasing

    RANGE scaling

    GLOBAL time_last_emission
    GLOBAL time_last_fire

	GLOBAL diffusion_const
}


PARAMETER {

    gmax = 0.0001  : Small gmax, not enough to make cell fire...	

    tau1 = 1 (ms) <1e-9,1e9>
    tau2 = 2 (ms) <1e-9,1e9>
    e = 0  (mV)

    x = 0       : these will be set by neuroConstruct per synapse if RequiresXYZ = 1 in the internal props
    y = 0
    z = 0

    source_x = 100   : these are set by extra hoc code under tab NEURON
    source_y = 100 
    source_z = 100

    time_last_emission = -1  : time when there was last an emission of NO at source

    time_last_fire = -1      : time syn last fired

    releasing = 0            : whether THIS cell is releasing NO & how much

    scaling = 1              : scaling for g

    local_conc_NO = 0        : local concentration

    emitting_NO = 0          : whether source is emitting NO

    prev_emitted_NO = 0      : last recorded amount of NO emitted by source

	diffusion_const = 100    : Typical value: 3.3e-5 cm^2/s or 3.3 um^2/ms

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
    if (tau1/tau2 > .9999) {
        tau1 = .9999*tau2
    }
    A = 0
    B = 0

    tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
    factor = -exp(-tp/tau1) + exp(-tp/tau2)
    factor = 1/factor

}


BREAKPOINT {
    LOCAL distance, tdiff, expDecay, halfMaxResp

    SOLVE state METHOD cnexp

    distance = sqrt((x-source_x)^2 + (y-source_y)^2 + (z-source_z)^2)


	: This will cause the synapse to release if a) the postsynaptic cell is firing 
	: and b) the synapse has fired in the past 25 ms

    if (v>0 && (t-time_last_fire)<25 && releasing == 0) {  
      releasing = 10  : amount released, arbitrary value, to illustrate effect
    } else {
      releasing = 0.0
    }



    if (time_last_emission > 0) {

            tdiff = t - time_last_emission

			if (tdiff>0) {
				expDecay = exp(- (distance*distance)/(4 * diffusion_const * tdiff))/ ((4 * 3.14159265 * diffusion_const * tdiff)^1.5)
			} else {
				if (distance == 0) {
					expDecay = 1
				} else {
					expDecay = 0
				}
			}
       
            local_conc_NO  = prev_emitted_NO * expDecay      
    }


    if (emitting_NO >= 1) {
            time_last_emission = t
			prev_emitted_NO	= emitting_NO
    }

	halfMaxResp = 1e-6  : typical conc of is NO 1e-5 mM

	
    if (local_conc_NO == 0) {
		scaling = 1
	} else {
    	scaling  = 1 - (local_conc_NO/ (local_conc_NO + halfMaxResp))
	}

    g = gmax * scaling * (B - A)
    
    i = g*(v - e)


}


DERIVATIVE state {
    A' = -A/tau1
    B' = -B/tau2 
}


NET_RECEIVE(weight (uS)) {
    state_discontinuity(A, A + weight*factor)
    state_discontinuity(B, B + weight*factor)
    total = total+weight


    time_last_fire = t

}

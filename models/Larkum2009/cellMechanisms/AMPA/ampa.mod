COMMENT
//****************************//
// Created by Alon Polsky 	//
//    apmega@yahoo.com		//
//		2007			//
//****************************//
ENDCOMMENT

TITLE NMDA synapse with depression

NEURON {
	POINT_PROCESS %Name%
	
	NONSPECIFIC_CURRENT i
	RANGE e ,gmax,ntar,local_v,i
	RANGE g
	
	GLOBAL tau_ampa
}

UNITS {
	(nA) 	= (nanoamp)
	(mV)	= (millivolt)
	(nS) 	= (nanomho)
	(mM)    = (milli/liter)
        F	= 96480 (coul)
        R       = 8.314 (volt-coul/degC)

}

PARAMETER {
	gmax=1	(nS)
	e= 0.0	(mV)
	tau_ampa=2	(ms)	

	dt (ms)
	v		(mV)

}

ASSIGNED { 
	i		(nA)  
	local_v	(mV):local voltage
}
STATE {
	g

}

INITIAL {
      g=0 

}    

BREAKPOINT {  

	SOLVE state METHOD cnexp
	
	:this loop was used only to generate the spike train
	:state_discontinuity operations are moved to the NET_RECEIVE block
	:FROM count=0 TO Nspike-1 {
	:	IF(at_time(count*Tspike+del)){
	:		state_discontinuity( g, g+ gmax)
	:	}
	:}

	i= (1e-3)*g* (v- e)
	local_v=v
}

DERIVATIVE state {
	g'=-g/tau_ampa
}



NET_RECEIVE(weight (uS), tsyn (ms)) {

   state_discontinuity(g, g+ gmax)
   
   tsyn = t

}
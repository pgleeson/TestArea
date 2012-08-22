

TITLE GABAAslow synapse

NEURON {
	POINT_PROCESS GABAAslow  	
	NONSPECIFIC_CURRENT i  :can have two components lumped together

	RANGE e ,gmax,local_v,g, i	
	
	GLOBAL taudecay,taurise

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
	gmax=0.5	(nS)
	e= -60.00	(mV)
	taudecay=40 (ms)	
	taurise=3	(ms) 
	dt (ms)
	v		(mV)
	g


}

ASSIGNED { 
        i		(nA)	
	local_v	(mV):local voltage
	
	
}
STATE {
	A (nS)
	B (nS)
	

}

INITIAL {

	A=0
	B=0
	

}    

BREAKPOINT {  
    
	:LOCAL gnmda, inmda
	SOLVE state METHOD cnexp	
	
	:this loop was used only to generate the spike train
	:state_discontinuity operations are moved to the NET_RECEIVE block
	:FROM count=0 TO Nspike-1 {
	:	IF(at_time(count*Tspike+del)){
	:		state_discontinuity( A, A+ gmax)
	:		state_discontinuity( B, B+ gmax)
	:		state_discontinuity( gampa, gampa+ gmax/ntar)
	:	}
	:}
	
	
	g=(A-B)	
	i= (1e-3)*g* (v- e)
	local_v=v
}

DERIVATIVE state {	
	A'=-A/taudecay
	B'=-B/taurise	

}


NET_RECEIVE(weight (uS), tsyn (ms)) {

   state_discontinuity( A, A+ gmax)
   state_discontinuity( B, B+ gmax)
   
   tsyn = t

}






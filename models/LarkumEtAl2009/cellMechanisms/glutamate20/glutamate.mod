COMMENT
//****************************//
// Created by Alon Polsky 	//
//    apmega@yahoo.com		//
//		2007			//
//****************************//
ENDCOMMENT

TITLE NMDA synapse with depression

NEURON {
	POINT_PROCESS %Name%  :glutamate :
	USEION ca READ cai WRITE ica VALENCE 2		
	NONSPECIFIC_CURRENT i  :the two components are lumped together

	RANGE e ,gmax,ntar,local_v, i	
	RANGE g, gnmda, inmda, ica
	
	GLOBAL n, gama,tau1,tau2,tau_ampa,tauh,cah

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
	gmax=20	(nS)
	e= 0.0	(mV)
	tau1=70 (ms)
	tau2=3	(ms) 
	tau_ampa=1	(ms)	
	n=0.3 (/mM)	
	gama=0.08 	(/mV) 
	dt (ms)
	ntar= 1	:NMDA to AMPA ratio
	v		(mV)
	cah   = 8	(/ms)		: max act rate  
	tauh   = 1000	(/ms)		: max deact rate 
	gnmda
	inmda


}

ASSIGNED { 
        i		(nA)	
	local_v	(mV):local voltage
	
	ica 		(mA/cm2)
	cai		(mM)
	gh		(nS)
	
}
STATE {
	g
	A (nS)
	B (nS)
	h		(nS)
	

}

INITIAL {

	g=0
	A=0
	B=0
	h=0
	

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
	
	
	gnmda=(A-B)/(1+n*exp(-gama*v) )	
	gh=(exp(-h))
	inmda =(1e-3)* gnmda * gh * (v-e)
	ica=inmda/10
	i= (1e-3)*g* (v- e) + inmda
	local_v=v
}

DERIVATIVE state {	
	g' = -g/tau_ampa
	A'=-A/tau1
	B'=-B/tau2	
	h'=(cah*cai-h)/tauh

}


NET_RECEIVE(weight (uS), tsyn (ms)) {

   state_discontinuity( A, A+ gmax)
   state_discontinuity( B, B+ gmax)
   state_discontinuity( g, g + gmax/ntar)
   
   tsyn = t

}






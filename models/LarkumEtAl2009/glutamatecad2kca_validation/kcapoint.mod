
COMMENT

kcapoint.mod

Calcium-dependent potassium channel
Based on
Pennefather (1990) -- sympathetic ganglion cells
taken from
Reuveni et al (1993) -- neocortical cells

Author: Zach Mainen, Salk Institute, 1995, zach@salk.edu
	
ENDCOMMENT

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	POINT_PROCESS kcapoint

	NONSPECIFIC_CURRENT ikca
	USEION ca READ cai
	USEION k READ ek
	RANGE n, gk, ikca
	RANGE ninf, ntau
	GLOBAL Ra, Rb, caix, gbar
	GLOBAL q10, temp, tadj, vmin, vmax
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(pS) = (picosiemens)
	(um) = (micron)
} 

PARAMETER {
	gbar = 30.0 	(pS)	: 0.03 mho/cm2
	v 		(mV)
	cai  		(mM)
	caix = 4	
									
	Ra   = 0.05	(/ms)		: max act rate  
	Rb   = 0.1	(/ms)		: max deact rate 

	dt		(ms)
	celsius		(degC)
	temp = 23	(degC)		: original temp 	
	q10  = 2.3			: temperature sensitivity

	vmin = -120	(mV)
	vmax = 100	(mV)
} 


ASSIGNED {
	a		(/ms)
	b		(/ms)
	ikca 		(nA)
	gk		(pS)
	ek		(mV)
	ninf
	ntau 		(ms)	
	tadj
}
 

STATE { n }

INITIAL { 
	rates(cai)
	n = ninf
}

BREAKPOINT {
        SOLVE states
	gk = tadj*gbar*n
	ikca = (1e-6) * gk * (v - ek)
} 

LOCAL nexp

PROCEDURE states() {   :Computes state variable n 
        rates(cai)      :             at the current v and dt.
        n = n + nexp*(ninf-n)

        VERBATIM
        return 0;
        ENDVERBATIM
}

PROCEDURE rates(cai(mM)) {  

        LOCAL tinc

        a = Ra * cai^caix
        b = Rb
        ntau = 1/(a+b)
	ninf = a*ntau

        tadj = q10^((celsius - temp)/10)

        tinc = -dt * tadj
        nexp = 1 - exp(tinc/ntau)
}












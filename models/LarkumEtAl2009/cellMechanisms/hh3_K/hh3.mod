TITLE HH channel
: Mel-modified Hodgkin - Huxley conductances (after Ojvind et al.)
: accounting for K component only 

VERBATIM
static const char rcsid[]="$Id: hh3.mod,v 1.1 1996/05/19 19:26:28 karchie Exp $";
ENDVERBATIM

NEURON {
	SUFFIX %Name%
	USEION k READ ek WRITE ik
	RANGE gmax,vshift
	GLOBAL taun,nN
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

PARAMETER {
	v (mV)
	celsius = 37	(degC):34
	dt (ms)
	gmax = %Max Conductance Density% (mho/cm2)
	ek = -80 (mV):-77
	taun=1.5 : 1
	nN=3
	vshift=0
}

STATE {
	n 
}

ASSIGNED {
	ik (mA/cm2)
}

BREAKPOINT {
	SOLVE states
	
	ik = gmax*(v - ek)*n^nN
}

PROCEDURE states() {	: exact when v held constant
	n = n + (1 - exp(-dt/taun))*(1 / (1 + exp((v + 40+vshift)/(-3)))  - n)
	VERBATIM
	return 0;
	ENDVERBATIM
}


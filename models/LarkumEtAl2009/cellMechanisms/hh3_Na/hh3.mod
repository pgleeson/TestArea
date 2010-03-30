TITLE HH channel
: Mel-modified Hodgkin - Huxley conductances (after Ojvind et al.)
: accounting for Na component only 

VERBATIM
static const char rcsid[]="$Id: hh3.mod,v 1.1 1996/05/19 19:26:28 karchie Exp $";
ENDVERBATIM

NEURON {
	SUFFIX %Name%
	USEION na READ ena WRITE ina
	RANGE gmax, vshift
	GLOBAL taus,taum,tauh,tausb
	GLOBAL tausv,tausd,mN,sN
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
	gmax = %Max Conductance Density%  (mho/cm2)
	ena = 40 (mV):50
	taum=0.05
	tauh=0.6 :0.5
	taus=50
	tausv=30
	tausd=1
	mN=3
	sN= 0 :1
	tausb=0.5
	vshift=0
}
STATE {
	m h s
}
ASSIGNED {
	ina (mA/cm2)
}

BREAKPOINT {
	SOLVE states

	ina = gmax*h*s^sN*(v - ena)*m^mN
}

PROCEDURE states() {	: exact when v held constant
	LOCAL sigmas
	sigmas=1/(1+exp((v+tausv+vshift)/tausd))
	m = m + (1 - exp(-dt/taum))*(1 / (1 + exp((v + 40+vshift)/(-3)))  - m)
	h = h + (1 - exp(-dt/tauh))*(1 / (1 + exp((v + 45+vshift)/3))  - h)
	s = s + (1 - exp(-dt/(taus*sigmas+tausb)))*(1 / (1 + exp((v + 44+vshift)/3))  - s)
	VERBATIM
	return 0;
	ENDVERBATIM
}


TITLE Calcium dependent potassium channel
: KCa channel with parameters from US Bhalla and JM Bower,
: J. Neurophysiol. 69:1948-1983 (1993)
: Andrew Davison, The Babraham Institute, 1998.

: See notes below on rate expressions for voltage dependent and conc dep parts of Y
: Padraig Gleeson 2010

NEURON {
	SUFFIX %Name%
	USEION k READ ek WRITE ik
	USEION ca READ cai
	RANGE gmax, ik, Yconcdep, Yvdep
	GLOBAL Yalpha, Ybeta
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(molar) = (1/liter)
	(mM) = (millimolar)
}

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

PARAMETER {
	v (mV)
	dt (ms)
	gmax= %Max Conductance Density% (mho/cm2) <0,1e9>
	ek = -80 (mV)
	Ybeta = 0.05 (/ms)
	cai (mM) := 1e-5 (mM)
}


STATE {
	Y
}

ASSIGNED {
	ik (mA/cm2)
	Yalpha   (/ms)
	Yvdep    
	Yconcdep (/ms)
}

INITIAL {
	rate(v,cai)
	Y = Yalpha/(Yalpha + Ybeta)
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	ik = gmax*Y*(v - ek)
}

DERIVATIVE state {
	rate(v,cai)
	Y' = Yalpha*(1-Y) - Ybeta*Y
}

PROCEDURE rate(v(mV),cai(mM)) {
	vdep(v)
	concdep(cai)
	Yalpha = Yvdep*Yconcdep
}

PROCEDURE vdep(v(mV)) {
	TABLE Yvdep FROM -100 TO 100 WITH 100
    ? Yvdep = exp((v*1(/mV)+70)/27)  ? this is at odds with eqns 11 in Appendix C of Bhalla & Bower 1993
    Yvdep = exp((v*1(/mV)-65)/27)
}

PROCEDURE concdep(cai(mM)) {
	TABLE Yconcdep FROM 0 TO 0.1 WITH 10000  ?  PG changed this to 10000 steps and 0.1 for testing at larger concs
    ? if statement below removed so that chennel could be tested with concs beyond 0.01
	?if (cai < 0.01) {
		Yconcdep = 500(/ms)*( 0.015-cai*1(/mM) )/( exp((0.015-cai*1(/mM))/0.0013) -1 )
	?} else {
	?	Yconcdep = 500(/ms)*0.005/( exp(0.005/0.0013) -1 )
	?}
}

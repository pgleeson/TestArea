

TITLE Calcium Clamp

COMMENT
        Calcium "Clamp": not really physiological
ENDCOMMENT

NEURON {
        SUFFIX %Name%
        USEION ca READ ica WRITE cai
        RANGE del, dur, level1, level2, targetLevel
}

UNITS {
        (mV)    = (millivolt)
        (mA)    = (milliamp)
	(um)    = (micron)
	(molar) = (1/liter)
        (mM)    = (millimolar)
}

PARAMETER {
        ica             (mA/cm2)
        del = 20           (ms)
        dur = 20           (ms)
        level1 = 5e-5     (mM)
        level2 = 5e-4     (mM)
}

ASSIGNED {
	ca_pump_i	(mA)
	targetLevel	(mM)
}
STATE {
	cai (mM)
}

INITIAL {
        cai = level1
}

BREAKPOINT {
        if (t > del && t<= (del+dur)) {
            targetLevel = level2
        }
        else {
            targetLevel = level1
        }
        SOLVE conc METHOD derivimplicit
}

DERIVATIVE conc {

	cai' =  6e-2 * (targetLevel - cai)
}



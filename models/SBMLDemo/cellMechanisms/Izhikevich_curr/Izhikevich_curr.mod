TITLE SBML model: Izhikevich_curr generated from file: C:\neuroConstruct\models\SBMLDemo\cellMechanisms\Izhikevich_curr\Izhikevich_curr.xml

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}

NEURON {
  SUFFIX Izhikevich_curr
  RANGE cell
  RANGE a
  RANGE b
  RANGE c
  RANGE d
  RANGE Vthresh
}

PARAMETER {
  cell = 1.0
  a = 0.02
  b = 0.2
  c = -65.0
  d = 8.0
  Vthresh = 30.0
  v (mV)
}

STATE {
  i_mech
  U
}

INITIAL {
  i_mech = 0.0
  U = -14.0
}

BREAKPOINT {
  SOLVE states METHOD derivimplicit
  ? Need to check order in which assignments/event assignments should be updated!!!
  if (gt(v, Vthresh)) {
    v = c
    U = U + d
  }

}

DERIVATIVE states {
  i_mech' = 0.04 * v * v + 5 * v + 140 - U
  U' = a * (b * v - U)
}

FUNCTION gt(A, B) {
    if (A > B) {gt = 1}
    else {gt = 0}
}


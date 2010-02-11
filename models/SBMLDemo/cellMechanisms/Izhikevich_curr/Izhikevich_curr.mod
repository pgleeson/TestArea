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
  RANGE v
}

PARAMETER {
  cell = 1.0
  a = 0.02
  b = 0.2
  c = -65.0
  d = 8.0
  Vthresh = 30.0
  v = -70.0
}

STATE {
  i
  U
}

INITIAL {
  i = 0.0
  U = -14.0
}

BREAKPOINT {
  SOLVE states METHOD derivimplicit
  if (gt(v, Vthresh)) {
    v = c
    U = U + d
  }

}

DERIVATIVE states {
  i' = 0.04 * pow(v, 2) + 5 * i + 140 - U + i
  U' = a * (b * v - U)
}

FUNCTION gt(A, B) {
    if (A > B) {gt = 1}
    else {gt = 0}
}


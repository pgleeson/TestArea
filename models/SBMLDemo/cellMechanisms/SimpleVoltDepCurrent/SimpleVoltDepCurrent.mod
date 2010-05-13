TITLE SBML model: SimpleVoltDepCurrent generated from file: C:\neuroConstruct\models\SBMLDemo\cellMechanisms\SimpleVoltDepCurrent\SimpleVoltDepCurrent.xml

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}

NEURON {
  SUFFIX SimpleVoltDepCurrent
  RANGE cell
  RANGE a
  RANGE b
  RANGE erev
  NONSPECIFIC_CURRENT i
}

PARAMETER {
  cell = 1.0
  a = 2e-008
  b = 3e-008
  erev = -30.0
  v (mV)
}

ASSIGNED {
  i (nanoamp)
}

STATE {
  g
}

INITIAL {
  g = 0.0
}

BREAKPOINT {
  SOLVE states METHOD derivimplicit
  ? Need to check order in which assignments/event assignments should be updated!!!

  ? Assignment rule here: i = g * (v - erev)
  i = g * (v - erev)
}

DERIVATIVE states {
  g' = v * a
}


TITLE SBML model: KChan_SBML generated from file: C:\neuroConstruct\models\SBMLDemo\cellMechanisms\KChan_SBML\KChan_SBML.xml

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}

NEURON {
  SUFFIX KChan_SBML
  RANGE cell
  RANGE erev
  RANGE alpha_n
  RANGE beta_n
  RANGE gmax
  NONSPECIFIC_CURRENT i
}

PARAMETER {
  cell = 1.0
  erev = -77.0
  v (mV)
  alpha_n = 0.0
  beta_n = 0.0
  gmax = 0.036
}

ASSIGNED {
  i (nanoamp)
}

STATE {
  n
}

INITIAL {
  n = 0.0
}

BREAKPOINT {
  SOLVE states METHOD derivimplicit
  ? Need to check order in which assignments/event assignments should be updated!!!

  ? Assignment rule here: i = gmax * pow(n, 4) * (v - erev)
  i = gmax * pow(n, 4) * (v - erev)

  ? Assignment rule here: beta_n = 0.125 * exp((v - -65) / -80)
  beta_n = 0.125 * exp((v - -65) / -80)

  ? Assignment rule here: alpha_n = 0.01 * (v - -55) / (1 - exp((v - -55) / -10))
  alpha_n = 0.01 * (v - -55) / (1 - exp((v - -55) / -10))
}

DERIVATIVE states {
  n' = alpha_n * (1 - n) - beta_n * n
}


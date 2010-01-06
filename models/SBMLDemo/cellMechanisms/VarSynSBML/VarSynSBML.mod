TITLE SBML model: VarSynSBML generated from file: C:\neuroConstruct\models\SBMLDemo\cellMechanisms\VarSynSBML\VarSynSBML.xml

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}

NEURON {
  SUFFIX VarSynSBML
  RANGE default
  RANGE re1_k1
}

PARAMETER {
  default = 1.000000
  re1_k1 = -0.000100
}

ASSIGNED {
    v (mV)
}

STATE {
  s1
  s2
}

INITIAL {
  s1 = 1.0
  s2 = 0.0
}

BREAKPOINT {
  SOLVE states METHOD cnexp
}

DERIVATIVE states {
  :  (s1) -> (s2) with formula : s1 * re1_k1 * v (ORIGINALLY: s1 * k1 * VOLTAGE)
  s1' =  - (s1 * re1_k1 * v)  
  s2' =  (s1 * re1_k1 * v) 
}

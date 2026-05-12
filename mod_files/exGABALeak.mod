COMMENT
Low extrasynaptic GABA receptor activation implemented as a 
non-specific passive leak current
MPJ, Yale, 2017
ENDCOMMENT

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
    (um) = (micrometer)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (l) = (liter)
}

NEURON {
    SUFFIX exGABALeak
    RANGE Erev
    NONSPECIFIC_CURRENT i
    RANGE gbar, gion
}

PARAMETER { 
    gbar = 0.0003 (S/cm2)  : default value, should be overwritten when conductance placed on cell
    Erev = -70 (mV)        : default value, should be overwritten when conductance placed on cell
}

ASSIGNED {
    v (mV)
    i (mA/cm2)
}

BREAKPOINT { 
    i = gbar*(v - Erev) 
}


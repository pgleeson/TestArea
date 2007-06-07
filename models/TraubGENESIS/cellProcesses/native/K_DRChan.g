/*
** This file is copied from the traub91 example inclused with the standard GENESIS distribution
**
** The 1991 Traub set of voltage and concentration dependent channels
** Implemented as tabchannels by : Dave Beeman
**      R.D.Traub, R. K. S. Wong, R. Miles, and H. Michelson
**	Journal of Neurophysiology, Vol. 66, p. 635 (1991)
*/

// CONSTANTS

float EREST_ACT = -0.060 /* hippocampal cell resting potl */
float ENA = 0.115 + EREST_ACT // 0.055
float EK = -0.015 + EREST_ACT // -0.075
float ECA = 0.140 + EREST_ACT // 0.080
float SOMA_A = 3.320e-9       // soma area in square meters


//========================================================================
//                Tabchannel K(DR) Hippocampal cell channel
//========================================================================

function make_%Name%

        str chanpath = "/library/%Name%"
	if ({exists {chanpath}})
	    return
	end

        create  tabchannel      {chanpath}
                setfield        ^       \
                Ek              {EK}	\	           //      V
                Gbar            %Max Conductance Density%     \      //      S
                Ik              0       \                  //      A
                Gk              0       \                  //      S
                Xpower  1       \
                Ypower  0       \
                Zpower  0

        setupalpha {chanpath} X                          \
                   {16e3 * (0.0351 + EREST_ACT)}   \  // AA
                   -16e3                           \  // AB
                   -1.0                            \  // AC
                   {-1.0 * (0.0351 + EREST_ACT) }  \  // AD
                   -0.005                          \  // AF
                   250                             \  // BA
                   0.0                             \  // BB
                   0.0                             \  // BC
                   {-1.0 * (0.02 + EREST_ACT)}     \  // BD
                   0.04                               // BF
end


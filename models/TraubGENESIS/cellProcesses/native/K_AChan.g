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
//                Tabchannel K(A) Hippocampal cell channel
//========================================================================

function make_%Name%

        str chanpath = "/library/%Name%"
	if ({exists {chanpath}})
	    return
	end
        create  tabchannel      {chanpath}
                setfield        ^       \
                Ek              {EK}    \	          //      V
                Gbar            %Max Conductance Density%     \     //      S
                Ik              0       \                 //      A
                Gk              0       \                 //      S
                Xpower  1       \
                Ypower  1       \
                Zpower  0

        setupalpha {chanpath} X {20e3 * (0.0131 + EREST_ACT)}  \
                 -20e3 -1.0 {-1.0 * (0.0131 + EREST_ACT) } -0.01    \
                 {-17.5e3 * (0.0401 + EREST_ACT) }  \
                 17.5e3 -1.0 {-1.0 * (0.0401 + EREST_ACT) } 0.01 

        setupalpha {chanpath} Y 1.6 0.0 0.0  \
                {0.013 - EREST_ACT} 0.018  \
                50.0 0.0 1.0 {-1.0 * (0.0101 + EREST_ACT) } -0.005 
end

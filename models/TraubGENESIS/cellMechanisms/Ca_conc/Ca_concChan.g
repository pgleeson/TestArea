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
//                      Ca conc
//========================================================================

function make_%Name%

        str chanpath = "/library/%Name%"
	if ({exists {chanpath}})
	    return
	end
	
        create Ca_concen {chanpath}
	
        setfield {chanpath} \
                tau     0.01333   \      // sec
                B       17.402e12 \      // Curr to conc for soma
                Ca_base 0.0
		
        addfield {chanpath} addmsg1
        setfield {chanpath} \
                addmsg1        "../Ca . I_Ca Ik"
end

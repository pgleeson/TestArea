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
//             Tabulated Ca-dependent K AHP Channel
//========================================================================


function make_%Name%

        str chanpath = "/library/%Name%"
	if ({exists {chanpath}})
	    return
	end

        create  tabchannel      {chanpath}
                setfield        ^       \
                Ek              {EK}   \               //      V
                Gbar            %Max Conductance Density%     \    //      S
                Ik              0       \              //      A
                Gk              0       \              //      S
                Xpower  0       \
                Ypower  0       \
                Zpower  1

// Allocate space in the Z gate A and B tables, covering a concentration
// range from xmin = 0 to xmax = 1000, with 50 divisions
        float   xmin = 0.0
        float   xmax = 1000.0
        int     xdivs = 50

        call {chanpath} TABCREATE Z {xdivs} {xmin} {xmax}
        int i
        float x,dx,y
        dx = (xmax - xmin)/xdivs
        x = xmin
        for (i = 0 ; i <= {xdivs} ; i = i + 1)
            if (x < 500.0)
                y = 0.02*x
            else
                y = 10.0
            end
            setfield {chanpath} Z_A->table[{i}] {y}
            setfield {chanpath} Z_B->table[{i}] {y + 1.0}
            x = x + dx
        end
// For speed during execution, set the calculation mode to "no interpolation"
// and use TABFILL to expand the table to 3000 entries.
        setfield {chanpath} Z_A->calc_mode 0   Z_B->calc_mode 0
        call {chanpath} TABFILL Z 3000 0
	
// Use an added field to tell the cell reader to set up the
// CONCEN message from the Ca_concen element
        addfield {chanpath} addmsg1
	
        setfield {chanpath} \
                addmsg1        "../Ca_conc . CONCEN Ca"
end


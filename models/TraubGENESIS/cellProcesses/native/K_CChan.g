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
//  Ca-dependent K Channel - K(C) - (vdep_channel with table and tabgate)
//========================================================================


function make_%Name%

        str chanpath = "/library/%Name%"
	if ({exists {chanpath}})
	    return
	end

        create  tabchannel    {chanpath}
                setfield        ^       \
                Ek              {EK}    \                       //      V
                Gbar            %Max Conductance Density%       \       //      S
                Ik              0       \                       //      A
                Gk              0                               //      S

// Now make a X-table for the voltage-dependent activation parameter.
        float   xmin = -0.1
        float   xmax = 0.05
        int     xdivs = 49
        call {chanpath} TABCREATE X {xdivs} {xmin} {xmax}
        int i
        float x,dx,alpha,beta
        dx = (xmax - xmin)/xdivs
        x = xmin
        for (i = 0 ; i <= {xdivs} ; i = i + 1)
            if (x < EREST_ACT + 0.05)
                alpha = {exp {53.872*(x - EREST_ACT) - 0.66835}}/0.018975
		beta = 2000*{exp {(EREST_ACT + 0.0065 - x)/0.027}} - alpha
            else
		alpha = 2000*{exp {(EREST_ACT + 0.0065 - x)/0.027}}
		beta = 0.0
            end
            setfield {chanpath} X_A->table[{i}] {alpha}
            setfield {chanpath} X_B->table[{i}] {alpha+beta}
            x = x + dx
        end
// Expand the tables to 3000 entries to use without interpolation
	setfield {chanpath} X_A->calc_mode 0 X_B->calc_mode 0
	setfield {chanpath} Xpower 1
	call {chanpath} TABFILL X 3000 0

// Create a table for the function of concentration, allowing a
// concentration range of 0 to 1000, with 50 divisions.  This is done
// using the Z gate, which can receive a CONCEN message.  By using
// the "instant" flag, the A and B tables are evaluated as lookup tables,
//  rather than being used in a differential equation.

        float   xmin = 0.0
        float   xmax = 1000.0
        int     xdivs = 50

        call {chanpath} TABCREATE Z {xdivs} {xmin} {xmax}
        int i
        float x,dx,y
        dx = (xmax - xmin)/xdivs
        x = xmin
        for (i = 0 ; i <= {xdivs} ; i = i + 1)
            if (x < 250.0)
                y = x/250.0
            else
                y = 1.0
            end
	    /* activation will be computed as Z_A/Z_B */
            setfield {chanpath} Z_A->table[{i}] {y}
            setfield {chanpath} Z_B->table[{i}] 1.0
            x = x + dx
        end

	setfield {chanpath} Z_A->calc_mode 0 Z_B->calc_mode 0
	setfield {chanpath} Zpower 1
// Make it an instantaneous gate (no time constant)
	setfield {chanpath} instant {INSTANTZ}
// Expand the table to 3000 entries to use without interpolation. 
	call {chanpath} TABFILL Z 3000 0

// Now we need to provide for messages that link to external elements.
// The message that sends the Ca concentration to the Z gate tables is stored
// in an added field of the channel, so that it may be found by the cell
// reader.
        addfield {chanpath} addmsg1
        setfield {chanpath} addmsg1  "../Ca_conc  . CONCEN Ca" 
end



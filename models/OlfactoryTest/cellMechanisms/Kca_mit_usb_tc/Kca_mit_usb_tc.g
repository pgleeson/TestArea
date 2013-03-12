// genesis

/* Channels used in:
'Exploring parameter space in detailed single neuron models:
simulations of the mitral and granule cells of the olfactory bulb'
Upinder S. Bhalla and James M. Bower
Journal of Neurophysiology Vol 69 No. 6, June 1993 pp 1948-1965
*/

//========================================================================
// Alternate version of Kca_mit_usb which uses simple tabchannels
// instead of the vdep_channels.
//========================================================================

function make_%Name%
	int i
	int xdivs = 3000
	float EK = -0.08
	float EREST_ACT = -0.065
	str chanpath
	chanpath = "/library/%Name%"

	if (!({exists {chanpath}}))
	create tabchannel {chanpath}
		setfield {chanpath}	\
		Ek 		{EK}	\			//	V
		Gbar 		%Max Conductance Density%  \	//	S
		Ik 		0	\			//	A
		Gk		0	\			//	S
		Xpower 1 \
		Ypower 0 \
		Zpower 1 \
		instant {INSTANTX}

	
	int XDIVS = 3000
	float XMIN = -0.1
	float XMAX = 0.05
	call {chanpath} TABCREATE X {XDIVS} {XMIN} {XMAX}
	end
		float x = {XMIN}
		float dx = {XMAX - XMIN} / {XDIVS}
		float y
		for (i = 0 ; i <= {XDIVS} ; i = i + 1)
			y = {exp {(x - {EREST_ACT})/0.027}}
			setfield {chanpath} X_A->table[{i}] {y}
            setfield {chanpath} X_B->table[{i}] {y + 1.0}
			x = x + dx
		end
	
		setupalpha {chanpath} Z \
			{5.0e5*0.015} -5.0e5 -1.0 -0.015 -0.0013 \
			50 0 0 1 1 \
			-size 1000 -range 0.0 0.01
			xdivs = 1000
    		for (i = 0 ; i <= {xdivs} ; i = i + 1)
         		setfield {chanpath} Z_B->table[{i}] 50.0
    		end
		
    addfield {chanpath} addmsg1
    setfield {chanpath} addmsg1  "../Ca_mit_conc  . CONCEN Ca" 
end

// genesis

/* Channels used in:
'Exploring parameter space in detailed single neuron models:
simulations of the mitral and granule cells of the olfactory bulb'
Upinder S. Bhalla and James M. Bower
Journal of Neurophysiology Vol 69 No. 6, June 1993 pp 1948-1965
*/



//========================================================================
//			Ca conc - mitral cell
//========================================================================

function make_%Name%
	str chanpath
	chanpath = "/library/%Name%"

	echo "Making prototype Ca_concen:" {chanpath}

	if (!({exists {chanpath}}))
//		return
//	end
	create Ca_concen {chanpath}
	setfield {chanpath} \
		tau		0.01	\			// sec
		B		5.2e-6	\	// Curr to conc
		Ca_base		0.00001
        addfield  {chanpath} addmsg1
	setfield  {chanpath}  \
	    addmsg1 "../LCa3_mit_usb	.		I_Ca	Ik"

	end
end

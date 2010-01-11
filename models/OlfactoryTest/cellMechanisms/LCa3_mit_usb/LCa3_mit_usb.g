// genesis

/* Channels used in:
'Exploring parameter space in detailed single neuron models:
simulations of the mitral and granule cells of the olfactory bulb'
Upinder S. Bhalla and James M. Bower
Journal of Neurophysiology Vol 69 No. 6, June 1993 pp 1948-1965
*/

/* FILE INFORMATION
** Some Ca channels for the purkinje cell
** L Channel data from :
**	T. Hirano and S. Hagiwara Pflugers A 413(5) pp463-469, 1989
*/


//========================================================================
//                        Adjusted LCa channel
//========================================================================

float ECa = 0.07

function make_%Name%
	str chanpath
	chanpath = "/library/%Name%"

	echo "Making prototype channel:" {chanpath}
	if (!({exists {chanpath}}))
//		return
//	end

// float ECa = 0.07	// (I-current)

    	create  tabchannel {chanpath}
    		setfield {chanpath}	\ 
		Ek 		{ECa}	\ 
		Gbar		%Max Conductance Density%	\  
		Ik 		0	\ 
		Gk 		0  	\
        	Xpower 1 \
		Ypower 1 \
		Zpower 0

	end

	setupalpha {chanpath} X 7500.0 0.0 1.0 -0.013 -0.007 1650.0 \
	     0.0 1.0 -0.014 0.004

	setupalpha {chanpath} Y 6.8 0.0 1.0 0.030 0.012 60.0 0.0  \
	    1.0 0.0 -0.011
end


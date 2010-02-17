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
        create vdep_channel {chanpath}
        //  V
        //  S
        //  A
        //  S
    
        setfield ^ Ek {EK} gbar %Max Conductance Density% Ik 0 Gk 0
    
        create table {chanpath}/qv
        call {chanpath}/qv TABCREATE 100 -0.1 0.1
        create tabgate {chanpath}/qca
    end 
    
    int i
    float x, dx, y
    x = -0.1
    dx = 0.2/100.0
    for (i = 0; i <= 100; i = i + 1)
        y = {exp {(x - {EREST_ACT})/0.027}}
        setfield {chanpath}/qv table->table[{i}] {y}
        x = x + dx
    end


    setupgate {chanpath}/qca alpha  {5.0e5*0.015}  \
        -5.0e5 -1.0 -0.015.0 -0.0013 -size 1000 -range 0.0 0.01

    call {chanpath}/qca TABCREATE beta 1 -1 100
    setfield {chanpath}/qca beta->table[0] 50
    setfield {chanpath}/qca beta->table[1] 50

    addmsg {chanpath}/qv {chanpath}/qca PRD_ALPHA output
    addmsg {chanpath}/qca {chanpath} MULTGATE m 1
    
    // NOTE from PG: changing sendmsg1 to addmsg1
    
    addfield {chanpath} addmsg1
    addfield {chanpath} addmsg2
    
    setfield  {chanpath}  addmsg1 "../Ca_mit_conc        qca     VOLTAGE     Ca" 
    setfield  {chanpath}  addmsg2 "..                    qv      INPUT       Vm"
        

end

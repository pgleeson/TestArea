

function makechannel_%Name%(compartmentA, compartmentB)
        

        str compartmentA
        str compartmentB

        float conductance 
        conductance = 3
    
        addmsg {compartmentA} {compartmentB} RAXIAL {1/conductance} Vm
        addmsg {compartmentB} {compartmentA} RAXIAL {1/conductance} Vm 

end


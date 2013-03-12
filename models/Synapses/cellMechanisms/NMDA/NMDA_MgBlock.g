
float E_NMDA = 0.0
/////////////////float G_NMDA =  1.873087796e-10
float G_NMDA =  1e-6


float Q10_synapse =   3.0

//[Mg] in mM
float CMg = 1.2
// per mM
float eta = 0.2801

float gamma = 62
float offset = - 0.01
echo eta = {eta}
eta = eta * {exp {- gamma * offset}}
// per V

function makechannel_%Name%(compartment, name)

    str compartment   
    str name
    
	if (!({exists {compartment}/{name}}))
    
		create synchan {compartment}/{name}
        
        setfield {compartment}/{name} \
                    Ek {E_NMDA} \
                    tau2 {3e-3  / Q10_synapse} \
                    tau1 {40e-3 / Q10_synapse} \
                    gmax {G_NMDA}
                    
        //addmsg   {compartment}/{name}   {compartment} CHANNEL Gk Ek
        addmsg   {compartment}   {compartment}/{name} VOLTAGE Vm 
	end


                                  
    if (! {exists {compartment}/{name}/Mg_BLOCK})
    
        create Mg_block {compartment}/{name}/Mg_BLOCK
            
        setfield {compartment}/{name}/Mg_BLOCK \
                    CMg {CMg}  \
                    KMg_A {1/eta} \ 
                    KMg_B {1.0/gamma}
    
	    addmsg  {compartment}/{name}             {compartment}/{name}/Mg_BLOCK   CHANNEL    Gk Ek
        addmsg  {compartment}/{name}/Mg_BLOCK    {compartment}                   CHANNEL    Gk Ek
	    addmsg  {compartment}                    {compartment}/{name}/Mg_BLOCK   VOLTAGE    Vm
    end


    
end

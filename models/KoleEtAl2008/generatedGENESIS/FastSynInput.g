

// **************************************************
// File generated by: neuroConstruct v1.1.4 
// **************************************************

// This file holds the implementation in GENESIS of the Cell Mechanism:
// FastSynInput (Type: Synaptic mechanism, Model: Template based ChannelML file)

// with parameters: 
// /channelml/@units = Physiological Units 
// /channelml/notes = ChannelML file describing a single synaptic mechanism 
// /channelml/synapse_type/@name = FastSynInput 
// /channelml/synapse_type/status/@value = stable 
// /channelml/synapse_type/status/contributor/name = Padraig Gleeson 
// /channelml/synapse_type/notes = Simple example of a synaptic mechanism, which consists of a postsynaptic conductance which changes as          double exponential function of time. Mappings exist for NEURON and GENESIS. 
// /channelml/synapse_type/neuronDBref/modelName = Receptor properties 
// /channelml/synapse_type/neuronDBref/uri = http://senselab.med.yale.edu/senselab/NeuronDB/receptors2.asp 
// /channelml/synapse_type/doub_exp_syn/@max_conductance = 1.0E-4 
// /channelml/synapse_type/doub_exp_syn/@rise_time = .24 
// /channelml/synapse_type/doub_exp_syn/@decay_time = .26 
// /channelml/synapse_type/doub_exp_syn/@reversal_potential = 40 

// File from which this was generated: C:\neuroConstruct\models\KoleEtAl2008\cellMechanisms\FastSynInput\DoubExpSyn.xml

// XSL file with mapping to simulator: C:\neuroConstruct\models\KoleEtAl2008\cellMechanisms\FastSynInput\ChannelML_v1.7.1_GENESIStab.xsl



// This is a GENESIS script file generated from a ChannelML v1.7.1 file
// The ChannelML file is mapped onto a tabchannel object


// Units of ChannelML file: Physiological Units, units of GENESIS file generated: SI Units

/*
    ChannelML file describing a single synaptic mechanism
*/


function makechannel_FastSynInput(compartment, name)
        
        /*
            Simple example of a synaptic mechanism, which consists of a postsynaptic conductance which changes as 
        double exponential function of time. Mappings exist for NEURON and GENESIS.
        */
        
        str compartment
        str name

        if (!({exists {compartment}/{name}}))

            create      synchan               {compartment}/{name}

            setfield    ^ \
                    Ek                      0.04 \
                    tau1                    0.00026000000000000003 \
                    tau2                    0.00023999999999999998 \
                    gmax                    0.00000010000000000000001

            float tau1 = {getfield {compartment}/{name} tau1}
            if (tau1 == 0)
                setfield {compartment}/{name} tau1 1e-9  
            end
            
            addmsg   {compartment}/{name}   {compartment} CHANNEL Gk Ek
            addmsg   {compartment}   {compartment}/{name} VOLTAGE Vm


        end

end


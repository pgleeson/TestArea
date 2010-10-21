

// **************************************************
// File generated by: neuroConstruct v1.4.1 
// **************************************************

// This file holds the implementation in GENESIS of the Cell Mechanism:
// NaF (Type: Channel mechanism, Model: ChannelML based process)

// with parameters: 
// /channelml/@units = SI Units 
// /channelml/notes = .... 
// /channelml/channel_type/@name = NaF 
// /channelml/channel_type/@density = yes 
// /channelml/channel_type/status/@value = in_progress 
// /channelml/channel_type/notes = .... 
// /channelml/channel_type/authorList/modelTranslator/name = Padraig Gleeson 
// /channelml/channel_type/authorList/modelTranslator/institution = UCL 
// /channelml/channel_type/authorList/modelTranslator/email = p.gleeson - at - ucl.ac.uk 
// /channelml/channel_type/neuronDBref/modelName = Na channels 
// /channelml/channel_type/neuronDBref/uri = http://senselab.med.yale.edu/senselab/NeuronDB/channelGene2.htm#table2 
// /channelml/channel_type/current_voltage_relation/@cond_law = ohmic 
// /channelml/channel_type/current_voltage_relation/@ion = na 
// /channelml/channel_type/current_voltage_relation/@default_erev = 0.050 
// /channelml/channel_type/current_voltage_relation/@default_gmax = 1200 
// /channelml/channel_type/current_voltage_relation/q10_settings/@q10_factor = 3 
// /channelml/channel_type/current_voltage_relation/q10_settings/@experimental_temp = 32 
// /channelml/channel_type/current_voltage_relation/gate[1]/@name = m 
// /channelml/channel_type/current_voltage_relation/gate[1]/@instances = 3 
// /channelml/channel_type/current_voltage_relation/gate[1]/closed_state/@id = m0 
// /channelml/channel_type/current_voltage_relation/gate[1]/open_state/@id = m 
// /channelml/channel_type/current_voltage_relation/gate[1]/time_course/@name = tau 
// /channelml/channel_type/current_voltage_relation/gate[1]/time_course/@from = m0 
// /channelml/channel_type/current_voltage_relation/gate[1]/time_course/@to = m 
// /channelml/channel_type/current_voltage_relation/gate[1]/time_course/@expr_form = generic 
// /channelml/channel_type/current_voltage_relation/gate[1]/time_course/@expr = 5.833e-3/((exp ((v - 0.0064)/-0.009)) + (exp ((v + 0.097)/0.017))) + 2.5e-5 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@name = inf 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@from = m0 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@to = m 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@expr_form = sigmoid 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@rate = 1 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@scale = -0.007324 
// /channelml/channel_type/current_voltage_relation/gate[1]/steady_state/@midpoint = -0.045 
// /channelml/channel_type/current_voltage_relation/gate[2]/@name = h 
// /channelml/channel_type/current_voltage_relation/gate[2]/@instances = 1 
// /channelml/channel_type/current_voltage_relation/gate[2]/closed_state/@id = h0 
// /channelml/channel_type/current_voltage_relation/gate[2]/open_state/@id = h 
// /channelml/channel_type/current_voltage_relation/gate[2]/time_course/@name = tau 
// /channelml/channel_type/current_voltage_relation/gate[2]/time_course/@from = h0 
// /channelml/channel_type/current_voltage_relation/gate[2]/time_course/@to = h 
// /channelml/channel_type/current_voltage_relation/gate[2]/time_course/@expr_form = generic 
// /channelml/channel_type/current_voltage_relation/gate[2]/time_course/@expr = 16.67e-3/((exp ((v - 0.0083)/-0.029)) + (exp ((v + 0.066)/0.009))) + 2.0e-04 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@name = inf 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@from = h0 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@to = h 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@expr_form = sigmoid 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@rate = 1 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@scale = 0.0059 
// /channelml/channel_type/current_voltage_relation/gate[2]/steady_state/@midpoint = -0.042 
// /channelml/channel_type/impl_prefs/table_settings/@max_v = 0.1 
// /channelml/channel_type/impl_prefs/table_settings/@min_v = -0.15 
// /channelml/channel_type/impl_prefs/table_settings/@table_divisions = 300 

// File from which this was generated: /home/padraig/neuroConstruct/models/SteuberEtAl-DeepCerebNucleusCell/cellMechanisms/NaF/NaChannel_HH.xml

// XSL file with mapping to simulator: /home/padraig/neuroConstruct/models/SteuberEtAl-DeepCerebNucleusCell/cellMechanisms/NaF/ChannelML_v1.8.1_GENESIStab.xsl



// This is a GENESIS script file generated from a ChannelML v1.8.1 file
// The ChannelML file is mapped onto a tabchannel object


// Units of ChannelML file: SI Units, units of GENESIS file generated: SI Units

/*
    ....
*/

function make_NaF

        /*
            ....

        */
        

        str chanpath = "/library/NaF"

        if ({exists {chanpath}})
            return
        end
        
        create tabchannel {chanpath}
            

        setfield {chanpath} \ 
            Ek              0.050 \
            Ik              0  \
            Xpower          3 \
            Ypower          1
        
        setfield {chanpath} \
            Gbar 1200 \
            Gk              0 

        
        // There is a Q10 factor which will alter the tau of the gates
                         

        float temp_adj_m = {pow 3 {(celsius - 32)/10}}             

        float temp_adj_h = {pow 3 {(celsius - 32)/10}}

        float tab_divs = 300
        float v_min = -0.15

        float v_max = 0.1

        float v, dv, i
            
        // Creating table for gate m, using name X for it here

        float dv = ({v_max} - {v_min})/{tab_divs}
            
        call {chanpath} TABCREATE X {tab_divs} {v_min} {v_max}
                
        v = {v_min}

            

        for (i = 0; i <= ({tab_divs}); i = i + 1)
            
            // Looking at rate: tau
                

            float tau
                
                        
            // Found a generic form of rate equation for tau, using expression: 5.833e-3/((exp ((v - 0.0064)/-0.009)) + (exp ((v + 0.097)/0.017))) + 2.5e-5
            // Will translate this for GENESIS compatibility...
                    tau = 5.833e-3/{{exp {{v - 0.0064}/-0.009}} + {exp {{v + 0.097}/0.017}}} + 2.5e-5
            
            // Looking at rate: inf
                

            float inf
                
            float A, B, Vhalf
                             

            // ChannelML form of equation: inf which is of form sigmoid, with params:
            // A = 1, B = -0.007324, Vhalf = -0.045, in units: SI Units
            A = 1
            B = -0.007324
            Vhalf = -0.045
            inf = A / ( {exp {(v - Vhalf) / B}} + 1)
        

            // Evaluating the tau and inf expressions

                    
            tau = tau/temp_adj_m
    

            
            // Working out the "real" alpha and beta expressions from the tau and inf
            
            float alpha
            float beta
            alpha = inf / tau   
            beta = (1- inf)/tau
            
            
            setfield {chanpath} X_A->table[{i}] {alpha}
            setfield {chanpath} X_B->table[{i}] {alpha + beta}

                
            v = v + dv

        end // end of for (i = 0; i <= ({tab_divs}); i = i + 1)
            
        setfield {chanpath} X_A->calc_mode 1 X_B->calc_mode 1
                    
        // Creating table for gate h, using name Y for it here

        float dv = ({v_max} - {v_min})/{tab_divs}
            
        call {chanpath} TABCREATE Y {tab_divs} {v_min} {v_max}
                
        v = {v_min}

            

        for (i = 0; i <= ({tab_divs}); i = i + 1)
            
            // Looking at rate: tau
                

            float tau
                
                        
            // Found a generic form of rate equation for tau, using expression: 16.67e-3/((exp ((v - 0.0083)/-0.029)) + (exp ((v + 0.066)/0.009))) + 2.0e-04
            // Will translate this for GENESIS compatibility...
                    tau = 16.67e-3/{{exp {{v - 0.0083}/-0.029}} + {exp {{v + 0.066}/0.009}}} + 2.0e-04
            
            // Looking at rate: inf
                

            float inf
                
            float A, B, Vhalf
                             

            // ChannelML form of equation: inf which is of form sigmoid, with params:
            // A = 1, B = 0.0059, Vhalf = -0.042, in units: SI Units
            A = 1
            B = 0.0059
            Vhalf = -0.042
            inf = A / ( {exp {(v - Vhalf) / B}} + 1)
        

            // Evaluating the tau and inf expressions

                    
            tau = tau/temp_adj_h
    

            
            // Working out the "real" alpha and beta expressions from the tau and inf
            
            float alpha
            float beta
            alpha = inf / tau   
            beta = (1- inf)/tau
            
            
            setfield {chanpath} Y_A->table[{i}] {alpha}
            setfield {chanpath} Y_B->table[{i}] {alpha + beta}

                
            v = v + dv

        end // end of for (i = 0; i <= ({tab_divs}); i = i + 1)
            
        setfield {chanpath} Y_A->calc_mode 1 Y_B->calc_mode 1
                    


end


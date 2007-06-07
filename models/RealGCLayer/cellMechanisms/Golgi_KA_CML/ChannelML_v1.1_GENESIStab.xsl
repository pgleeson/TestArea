<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:meta="http://morphml.org/metadata/schema" 
    xmlns:cml="http://morphml.org/channelml/schema">

<!--
    This file is used to convert ChannelML files to GENESIS tabchannel based script files
    This file is part of the neuroConstruct source code
    Author: Padraig Gleeson
-->

<xsl:output method="text" indent="yes" />

<!-- Can be altered in this file to include/exclude lines printed during execution, for decoding purposes -->
<xsl:variable name="consoleOutput">no</xsl:variable>   

<!-- The unit system (SI or Physiological) as used in the ChannelML file we're converting -->
<xsl:variable name="xmlFileUnitSystem"><xsl:value-of select="/cml:channelml/@units"/></xsl:variable>   

<!-- The unit system (SI or Physiological) we wish to convert into (Note changing this value in this file
     will create a GENESIS script in different units) -->
<xsl:variable name="targetUnitSystem">Physiological Units</xsl:variable>   

<!--Main template-->

<xsl:template match="/cml:channelml">
<xsl:text>// This is a GENESIS script file generated from a ChannelML file
// ChannelML file is mapped onto a tabchannel object

</xsl:text>
// Units of ChannelML file: <xsl:value-of select="$xmlFileUnitSystem"/>, units of GENESIS file generated: <xsl:value-of 
select="$targetUnitSystem"/>

<xsl:if test="count(meta:notes) &gt; 0">

/*
    <xsl:value-of select="meta:notes"/>
*/
</xsl:if>


<!-- Only do the first channel -->
<xsl:apply-templates  select="cml:channel_type"/>

<!-- If there is a concentration mechanism present -->
<xsl:apply-templates  select="cml:ion_concentration"/>

</xsl:template>
<!--End Main template-->


<xsl:template match="cml:channel_type">

function make_<xsl:value-of select="@name"/>
        <xsl:if test="count(meta:notes) &gt; 0">

        /*
            <xsl:value-of select="meta:notes"/>
        */
        </xsl:if>

        str chanpath = "/library/<xsl:value-of select="@name"/>"
	
        if ({exists {chanpath}})
            return
        end<xsl:text>
        </xsl:text>
        
                        
        <xsl:variable name="ionname"><xsl:value-of select="cml:current_voltage_relation/cml:ohmic/@ion"/></xsl:variable>   
        
        <xsl:choose>
            <xsl:when test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/*) = 0">
        create leakage {chanpath}
            </xsl:when>
            <xsl:otherwise>
        create tabchannel {chanpath}
            </xsl:otherwise>
        </xsl:choose>
        
        setfield {chanpath} \
            Ek              <xsl:call-template name="convert">
                                    <xsl:with-param name="value" select="/cml:channelml/cml:ion[@name=$ionname]/@default_erev"/>
                                    <xsl:with-param name="quantity">Voltage</xsl:with-param>
                               </xsl:call-template> \ 
            Gbar            <xsl:call-template name="convert">
                                    <xsl:with-param name="value" select="cml:current_voltage_relation/cml:ohmic/cml:conductance/@default_gmax"/>
                                    <xsl:with-param name="quantity">Conductance Density</xsl:with-param>
                               </xsl:call-template> \ 
            Ik              0 \
            Gk              0 <xsl:if test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate[1]) &gt; 0"> \
            Xpower          <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate[1]/@power"/>    
            </xsl:if><xsl:if test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate[2]) &gt; 0"> \
            Ypower          <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate[2]/@power"/>   
            </xsl:if><xsl:if test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate[3]) &gt; 0"> \
            Zpower          <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate[3]/@power"/>
            </xsl:if>
            <xsl:text>
                                    
        </xsl:text>
            
    
        
        <xsl:if test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/*) &gt; 0">
            <xsl:choose>
                <xsl:when test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:q10_settings) &gt; 0">
        // There is a Q10 factor which will alter the tau of the gates 
        float temp_adj = {pow <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:q10_settings/@q10_factor"
        /> {(celsius - <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:q10_settings/@experimental_temp"/>)/10}}
        
        <xsl:if test="$consoleOutput='yes'">echo "Temperature adjustment factor: " {temp_adj}</xsl:if>
        
                </xsl:when>
                <xsl:otherwise>
        // No Q10 temperature adjustment found
        float temp_adj = 1
                </xsl:otherwise>
            </xsl:choose>
            
        <!-- Perhaps too many... -->
        float tab_divs = 400
        
        float tab_min = <xsl:choose>
                            <xsl:when test="$targetUnitSystem  = 'Physiological Units'">-100</xsl:when>
                            <xsl:otherwise>-0.1</xsl:otherwise>
                        </xsl:choose>
                        
        float tab_max = <xsl:choose>
                            <xsl:when test="$targetUnitSystem  = 'Physiological Units'">100</xsl:when>
                            <xsl:otherwise>0.1</xsl:otherwise>
                        </xsl:choose>
        
        float v, dv, i
        </xsl:if>
                
        <xsl:for-each select='cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate'>
     
            <xsl:variable name='gateRef'>
                <xsl:if test='position()=1'>X</xsl:if>
                <xsl:if test='position()=2'>Y</xsl:if>
                <xsl:if test='position()=3'>Z</xsl:if>
            </xsl:variable>
        
        call {chanpath} TABCREATE <xsl:value-of select="$gateRef"/> {tab_divs} {tab_min} {tab_max}
        
        v = {tab_min}
        
        float dv = ({tab_max} - {tab_min})/{tab_divs}
        
            <xsl:if test="count(../cml:rate_adjustments/cml:offset) &gt; 0">
        // There is a voltage offset of <xsl:value-of select="../cml:rate_adjustments/cml:offset/@value"/>. This will shift the dependency of the rate equations 
        v = v - <xsl:call-template name="convert">
                    <xsl:with-param name="value" select="../cml:rate_adjustments/cml:offset/@value"/>
                    <xsl:with-param name="quantity">Voltage</xsl:with-param>
                </xsl:call-template><xsl:text>
            </xsl:text>          
            </xsl:if>
        
        for (i = 0; i &lt;= ({tab_divs}); i = i + 1)
       
            <xsl:for-each select='cml:state/cml:transition/cml:voltage_gate/*'>           
            // Looking at rate: <xsl:value-of select="name()"/><xsl:text>
                </xsl:text>
            float <xsl:value-of select="name()"/>    <xsl:text>
                </xsl:text>
          
                <xsl:choose>
                    <xsl:when  test="count(cml:parameterised_hh) &gt; 0">
            float A, B, k, V0
                        <xsl:call-template name="generateEquation">
                            <xsl:with-param name="name"><xsl:value-of select="name()"/></xsl:with-param>
                            <xsl:with-param name="functionForm" select="cml:parameterised_hh/@type" />
                            <xsl:with-param name="expression"   select="cml:parameterised_hh/@expr" />
                            <xsl:with-param name="A_cml" select="cml:parameterised_hh/cml:parameter[@name='A']/@value"/>
                            <xsl:with-param name="k_cml" select="cml:parameterised_hh/cml:parameter[@name='k']/@value"/>
                            <xsl:with-param name="d_cml" select="cml:parameterised_hh/cml:parameter[@name='d']/@value"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="count(cml:generic_equation_hh) &gt; 0">
            // Found a generic form of rate equation for <xsl:value-of select="name()"/>, using expression: <xsl:value-of select="cml:generic_equation_hh/@expr" />
            // Will translate this for GENESIS compatibility...<xsl:text>
                    </xsl:text>
                    <xsl:if test="string($xmlFileUnitSystem) != string($targetUnitSystem)">
            // Equation (and all ChannelML file values) in <xsl:value-of select="$xmlFileUnitSystem" 
            /> but this script in <xsl:value-of select="$targetUnitSystem" /><xsl:text>
            </xsl:text>
            v = v * <xsl:call-template name="convert">
                        <xsl:with-param name="value">1</xsl:with-param>
                        <xsl:with-param name="quantity">InvVoltage</xsl:with-param>
                    </xsl:call-template> // temporarily set v to units of equation...<xsl:text>
            </xsl:text>
                        <xsl:if test="(name()='tau' or name()='inf') and 
                                      (contains(string(cml:generic_equation_hh/@expr), 'alpha') or
                                      contains(string(cml:generic_equation_hh/@expr), 'beta'))">
            // Equation depends on alpha/beta, so converting them too...
            alpha = alpha * <xsl:call-template name="convert">
                                <xsl:with-param name="value">1</xsl:with-param>
                                <xsl:with-param name="quantity">Time</xsl:with-param>
                            </xsl:call-template>  
            beta = beta * <xsl:call-template name="convert">
                                <xsl:with-param name="value">1</xsl:with-param>
                                <xsl:with-param name="quantity">Time</xsl:with-param>   
                            </xsl:call-template>     
                        </xsl:if>
                    </xsl:if>
                    <xsl:variable name="newExpression">
                        <xsl:call-template name="formatExpression">
                            <xsl:with-param name="variable">
                                <xsl:value-of select="name()"/>
                            </xsl:with-param>
                            <xsl:with-param name="oldExpression">
                                <xsl:value-of select="cml:generic_equation_hh/@expr" />
                            </xsl:with-param>
                        </xsl:call-template>
                    </xsl:variable>
            <xsl:value-of select="$newExpression" /><xsl:text>
            </xsl:text>
                    <xsl:if test="string($xmlFileUnitSystem) != string($targetUnitSystem)">
            v = v * <xsl:call-template name="convert">
                        <xsl:with-param name="value">1</xsl:with-param>
                        <xsl:with-param name="quantity">Voltage</xsl:with-param>
                    </xsl:call-template> // reset v<xsl:text>
            </xsl:text>
                    <xsl:if test="(name()='tau' or name()='inf') and 
                                      (contains(string(cml:generic_equation_hh/@expr), 'alpha') or
                                      contains(string(cml:generic_equation_hh/@expr), 'beta'))">
            alpha = alpha * <xsl:call-template name="convert">
                                <xsl:with-param name="value">1</xsl:with-param>
                                <xsl:with-param name="quantity">InvTime</xsl:with-param>
                            </xsl:call-template>  // resetting alpha
            beta = beta * <xsl:call-template name="convert">
                                <xsl:with-param name="value">1</xsl:with-param>
                                <xsl:with-param name="quantity">InvTime</xsl:with-param>   
                            </xsl:call-template>  // resetting beta
                        </xsl:if>
                    </xsl:if>
                    
                    
                    
            
                    <xsl:if test="(name()='alpha' or name()='beta')
                                   and (string($xmlFileUnitSystem) != string($targetUnitSystem))">
            // Set correct units of <xsl:value-of select="name()"/><xsl:text>
            </xsl:text>    
            <xsl:value-of select="name()"/> = <xsl:value-of select="name()"/> * <xsl:call-template name="convert">
                            <xsl:with-param name="value">1</xsl:with-param>
                            <xsl:with-param name="quantity">InvTime</xsl:with-param> 
                        </xsl:call-template><xsl:text>
                            
            </xsl:text>   
                    </xsl:if>  
                                      
                    <xsl:if test="name()='tau' and (string($xmlFileUnitSystem) != string($targetUnitSystem))">
            // Set correct units of <xsl:value-of select="name()"/><xsl:text>
            </xsl:text>
            <xsl:value-of select="name()"/> = <xsl:value-of select="name()"/> * <xsl:call-template name="convert">
                            <xsl:with-param name="value">1</xsl:with-param>
                            <xsl:with-param name="quantity">Time</xsl:with-param>
                        </xsl:call-template>
                    </xsl:if>
                    
                    
                       
                    </xsl:when>
                    <xsl:otherwise>
            ? ERROR: Unrecognised form of the rate equation for <xsl:value-of select="name()"/>...

                    </xsl:otherwise>
                </xsl:choose>

            </xsl:for-each>
                           
            <!-- Working out the conversion of alpha and beta to tau & inf-->
            <xsl:choose>
                <xsl:when test="count(cml:state/cml:transition/cml:voltage_gate/cml:alpha)=1 and
                                count(cml:state/cml:transition/cml:voltage_gate/cml:beta)=1 and
                                count(cml:state/cml:transition/cml:voltage_gate/cml:tau)=0 and
                                count(cml:state/cml:transition/cml:voltage_gate/cml:inf)=0">
                          
            // Using the alpha and beta expressions to populate the tables
            
            float tau = 1/(temp_adj * (alpha + beta))   
            <xsl:if test="$consoleOutput='yes'">echo "tab <xsl:value-of select="$gateRef"/>: i: "{i}", v: "{v} ", alpha: "{alpha}", beta: "{beta}", tau: "{tau}</xsl:if>
            
            setfield {chanpath} <xsl:value-of select="$gateRef"/>_A->table[{i}] {temp_adj * alpha}
            setfield {chanpath} <xsl:value-of select="$gateRef"/>_B->table[{i}] {temp_adj * (alpha + beta)}  
                </xsl:when>
                <xsl:otherwise>
                
            // Using the tau and inf expressions to populate the tables
            
                    <xsl:choose>
                        <xsl:when test="count(cml:state/cml:transition/cml:voltage_gate/cml:tau)=0">
            float tau = 1/(temp_adj * (alpha + beta))   
                        </xsl:when>
                        <xsl:otherwise>
            tau = tau/temp_adj
                        </xsl:otherwise>
                    </xsl:choose>                    
                    <xsl:if test="count(cml:state/cml:transition/cml:voltage_gate/cml:inf)=0">
            float inf = alpha/(alpha + beta)   
                    </xsl:if>
            
            <xsl:if test="$consoleOutput='yes'">echo "tab <xsl:value-of select="$gateRef"/>: v: "{v} ", tau: "{tau} ", inf: "{inf}</xsl:if>
            
            setfield {chanpath} <xsl:value-of select="$gateRef"/>_A->table[{i}] {tau}
            
            setfield {chanpath} <xsl:value-of select="$gateRef"/>_B->table[{i}] {inf}  
                </xsl:otherwise>
                </xsl:choose>
             
            v = v + dv
        end       
             
            <xsl:if test='count(cml:state/cml:transition/cml:voltage_gate/cml:tau) &gt; 0 or
                      count(cml:state/cml:transition/cml:voltage_gate/cml:inf) &gt; 0'>
        // Using the tau, inf form of rate equations, so tweaking...
        tweaktau {chanpath} <xsl:value-of select="$gateRef"/>
            </xsl:if>
        
        setfield {chanpath} <xsl:value-of select="$gateRef"/>_A->calc_mode 1 <xsl:value-of select="$gateRef"/>_B->calc_mode 1    
        
        
        </xsl:for-each>
        

end

</xsl:template>
<!--End Main template-->




<xsl:template match="cml:ion_concentration">

function make_<xsl:value-of select="@name"/>
        <xsl:if test="count(meta:notes) &gt; 0">

        /*
            <xsl:value-of select="meta:notes"/>
        */
        </xsl:if>

        str chanpath = "/library/<xsl:value-of select="@name"/>"
	
        if ({exists {chanpath}})
            return
        end<xsl:text>
        </xsl:text>
                                
        <xsl:variable name="ionname"><xsl:value-of select="cml:current_voltage_relation/cml:ohmic/@ion"/></xsl:variable>   
        
        create Ca_concen {chanpath}
        
        <xsl:if test="count(cml:decaying_pool_model) &gt; 0">
        
        // Setting params for a decaying_pool_model
        
        setfield {chanpath} \
            tau               <xsl:call-template name="convert">
                                    <xsl:with-param name="value" select="cml:decaying_pool_model/cml:decay_constant"/>
                                    <xsl:with-param name="quantity">Time</xsl:with-param>
                               </xsl:call-template> \
            Ca_base               <xsl:call-template name="convert">
                                    <xsl:with-param name="value" select="cml:decaying_pool_model/cml:resting_conc"/>
                                    <xsl:with-param name="quantity">Concentration</xsl:with-param>
                               </xsl:call-template>
        </xsl:if>
        
        <xsl:if test="count(cml:decaying_pool_model/cml:pool_volume_info) &gt; 0">
        
        setfield {chanpath} \
            thick               <xsl:call-template name="convert">
                                    <xsl:with-param name="value" select="cml:decaying_pool_model/cml:pool_volume_info/cml:shell_thickness"/>
                                    <xsl:with-param name="quantity">Length</xsl:with-param>
                               </xsl:call-template> 
        </xsl:if>
        
end
            
</xsl:template>




<!-- Function to return 1 for exponential, 2 for sigmoid, 3 for linoid-->
<xsl:template name="getFunctionForm">
    <xsl:param name="stringFunctionName"/>
    <xsl:choose>
        <xsl:when test="$stringFunctionName = 'exponential'">1</xsl:when>
        <xsl:when test="$stringFunctionName = 'sigmoid'">2</xsl:when>
        <xsl:when test="$stringFunctionName = 'linoid'">3</xsl:when>       
    </xsl:choose>
</xsl:template>



<!-- Function to get value converted to proper units.-->
<xsl:template name="convert">
    <xsl:param name="value" />
    <xsl:param name="quantity" />
    <xsl:choose>
        <xsl:when test="$xmlFileUnitSystem  = $targetUnitSystem"><xsl:value-of select="$value"/></xsl:when>   
        <xsl:when test="$xmlFileUnitSystem  = 'Physiological Units' and $targetUnitSystem  = 'SI Units'">
            <xsl:choose>
                <xsl:when test="$quantity = 'Conductance Density'"><xsl:value-of select="number($value*10)"/></xsl:when>
                <xsl:when test="$quantity = 'Voltage'"><xsl:value-of select="number($value div 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'InvVoltage'"><xsl:value-of select="number($value * 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'Time'"><xsl:value-of select="number($value div 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'Length'"><xsl:value-of select="number($value * 1000000)"/></xsl:when>
                <xsl:when test="$quantity = 'InvTime'"><xsl:value-of select="number($value * 1000)"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="number($value)"/></xsl:otherwise>
            </xsl:choose>
        </xsl:when>           
        <xsl:when test="$xmlFileUnitSystem  = 'SI Units' and $targetUnitSystem  = 'Physiological Units'">
            <xsl:choose>
                <xsl:when test="$quantity = 'Conductance Density'"><xsl:value-of select="number($value div 10)"/></xsl:when>
                <xsl:when test="$quantity = 'Voltage'"><xsl:value-of select="number($value * 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'InvVoltage'"><xsl:value-of select="number($value div 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'Time'"><xsl:value-of select="number($value * 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'Length'"><xsl:value-of select="number($value div 1000000)"/></xsl:when>
                <xsl:when test="$quantity = 'InvTime'"><xsl:value-of select="number($value div 1000)"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="number($value)"/></xsl:otherwise>
            </xsl:choose>
        </xsl:when>   
        <xsl:when test="$xmlFileUnitSystem  = 'SI Units'">si</xsl:when>   
    </xsl:choose>
</xsl:template>



<!-- Function to get equation in GENESIS format-->
<xsl:template name="generateEquation">
    <xsl:param name="name" />
    <xsl:param name="functionForm" />
    <xsl:param name="expression" />
    <xsl:param name="A_cml" />
    <xsl:param name="k_cml" />
    <xsl:param name="d_cml" />
    <xsl:choose>
    
        <xsl:when test="string-length($functionForm) &gt; 0"> <!-- So not an empty string-->
            // ChannelML form of equation: <xsl:value-of select="$name"/> = <xsl:value-of select="$expression" />, with params:
            // A = <xsl:value-of select="$A_cml"/>, k = <xsl:value-of select="$k_cml" />, d = <xsl:value-of 
            select="$d_cml" />, in units: <xsl:value-of select="$xmlFileUnitSystem"/>
            
            <xsl:choose>
                <xsl:when test="string($name) = 'alpha' or string($name) = 'beta'">
            A = <xsl:call-template name="convert">
                    <xsl:with-param name="value"><xsl:value-of select="$A_cml"/></xsl:with-param>
                    <xsl:with-param name="quantity">InvTime</xsl:with-param>
                </xsl:call-template>
                </xsl:when>
                <xsl:when test="string($name) = 'tau'">
            A = <xsl:call-template name="convert">
                    <xsl:with-param name="value"><xsl:value-of select="$A_cml"/></xsl:with-param>
                    <xsl:with-param name="quantity">Time</xsl:with-param>
                </xsl:call-template>
                </xsl:when>
                <xsl:when test="string($name) = 'inf'">
            A = <xsl:value-of select="$A_cml"/>
                </xsl:when>
            </xsl:choose>
                
            k = <xsl:call-template name="convert">
                    <xsl:with-param name="value"><xsl:value-of select="$k_cml"/></xsl:with-param>
                    <xsl:with-param name="quantity">InvVoltage</xsl:with-param>
                </xsl:call-template>
            B = 1/k
            V0 = <xsl:call-template name="convert">
                    <xsl:with-param name="value"><xsl:value-of select="$d_cml"/></xsl:with-param>
                    <xsl:with-param name="quantity">Voltage</xsl:with-param>
                </xsl:call-template><xsl:text>
            </xsl:text>

    <xsl:choose>
        <xsl:when test="$functionForm = 'exponential'">

            <xsl:value-of select="$name"/> = A * {exp {(v - V0) / B}}
        </xsl:when>
        <xsl:when test="$functionForm = 'sigmoid'">
            <xsl:value-of select="$name"/> = A / ( {exp {(v - V0) / B}} + 1)
        </xsl:when>
            <xsl:when test="$functionForm = 'linoid'">
            
            if ( {abs {(v - V0)/ B}} &lt; 1e-6) 
                <xsl:value-of select="$name"/> = A * (1 + (v - V0)/B/2)
            else  
                <xsl:value-of select="$name"/> = A * ((v - V0) / B) /(1 - {exp {-1 * (v - V0)/B}})
            end
            
        </xsl:when>
    </xsl:choose>
        </xsl:when>
        
            <!-- In the case when the info on the gate is missing -->
        <xsl:otherwise>
            <xsl:value-of select="$name"/> = 1 // Gate is not present, power should = 0 so value of <xsl:value-of 
                            select="$name"/> is not relevant
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>



<!-- Function to try to format the rate expression to something this simulator is a bit happier with-->
<xsl:template name="formatExpression">
    <xsl:param name="variable" />
    <xsl:param name="oldExpression" />
    <xsl:choose>
        <xsl:when test="contains($oldExpression, '?')">
    <!-- Expression contains a condition!!-->
    <xsl:variable name="ifTrue"><xsl:value-of select="substring-before(substring-after($oldExpression,'?'), ':')"/></xsl:variable>
    <xsl:variable name="ifFalse"><xsl:value-of select="substring-after($oldExpression,':')"/></xsl:variable>
    <xsl:variable name="condition"><xsl:value-of select="substring-before($oldExpression,'?')"/></xsl:variable>
    
            if (<xsl:value-of select="translate($condition,'()','{}')"/>)<xsl:text>
                </xsl:text><xsl:value-of select="$variable"/> = <xsl:value-of select="translate($ifTrue,'()','{}')"/>
            else<xsl:text>
                </xsl:text><xsl:value-of select="$variable"/> = <xsl:value-of select="translate($ifFalse,'()','{}')"/>
            end
        </xsl:when>
        <xsl:otherwise>
    <xsl:value-of select="$variable"/> = <xsl:value-of select="translate($oldExpression,'()','{}')"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

</xsl:stylesheet>

<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:meta="http://morphml.org/metadata/schema" 
    xmlns:cml="http://morphml.org/channelml/schema">

<!--
    This file is used to convert v1.1 ChannelML files to NEURON mod files
    This file is part of the neuroConstruct source code
    Author: Padraig Gleeson
-->

<xsl:output method="text" indent="yes" />

<xsl:variable name="xmlFileUnitSystem"><xsl:value-of select="/cml:channelml/@units"/></xsl:variable>   

<!--Main template-->

<xsl:template match="/cml:channelml">
?  This is a NEURON mod file generated from a v1.1 ChannelML file

?  Unit system of ChannelML file: <xsl:value-of select="$xmlFileUnitSystem"/><xsl:text>
</xsl:text>
<xsl:if test="count(meta:notes) &gt; 0">

COMMENT
    <xsl:value-of select="meta:notes"/>
ENDCOMMENT
</xsl:if>
<!-- Only do the first channel -->
<xsl:apply-templates  select="cml:channel_type"/>
</xsl:template>
<!--End Main template-->

<xsl:template match="cml:channel_type">
TITLE Channel: <xsl:value-of select="@name"/>

<xsl:if test="count(meta:notes) &gt; 0">

COMMENT
    <xsl:value-of select="meta:notes"/>
ENDCOMMENT
</xsl:if>

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

<xsl:variable name="nonSpecificCurrent">
    <xsl:choose>
        <xsl:when test="cml:current_voltage_relation/cml:ohmic/@ion='non_specific'">yes</xsl:when>
        <xsl:otherwise>no</xsl:otherwise>
    </xsl:choose>
</xsl:variable>
    
NEURON {
    SUFFIX <xsl:value-of select="@name"/>
    
    <xsl:for-each select="/cml:channelml/cml:ion[@name!='non_specific']">
    USEION <xsl:value-of select="@name"/> READ e<xsl:value-of select="@name"/> WRITE i<xsl:value-of select="@name"/>
    </xsl:for-each>
    
    <xsl:if test="string($nonSpecificCurrent)='yes'">
    ? A non specific current is present
    RANGE e
    NONSPECIFIC_CURRENT i
    </xsl:if>
    RANGE gmax, gion
    <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">
    RANGE <xsl:value-of select="cml:state/@name"/>inf, <xsl:value-of select="cml:state/@name"/>tau
    </xsl:for-each>
}

PARAMETER { 
    gmax = <xsl:call-template name="convert">
            <xsl:with-param name="value" select="cml:current_voltage_relation/cml:ohmic/cml:conductance/@default_gmax"/>
            <xsl:with-param name="quantity">Conductance Density</xsl:with-param>
          </xsl:call-template> (S/cm2) 
    <xsl:if test="string($nonSpecificCurrent)='yes'">
    e = <xsl:call-template name="convert">
            <xsl:with-param name="value" select="/cml:channelml/cml:ion[@name='non_specific']/@default_erev"/>
            <xsl:with-param name="quantity">Voltage</xsl:with-param>
            </xsl:call-template> (mV)
    </xsl:if>
}



ASSIGNED {
    v (mV)
    <xsl:choose>
        <xsl:when test="string($nonSpecificCurrent)='yes'">    
    i (mA/cm2)
        </xsl:when>
        <xsl:otherwise>
    celsius (degC)
    <xsl:for-each select="/cml:channelml/cml:ion[@name!='non_specific']">
    e<xsl:value-of select="@name"/> (mV)
    i<xsl:value-of select="@name"/> (mA/cm2)
    </xsl:for-each>
    gion (S/cm2)
    <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">
<xsl:value-of select="cml:state/@name"/>inf<xsl:text>
    </xsl:text><xsl:value-of select="cml:state/@name"/>tau (ms)<xsl:text>
    </xsl:text></xsl:for-each>
        </xsl:otherwise>
        </xsl:choose>
}

BREAKPOINT {
    <xsl:choose>
        <xsl:when test="string($nonSpecificCurrent)='yes'">
    i = gmax*(v - e) 
        </xsl:when>
        <xsl:otherwise>
    SOLVE states METHOD cnexp
    
    gion = gmax<xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">*((<xsl:value-of select="cml:state/@fraction"/>*<xsl:value-of select="cml:state/@name"/>)^<xsl:value-of select="@power"/>)</xsl:for-each>
    
            <xsl:for-each select="/cml:channelml/cml:ion">
    i<xsl:value-of select="@name"/> = gion*(v - e<xsl:value-of select="@name"/>)
            </xsl:for-each>
        </xsl:otherwise>
        </xsl:choose>
}
    
<xsl:if test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate) &gt; 0">
INITIAL {
<xsl:variable name="ionname"><xsl:value-of select="cml:current_voltage_relation/cml:ohmic/@ion"/></xsl:variable>  
<xsl:variable name="defaultErev"><xsl:call-template name="convert">
            <xsl:with-param name="value" select="/cml:channelml/cml:ion[@name=$ionname]/@default_erev"/>
            <xsl:with-param name="quantity">Voltage</xsl:with-param>
            </xsl:call-template></xsl:variable>
<xsl:for-each select="/cml:channelml/cml:ion">
    e<xsl:value-of select="@name"/> = <xsl:value-of select="$defaultErev"/>
    </xsl:for-each>
    rates(v)
    <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">
    <xsl:value-of select="cml:state/@name"/> = <xsl:value-of select="cml:state/@name"/>inf<xsl:text>
    </xsl:text></xsl:for-each>
}
    
STATE {
    <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">
    <xsl:value-of select="cml:state/@name"/><xsl:text>
    </xsl:text>
    </xsl:for-each>
}

DERIVATIVE states {
    rates(v)
    <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">
    <xsl:value-of select="cml:state/@name"/>' = (<xsl:value-of select="cml:state/@name"/>inf - <xsl:value-of select="cml:state/@name"/>)/<xsl:value-of select="cml:state/@name"/>tau<xsl:text>
    </xsl:text></xsl:for-each>
}

 
PROCEDURE rates(v(mV)) {
    
    ? Note, not all of these may be used, depending on the form of rate equations
    LOCAL  alpha, beta, A, B, k, d, tau, inf, temp_adj  
    <xsl:variable name="numGates"><xsl:value-of select="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate)"/></xsl:variable>
    ? May be too many table points and too wide a range...
    TABLE <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate"><xsl:value-of 
    select="cml:state/@name"/>inf, <xsl:value-of select="cml:state/@name"/>tau<xsl:if test="position() &lt; number($numGates)">,</xsl:if> </xsl:for-each> DEPEND celsius FROM -100 TO 100 WITH 400
    
    
    UNITSOFF
    <xsl:choose>
        <xsl:when test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:q10_settings) &gt; 0">
    ? There is a Q10 factor which will alter the tau of the gates 
    temp_adj = <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:q10_settings/@q10_factor"
    />^((celsius - <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:q10_settings/@experimental_temp"/>)/10)
        </xsl:when>
        <xsl:otherwise>
    temp_adj = 1
        </xsl:otherwise>
    </xsl:choose>
    
    <xsl:if test="count(cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:offset) &gt; 0">
    ? There is a voltage offset of <xsl:value-of select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:offset/@value"/>. This will shift the dependency of the rate equations 
    v = v - (<xsl:call-template name="convert">
            <xsl:with-param name="value" select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:rate_adjustments/cml:offset/@value"/>
            <xsl:with-param name="quantity">Voltage</xsl:with-param>
            </xsl:call-template>)<xsl:text>
    </xsl:text>          
    </xsl:if>
    
    
    <xsl:for-each select="cml:current_voltage_relation/cml:ohmic/cml:conductance/cml:gate">
    
    ? Adding rate equations for gate: <xsl:value-of select="cml:state/@name"/><xsl:text>
    </xsl:text>   
    <xsl:for-each select='cml:state/cml:transition/cml:voltage_gate/*'>

        <xsl:choose>
            <xsl:when  test="count(cml:parameterised_hh) &gt; 0">
    ? Found a parameterised form of rate equation for <xsl:value-of select="name()"/>, using expression: <xsl:value-of select="cml:parameterised_hh/@expr" /><xsl:text>
    </xsl:text>   
    
                <xsl:for-each select="cml:parameterised_hh/cml:parameter">
    <xsl:value-of select="@name"/> = <xsl:value-of select="@value"/><xsl:text>
    </xsl:text>
                </xsl:for-each>
    
                <xsl:if test="$xmlFileUnitSystem  = 'SI Units'">
    ? Unit system in ChannelML file is SI units, therefore need to 
    ? convert these to NEURON quanities...
                <xsl:choose>
                    <xsl:when test="string(name()) = 'alpha' or string(name()) = 'beta'">
    A = A * <xsl:call-template name="convert">
            <xsl:with-param name="value">1</xsl:with-param>
            <xsl:with-param name="quantity">InvTime</xsl:with-param>
        </xsl:call-template>   ? 1/ms
                    </xsl:when>
                    <xsl:when test="string(name()) = 'tau'">
    A = A * <xsl:call-template name="convert">
            <xsl:with-param name="value">1</xsl:with-param>
            <xsl:with-param name="quantity">Time</xsl:with-param>
        </xsl:call-template>   ? ms
                    </xsl:when>
                    <xsl:when test="string(name()) = 'inf'">
    A = A   ? Dimensionless
                    </xsl:when>
                </xsl:choose>
    k = k * <xsl:call-template name="convert">
            <xsl:with-param name="value">1</xsl:with-param>
            <xsl:with-param name="quantity">InvVoltage</xsl:with-param>
          </xsl:call-template>   ? mV
    d = d * <xsl:call-template name="convert">
            <xsl:with-param name="value">1</xsl:with-param>
            <xsl:with-param name="quantity">Voltage</xsl:with-param>
          </xsl:call-template>   ? mV
          
                </xsl:if>
    B = 1/k<xsl:text> 
    
    </xsl:text>
                <xsl:choose>
                    <xsl:when test="cml:parameterised_hh/@type='exponential'">
    <xsl:value-of select="name()"/> = A * exp((v - d) / B)<xsl:text>
    
    </xsl:text>
                    </xsl:when>
                    <xsl:when test="cml:parameterised_hh/@type='sigmoid'">
    <xsl:value-of select="name()"/> = A / (exp((v - d) / B) + 1)<xsl:text>
    
    </xsl:text>
                    </xsl:when>
                    <xsl:when test="cml:parameterised_hh/@type='linoid'">
    <xsl:value-of select="name()"/> = A * vtrap((v - d), B)<xsl:text>
    
    </xsl:text>
                    </xsl:when>
                </xsl:choose>
    
    
            </xsl:when>
            <xsl:when test="count(cml:generic_equation_hh) &gt; 0">
    ? Found a generic form of rate equation for <xsl:value-of select="name()"/>, using expression: <xsl:value-of select="cml:generic_equation_hh/@expr" /><xsl:text>
    </xsl:text>  
    <xsl:if test="string($xmlFileUnitSystem) = 'SI Units'">
    ? Note: Equation (and all ChannelML file values) in <xsl:value-of select="$xmlFileUnitSystem"/> so need to convert v first...<xsl:text>
    </xsl:text>
    v = v * <xsl:call-template name="convert">
                <xsl:with-param name="value">1</xsl:with-param>
                <xsl:with-param name="quantity">InvVoltage</xsl:with-param>
            </xsl:call-template>   ? temporarily set v to units of equation...
        <xsl:if test="(name()='tau' or name()='inf') and 
                      (contains(string(cml:generic_equation_hh/@expr), 'alpha') or
                       contains(string(cml:generic_equation_hh/@expr), 'beta'))">
    ? Equation depends on alpha/beta, so converting them too...
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
    <xsl:call-template name="formatExpression">
        <xsl:with-param name="variable">
            <xsl:value-of select="name()"/>
        </xsl:with-param>
        <xsl:with-param name="oldExpression">
            <xsl:value-of select="cml:generic_equation_hh/@expr" />
        </xsl:with-param>
    </xsl:call-template>
    <xsl:if test="string($xmlFileUnitSystem) = 'SI Units'">
        
        <xsl:if test="name()='alpha' or name()='beta'">
    ? Set correct units of <xsl:value-of select="name()"/> for NEURON<xsl:text>
    </xsl:text>    
    <xsl:value-of select="name()"/> = <xsl:value-of select="name()"/> * <xsl:call-template name="convert">
                            <xsl:with-param name="value">1</xsl:with-param>
                            <xsl:with-param name="quantity">InvTime</xsl:with-param>
                        </xsl:call-template>
        </xsl:if>  
                                      
        <xsl:if test="name()='tau'">
    ? Set correct units of <xsl:value-of select="name()"/> for NEURON<xsl:text>
    </xsl:text>
    <xsl:value-of select="name()"/> = <xsl:value-of select="name()"/> * <xsl:call-template name="convert">
                    <xsl:with-param name="value">1</xsl:with-param>
                    <xsl:with-param name="quantity">Time</xsl:with-param>
                </xsl:call-template>
        </xsl:if> 
    
    v = v * <xsl:call-template name="convert">
                <xsl:with-param name="value">1</xsl:with-param>
                <xsl:with-param name="quantity">Voltage</xsl:with-param>
            </xsl:call-template>   ? reset v
        <xsl:if test="(name()='tau' or name()='inf') and 
                      (contains(string(cml:generic_equation_hh/@expr), 'alpha') or
                       contains(string(cml:generic_equation_hh/@expr), 'beta'))">
    alpha = alpha * <xsl:call-template name="convert">
                        <xsl:with-param name="value">1</xsl:with-param>
                        <xsl:with-param name="quantity">InvTime</xsl:with-param>
                    </xsl:call-template>  ? resetting alpha
    beta = beta * <xsl:call-template name="convert">
                        <xsl:with-param name="value">1</xsl:with-param>
                        <xsl:with-param name="quantity">InvTime</xsl:with-param>   
                    </xsl:call-template>  ? resetting beta
        </xsl:if>
    </xsl:if>      <xsl:text>
    </xsl:text>  
           
            </xsl:when>
            <xsl:otherwise>
    ? ERROR: Unrecognised form of the rate equation for <xsl:value-of select="name()"/>
            
            </xsl:otherwise>
        </xsl:choose>
                
       <xsl:if test="name()='tau'">
    <xsl:value-of select="../../../@name"/>tau = tau/temp_adj<xsl:text>
    </xsl:text>   
       </xsl:if>    
                   
       <xsl:if test="name()='inf'">
    <xsl:value-of select="../../../@name"/>inf = inf<xsl:text>
    </xsl:text>   
       </xsl:if>
      
    </xsl:for-each>
    
    <!-- Finishing off the alpha & beta to tau & inf conversion... -->

         
        <xsl:if test="count(cml:state/cml:transition/cml:voltage_gate/cml:tau)=0">
    <xsl:value-of select="cml:state/@name"/>tau = 1/(temp_adj*(alpha + beta))<xsl:text>
    </xsl:text>
       </xsl:if>       
         
       <xsl:if test="count(cml:state/cml:transition/cml:voltage_gate/cml:inf)=0">
    <xsl:value-of select="cml:state/@name"/>inf = alpha/(alpha + beta)<xsl:text>
    </xsl:text>
       </xsl:if>    
       
    
    ? Finished rate equations for gate: <xsl:value-of select="cml:state/@name"/>

    </xsl:for-each>
}

FUNCTION vtrap(VminV0, B) {
    if (fabs(VminV0/B) &lt; 1e-6) {
    vtrap = (1 + VminV0/B/2)
}else{
    vtrap = (VminV0 / B) /(1 - exp((-1 *VminV0)/B))
    }
}

UNITSON


</xsl:if>

</xsl:template>


<!-- Function to get value converted to proper units.-->
<xsl:template name="convert">
    <xsl:param name="value" />
    <xsl:param name="quantity" />
    <xsl:choose> 
        <xsl:when test="$xmlFileUnitSystem  = 'Physiological Units'">
            <xsl:choose>
                <xsl:when test="$quantity = 'Conductance Density'"><xsl:value-of select="number($value div 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'Voltage'"><xsl:value-of select="$value"/></xsl:when> <!-- same -->
                <xsl:when test="$quantity = 'InvVoltage'"><xsl:value-of select="$value"/></xsl:when> <!-- same -->
                <xsl:when test="$quantity = 'Time'"><xsl:value-of select="number($value)"/></xsl:when> <!-- same -->
                <xsl:when test="$quantity = 'InvTime'"><xsl:value-of select="number($value)"/></xsl:when> <!-- same --> 

                <xsl:otherwise><xsl:value-of select="number($value)"/></xsl:otherwise>
            </xsl:choose>
        </xsl:when>           
        <xsl:when test="$xmlFileUnitSystem  = 'SI Units'">
            <xsl:choose>
                <xsl:when test="$quantity = 'Conductance Density'"><xsl:value-of select="number($value div 10000)"/></xsl:when>
                <xsl:when test="$quantity = 'Voltage'"><xsl:value-of select="number($value * 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'InvVoltage'"><xsl:value-of select="$value div 1000"/></xsl:when>
                <xsl:when test="$quantity = 'Time'"><xsl:value-of select="number($value * 1000)"/></xsl:when>
                <xsl:when test="$quantity = 'InvTime'"><xsl:value-of select="number($value div 1000)"/></xsl:when>

                <xsl:otherwise><xsl:value-of select="number($value)"/></xsl:otherwise>
            </xsl:choose>
        </xsl:when>   
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
    
    if (<xsl:value-of select="substring-before($oldExpression,'?')"/>) {<xsl:text>
        </xsl:text><xsl:value-of select="$variable"/> = <xsl:value-of select="$ifTrue"/>
    } else {<xsl:text>
        </xsl:text><xsl:value-of select="$variable"/> = <xsl:value-of select="$ifFalse"/>
    }</xsl:when>
        <xsl:otherwise>
    <xsl:value-of select="$variable"/> = <xsl:value-of select="$oldExpression"/><xsl:text>
        </xsl:text>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>


</xsl:stylesheet>

<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:meta="http://morphml.org/metadata/schema"
    xmlns:cml="http://morphml.org/channelml/schema"
    exclude-result-prefixes="meta cml">
    
<!--
    This file is used to convert ChannelML files to PSICS script files
    Funding for this work has been received from the Medical Research Council and Wellcome Trust
    Author: Padraig Gleeson, Robert cannon
-->

<xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>

<xsl:variable name="includeComments">0</xsl:variable>

<xsl:variable name="physiolunits">
     <xsl:choose>
        <xsl:when test="/cml:channelml/@units = 'Physiological Units'">true</xsl:when>
        <xsl:otherwise>false</xsl:otherwise>
    </xsl:choose>
</xsl:variable>

<xsl:variable name="vunits">
    <xsl:choose>
        <xsl:when test="$physiolunits = 'true'">mV</xsl:when>
        <xsl:otherwise>V</xsl:otherwise>
    </xsl:choose>
</xsl:variable>

<xsl:variable name="rateunits">
     <xsl:choose>
        <xsl:when test="$physiolunits = 'true'">per_ms</xsl:when>
        <xsl:otherwise>per_s</xsl:otherwise>
    </xsl:choose>
</xsl:variable>


<!--Main template-->

<xsl:template match="/cml:channelml">
<xsl:if test="$includeComments='1'">
<xsl:comment>This is a PSICS channel model file generated from a ChannelML v1.8.0 file.</xsl:comment>
</xsl:if>
 
<xsl:if test="count(meta:notes) &gt; 0 and $includeComments='1'">
    <xsl:comment>
    <xsl:value-of select="meta:notes"/>
    </xsl:comment>
</xsl:if>


<xsl:choose>
<xsl:when test="count(cml:channel_type/cml:current_voltage_relation/cml:integrate_and_fire) &gt; 0">
    <xsl:comment>Error: this channel contains an Integrate and Fire mechanisms that cannot be mapped to PSICS.</xsl:comment>
</xsl:when>

<xsl:otherwise>
<xsl:apply-templates  select="cml:channel_type"/>
</xsl:otherwise>
</xsl:choose>

</xsl:template>
<!--End Main template-->


<xsl:template match="cml:channel_type">

     <xsl:choose>
            <xsl:when test="count(//cml:voltage_conc_gate) &gt; 0">
            <xsl:comment>Error: the channel has a voltage_conc gate that is not supported in PSICS</xsl:comment>
            </xsl:when>
            <xsl:when test="count(//cml:conc_dependence) &gt; 0">
            <xsl:comment>Error: the channel has a conc dependent gate that is not supported in PSICS</xsl:comment>
            </xsl:when>
            <xsl:otherwise></xsl:otherwise>
     </xsl:choose>

    <xsl:apply-templates select="cml:current_voltage_relation">
        <xsl:with-param name="name" select="@name"/>
    </xsl:apply-templates>
</xsl:template>


<xsl:template match="cml:current_voltage_relation">
    <xsl:param name="name" select="missing_name"/>
    <KSChannel  id="{$name}" permeantIon ="{@ion}" gSingle="10pS">
        <xsl:apply-templates select="cml:gate"/>
        <xsl:if test="count(cml:gate) = 0">
            <OpenState id="o1"/>
        </xsl:if>
    </KSChannel>
</xsl:template>


<xsl:template match="cml:gate">
    <KSComplex instances="{@instances}">
        <xsl:apply-templates select="cml:closed_state"/>
        <xsl:apply-templates select="cml:open_state"/>
        <xsl:apply-templates select="cml:transition"/>
    </KSComplex>
</xsl:template>


<xsl:template match="cml:closed_state">
    <ClosedState id="{@id}"/>
</xsl:template>

<xsl:template match="cml:open_state">
    <OpenState id="{@id}"/>
</xsl:template>

<xsl:template match="cml:transition">
    <xsl:choose>
        <xsl:when test="@expr_form = 'exp_linear'">
            <ExpLinearTransition from="{@from}" to="{@to}"
                rate="{@rate}{$rateunits}" scale="{@scale}{$vunits}" midpoint="{@midpoint}{$vunits}"/>

        </xsl:when>


        <xsl:when test="@expr_form = 'exponential'">
            <ExpTransition from="{@from}" to="{@to}"
                rate="{@rate}{$rateunits}" scale="{@scale}{$vunits}" midpoint="{@midpoint}{$vunits}"/>
        </xsl:when>


        <xsl:when test="@expr_form = 'sigmoid'">
            <!-- Note the different use of scale in ChannelML!! -->
            <xsl:variable name="psicsScale" select="number(@scale) * -1"/>
            <SigmoidTransition from="{@from}" to="{@to}"
                rate="{@rate}{$rateunits}" scale="{$psicsScale}{$vunits}" midpoint="{@midpoint}{$vunits}"/>
        </xsl:when>


        <xsl:otherwise>
            <xsl:comment>unsupported transition type <xsl:value-of select="@expr_form"/></xsl:comment>
        </xsl:otherwise>


    </xsl:choose>

</xsl:template>


</xsl:stylesheet>
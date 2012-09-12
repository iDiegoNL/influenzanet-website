<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:s="http://dndg.it/ns/pollster-1.0"
 xmlns="http://www.w3.org/1999/xhtml">
<xsl:template match="s:survey">
 <style><![CDATA[
	html * { margin: 0; padding: 0 }
	h1 { font-size: 1.2em; margin: 0 .5em .5em .5em }
	h2 { font-size: 1em; margin: 0 .5em .5em .5em }
	#survey { margin: 1em; padding: .5em; border: 2px solid #E66101 }
	.question { margin: 1em; padding: .5em; border: 2px solid #EEE; border-radius: .3em}
	.types span { margin-left: .5em }
	.option div { display:inline; margin-left: .2em	}
	
	.option .value { 	}
	.flags { padding: .4em; }
	.flags span { padding: .2em; border: 1px solid #DDD; border-radius: .4em; color: white; font-weight: bold; font-size: .8em; background-color: #DDD }
	.dataname { font-weight: bold; color: #999 }
	
	.flags span.mandatory { background-color: red; font-weight: bold; border-color: red }
	.flags span.virtual { background-color: green; font-weight: bold; border-color: green }
	.flags span.open { background-color: pink; font-weight: bold; border-color: pink }
	
	.value { margin-left: .3em; font-weight: bold; color: #999 }
	.value:before { content:"[" }
	.value:after { content:"]" }
	
	.rule-name { font-weight: bold; }
 ]]></style>
 <div id="survey">
  <h1><xsl:value-of select="s:title"/> [<xsl:value-of select="s:shortname"/>]</h1>
  
  <xsl:apply-templates select="s:questions/s:question"/>

 </div>
</xsl:template>

<xsl:template match="s:question">
<div class="question">
	<xsl:variable name="id" select="@id"/>
	<h2><xsl:value-of select="s:title"/></h2>
	<div class="types">
		<span class="id"><xsl:value-of select="$id"/></span>
		<span class="dataname"><xsl:value-of select="s:data_name"/></span>
		<span class="type"><xsl:value-of select="s:type"/></span>
		<span class="data_type"><xsl:value-of select="s:data_type"/></span>
	</div>
	<div class="flags">
	<xsl:if test="s:starts_hidden='true'">
		<span class="hidden">hidden</span>
	</xsl:if>
	<xsl:if test="s:is_mandatory='true'">
		<span class="mandatory">mandatory</span>
	</xsl:if>
    </div>
	<ul class="options">
		<xsl:apply-templates select="s:options/s:option"/>
	</ul>
	<ul class="rules">
	<xsl:apply-templates select="/s:survey/s:rules/s:rule/s:subject_question[@ref=$id]/parent::node()"/>
	</ul>
</div>
</xsl:template>

<xsl:template match="s:option">
<li class="option">
	<div class="group"><xsl:value-of select="s:group"/></div>
	<div class="dataname"><xsl:value-of select="s:data_name"/></div>
	<div class="flags">
	<xsl:if test="s:is_virtual='true'">
		<span class="virtual">virtual</span>
	</xsl:if>
	<xsl:if test="s:is_open='true'">
		<span class="is_open">open</span>
	</xsl:if>
	<xsl:if test="s:starts_hidden='true'">
		<span class="hidden">hidden</span>
	</xsl:if>
    </div>
	<div class="text"><xsl:value-of select="s:text"/></div>
	<div class="value"><xsl:value-of select="s:value"/></div>
</li>
</xsl:template>

<xsl:template match="s:rule">
 <li>
	when option <xsl:for-each select="s:subject_options/s:subject_option">
	 <xsl:variable select="@ref" name="opt"/>
	  "<xsl:value-of select="//s:option[@id=$opt]/s:value"/>",
	</xsl:for-each>
	apply <span class="rule-name"><xsl:value-of select="substring(s:type,20)"/></span> to <xsl:value-of select="s:object_question/@ref"/>
 </li>
</xsl:template>

</xsl:stylesheet>

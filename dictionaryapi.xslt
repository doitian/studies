<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:regexp="http://exslt.org/regular-expressions"
  extension-element-prefixes="regexp"
  >

  <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
  <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
  <xsl:variable name="ew" select="*/entry[1]/ew/text()" />

  <xsl:key name="vt" match="*[name() != 'vt']" use="generate-id(preceding-sibling::vt[1])"/>
  <xsl:key name="sn_outer" match="sn[regexp:match(., '^[a-z]')]" use="generate-id(preceding-sibling::sn[regexp:match(., '^[0-9]')][1])"/>
  <xsl:key name="sn_inner" match="dt|slb" use="generate-id(preceding-sibling::sn[1])"/>

  <xsl:template match="/">
    <dl>
      <xsl:apply-templates select="*" />
    </dl>
  </xsl:template>

  <xsl:template match="entry">
    <xsl:if test="ew = $ew">
      <dt>
        <xsl:apply-templates select="fl" />&#160;<xsl:apply-templates select="pr" /><xsl:apply-templates select="vr" />
      </dt>
      <dd style="margin:0;padding:0;">
        <xsl:apply-templates select="def" />
        <!--xsl:if test="uro|dro">
          <ul style="list-style:none;padding-left:0;">
            <xsl:apply-templates select="uro|dro" />
          </ul>
        </xsl:if-->
        <!--xsl:apply-templates select="et" /-->
      </dd>
    </xsl:if>
  </xsl:template>

  <xsl:template match="pr">
    <code>\ <xsl:value-of select="." /> \</code>
  </xsl:template>
  <xsl:template match="def">
    <xsl:choose>
      <xsl:when test="vt">
        <xsl:for-each select="vt">
          <p><xsl:value-of select="." /></p>
          <xsl:choose>
            <xsl:when test="key('vt', generate-id())[name() = 'sn']">
              <ol style="margin:0;padding:0 0 0 1.5em;">
                <xsl:apply-templates select="key('vt', generate-id())[name() = 'sn' and regexp:match(., '^[0-9]')]" />
              </ol>
            </xsl:when>
            <xsl:otherwise>
              <ol style="list-style:none;margin:0;padding:0 0 1.5em;">
                <li><xsl:apply-templates select="key('vt', generate-id())" /></li>
              </ol>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
      </xsl:when>
      <xsl:when test="sn">
        <ol style="margin:0;padding:0 0 0 1.5em;">
          <xsl:apply-templates select="sn[regexp:match(., '^[0-9]')]" />
        </ol>
      </xsl:when>
      <xsl:otherwise>
        <ol style="list-style:none;margin:0;padding:0 0 1.5em;">
          <li><xsl:apply-templates select="*" /></li>
        </ol>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template match="et">
    <strong style="font-size:0.8em;">ETYMOLOGY</strong>
    <p><xsl:apply-templates /></p>
  </xsl:template>
  <xsl:template match="sn[regexp:match(., '^[0-9]')]">
    <li>
      <p>
        <xsl:if test="contains(., ' ')"><span style="padding-right:0.3em"><xsl:value-of select="substring-after(., ' ')" /></span></xsl:if>
        <xsl:apply-templates select="key('sn_inner', generate-id())" />
      </p>
      <xsl:apply-templates select="key('sn_outer', generate-id())" />
    </li>
  </xsl:template>
  <xsl:template match="sn">
    <p><span style="padding-right:0.3em"><xsl:value-of select="." /></span><xsl:apply-templates select="key('sn_inner', generate-id())" /></p>
  </xsl:template>
  <xsl:template match="dt">
    <xsl:for-each select="* | text()">
      <xsl:choose>
        <xsl:when test="position() = 1">
          <span style="padding-right:0.3em">:</span><xsl:value-of select="substring(., 2)" />
        </xsl:when>
        <xsl:when test="self::text()">
          <xsl:value-of select="." />
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates select="." />
        </xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="slb">
    <em style="padding-right:0.3em"><xsl:value-of select="." /></em>
  </xsl:template>
  <xsl:template match="uro">
    <li>
      <strong>— <xsl:value-of select="ure" /></strong>&#160;
      <xsl:apply-templates select="pr" />&#160;<xsl:apply-templates select="fl" /><xsl:apply-templates select="def" />
    </li>
  </xsl:template>
  <xsl:template match="dro">
    <li>
      <strong>— <xsl:value-of select="drp" /></strong>&#160;
      <xsl:apply-templates select="pr" />&#160;<xsl:apply-templates select="fl" /><xsl:apply-templates select="def" />
    </li>
  </xsl:template>
  <xsl:template match="date">
    <xsl:value-of select="." />
  </xsl:template>
  <xsl:template match="it|fl|d_link|dxt">
    <em><xsl:value-of select="." /></em>
  </xsl:template>
  <xsl:template match="vi">
    <span style="color:#5690B1;"> • </span><em><xsl:value-of select="." /></em>
  </xsl:template>
  <xsl:template match="sx">
    <span style="font-size:0.8em;"><xsl:value-of select="translate(., $lowercase, $uppercase)" /></span>
  </xsl:template>
  <xsl:template match="date"></xsl:template>
  <xsl:template match="sd">;<em style="padding:0 0.3em;"><xsl:value-of select="." /></em></xsl:template>
  <xsl:template match="vr"><xsl:apply-templates select="pr" /></xsl:template>
</xsl:stylesheet>

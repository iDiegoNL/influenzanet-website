#!/usr/bin/python

from datetime import date, timedelta
import subprocess

today = date.today()
if today.day != 1:
    exit()


METADATA = """<em:em xmlns:em="http://epiwork.di.fc.ul.pt/metadata/">
	<em:epidemiological>
		<em:diagnosticMethod />
		<em:disease>Flu</em:disease>
		<em:drug />
		<em:hostSp>human</em:hostSp>
		<em:hostGroup />
		<em:pathoSp />
		<em:pathoGroup />
		<em:pathoStrain>H1N1</em:pathoStrain>
		<em:vaccine />
		<em:vector />
	</em:epidemiological>
	<em:typeOfDoc>survey data</em:typeOfDoc>
	<em:title>Epiwork 5 Survey Data</em:title>
	<em:subject>Epidemiology</em:subject>
	<em:generalDescription>
		<em:abstract>Influenzanet is a system to monitor the activity of influenza-like-illness (ILI) with the aid of volunteers via the internet. These are the results of this survey for the country %(country_code)s and the period %(month)s</em:abstract>
		<em:citation />
		<em:DOI />
		<em:ISBN />
		<em:ISSN />
		<em:format>text/csv</em:format>
		<em:language />
		<em:pubmedID />
		<em:type>Epidemiological data</em:type>
		<em:URL />
		<em:version />
	</em:generalDescription>
	<em:date>2009-01-01T01:00:00Z</em:date>
	<em:dateSubmitted>2012-03-15T17:20:08Z</em:dateSubmitted>
	<em:organisation>
		<em:orgName>Influenzanet</em:orgName>
		<em:orgURL>http://www.influenzanet.eu/</em:orgURL>
	</em:organisation>
	<em:publisher>
		<em:pubName>Klaas van Schelven</em:pubName>
		<em:pubOrg>Influenzanet</em:pubOrg>
		<em:pubURL />
		<em:pubUserName>epidb</em:pubUserName>
	</em:publisher>
	<em:temporal>
        <em:tempFrom>%(begin)sT00:00:00Z</em:tempFrom>
        <em:tempTo>%(end)sT23:59:59Z</em:tempTo>
  	</em:temporal>
</em:em>"""

for country_code in ['BE', 'uk', 'IT', 'PT', 'NL']:
    begin = today - timedelta(30)
    begin = date(begin.year, begin.month, 1)
    begin = "%04d-%02d-%02d" % (begin.year, begin.month, begin.day)

    end = today - timedelta(1)
    end = "%04d-%02d-%02d" % (end.year, end.month, end.day)

    month = begin[:7]

    subprocess.call("""echo "COPY (select * from pollster_ili_incidence('%(begin)s', '%(end)s', '%(country_code)s')) TO stdout WITH CSV HEADER;" | psql > /home/epidb/data/incidence-%(month)s-%(country_code)s.csv""" % locals(), shell=True)

    f = open("/home/epidb/data/incidence-%(month)s-%(country_code)s.metadata" % locals(), "w")
    f.write(METADATA % locals())
    f.close()

    subprocess.call("""./SimpleEmClient.py  -u /home/epidb/data/incidence-%(month)s-%(country_code)s.csv empid:1 /home/epidb/data/incidence-%(month)s-%(country_code)s.metadata -Uepidb -pxxxx""" % locals(), shell=True)
    

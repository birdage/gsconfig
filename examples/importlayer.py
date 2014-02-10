from geoserver.catalog import Catalog
from geoserver.layer import Layer
from geoserver.store import coveragestore_from_index, datastore_from_index, \
    DataStore, CoverageStore, UnsavedDataStore, UnsavedCoverageStore
from geoserver.style import Style
from geoserver.support import prepare_upload_bundle
from geoserver.layergroup import LayerGroup, UnsavedLayerGroup
from geoserver.workspace import workspace_from_index, Workspace
from geoserver.resource import FeatureType
from geoserver.support import prepare_upload_bundle, url

style_to_check = "point"
cat = Catalog("http://localhost:8080/geoserver/rest", "admin", "admin")
ooiDataStore = "ooi"
ooiworkspace = "geonode"

#update layer
that_layer = cat.get_layer("1k time varying test")
that_layer.enabled = False
# at this point that_layer is still published in GeoServer
cat.save(that_layer)
# now it is disabled

that_layer = cat.get_layer("1k time varying test")
that_layer.enabled = True
cat.save(that_layer)

ooitest = cat.get_workspace("ooi_test")
data = cat.get_resources(store="asd",workspace="geonode")
print data
layer = cat.get_layer("1k time varying test")
print layer.href
cat.add_data_to_store
print layer

#drop those things not of interest

wmstest = cat.get_workspace("geonode")

try:
    wmsstore = cat.get_store("ooi")
    cat.delete(wmsstore)
except:
    print "opps"    


#create the data store
wmsstore = cat.create_datastore("ooi", wmstest)
wmsstore.capabilitiesURL = "http://www.geonode.org/"
wmsstore.type = "PostGIS"
#connection info

params = {
    'Connection timeout': '20',
    'Estimated extends': 'true',
    'Expose primary keys': 'false',
    'Loose bbox': 'true',
    'Max open prepared statements': '50',
    'database': 'postgres',
    'dbtype': 'postgis',
    'encode functions': 'false',
    'fetch size': '1000',
    'host': 'localhost',
    'max connections': '10',
    'min connections': '1',
    'namespace': 'http://www.geonode.org/',
    'port': '5432',
    'preparedStatements': 'false',
    'schema': 'public',
    'user': 'rpsdev',
    'validate connections': 'true'
    }

wmsstore.connection_parameters = params
#could be added!
#'Session startup SQL': 'drop view IF EXISTS covproj;\nselect runCovTest();\nCREATE or replace VIEW covproj as \nSELECT ST_SetSRID(ST_MakePoint(lon, lat),4326) as proj, dataset_id, time, cond, temp from covtest;',

#MUST SAVE IT!
cat.save(wmsstore)


#curl -v -u admin:admin -XGET http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/asd/featuretypes.xml
#import requests
#r = requests.get('http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/asd/featuretypes.xml', auth=('admin', 'admin'))
import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
r, content = h.request("http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/ooi/featuretypes.xml", "GET")

print content
print "----------------\n"

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

xml = """ 
<featureType>
  <name>qwewqeqweqwe</name>
  <nativeName>sdfsdfsdf</nativeName>
  <namespace>
    <name>geonode</name>
    <atom:link xmlns:atom="http://www.w3.org/2005/Atom\" rel=\"alternate\" href=\"http://localhost:8080/geoserver/rest/namespaces/geonode.xml\" type=\"application/xml\"/>
  </namespace>
  <title>geoserverlayer</title>
  <keywords>
    <string>geoserverlayer</string>
    <string>features</string>
  </keywords>
  <srs>EPSG:4326</srs>
  <nativeBoundingBox>
    <minx>-1.0</minx>
    <maxx>0.0</maxx>
    <miny>-1.0</miny>
    <maxy>0.0</maxy>
  </nativeBoundingBox>
  <latLonBoundingBox>
    <minx>-1.0</minx>
    <maxx>0.0</maxx>
    <miny>-1.0</miny>
    <maxy>0.0</maxy>
  </latLonBoundingBox>
  <projectionPolicy>FORCE_DECLARED</projectionPolicy>
  <enabled>true</enabled>
  <metadata>
    <entry key=\"cachingEnabled\">false</entry>
    <entry key=\"JDBC_VIRTUAL_TABLE\">
      <virtualTable>
        <name>geoserverlayer</name>
        <sql>select count(*)</sql>
        <escapeSql>false</escapeSql>
      </virtualTable>
    </entry>
  </metadata>
  <store class=\"dataStore\">
    <name>ooi</name>
    <atom:link xmlns:atom=\"http://www.w3.org/2005/Atom\" rel=\"alternate\" href=\"http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/ooi.xml\" type=\"application/xml\"/>
  </store>
  <maxFeatures>0</maxFeatures>
  <numDecimals>0</numDecimals>
  <attributes>
    <attribute>
      <name>count</name>
      <minOccurs>0</minOccurs>
      <maxOccurs>1</maxOccurs>
      <nillable>true</nillable>
      <binding>java.lang.Long</binding>
    </attribute>
  </attributes>
</featureType>"""

r, content = h.request("http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/ooi/featuretypes", "POST",
                       body=xml, headers={'content-type':'application/xml'} )
print r['status']


print "----------------\n"
r, content = h.request("http://localhost:8080/geoserver/rest/workspaces/geonode/datastores/ooi/featuretypes.xml", "GET")
print 
print content
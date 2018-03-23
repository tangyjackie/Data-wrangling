from pymongo import MongoClient 

# The Toronto OSM file is approximately 1.223 GB, and the size of the uncompressed file was 83 MB.

import xml.etree.cElementTree as ET
import pprint
import re

#The code below calculates the number of unique contributors to the Toronto Open Street Map
def get_user(element):
    if "uid" in element.attrib:
      return element.attrib("uid")


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if "uid" in element.attrib:
            users.add(element.attrib.get("uid"))
            users.discard(None)

    return users

def test():

    users = process_map('/Users/Jackie/Downloads/toronto_canada.osm')
    pprint.pprint(len(users))

#test()
#The Toronto OSM file has 2743 unique contributors as of July 30th, 2017.

def count_tags(filename):
        tags = {}
        for event, element in ET.iterparse(filename):
            if element.tag in tags:
                tags[element.tag] += 1
            else:
                tags[element.tag] = 1
        return tags
    
#count_tags('/Users/Jackie/Downloads/toronto_canada.osm')





lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    
    if element.tag == "tag":
        k = element.attrib['k']
        if len(lower.findall(k)) > 0:
            keys["lower"]  += 1
        elif len(lower_colon.findall(k)) > 0:
            keys["lower_colon"] += 1
        elif len(problemchars.findall(k)) >0:
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
        
    return keys



#def process_map(filename):
#    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
#    for _, element in ET.iterparse(filename):
#        keys = key_type(element, keys)

#    return keys

#process_map('/Users/Jackie/Downloads/interpreter')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

from datetime import datetime
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

POS = ["lat", "lon"]

def clean_postcode(postcode):
    postcode = postcode.upper()

    return postcode

def check_lower_letters(filename, pretty = False):
	postcodes = set() 
	for event, elem in ET.iterparse(filename): 
		for child in elem: 
			if child.tag == 'tag': 
				if child.attrib['k'] == 'addr:postcode':
					postcodes.add(child.attrib['v'])
					#for i in postcodes:
						#print len(lower.findall(i))
						#sum = 0					
						#sum += len(lower.findall(i))
						#print sum
	new_postcodes = set()
	for postcode in postcodes:
		new_postcode = clean_postcode(postcode)
		new_postcodes.add(new_postcode)
						#print new_postcodes
	
	s = 0
	for item in new_postcodes:
		s += len(lower.findall(item))
	print s
			#print lower.findall(item)
			#break
					


#check_lower_letters('/Users/Jackie/Downloads/toronto_canada.osm', pretty = False)

#Write a function that removes the addr:interpolation field when other addr:street fields are not present
#It does not make sense to have this field when no street address is known since the value 'odd' and 'even' indicate the 


city_list = ["City of Hamilton", "City of Oshawa", "Town of Niagara-On-The-Lake", "Town of New Tecumseth", "Town of Bradford West Gwillimbury", "Town of Mono",
"City of St. Catharines", "Orangeville", "Township of Adjala-Tosorontio", "Town of Grimsby", "Hamilton", "Township of Guelph/Eramosa", "Township of Mulmur", 
"Township of Puslinch", "Township of East Garafraxa", "Carlisle", "Township of Amaranth", "Township of Essa", "City of Kawartha Lakes", "Town of Innisfil",
"Stoney Creek", "Port Perry", "Mono", "Niagara-On-The-Lake", "Waterdown", "Campbellville", "?", "Orangeville", "Bradford", "Lynden", "Ancaster", "Niagara-on-the-Lake",
"Ballinafad", "Orangeville", "Youngstown", "Township of Adjala-Tosorontio (Rosemont)", "Alliston", "Kailua", "Virgil", "Puslinch", "Fort Myers", "Rockton","Rockwood", "Erin",
"Town of Erin", "Dundas"]
							
def shape_element(element):
    node = {}
    created = {}
    address = {}
    amenity = {}
    shop = {}
    pos = [0,0]
    node_refs = []
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        
        for a in element.attrib.keys():
            if a in CREATED:
                #insert key:value pair into created dictionary 
				created[a] = element.attrib[a]

            elif a in ['lat', 'lon']:
                if a == 'lat':
                    pos[0] = float(element.attrib[a])
            
                elif a == 'lon':
                    pos[1] = float(element.attrib[a])

            else:
                node[a] = element.get(a)	
		
		
	    #for subtag in element:
		#	if subtag.tag == 'tag':
		#		if subtag.attrib['k'] == 'addr:postcode':
		#			postcode = clean_postcode(subtag.attrib['v'])
		
        for subtag in element:
            if subtag.tag == 'tag':
				
                if subtag.attrib['k'] == 'addr:interpolation':
					continue
				
                # if the tag has problematic characters, ignore it and just continue
                elif re.search(problemchars, subtag.get('k')):
                    continue		
				
				#Remove elements that are in the city_list (which represents cities that are not in the Greater Toronto Area)
                elif subtag.attrib['k'] == 'addr:city':
                    if subtag.attrib['v'] in city_list:
                        return
                
				# if the tag starts with addr:, add to the dictionary "address"
                if subtag.get('k').startswith('addr:'):

						key = subtag.get('k')[5:]
						#if key == 'interpolation':
						#	address[key] = []
						
						if key == 'postcode':
							address[key] = subtag.get('v')
							#This is to ensure that all postcodes are uppercase
							address[key] = address[key].upper()
							#This if condition ensures that all postcodes have at least one space in between the first 3 letters and last 3 letters
							#This is how postal codes are written in Canada
							if address[key][3:4] != " ": 
							#!= (address['postcode'][:3] + " " + address['postcode'][4:]):
								address[key] = address[key][:3] + " " + address[key][3:]
						elif key != 'postcode':
							address[key] = subtag.get('v')
						if address:
							#print address
							if address.get('postcode'):
								k = address['postcode']
								s = len(lower.findall(k))
								if s > 0:
									print "PROBLEM, there exist lower case postal code letters!"
								#elif no_space_re.search(k):
								#	k = k[:3] + " " + k[3:]
							#remove elements where addr:interpolation fields are present without addr:street are not
							#if address.get('interpolation'):
						#if address.get('street') == None:
						#	address = {}
						
						
                elif subtag.get('k') == 'amenity':
					key = subtag.get('k')
					value = subtag.get('v')
					node['amenity'] = value
					
				
                elif subtag.get('k') == 'shop':
					key = subtag.get('k')
					value = subtag.get('v')
					node['shop'] = value
				
                elif subtag.get('k') == 'cuisine':
					value = subtag.get('v')
					node['cuisine'] = value
				
                elif subtag.get('k') == 'name':
					value = subtag.get('v')
					node['name'] = value
				
                else	: node[subtag.get('k')] = subtag.get('v')
			
                #add ref attributes to a the node_refs dictionary
				
		    
		if subtag.tag == 'nd':
			    node_refs.append(subtag.get('ref'))


			
    if created:
        node['created'] = created
    if address:
        node['address'] = address
    
    if node_refs:
        node['node_refs'] = node_refs
    if pos != [0,0]:
       node['pos'] = pos
    if amenity:
	   node['amenity'] = amenity
    if shop:
		node['shop'] = shop
    if node:
        return node
    else:
        return None
    
    print node
    return node


#with open('C:\\MongoDB\\Server\\3.4\\bin\\interpreter.json', 'r') as f:
 #   for line in f:
  #      if 'interpolation' in line:
   #         print line
	
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
	

process_map('/Users/Jackie/Downloads/toronto_canada.osm', pretty = False)
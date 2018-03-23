from pymongo import MongoClient
import pprint
client = MongoClient('mongodb://localhost:27017/')

db = client.db_test8b
coll = db.collection_test

print '\nFirst document:', coll.find_one()

#SUMMARY STATISTICS
def num_documents():
	documents_num = coll.find().count()
	print documents_num

def num_nodes():
	nodes_num = coll.find({"type": "node"}).count()
	print nodes_num

def unique_users():
	users = len(coll.distinct("created.user"))
	print users

def find():
    cursor = coll.aggregate([{"$match":{"amenity":{"$exists":1}}}, 
    {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])

    for documents in cursor:
        print documents

def find1():
    cursor = coll.aggregate([{"$match":{"shop":{"$exists":1}}}, 
    {"$group":{"_id":"$shop", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])

    for documents in cursor:
        print documents		

def find2():
	
	cursor1 = coll.aggregate([{"$match":{"address": {"$exists":1}}}, 
    {"$group":{"_id":"$address", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])

	for documents in cursor1:
	    print documents


def find3():
    cursor = coll.aggregate([{"$match":{"cuisine":{"$exists":1}}}, 
    {"$group":{"_id":"$cuisine", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])

    for documents in cursor:
        print documents				

def find5():
    cursor = coll.aggregate([{"$match":{"building":{"$exists":1}}}, 
    {"$group":{"_id":"$building", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])

    for documents in cursor:
        print documents			

def find6():
    cursor = coll.aggregate([{"$match":{"address.postcode":{"$exists":1}}}, 
    {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])

    for documents in cursor:
        print documents		

def find7():
    cursor = coll.aggregate([{"$match":{"created.user":{"$exists":1}}}, 
    {"$group":{"_id":"$created.user", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":10}])
	
	
    for documents in cursor:
        print documents	
		
#Look at cities and which ones are represented the most in the data

def find8():
	cursor = coll.aggregate([{"$match":{"address.city":{"$exists":1}}}, 
    {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, 
    {"$sort":{ "count" : -1}}, 
    {"$limit":100}])
    
	for documents in cursor:
			print documents	
		
if __name__ == '__main__':
	#print '\nNumber of documents: \n', num_documents()
	#print '\nNumber of nodes: \n', num_nodes()
	print '\nNumber of unique users: \n', unique_users()
	print '\nTop 10 Amenities: \n' , find()
	print '\nTop 10 Shops: \n' , find1()
	#print '\nTop 10 Addresses: \n' , find2()
	print '\nTop 10 Cuisines: \n' , find3()
	print '\nTop 10 Buildings: \n', find5()
	print '\nTop 10 Postcodes:\n', find6()
	print '\nTop 10 Users:\n', find7()
	print '\nTop 10 Cities:\n', find8()

#Investigative query
#One suggestion for improvement would be that many building types are classified as "yes", but what does is yes refer to?
#Code below shows some of the entries in which building types were classified as "yes"


def building_types():
	bldg = coll.find({"building": "yes"}).limit(5)
	
	for i in bldg:
		print i
#building_types()
#It can be easily seen from the first few entries that the names can give some indication of what the building should be classified as
#These include arenas, community centres etc. and a simple query on the name field such as if name contains the word arena, community
#then building = public and amenity = recreation

#Further investigative query
#There are 15000 houses, which is abnormally low
def house_types():
	house = coll.find({"building": "house"}).limit(10)
	
	for i in house:
		print i
#house_types()		

def shop_vacancies():
	vacant = coll.find({"shop": "vacant"}).limit(10)
	
	for i in vacant:
		print i
#shop_vacancies()	

	
def find4():
		cursor = coll.find({"address.interpolation": 'odd'})
		for i in cursor:
			print i
#find4()
	
	
#show that the 1st problem with the postal codes having some lower case letters has been corrected
def find3():
	coll.aggregate([{"$match": {"address.postcode": {"$exists":1}}},
	{"$project":{"address.postcode": {"$toUpper": "$address.postcode"}}}])

	coll.aggregate([
	{"$project":{"address.postcode": {"$toUpper": "$address.postcode"}}}, {"$out": "results"}])
	
	coll.aggregate([{"$project":{"address.postcode": { "$toUpper": "$address.postcode" }}}])
	
	cursor = coll.find({"address.postcode": "M2N 6K7"})
	
	#lower = re.compile(r'^([a-z]|_)*$')	
	
	
	for documents in cursor:
		print documents

#find3()
#check to see if the postal code problem has been created by running query on example that had lower case

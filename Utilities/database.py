import pymongo
from Environment import DATABASE_DC

def check_database_connection() :
	try :
		client = MongoClient()
		client.server_info()
		port = client.address[1]
		return (True, f"Database connection successful on port {port}")
	except :
		return (False, "Database connection failed")

class MongoClient(pymongo.MongoClient):

	__user_info_collection_define = DATABASE_DC.COLLECTION_NAMES["__user_info_collection_define"]
	__user_data_collection_define = DATABASE_DC.COLLECTION_NAMES["__user_data_collection_define"]

	def __init__(self, connection_string=None, db_name=None):
		if db_name is None:
			db_name = DATABASE_DC.DATABASE_NAME
		if connection_string is None:
			connection_string = DATABASE_DC.CONNECTION_STRING
		super().__init__(connection_string)

		self.db = self[db_name]
		self.user_info = UserInfo(self, self.db, self.__user_info_collection_define)
		self.user_data = UserData(self, self.db, self.__user_data_collection_define)

	def get_all_user_ids(self):
		return self.user_info.distinct("_id")
	
	def documentisize(self, data) :

		user_info_document = {
			"_id" : data["student_national_id"],
			"student_school_id" : data["student_school_id"],
			"student_name" : data["student_name"],
			"student_surname" : data["student_surname"],
			"student_faculty" : data["student_faculty"],
			"student_department" : data["student_department"],
			"language_of_instruction" : data["language_of_instruction"],
			"student_status" : data["student_status"]
		}

		user_data_document = {
			"owner_id" : data["student_national_id"],
			"parsing_type" : data["parsing_type"],
			"parsing_language" : data["parsing_language"],
			"transcript_manager_date" : data["transcript_manager_date"],
			"transcript_creation_date" : data["transcript_creation_date"],
			"semesters" : data["semesters"],
			"original_course_list" : data["original_course_list"],
			"filtering" : None,
			"sorting" : None,
			"modified_course_list" : None,
			"document_name" : "Untitled Document",
			"updated_course_list" : None,
			"subtracted_course_list" : None,
			"added_course_list" : None,
		}

		return user_info_document, user_data_document

class UserInfo(pymongo.collection.Collection):
	def __init__(self, client, db, collection_name):
		super().__init__(db, collection_name)
		self.client = client

	def push_init(self, document) :
		filter = {"_id" : document["_id"]}
		update = {"$set" : document}
		result = self.update_one(filter, update, upsert=True)

		if result.matched_count == 1 :
			#print("User already exists")
			pass
		elif result.upserted_id is not None :
			#print("User added")
			pass

class UserData(pymongo.collection.Collection):
	def __init__(self, client, db, collection_name):
		super().__init__(db, collection_name)
		self.client = client     

	def push_init(self, document):
		
		owner_id = document["owner_id"]
		if owner_id not in self.client.get_all_user_ids() :
			#print("User not found, data is not pushed")
			return
		
		filter = { # Only one change between them is enough ! For example different name of document and etc ...
			"owner_id" : owner_id,
			"document_name" : document["document_name"],
		}

		if self.count_documents(filter) > 0 :
			#print("Same document already exists, data is not pushed")
			return
		
		self.insert_one(document)

	def get_available_documents(self, owner_id) :
		filter = {
			"owner_id" : owner_id,
		}
		projection = {
			"_id" : 0,
			"document_name" : 1,
		}
		
		#found = self.find(filter, projection)
		found = self.find(filter)

		return found
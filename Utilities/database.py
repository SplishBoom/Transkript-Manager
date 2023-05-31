from 	Environment	import	DATABASE_DC # Database values & connection and config
import 	pymongo # Database connection

def check_database_connection() -> tuple:
	"""
	Method to check if securely connected to database
	@Parameters:
		None
	@Returns:
		(bool, str) : (True, "Database connection successful on port {port}") or (False, "Database connection failed")
	"""
	# Try to establish a connection to database
	try :
		client = MongoClient()
		client.server_info()
		port = client.address[1]
		# If connection is successful, return True
		return (True, f"Database connection successful on port {port}")
	except :
		# If connection is not successful, return False
		return (False, "Database connection failed")

class MongoClient(pymongo.MongoClient) :

	# Class fields
	__user_info_collection_define = DATABASE_DC.COLLECTION_NAMES["__user_info_collection_define"]
	__user_data_collection_define = DATABASE_DC.COLLECTION_NAMES["__user_data_collection_define"]

	def __init__(self, connection_string : str = None, db_name : str = None) -> None:
		"""
		Constructor method for MongoClient class, which is a wrapper for pymongo.MongoClient class
		@Parameters:
			connection_string - Optional : Connection string for database connection. (str) (default = None) -> Used to connect to database
			db_name - Optional : Database name to connect. (str) (default = None) -> Used to connect to database
		@Returns:
			None
		"""
		# Check for database connection config, for ungivens load the default ones from DATABASE_DC
		if db_name is None:
			db_name = DATABASE_DC.DATABASE_NAME
		if connection_string is None:
			connection_string = DATABASE_DC.CONNECTION_STRING
		# Initialize MongoClient class
		super().__init__(connection_string)

		# Initialize database and collections
		self.db = self[db_name]
		self.user_info = UserInfo(self, self.db, self.__user_info_collection_define)
		self.user_data = UserData(self, self.db, self.__user_data_collection_define)

	def get_all_user_ids(self) -> list:
		"""
		Method to get all user ids from database
		@Parameters:
			None
		@Returns:
			(list) : List of all user ids
		"""
		# Return all user ids
		return self.user_info.distinct("_id")
	
	def documentisize(self, data : dict) -> tuple:
		"""
		Method to create user_info and user_data documents from given data
		@Parameters:
			data - Required : Data to create documents (dict) -> Used to create documents
		@Returns:
			(tuple) : Tuple of user_info and user_data documents
		"""
		# Create user_info from given data
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

		# Create user_data from given data (INITIALIZE WITH NONE !)
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
			"document_name" : "Transcript Document",
			"updated_course_list" : None,
			"subtracted_course_list" : None,
			"added_course_list" : None,
		}

		# Return user_info and user_data documents
		return user_info_document, user_data_document

class UserInfo(pymongo.collection.Collection) :

	def __init__(self, client : pymongo.MongoClient , db : str, collection_name : str) -> None:
		"""
		Constructor method for UserInfo class, which is a wrapper for pymongo.collection.Collection class
		@Parameters:
			client - Required : MongoClient object (pymongo.MongoClient) -> Used to connect to database
			db - Required : Database name (str) -> Used to connect to database
			collection_name - Required : Collection name (str) -> Used to connect to database
		@Returns:
			None
		"""
		# Initialize pymongo.collection.Collection class
		super().__init__(db, collection_name)

		# Initialize client
		self.client = client

	def push_init(self, document : dict) -> None:
		"""
		Method to push user_info document to database
		@Parameters:
			document - Required : User_info document (dict) -> Used to push to database
		@Returns:
			None
		"""
		# Setup match variables
		filter = {"_id" : document["_id"]}
		update = {"$set" : document}

		# Apply filter and get result (NOW DATA IS ALSO PUSHED TO DATABASE !)
		result = self.update_one(filter, update, upsert=True)

		# Check for result - CURRENTLY NOT USED
		if result.matched_count == 1 :
			#print("User already exists")
			pass
		elif result.upserted_id is not None :
			#print("User added")
			pass

class UserData(pymongo.collection.Collection):

	def __init__(self, client : pymongo.MongoClient, db : str, collection_name : str) -> None:
		"""
		Constructor method for UserData class, which is a wrapper for pymongo.collection.Collection class
		@Parameters:
			client - Required : MongoClient object (pymongo.MongoClient) -> Used to connect to database
			db - Required : Database name (str) -> Used to connect to database
			collection_name - Required : Collection name (str) -> Used to connect to database
		@Returns:
			None
		"""
		# Initialize pymongo.collection.Collection class
		super().__init__(db, collection_name)

		# Initialize client
		self.client = client     

	def push_init(self, document : dict) -> None:
		"""
		Method to push user_data document to database
		@Parameters:
			document - Required : User_data document (dict) -> Used to push to database
		@Returns:
			None
		"""
		# Setup match variables
		owner_id = document["owner_id"]
		if owner_id not in self.client.get_all_user_ids() :
			#print("User not found, data is not pushed")
			return
		
		# Setup match variables
		filter = { # Only one change between them is enough ! For example different name of document and etc ...
			"owner_id" : owner_id,
			"document_name" : document["document_name"],
		}

		# Check if document already exists
		if self.count_documents(filter) > 0 :
			#print("Same document already exists, data is not pushed")
			return
		
		# Push applied document to database
		self.insert_one(document)

	def get_available_documents(self, owner_id : str) -> list:
		"""
		Method to get available documents of given user
		@Parameters:
			owner_id - Required : Owner id (str) -> Used to get available documents
		@Returns:
			(list) : List of available documents
		"""
		# Setup match variables
		filter = {
			"owner_id" : owner_id,
		}
		# Setup projection variables - NOT USED CURRENTLY
		projection = {
			"_id" : 0,
			"document_name" : 1,
		}
		
		#found = self.find(filter, projection)
		# Get available documents
		found = self.find(filter)

		# Return found documents
		return found
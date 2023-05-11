from Utilities import MongoClient, OfflineParser, OnlineParser
from dotenv import load_dotenv
import os


if __name__ == "__main__" :

    load_dotenv()

    # ------------------------------------------------------------------------

    test_file_paths = os.getenv("test_file_paths")[1:-1].replace(" ", "").replace("\"", "").split(",")

    parser = OfflineParser(path_to_file=test_file_paths[0], save_to_file=False)
    data1 = parser.get_transcript_data()

    parser = OfflineParser(path_to_file=test_file_paths[1], save_to_file=False)
    data2 = parser.get_transcript_data()

    parser = OfflineParser(path_to_file=test_file_paths[2], save_to_file=False)
    data3 = parser.get_transcript_data()

    # ------------------------------------------------------------------------

    connection_string = os.getenv("connection_string")
    database_name = os.getenv("database_name")

    client = MongoClient(connection_string, database_name)
    
    user_info_document, user_data_document = client.documentisize(data1)
    client.user_info.push_init(user_info_document)
    client.user_data.push_init(user_data_document)

    user_info_document, user_data_document = client.documentisize(data2)
    client.user_info.push_init(user_info_document)
    client.user_data.push_init(user_data_document)

    user_info_document, user_data_document = client.documentisize(data3)
    client.user_info.push_init(user_info_document)
    client.user_data.push_init(user_data_document)

    client.close()
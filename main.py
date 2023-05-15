from Utilities import MongoClient, OfflineParser, OnlineParser
from dotenv import load_dotenv
import os


if __name__ == "__main__" :

    load_dotenv()

    # ------------------------------------------------------------------------

    test_file_paths = eval(os.getenv("env_test_file_paths"))
    
    username = str(os.getenv("env_username"))
    password = str(os.getenv("env_password"))

    parser = OnlineParser(username=username, password=password)
    data0 = parser.get_transcript_data()

    parser = OfflineParser(path_to_file=test_file_paths[0])
    data1 = parser.get_transcript_data()

    parser = OfflineParser(path_to_file=test_file_paths[1])
    data2 = parser.get_transcript_data()

    parser = OfflineParser(path_to_file=test_file_paths[2])
    data3 = parser.get_transcript_data()

    # ------------------------------------------------------------------------

    connection_string = str(os.getenv("env_connection_string"))
    database_name = str(os.getenv("env_database_name"))

    client = MongoClient(connection_string, database_name)
    
    user_info_document, user_data_document = client.documentisize(data0)
    client.user_info.push_init(user_info_document)
    client.user_data.push_init(user_data_document)

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

    print("Done")
import pymongo
import datetime

def init_connection():
    #return pymongo.MongoClient("mongodb://localhost:27142")
     return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()


def LogChat(user_id, type_of_DB, user_input, chatbot_response, ps_time):
    db = client.DB_Eksamen
    db.Chats.insert_one({"user_id": user_id, "user_input": user_input, "chatbot_response": chatbot_response, "timestamp": datetime.datetime.now(), "type_of_DB": type_of_DB, "process_time": ps_time, "Score": 0, "Sentences": 0, "Contains_correct_awnser": None})

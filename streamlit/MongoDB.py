import streamlit as st
import pymongo
import datetime

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()

@st.cache_data(ttl=600)
def GetChatHistory(userId):
    db = client.DB_Eksamen
    items = db.Chats.find({"user_id": userId})
    return items

def InsertChatHistory(user_id, user_input, chatbot_response):
    db = client.DB_Eksamen
    db.Chats.insert_one({"user_id": user_id, "user_input": user_input, "chatbot_response": chatbot_response, "timestamp": datetime.datetime.now()})

def delete_chat_history(userid):
    db = client.DB_Eksamen
    db.Chats.delete_many({"user_id": userid})

def get_number_of_chats(userid):
    db = client.DB_Eksamen
    match = {"$match": {"user_id": userid}}
    group = {"$group": {"_id": "$user_id", "number of Chats": {"$sum": 1}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)
import streamlit as st
import pymongo
import datetime
import pandas as pd

# Initialize connection.
# Uses st.cache_resource to only run once.

def init_connection():
    #return pymongo.MongoClient("mongodb://localhost:27142")
     return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()


def GetChatHistory(userId):
    db = client.DB_Eksamen
    items = db.Chats.find({"user_id": userId})
    return items

def InsertChatHistory(user_id, user_input, chatbot_response, times):
    db = client.DB_Eksamen
    db.Chats.insert_one({"user_id": user_id, "user_input": user_input, "chatbot_response": chatbot_response, "timestamp": datetime.datetime.now(), "time": times})

def delete_chat_history(userid):
    db = client.DB_Eksamen
    db.Chats.delete_many({"user_id": userid})

def get_number_of_chats(userid):
    db = client.DB_Eksamen
    match = {"$match": {"user_id": userid}}
    group = {"$group": {"_id": "$user_id", "number of Chats": {"$sum": 1}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)


def number_of_score_and_sentences(type_of_DB, Contains_correct_awnser):
    db = client.DB_Eksamen
    match = {"$match": {"Contains_correct_awnser" : Contains_correct_awnser, "type_of_DB" : type_of_DB}}
    group = {"$group": {"_id": {"Score" : "$Score", "sentences": "$Sentences" }, "number of Chats": {"$sum": 1}}}
    pipeline = [ match, group]
    #Chats.find({"Contains_correct_awnser" : Contains_correct_awnser, "type_of_DB" : type_of_DB}, {"Score": 1, "Sentences": 1, "number of Chats": {"$sum": 1}}))
    return db.Chats.aggregate(pipeline)

def number_of_entries(type_of_DB):
    db = client.DB_Eksamen
    return db.Chats.count_documents({"type_of_DB" : type_of_DB})

def number_of_incorrect(type_of_DB):
    db = client.DB_Eksamen
    return db.Chats.count_documents({ "$and" : [ {"type_of_DB" : type_of_DB}, {"Contains_correct_awnser" : False} ]})

def number_of_correct(type_of_DB):
    db = client.DB_Eksamen
    return db.Chats.count_documents({ "$and" : [ {"type_of_DB" : type_of_DB}, {"Contains_correct_awnser" : True} ]})

def Score_precentence(type_of_DB):
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : type_of_DB}}
    group = {"$group": {"_id": "$Score", "numberOf": {"$sum": 1}}}
    project = {"$project": {"_id" : "$_id", "Percentage": {"$multiply": [ {"$divide" : ["$numberOf", number_of_entries(type_of_DB)] }, 100] } }}
    pipeline = [ match, group, project]
    #Chats.find({"Contains_correct_awnser" : Contains_correct_awnser, "type_of_DB" : type_of_DB}, {"Score": 1, "Sentences": 1, "number of Chats": {"$sum": 1}}))
    return db.Chats.aggregate(pipeline)

def percentes_of_I_dont_know():
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : {"$ne": "null"}, "chatbot_response" : {"$regex" : "I don't know"}}}
    total = number_of_entries("vector") + number_of_entries("graph") + number_of_entries("Vector_with_graph_as_context")
    group = {"$group": {"_id": "$type_of_DB", "numberOf": {"$sum": 1}}}
    project = {"$project": {"_id" : "$_id", "percentes": {"$multiply": [ {"$divide" : ["$numberOf", total] }, 100] } }}
    pipeline = [ match, group, project]
    return db.Chats.aggregate(pipeline)


def Rigth_and_wrong_awnser_all():
    db = client.DB_Eksamen
    match = {"$match": { "$or": [ { "type_of_DB" : "graph" }, { "type_of_DB": "vector" }, {"type_of_DB" : "Vector_with_graph_as_context"} ] }}
    group = {"$group": {"_id": "$user_input", "correct": {"$sum": {"$cond" : ["$Contains_correct_awnser",1,0]}}, "wrong": {"$sum": {"$cond" : ["$Contains_correct_awnser",0,1]}}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)

def Rigth_and_wrong_awnser(type_of_DB):
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : type_of_DB}}
    group = {"$group": {"_id": "$user_input", "correct": {"$sum": {"$cond" : ["$Contains_correct_awnser",1,0]}}, "wrong": {"$sum": {"$cond" : ["$Contains_correct_awnser",0,1]}}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)

def percent_accurcy(type_of_DB):
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : type_of_DB}}
    group = {"$group": {"_id": "$type_of_DB", "correct": {"$sum": {"$cond" : ["$Contains_correct_awnser",1,0]}}, "wrong":{"$sum": {"$cond" : ["$Contains_correct_awnser",0,1]}}}}
    project = {"$project": {"_id" : "$_id", "correct": "$correct", "wrong": "$wrong", "accurcy": {"$multiply": [ {"$divide" : [number_of_correct(type_of_DB), number_of_entries(type_of_DB)] }, 100] } }}
    pipeline = [ match, group, project]
    return db.Chats.aggregate(pipeline)

def avg_sentences():
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : {"$ne": "null"}}}
    group = {"$group": {"_id": "$type_of_DB", "avg number of sentences": {"$avg": "$Sentences"}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)

def avg_sentences_pr_score(type_of_DB):
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : type_of_DB}}
    group = {"$group": {"_id": "$Score", "avg number of sentences": {"$avg": "$Sentences"}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)


def avg_score():
    db = client.DB_Eksamen
    match = {"$match": {"type_of_DB" : {"$ne": "null"}}}
    group = {"$group": {"_id": "$type_of_DB", "avg score": {"$avg": "$Score"}}}
    pipeline = [ match, group]
    return db.Chats.aggregate(pipeline)
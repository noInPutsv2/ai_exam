import streamlit as st # type: ignore
import pyodbc # type: ignore

@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )


conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchone()

def check_login(username, password):
    query = f"SELECT id FROM dbo.users WHERE username = '{username}' AND password = '{password}'"
    with conn.cursor() as cur:
        if cur.execute(query).fetchone():
            return cur.execute(query).fetchone()[0]
    return False

def check_username(username):
    query = f"SELECT * FROM dbo.users WHERE username = '{username}'"
    with conn.cursor() as cur:
        if cur.execute(query).fetchone():
            return False
    return True

def register_user(email, username, password):
    query = f"INSERT INTO dbo.users (email, username, password) VALUES ('{email}', '{username}', '{password}')"
    with conn.cursor() as cur:
        return cur.execute(query)
    
def add_to_logs(userid, login):
    query =f"INSERT INTO dbo.user_logs (id, time_stamp, log_in) VALUES ('{userid}', GETDATE(), '{login}')"
    with conn.cursor() as cur:
        return cur.execute(query)
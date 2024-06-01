import streamlit as st # type: ignore
import pyodbc # type: ignore
import MongoDB as mdb
import pandas as pd

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

###Checks if the username and password match the database
def check_login(username, password):
    query = f"SELECT id FROM dbo.users WHERE username = '{username}' AND password = '{password}'"
    with conn.cursor() as cur:
        res = cur.execute(query).fetchone()
        if res:
            return res[0]
    return False

###Checks if the username already exists in the database
def check_username(username):
    query = f"SELECT * FROM dbo.users WHERE username = '{username}'"
    with conn.cursor() as cur:
        if cur.execute(query).fetchone():
            return False
    return True


###Creates a new user in the database
def register_user(email, username, password):
    query = f"INSERT INTO dbo.users (email, username, password) VALUES ('{email}', '{username}', '{password}')"
    with conn.cursor() as cur:
        return cur.execute(query)

### adds data to userlog table   
def add_to_logs(userid, login):
    query =f"INSERT INTO dbo.user_logs (id, time_stamp, log_in) VALUES ('{userid}', GETDATE(), '{login}')"
    with conn.cursor() as cur:
        return cur.execute(query)
    
###Changes the password of the user
def change_password(userid, password):
    query = f"UPDATE dbo.users SET password = '{password}' WHERE id = '{userid}'"
    with conn.cursor() as cur:
        return cur.execute(query)
    
###changes the email of the user
def change_email(userid, email):
    query = f"UPDATE dbo.users SET email = '{email}' WHERE id = '{userid}'"
    with conn.cursor() as cur:
        return cur.execute(query)
    
###Deletes the user from the database
def delete_user(userid):
    mdb.delete_chat_history(userid)
    query = f"DELETE FROM dbo.users WHERE id = '{userid}'"
    with conn.cursor() as cur:
        return cur.execute(query)

def get_logs():
    query = f"SELECT * FROM dbo.user_logs"
    with conn.cursor() as cur:
        return pd.read_sql_query(query, conn)
    
def get_user_logs(id):
    query = f"SELECT * FROM dbo.user_logs WHERE id = '{id}'"
    with conn.cursor() as cur:
        return pd.read_sql_query(query, conn)

def get_users():
    query = f"SELECT * FROM user_info"
    with conn.cursor() as cur:
        return pd.read_sql_query(query, conn)


def admin_login(username, password):
    query = f"SELECT id FROM dbo.admin WHERE username = '{username}' AND password = '{password}'"
    with conn.cursor() as cur:
        if cur.execute(query).fetchone():
            return cur.execute(query).fetchone()[0]
    return False
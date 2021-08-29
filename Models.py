import sqlite3
import pandas as pd

def validate_user(username,password):
    msg=False
    with sqlite3.connect("users.sqlite3") as con:
        data=con.execute("select *from user where (username='{}' and password='{}' and auth_user='{}')".format(username,password,"yes"))
        row=data.fetchall()
        if len(row)==1:
            msg=True
    return msg
    con.close()

def validate_admin(username,password):
    msg=False
    with sqlite3.connect("users.sqlite3") as con:
        data=con.execute("select *from admin_account where (username='{}' and password='{}')".format(username,password))
        row=data.fetchall()
        if len(row)==1:
            msg=True
    return msg
    con.close()

def insert_user(email,username,password):
    with sqlite3.connect("users.sqlite3") as con:
        con.execute("insert into user (username,email,password,auth_user) values(?,?,?,?)",(username,email,password,"no"))
        con.commit()
        # con.close()



def insert_admin(username,password):
    with sqlite3.connect("users.sqlite3") as con:
        con.execute("insert into admin_account (username,password) values({},{})".format(username,password))
        con.commit()
        con.close()


def filldatabase():
    df=pd.read_csv('Papers data1.csv')
    print(df['paper_title'].values,"\n",df['author_keywords'].values,"\n",df['abstract'].values,"\n",df['area'].values)
    t1=df['paper_title'].values
    key1=df['author_keywords'].values
    abs1=df['abstract'].values
    area1=df['area'].values
    with sqlite3.connect("users.sqlite3") as con:
        for i,j,k,l in zip(t1,key1,abs1,area1):
            con.execute("insert into article (title,author_keywords,abstract,area) values(?,?,?,?)",(i,j,k,l))
            con.commit()
    con.close()

# filldatabase() #insert values using csv to sql table
from sqlalchemy import create_engine
con=create_engine("sqlite:///users.sqlite3").connect()
df1=pd.read_sql_table("article",con)
print(df1.columns)
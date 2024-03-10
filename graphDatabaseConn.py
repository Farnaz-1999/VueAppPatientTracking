from fastapi import FastAPI
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()
uri = os.getenv("uri")
user = os.getenv("user")
pwd = os.getenv("pwd")
print(uri,user,pwd)
def connection():
    driver = GraphDatabase.driver(uri=uri,auth=(user,pwd))
    return (driver)

app = FastAPI()
@app.get("/")
def default():
    return{"you are in the root"}

@app.get("/count")
def countnode(label):
    diver_neo4j = connection()
    session = diver_neo4j.session()
    q1 = """
        match(n) where labels(n) in [[$a]] return count(n)
        """
    x= {"a":label}
    results = session.run(q1,x)
    return{'response':[{'count(n)':resutl['count(n)']}for resutl in results]}
    # json_results = [dict(record) for record in results]
    # return json_results

# app=FastAPI()
# @app.post("/create")
# def createnode(node:nodemodel):
#     driver_neo4j=connection()
#     session=driver_neo4j.session()
#     q1="""
#     create(n:employee{name:$name,emp_id:$emp_id}) return n.name as name
#     """
#     x={"name":node.name,"emp_id":node.emp_id}
#     results=session.run(q1,x)
#     data=[{"Name":row["name"]}for row in results][0]["Name"]
#     return {"response":"node created with employee name as: "+data}
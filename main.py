from fastapi import FastAPI, Depends, HTTPException
from typing import Union, List
from pydantic import BaseModel
# import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import json

app = FastAPI()

# Create an engine and sessionmaker (outside of request context)
DATABASE_URL = "postgresql://postgres:password@localhost:5432/TestDb1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ErrorResponse(BaseModel):
    err_msg: str 
class UserResponse(BaseModel):
    user_id: int    
    first_name: str
    last_name: str
    email: str
    phone: str
class UserLogin(BaseModel):    
    user_name: str
    password: str

@app.get("/users/", response_model=List[UserResponse])
async def read_users(db: Session = Depends(get_db)):
    query = text("SELECT user_id, email, phone,first_name, last_name FROM users")
    users = db.execute(query).fetchall()
    return users

@app.post("/verify_login", response_model=Union[UserResponse, ErrorResponse])
async def verify_login(userlogin:UserLogin, db: Session = Depends(get_db)):
    
    query = text(f"SELECT user_id, email, phone,first_name, last_name, password FROM users where user_name = '{userlogin.user_name}'")
    users = db.execute(query).fetchall()

    if len(users) == 0:
        return ErrorResponse(err_msg= f"User {userlogin.user_name} does not exists!")
    else:
        if users[0].password == userlogin.password:
            return users[0]
        else:
            return ErrorResponse(err_msg= f"Incorrect password !!")                    

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/verifyuser")
# async def VerifyUser(username, password):
#     print(username, password)

#     userexist: bool = False
#     passwordexists : bool = False
#     resp_data: any = None;

#     f = open("users.json")
#     data = json.load(f)
#     for u in data:
#         if(u["username"] == username):
#             userexist = True
#             if(u["password"] == password):
#                 passwordexists = True
#                 resp_data = {
#                         "user_id": u["user_id"],
#                         "first_name": u["first_name"],
#                         "last_name": u["last_name"],
#                         "email_id": u["email_id"],
#                         "phone": u["phone"]
#                 }            

#     f.close()

#     if not userexist:
#        return "User does not exists !"
#     if not passwordexists:
#         return "Incorrect password"
    
#     if userexist and passwordexists:
#         return resp_data

# @app.get("/hi/{hello}/{there}")
# async def Hi(p: str, q: Union[str , None] = None):
#     return f"hi ... {p}...{q}"

# #pydantic model
# class Item(BaseModel):
#     item_id: int
#     name: str
#     is_offer: Union[bool, None] = None

# @app.put("/get_items/{item_id}")
# async def GetItems(item_id: int, item: Item):
#     return f"item id: {item_id}, {item}"

# class User1(BaseModel):
#     user_id: int
#     user_name: str
#     # first_name: str
#     # last_name: str
#     # email: str
#     # phone: str    
#     # password: str  

# @app.get("/get_users1")
# def GetUsers1():
#     users: any = None
#     try:
#         # Connect to your PostgreSQL database
#         connection = psycopg2.connect(user="postgres",
#                                     password="password",
#                                     host="localhost",
#                                     port="5432",
#                                     database="TestDb")

#         # Create a cursor to perform database operations
#         cursor = connection.cursor()

#         # Define the SELECT query
#         select_query = "SELECT user_id,user_name FROM users;"

#         # Execute the SELECT query
#         cursor.execute(select_query)

#         # Fetch all rows from the result
#         users_records = cursor.fetchall()

#         # Print each row
#         # for row in users_records:
#         #     print(row)
#         users = [User1(user_id=row[0],
#                       user_name=row[1],
#                       ) for row in users_records]
        
#         # email=user.email,
#         #               phone=user.phone, 
#         #               first_name = user.first_name,
#         #               last_name = user.last_name
#         print(users)

#     except (Exception, Error) as error:
#         print("Error while connecting to PostgreSQL:", error)
#     finally:
#         # Close the cursor and connection
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
    
#     return users
    


# @app.get("/verify_login/{user_name}/{password}", response_model=Union[UserResponse, ErrorResponse])
# async def read_users(user_name:str, password: str, db: Session = Depends(get_db)):
    
#     query = text(f"SELECT user_id, email, phone,first_name, last_name, password FROM users where user_name = '{user_name}'")
#     users = db.execute(query).fetchall()

#     if len(users) == 0:
#         return ErrorResponse(err_msg= f"User {user_name} does not exists!")
#     else:
#         if users[0].password == password:
#             return users[0]
#         else:
#             return ErrorResponse(err_msg= f"Incorrect password !!")




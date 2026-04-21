#Used to connect your Python app to the database
from sqlalchemy import create_engine

#Used to create database sessions (like transactions) like Insert, update, delete
from sqlalchemy.orm import sessionmaker

#Used to create models (tables) in Python
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.db"

#This actually connects to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) 

# autocommit=False → you manually commit changes
# autoflush=False → changes won’t auto-save
# bind=engine → connect session to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # used to create session factory

# This is used to create database tables (models)
Base = declarative_base()

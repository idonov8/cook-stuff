from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///db/cookStuff.db')
Base = declarative_base()
Base.metadata.create_all(engine)
session = scoped_session(sessionmaker(bind=engine, autoflush=False))

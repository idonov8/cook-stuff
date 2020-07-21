from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date 
from db.database import Base, engine

class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    name = Column(String)
    content = Column(String)

Base.metadata.create_all(engine)



    
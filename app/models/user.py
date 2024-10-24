from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.ddl import CreateTable

from app.backend.db import Base



class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    tasks = relationship('Task', back_populates='user')


print(CreateTable(User.__table__))

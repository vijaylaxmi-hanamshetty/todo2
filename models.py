from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid
class UserModel(Base):
    __tablename__="users"
    id=Column(String, primary_key=True, index=True,default=lambda: str(uuid.uuid4()))
    username=Column(String,unique=True,index=True,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    tasks=relationship("TaskModel",back_populates="owner")


class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="tasks")
from sqlalchemy import Column,Integer , String,Boolean , ForeignKey
from src.utils.db import Base #connect tabel/models to actual data

class TaskModel(Base):
    __tablename__="user_tasks"

    id=Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    is_completed=Column(Boolean,default=False)


    user_id=Column(Integer,ForeignKey("user_table.id",ondelete="CASCADE"))
    #ondelete -> will delete all the tasks related to a user if account is deleted 

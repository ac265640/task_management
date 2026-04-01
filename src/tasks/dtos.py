from pydantic import BaseModel
from typing import Optional

class  TaskSchema(BaseModel):
    title:str
    description:str
    is_completed:bool=False


class  TaskResponeSchema(BaseModel):
    id:int
    title:str
    description:str
    is_completed:bool=False
    user_id: Optional[int] = None
    
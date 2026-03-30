from pydantic import BaseModel

class  TaskSchema(BaseModel):
    title:str
    description:str
    is_completed:bool=False


class  TaskResponeSchema(BaseModel):
    id:int
    title:str
    description:str
    is_completed:bool=False
    
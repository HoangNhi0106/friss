from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PersonBase(BaseModel):
    firstname: str
    lastname: str
    birthday: Optional[datetime] = None
    identification: Optional[str] = None

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class PersonCheck(PersonBase):
    pass

class PersonInDBBase(PersonBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class Person(PersonInDBBase):
    pass

class PersonInDB(PersonInDBBase):
    pass
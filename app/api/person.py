from fastapi import APIRouter, Depends
from typing import Any
from sqlalchemy.orm import Session
from app.schemas.person import PersonCreate, Person, PersonCheck
from app.db.database import get_db
from app.schemas.response import BaseResponse
from app import crud

router = APIRouter()

@router.post("/store", response_model=BaseResponse[Person])
async def store_person(person: PersonCreate, db: Session = Depends(get_db)):
    (new_person, error) = crud.person.create(db=db, person=person)
    if error:
        return BaseResponse(status="400", message=f"Cannot store person to database: {error}", data=None)
    else:
        return BaseResponse(status="200", message="Person created successfully", data=new_person)
    
@router.post("/check", response_model=BaseResponse[Any])
async def check_person(person: PersonCheck, db: Session = Depends(get_db)):
    (persons, error) = crud.person.get_persons_with_highest_probability(db=db, person=person)
    print(persons, error)
    if error:
        return BaseResponse(status="400", message=f"Cannot get person: {error}", data=None)
    else:
        return BaseResponse(status="200", message="Get persons successfully", data=persons)
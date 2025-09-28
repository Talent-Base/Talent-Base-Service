from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import engine, Base, getDatabase
from .repository import UserRepository
from .schema import UserBase
from ..models import User

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def getUsers(database: Session = Depends(getDatabase)):
    users = UserRepository.getAllUsers(database)
    return users

@router.get("/{user_email}")
async def getUserByEmail(user_email: str, database: Session = Depends(getDatabase)):
    user = UserRepository.getUserByEmail(user_email, database)
    return user

@router.post("/")
async def createUser(request: UserBase, database: Session = Depends(getDatabase)):
    new_user = UserRepository.createUser(User(**request.model_dump()), database)
    return new_user

@router.put("/{user_email}")
async def updateUserByEmail(user_email: str, user_data: UserBase, database: Session = Depends(getDatabase)):
    updated_user = UserRepository.updateUser(user_email, User(**user_data.model_dump()), database)
    return updated_user

@router.delete("/{user_email}")
async def deleteUser(user_email: str, database: Session = Depends(getDatabase)):
    response = UserRepository.deleteUser(user_email, database)
    return response
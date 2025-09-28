from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..database import getDatabase
from ..models import User

class UserRepository:

    def getAllUsers(database: Session = Depends(getDatabase)):
        return database.query(User).all()
    
    def getUserByEmail(user_email: User, database: Session = Depends(getDatabase)):
        user = database.query(User).filter(User.email==user_email).first()
        if user:
            return user
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    def createUser(new_user: User, database: Session = Depends(getDatabase)):
        user_already_exists = database.query(User).filter(User.email == new_user.email).first()
        if user_already_exists:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
        return new_user
    
    def updateUser(user_email: str, user_data: User, database: Session = Depends(getDatabase)):
        user = database.query(User).filter(User.email == user_email).first()
        if user:
            for key, value in user_data.__dict__.items():  
                if key != "_sa_instance_state" and value is not None:
                    setattr(user, key, value)
            
            database.commit()
            database.refresh(user)
            
            return user_data
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        

    def deleteUser(user_email: str, database: Session = Depends(getDatabase)):
        user = database.query(User).filter(User.email == user_email).first()
        if user:
            database.delete(user)
            database.commit()
        else:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return Response(status_code = status.HTTP_204_NO_CONTENT)
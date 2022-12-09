from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from models import models
from database import database
from sqlalchemy.orm import Session

from authentication.hashing import Hash

router = APIRouter(
    tags=['User']
)

# Create User
@router.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(email=request.email, username=request.username, password=Hash.bcrypt(request.password))
    user_is_available = db.query(models.User).filter(models.User.email == new_user.email).first()
    
    if user_is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email already in use!")
    
    db.add(new_user)
    db.commit()

    db.refresh(new_user)
    return { "message" : "User successfully registered!" }

# See the user that succesfully created (You can only see email and username)
@router.get('/user', response_model=List[schemas.UserView])
def get_all_user(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

# See the user that succesfully created by id
@router.get('/user/{id}', status_code=200, response_model = (schemas.UserView))
def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User dengan id {id} tidak ada!")
    
    return users

# Delete user by id
@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User dengan id {id} tidak ada")
    user.delete(synchronize_session=False)
    db.commit()
    return {"Message": f"user dengan id {id} telah dihapus"}
from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from models import models
from database import database
from sqlalchemy.orm import Session

from authentication.hashing import HashPass

router = APIRouter(
    tags=['User']
)

# Create User
@router.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(email=request.email, username=request.username, password=HashPass.get_hash_password(request.password))
    user_is_available = db.query(models.User).filter(models.User.email == new_user.email).first()
    
    if user_is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email sudah terdaftar!")
    
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
def get_user_by_id(id, db: Session = Depends(database.get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User dengan id {id} tidak ada!")
    
    return users

# Delete user by id
@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(database.get_db)):
    delete_user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not delete_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User dengan {id} tidak ada!")
    db.commit()
    return { "message" : f"User dengan id {id} telah dihapus!"}
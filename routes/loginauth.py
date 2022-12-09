from fastapi import APIRouter, Depends, HTTPException, status
from schemas import schemas
from models import models
from database import database
from authentication.hashing import HashPass
from sqlalchemy.orm import Session

router = APIRouter(tags=['Login Authentication'])

@router.post('/login')
def user_login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kredensial yang dimasukkan salah!")

    if not HashPass.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password yang dimasukkan salah!")
    
    return { "message" : "User signed in successfully" }

from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from models import models
from database import database
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    tags = ["Course"]
)


@router.get("/courses", response_model = List[schemas.Course])
# Mendapatkan daftar seluruh mata kuliah
def get_all_course(db: Session = Depends(database.get_db)):
    db_course = db.query(models.Course).all()
    return db_course


@router.get("/courses/{course_id}", response_model = schemas.Course)
# Mendapatkan daftar seluruh mata kuliah
def get_all_course(course_id, db: Session = Depends(database.get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    return db_course


@router.get("/course/schedule", response_model = List[schemas.CourseScheduleView])
# Mendapatkan daftar seluruh mata kuliah dengan jadwalnya
def get_all_course_schedule(db: Session = Depends(database.get_db)):
    db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).order_by(models.CourseSchedule.course_id).all()
    return db_course


@router.get("/course/schedule/{course_id}", response_model = List[schemas.CourseScheduleView])
# Mendapatkan daftar mata kuliah dengan jadwalnya
def get_course_schedule(course_id, db: Session = Depends(database.get_db)):
    db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).filter(models.CourseSchedule.course_id == course_id).all()
    if not db_course :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Course didn't exist")
    
    return db_course

# BELOM
# @router.get("/course/schedule/{day}", response_model = List[schemas.CourseScheduleView])
@router.get("/course/schedule/{day}")
# Mendapatkan jadwal kuliah berdasarkan hari
def get_course_by_day(day, db: Session = Depends(database.get_db)):
    # db_course = db.query(models.CourseSchedule).join(models.Schedule, models.CourseSchedule.schedule_id == models.Schedule.id).all()
    # if db_course is None :
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Course didn't exist")
    
    # course_list = db_course[2]
    # return course_list
    # if day.lower() == 'senin':
    #     db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).filter(models.Schedule.day.like("Senin")).all()
    # elif day.lower() == 'selasa':
    #     db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).filter(models.Schedule.day.like("Selasa")).all()
    # elif day.lower() == 'rabu':
    #     db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).filter(models.Schedule.day.like("Rabu")).all()
    # elif day.lower() == 'kamis':
    #     db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).filter(models.Schedule.day.like("Kamis")).all()
    # elif day.lower() == 'jumat':
    #     db_course = db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).filter(models.Schedule.day.like("Jumat")).all()
    
    # if not db_course :
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Course didn't exist")
    
    # return db_course

    return db.query(models.CourseSchedule.course_id, models.CourseSchedule.name, models.Schedule.day, models.Schedule.time).join(models.Schedule).all()

    

# BELOM
@router.get("/course/schedule/{day}/{time}", response_model = List[schemas.CourseScheduleView])
# Mendapatkan jadwal kuliah berdasarkan hari dan jamnya
def get_course_by_session(day, time, db: Session = Depends(database.get_db)):
    pass
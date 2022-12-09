from fastapi import APIRouter, HTTPException, status, Depends
from schemas import schemas
from typing import List
from models import models
from database import database
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(
    tags = ["Student"]
)

@router.get("/students", response_model=List[schemas.Student])
# Mendapatkan data semua mahasiswa
def get_all_student(db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).all()
    return db_student


@router.get("/student/{student_id}", response_model = schemas.Student)
# Mendapatkan data mahasiswa dengan NIM = student_id
def get_student(student_id, db: Session = Depends(database.get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Student doesn't exist")
    
    return db_student


# @router.get("/participant/day/all")
@router.get("/participant/day/all", response_model = List[schemas.ParticipantDay])
# Mendapatkan data jumlah mahasiswa yang memiliki kelas setiap harinya
def get_all_participants(db: Session = Depends(database.get_db)):
    result = []
    # for i in range (0, 15, 3):
    #     db_participant = db.query(models.CourseTaken).join(models.CourseSchedule, models.CourseTaken.courseschedule_id == models.CourseSchedule.id).filter(models.CourseSchedule.schedule_id > 3, models.CourseSchedule.schedule_id <= 6).all()

    day_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    for day in day_list:
        idx = day_list.index(day) * 3
        db_sched = db_participant = db.query(models.CourseTaken).join(models.CourseSchedule, models.CourseTaken.courseschedule_id == models.CourseSchedule.id).filter(models.CourseSchedule.schedule_id > idx, models.CourseSchedule.schedule_id <= idx + 3).all()

        value = {
            "day": day,
            "total": len(db_participant)
        }

        result.append(value)

    return result

    

@router.get("/participant/day={day}", response_model = schemas.ParticipantDay)
# Mendapatkan jumlah mahasiswa yang memiliki jadwal kuliah pada hari = day
def get_participants_by_day(day: str, db: Session = Depends(database.get_db)):
    day_list = ['senin', 'selasa', 'rabu', 'kamis', 'jumat']

    try:
        idx = day_list.index(day.lower()) * 3
        db_participant = db.query(models.CourseTaken).join(models.CourseSchedule, models.CourseTaken.courseschedule_id == models.CourseSchedule.id).filter(models.CourseSchedule.schedule_id > idx, models.CourseSchedule.schedule_id <= idx + 3).all()
        total = len(db_participant)
        
        return { 
            "day" : day,
            "total" : total
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Day is not valid"
        )

    
# @router.get("participant/day/time/all", response_model = List[schemas.ParticipantDayTime])
@router.get("/participant/day/time/all")
def get_all_participant(db: Session = Depends(database.get_db)):
    result = []
    query = select([models.Schedule.day, models.Schedule.time])
    db_sched = database.engine.execute(query).all()

    for i in range(1, 16):
        db_participant = db.query(models.CourseTaken).join(models.CourseSchedule, models.CourseTaken.courseschedule_id == models.CourseSchedule.id).filter(models.CourseSchedule.schedule_id == i).all()
        value = {
            "day": db_sched[i-1][0],
            "time": db_sched[i-1][1],
            "total": len(db_participant)
        }

        result.append(value)

    return result


@router.get("/participant/day={day}/time={time}", response_model = schemas.ParticipantDayTime)
# Mendapatkan jumlah mahasiswa yang memiliki jadwal kuliah pada hari = day dan sesi = time
def get_participants_by_session(day: str, time: str, db: Session = Depends(database.get_db)):
    day_list = ['senin', 'selasa', 'rabu', 'kamis', 'jumat']
    session_list = ['pagi', 'siang', 'sore']
    try:
        idx = day_list.index(day.lower()) * 3 + session_list.index(time.lower()) + 1
        db_participant = db.query(models.CourseTaken).join(models.CourseSchedule, models.CourseTaken.courseschedule_id == models.CourseSchedule.id).filter(models.CourseSchedule.schedule_id == idx).all()
        total = len(db_participant)
        
        return { 
            "day" : day,
            "time" : time,
            "total" : total
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Day or time is not valid"
        )

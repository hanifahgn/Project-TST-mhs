from pydantic import BaseModel, EmailStr

class Student(BaseModel):
    id: int
    name: str
    department: str

    class Config():
        orm_mode = True

class Course(BaseModel):
    id: int
    name: str
    credits: int

    class Config():
        orm_mode = True

class Schedule(BaseModel):
    id: int
    day: str
    time: str

class CourseSchedule(BaseModel):
    id: int
    course_id: int     # foreign key to course
    schedule_id: int   # foreign key to schedule
    name: str          

class CourseScheduleView(BaseModel):
    course_id: int
    name: str
    day: str
    time: str

    class Config():
        orm_mode = True

class CourseTaken(BaseModel):
    student_id: int        # foreign key ke student
    courseschedule_id: int # foreign key ke course_scheulde

class ParticipantDay(BaseModel):
    day: str
    total: int

    class Config():
        orm_mode = True

class ParticipantDayTime(BaseModel):
    day: str
    time: str
    total: int

    class Config():
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserView(BaseModel):
    email: str
    username: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
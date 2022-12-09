from database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)

    course_taken = relationship("CourseTaken", back_populates = "student")

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    credits = Column(Integer)

    course_schedule = relationship("CourseSchedule", back_populates = "course")

class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key = True) 
    day = Column(String)
    time = Column(String)

    course_schedule = relationship("CourseSchedule", back_populates = "schedule")

class CourseSchedule(Base):
    __tablename__ = 'course_schedule'

    id = Column(Integer, primary_key = True)
    course_id = Column(Integer, ForeignKey("course.id")) # foreign key to course
    schedule_id = Column(Integer, ForeignKey("schedule.id")) # foreign key schedule
    # name = Column(String, ForeignKey("course.name")) # foreign key to course
    name = Column(String) # foreign key to course

    course = relationship("Course", back_populates = "course_schedule")
    schedule = relationship("Schedule", back_populates = "course_schedule")
    course_taken = relationship("CourseTaken", back_populates = "course_schedule")

class CourseTaken(Base):
    __tablename__ = 'course_taken'

    student_id = Column(Integer, ForeignKey("student.id"), primary_key = True) # foreign key ke student
    courseschedule_id = Column(Integer, ForeignKey("course_schedule.id"), primary_key = True) # foreign key ke course_scheulde

    student = relationship("Student", back_populates = "course_taken")
    course_schedule = relationship("CourseSchedule", back_populates = "course_taken")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)
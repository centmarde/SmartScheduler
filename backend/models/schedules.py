from . import db
from .teachers import Teacher
from .sections import Section
from .subjects import Subject
import os

class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    time_slot = db.Column(db.String, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    
    # Relationships
    teacher = db.relationship("Teacher", foreign_keys=[teacher_id], backref="teaching_schedules")
    section = db.relationship("Section", backref="schedules")
    subject = db.relationship("Subject", backref="schedules")
    
    def __repr__(self):
        return f"<Schedule(day='{self.day}', time='{self.time_slot}', section='{self.section.name}', subject='{self.subject.name}')>"

from . import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    subject_name = db.Column(db.String, nullable=False)
    
    # Optional: If you want to create a relationship with the Subject model
    # subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    # subject = db.relationship("Subject", back_populates="teachers")
    
    def __repr__(self):
        return f"<Teacher(name='{self.name}', subject='{self.subject_name}')>"
    
    @classmethod
    def seed(cls, session):
        """Seed the teachers table with initial data"""
        # Clear existing data
        session.query(cls).delete()
        
        teachers = [
            Teacher(name='John Smith', subject_name='Mapeh'),
            Teacher(name='Jane Doe', subject_name='Science'),
            Teacher(name='Mark Reyes', subject_name='English'),
            Teacher(name='Anna Cruz', subject_name='Filipino'),
            Teacher(name='Michael Tan', subject_name='Math'),
          
        ]
        
        session.add_all(teachers)
        session.commit()
        
        print("✅ Teachers data seeded successfully!")

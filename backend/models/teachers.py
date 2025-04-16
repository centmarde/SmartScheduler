from . import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    # Create relationship with the Subject model
    subject = db.relationship("Subject", backref="teachers")
    
    def __repr__(self):
        return f"<Teacher(name='{self.name}', subject='{self.subject.name if self.subject else None}')>"
    
    @classmethod
    def seed(cls, session):
        """Seed the teachers table with initial data"""
        # Clear existing data
        session.query(cls).delete()
        
        # Get subject IDs from database
        from .subjects import Subject
        math = session.query(Subject).filter_by(name='Mathematics').first()
        science = session.query(Subject).filter_by(name='Science').first()
        english = session.query(Subject).filter_by(name='English').first()
        filipino = session.query(Subject).filter_by(name='Filipino').first()
        mapeh = session.query(Subject).filter_by(name='Mapeh').first()
        
        # Ensure subjects exist
        if not all([math, science, english, filipino, mapeh]):
            print("⚠️ Some subjects are missing. Please run Subject.seed() first.")
            return
        
        teachers = [
            Teacher(name='John Smith', subject_id=mapeh.id),
            Teacher(name='Jane Doe', subject_id=science.id),
            Teacher(name='Mark Reyes', subject_id=english.id),
            Teacher(name='Anna Cruz', subject_id=filipino.id),
            Teacher(name='Michael Tan', subject_id=math.id),
        ]
        
        session.add_all(teachers)
        session.commit()
        
        print("✅ Teachers data seeded successfully!")

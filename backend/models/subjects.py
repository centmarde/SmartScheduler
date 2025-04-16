from . import db

# Association table for many-to-many relationship between sections and subjects
section_subject = db.Table(
    'section_subject',
    db.Column('section_id', db.Integer, db.ForeignKey('sections.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    
    # Relationship with sections (many-to-many)
    sections = db.relationship("Section", secondary=section_subject, back_populates="subjects")
    # Note: The teacher relationship is handled via backref in the Teacher model
    
    def __repr__(self):
        return f"<Subject(name='{self.name}', code='{self.code}')>"
    
    @classmethod
    def seed(cls, session):
        """Seed the subjects table with initial data"""
        # Clear existing data
        session.query(cls).delete()
        
        subjects = [
            Subject(name='Mathematics', code='MATH'),
            Subject(name='Science', code='SCI'),
            Subject(name='English', code='ENG'),
            Subject(name='Filipino', code='FIL'),
            Subject(name='Mapeh', code='MAPEH'),
           
        ]
        
        session.add_all(subjects)
        session.commit()
        
        print("✅ Subjects data seeded successfully!")
    
    @classmethod
    def seed_section_subject(cls, session):
        """Seed the section_subject association table with initial relationships"""
        # Clear existing data
        session.execute(section_subject.delete())
        
        # Get all sections and subjects
        from .sections import Section
        sections = session.query(Section).all()
        subjects = session.query(cls).all()
        
        # For this example, we'll assign all subjects to all sections
        # In a real application, you might have more specific assignments
        associations = []
        for section in sections:
            for subject in subjects:
                # Add the association by appending the subject to the section's subjects
                section.subjects.append(subject)
        
        session.commit()
        print("✅ Section-Subject associations seeded successfully!")

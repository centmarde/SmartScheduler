from . import db

class Section(db.Model):
    __tablename__ = 'sections'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    # Relationship with subjects (many-to-many)
    subjects = db.relationship("Subject", secondary="section_subject", back_populates="sections")
    
    def __repr__(self):
        return f"<Section(name='{self.name}')>"
    
    @classmethod
    def seed(cls, session):
        """Seed the sections table with initial data"""
        # Clear existing data
        session.query(cls).delete()
        
        sections = [
            Section(name='Grade 7 - Sunflower'),
            Section(name='Grade 7 - Daffodil'),
            Section(name='Grade 7 - Orchid'),
            Section(name='Grade 8 - Sunflower'),
          
           
        ]
        
        session.add_all(sections)
        session.commit()
        
        print("✅ Sections data seeded successfully!")

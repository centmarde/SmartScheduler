import random
import time
from collections import defaultdict

class HillClimbingScheduler:
    def __init__(self, session, Section, Subject, Teacher, Schedule):
        self.session = session
        self.Section = Section
        self.Subject = Subject
        self.Teacher = Teacher
        self.Schedule = Schedule
        
        # Constants for the hill climbing algorithm
        self.MAX_ITERATIONS = 1000
        self.MAX_NEIGHBORS = 100
        self.NO_IMPROVEMENT_LIMIT = 50
        
        # Load data from database
        self.teachers = session.query(Teacher).all()
        self.sections = session.query(Section).all()
        self.subjects = session.query(Subject).all()
        
        # Time slots and days
        self.time_slots = ["7:30-8:30", "8:30-9:30", "9:30-10:30", "10:30-11:30", 
                          "1:00-2:00", "2:00-3:00", "3:00-4:00", "4:00-5:00"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        # Create mappings for quick reference
        self.teacher_subjects = self._map_teacher_subjects()
        
    def _map_teacher_subjects(self):
        """Map teachers to their subjects based on specialization"""
        teacher_subjects = defaultdict(list)
        for teacher in self.teachers:
            for subject in self.subjects:
                if hasattr(teacher, 'specialization') and teacher.specialization == subject.name:
                    teacher_subjects[teacher.id].append(subject.id)
        
        # If a teacher has no specific subjects, assume they can teach any
        for teacher in self.teachers:
            if not teacher_subjects[teacher.id]:
                teacher_subjects[teacher.id] = [subject.id for subject in self.subjects]
                
        return teacher_subjects
    
    def _create_initial_schedule(self):
        """Create an initial random schedule"""
        schedule = []
        
        # Create a schedule for each section and required subject
        for section in self.sections:
            for subject in self.subjects:
                # Skip if section doesn't need this subject (implement your own logic)
                if hasattr(section, 'grade_level') and not self._section_needs_subject(section, subject):
                    continue
                
                # Find suitable teachers for this subject
                suitable_teachers = [teacher.id for teacher in self.teachers 
                                    if subject.id in self.teacher_subjects[teacher.id]]
                
                if not suitable_teachers:
                    suitable_teachers = [teacher.id for teacher in self.teachers]
                
                # Randomly select day, time, and teacher
                day = random.choice(self.days)
                time_slot = random.choice(self.time_slots)
                teacher_id = random.choice(suitable_teachers)
                
                # Add to schedule
                schedule.append({
                    'day': day,
                    'time_slot': time_slot,
                    'teacher_id': teacher_id,
                    'section_id': section.id,
                    'subject_id': subject.id
                })
        
        return schedule
    
    def _section_needs_subject(self, section, subject):
        """Determine if a section needs a particular subject"""
        # Implement logic based on your requirements
        return True  # Default: assume all sections need all subjects
    
    def _calculate_score(self, schedule):
        """Calculate a score for the schedule (higher is better)"""
        # 1. Teacher conflicts (lower is better)
        teacher_slots = defaultdict(int)
        for entry in schedule:
            key = (entry['teacher_id'], entry['day'], entry['time_slot'])
            teacher_slots[key] += 1
        
        teacher_conflicts = sum(count - 1 for count in teacher_slots.values() if count > 1)
        
        # 2. Section conflicts (lower is better)
        section_slots = defaultdict(int)
        for entry in schedule:
            key = (entry['section_id'], entry['day'], entry['time_slot'])
            section_slots[key] += 1
        
        section_conflicts = sum(count - 1 for count in section_slots.values() if count > 1)
        
        # 3. Teacher load balance (lower is better)
        teacher_loads = defaultdict(int)
        for entry in schedule:
            teacher_loads[entry['teacher_id']] += 1
        
        avg_load = sum(teacher_loads.values()) / max(len(teacher_loads), 1)
        load_variance = sum((load - avg_load) ** 2 for load in teacher_loads.values()) / max(len(teacher_loads), 1)
        
        # 4. Teacher-subject suitability (higher is better)
        suitability = 0
        for entry in schedule:
            if entry['subject_id'] in self.teacher_subjects[entry['teacher_id']]:
                suitability += 1
        
        # Combined score (higher is better)
        score = (
            -10 * teacher_conflicts
            -10 * section_conflicts
            -2 * load_variance
            +1 * suitability
        )
        
        return score, {
            'teacher_conflicts': teacher_conflicts,
            'section_conflicts': section_conflicts,
            'load_variance': load_variance,
            'suitability': suitability
        }
    
    def _get_neighbor(self, schedule):
        """Generate a neighboring schedule by making a small change"""
        neighbor = schedule.copy()
        
        # Select a random entry to modify
        idx = random.randint(0, len(neighbor) - 1)
        entry = neighbor[idx].copy()  # Create a copy to avoid modifying the original
        
        # Choose what to modify (day, time_slot, or teacher)
        modification = random.choice(['day', 'time_slot', 'teacher_id'])
        
        if modification == 'day':
            entry['day'] = random.choice(self.days)
        elif modification == 'time_slot':
            entry['time_slot'] = random.choice(self.time_slots)
        else:  # teacher_id
            suitable_teachers = [teacher.id for teacher in self.teachers 
                                if entry['subject_id'] in self.teacher_subjects[teacher.id]]
            
            if not suitable_teachers:
                suitable_teachers = [teacher.id for teacher in self.teachers]
            
            entry['teacher_id'] = random.choice(suitable_teachers)
        
        # Replace the modified entry
        neighbor[idx] = entry
        
        return neighbor
    
    def climb(self):
        """Execute hill climbing algorithm to find an optimized schedule"""
        # Generate initial solution
        current_schedule = self._create_initial_schedule()
        current_score, metrics = self._calculate_score(current_schedule)
        
        print(f"Initial schedule score: {current_score}")
        print(f"Initial metrics: {metrics}")
        
        iteration = 0
        no_improvement_count = 0
        
        while iteration < self.MAX_ITERATIONS and no_improvement_count < self.NO_IMPROVEMENT_LIMIT:
            # Generate neighbors
            best_neighbor = None
            best_neighbor_score = float('-inf')
            
            for _ in range(self.MAX_NEIGHBORS):
                neighbor = self._get_neighbor(current_schedule)
                neighbor_score, _ = self._calculate_score(neighbor)
                
                if neighbor_score > best_neighbor_score:
                    best_neighbor = neighbor
                    best_neighbor_score = neighbor_score
            
            # If best neighbor is better than current, move to it
            if best_neighbor_score > current_score:
                current_schedule = best_neighbor
                current_score = best_neighbor_score
                _, metrics = self._calculate_score(current_schedule)
                print(f"Iteration {iteration}: Found better schedule with score {current_score}")
                print(f"Metrics: {metrics}")
                no_improvement_count = 0
            else:
                no_improvement_count += 1
            
            iteration += 1
        
        final_score, final_metrics = self._calculate_score(current_schedule)
        print(f"Final schedule score: {final_score}")
        print(f"Final metrics: {final_metrics}")
        print(f"Total iterations: {iteration}")
        print(f"Stopped after {no_improvement_count} iterations without improvement")
        
        return current_schedule
    
    def create_schedules(self):
        """Run the hill climbing algorithm and save results to the database"""
        # Start timing
        start_time = time.time()
        
        # Run the hill climbing algorithm
        best_schedule = self.climb()
        
        # Get metrics for the best schedule
        _, metrics = self._calculate_score(best_schedule)
        
        # Save the schedule to the database
        count = 0
        for entry in best_schedule:
            # Check if this combination already exists
            existing = self.session.query(self.Schedule).filter_by(
                day=entry['day'],
                time_slot=entry['time_slot'],
                teacher_id=entry['teacher_id'],
                section_id=entry['section_id'],
                subject_id=entry['subject_id']
            ).first()
            
            if not existing:
                new_schedule = self.Schedule(
                    day=entry['day'],
                    time_slot=entry['time_slot'],
                    teacher_id=entry['teacher_id'],
                    section_id=entry['section_id'],
                    subject_id=entry['subject_id']
                )
                self.session.add(new_schedule)
                count += 1
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        return count, metrics, execution_time

def create_hill_climbing_schedule(session, Section, Subject, Teacher, Schedule):
    """Function to be called from the route handler"""
    scheduler = HillClimbingScheduler(session, Section, Subject, Teacher, Schedule)
    return scheduler.create_schedules()

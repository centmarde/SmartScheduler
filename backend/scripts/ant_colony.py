import random
import numpy as np
import time
from collections import defaultdict

class AntColonyScheduler:
    def __init__(self, session, Section, Subject, Teacher, Schedule):
        self.session = session
        self.Section = Section
        self.Subject = Subject
        self.Teacher = Teacher
        self.Schedule = Schedule
        
        # ACO parameters
        self.NUM_ANTS = 20
        self.MAX_ITERATIONS = 50
        self.EVAPORATION_RATE = 0.5
        self.ALPHA = 1.0  # Pheromone importance
        self.BETA = 2.0   # Heuristic importance
        self.Q = 100.0    # Pheromone deposit factor
        
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
        
        # Initialize pheromone structure
        self.pheromones = self._initialize_pheromones()
        
        # Define required schedules
        self.required_schedules = self._get_required_schedules()
        
    def _map_teacher_subjects(self):
        """Map teachers to their subjects based on the subject_id relationship"""
        teacher_subjects = defaultdict(list)
        for teacher in self.teachers:
            # Add the directly assigned subject
            teacher_subjects[teacher.id].append(teacher.subject_id)
            
        return teacher_subjects
    
    def _get_required_schedules(self):
        """Get list of required section-subject combinations"""
        required = []
        for section in self.sections:
            for subject in self.subjects:
                if self._section_needs_subject(section, subject):
                    required.append((section.id, subject.id))
        return required
    
    def _section_needs_subject(self, section, subject):
        """Determine if a section needs a particular subject"""
        # Implement custom logic here if needed
        return True  # Default assumption
    
    def _initialize_pheromones(self):
        """Initialize pheromone trails to a small positive value"""
        pheromones = {}
        
        # Structure: (section_id, subject_id, day, time_slot, teacher_id) -> pheromone value
        for section in self.sections:
            for subject in self.subjects:
                if not self._section_needs_subject(section, subject):
                    continue
                    
                for day in self.days:
                    for time_slot in self.time_slots:
                        for teacher in self.teachers:
                            if subject.id in self.teacher_subjects[teacher.id]:
                                key = (section.id, subject.id, day, time_slot, teacher.id)
                                pheromones[key] = 1.0  # Initial pheromone value
        
        return pheromones
    
    def _calculate_heuristic(self, section_id, subject_id, day, time_slot, teacher_id, current_solution):
        """Calculate heuristic value for assignment (higher is better)"""
        heuristic = 1.0  # Base value
        
        # Check teacher conflicts in this time slot
        teacher_busy = any(
            entry['teacher_id'] == teacher_id and 
            entry['day'] == day and 
            entry['time_slot'] == time_slot 
            for entry in current_solution
        )
        
        # Check section conflicts in this time slot
        section_busy = any(
            entry['section_id'] == section_id and 
            entry['day'] == day and 
            entry['time_slot'] == time_slot 
            for entry in current_solution
        )
        
        # Check if teacher specializes in this subject
        teacher_specializes = subject_id in self.teacher_subjects[teacher_id]
        
        # Calculate teacher's current load in solution
        teacher_load = sum(1 for entry in current_solution if entry['teacher_id'] == teacher_id)
        
        # Adjust heuristic based on constraints
        if teacher_busy or section_busy:
            heuristic = 0.01  # Very low but not zero to allow some exploration
        
        if teacher_specializes:
            heuristic *= 2.0
            
        # Balance teacher loads - favor less busy teachers
        heuristic *= (1.0 + 0.1 / (teacher_load + 1))
        
        return heuristic
    
    def _select_assignment(self, section_id, subject_id, current_solution):
        """Select day, time, and teacher for a section-subject combination"""
        candidates = []
        
        # Get all possible assignments
        for day in self.days:
            for time_slot in self.time_slots:
                suitable_teachers = [
                    teacher.id for teacher in self.teachers 
                    if subject_id in self.teacher_subjects[teacher.id]
                ]
                
                if not suitable_teachers:
                    suitable_teachers = [teacher.id for teacher in self.teachers]
                
                for teacher_id in suitable_teachers:
                    # Get pheromone value
                    key = (section_id, subject_id, day, time_slot, teacher_id)
                    # Ensure the key exists in the pheromones dictionary
                    if key not in self.pheromones:
                        self.pheromones[key] = 0.1
                    pheromone = self.pheromones[key]
                    
                    # Get heuristic value
                    heuristic = self._calculate_heuristic(
                        section_id, subject_id, day, time_slot, teacher_id, current_solution
                    )
                    
                    # Calculate probability
                    probability = (pheromone ** self.ALPHA) * (heuristic ** self.BETA)
                    
                    candidates.append({
                        'day': day,
                        'time_slot': time_slot,
                        'teacher_id': teacher_id,
                        'section_id': section_id,
                        'subject_id': subject_id,
                        'probability': probability
                    })
        
        # If no viable candidates, choose randomly
        if not candidates or all(c['probability'] == 0 for c in candidates):
            day = random.choice(self.days)
            time_slot = random.choice(self.time_slots)
            
            suitable_teachers = [
                teacher.id for teacher in self.teachers 
                if subject_id in self.teacher_subjects[teacher.id]
            ]
            
            if not suitable_teachers:
                suitable_teachers = [teacher.id for teacher in self.teachers]
                
            teacher_id = random.choice(suitable_teachers)
            
            return {
                'day': day,
                'time_slot': time_slot,
                'teacher_id': teacher_id,
                'section_id': section_id,
                'subject_id': subject_id
            }
        
        # Normalize probabilities
        total_prob = sum(c['probability'] for c in candidates)
        
        if total_prob == 0:
            # Random selection if all probabilities are zero
            return random.choice(candidates)
        
        # Roulette wheel selection
        r = random.random() * total_prob
        cumulative_prob = 0
        
        for candidate in candidates:
            cumulative_prob += candidate['probability']
            if r <= cumulative_prob:
                return {
                    'day': candidate['day'],
                    'time_slot': candidate['time_slot'],
                    'teacher_id': candidate['teacher_id'],
                    'section_id': candidate['section_id'],
                    'subject_id': candidate['subject_id']
                }
        
        # Fallback to last candidate
        candidate = candidates[-1]
        return {
            'day': candidate['day'],
            'time_slot': candidate['time_slot'],
            'teacher_id': candidate['teacher_id'],
            'section_id': candidate['section_id'],
            'subject_id': candidate['subject_id']
        }
    
    def _construct_solution(self):
        """Construct a complete solution (one ant's path)"""
        solution = []
        
        # Randomize the order of required schedules
        required_shuffled = self.required_schedules.copy()
        random.shuffle(required_shuffled)
        
        # Build solution incrementally
        for section_id, subject_id in required_shuffled:
            assignment = self._select_assignment(section_id, subject_id, solution)
            solution.append(assignment)
        
        return solution
    
    def _evaluate_solution(self, solution):
        """Evaluate solution quality (higher is better)"""
        # 1. Teacher conflicts (lower is better)
        teacher_slots = defaultdict(int)
        for entry in solution:
            key = (entry['teacher_id'], entry['day'], entry['time_slot'])
            teacher_slots[key] += 1
        
        teacher_conflicts = sum(count - 1 for count in teacher_slots.values() if count > 1)
        
        # 2. Section conflicts (lower is better)
        section_slots = defaultdict(int)
        for entry in solution:
            key = (entry['section_id'], entry['day'], entry['time_slot'])
            section_slots[key] += 1
        
        section_conflicts = sum(count - 1 for count in section_slots.values() if count > 1)
        
        # 3. Teacher load balance
        teacher_loads = defaultdict(int)
        for entry in solution:
            teacher_loads[entry['teacher_id']] += 1
        
        avg_load = sum(teacher_loads.values()) / max(len(teacher_loads), 1)
        load_variance = sum((load - avg_load) ** 2 for load in teacher_loads.values()) / max(len(teacher_loads), 1)
        
        # 4. Teacher-subject suitability
        suitability = sum(
            1 for entry in solution 
            if entry['subject_id'] in self.teacher_subjects[entry['teacher_id']]
        )
        
        # Combined score (higher is better)
        score = (
            100.0
            - 10.0 * teacher_conflicts
            - 10.0 * section_conflicts
            - 2.0 * load_variance
            + 1.0 * suitability
        )
        
        return max(0.1, score), {
            'teacher_conflicts': teacher_conflicts,
            'section_conflicts': section_conflicts,
            'load_variance': load_variance,
            'suitability': suitability
        }
    
    def _update_pheromones(self, solutions, scores):
        """Update pheromone trails based on solution quality"""
        # Evaporation
        for key in self.pheromones:
            self.pheromones[key] *= (1 - self.EVAPORATION_RATE)
        
        # Add new pheromones
        for solution, score in zip(solutions, scores):
            for entry in solution:
                try:
                    key = (
                        entry['section_id'], 
                        entry['subject_id'], 
                        entry['day'], 
                        entry['time_slot'], 
                        entry['teacher_id']
                    )
                    
                    # Ensure the key exists before updating
                    if key not in self.pheromones:
                        self.pheromones[key] = 0.1
                        
                    # Deposit pheromone proportional to solution quality
                    self.pheromones[key] += self.Q * score
                except (TypeError, KeyError) as e:
                    # Skip invalid entries and log error
                    print(f"Error updating pheromones: {e}, entry: {entry}")
                    continue
    
    def optimize(self):
        """Run the ant colony optimization algorithm"""
        best_solution = None
        best_score = 0
        best_metrics = None
        
        print("Starting ACO optimization...")
        
        for iteration in range(self.MAX_ITERATIONS):
            # Construct solutions with all ants
            solutions = []
            for _ in range(self.NUM_ANTS):
                solutions.append(self._construct_solution())
            
            # Evaluate solutions
            scores = []
            metrics_list = []
            for solution in solutions:
                score, metrics = self._evaluate_solution(solution)
                scores.append(score)
                metrics_list.append(metrics)
            
            # Find the best solution in this iteration
            iter_best_idx = scores.index(max(scores))
            iter_best_solution = solutions[iter_best_idx]
            iter_best_score = scores[iter_best_idx]
            iter_best_metrics = metrics_list[iter_best_idx]
            
            # Update global best
            if best_solution is None or iter_best_score > best_score:
                best_solution = iter_best_solution
                best_score = iter_best_score
                best_metrics = iter_best_metrics
                print(f"Iteration {iteration}: New best score: {best_score}")
                print(f"Metrics: {best_metrics}")
            
            # Update pheromones
            self._update_pheromones(solutions, scores)
        
        print(f"ACO optimization completed. Final best score: {best_score}")
        print(f"Final metrics: {best_metrics}")
        
        return best_solution
    
    def create_schedules(self):
        """Run the optimization and save results to the database"""
        # Start timing
        start_time = time.time()
        
        # Run the ant colony optimization
        best_schedule = self.optimize()
        
        # Get metrics for the best schedule
        _, metrics = self._evaluate_solution(best_schedule)
        
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

def create_ant_colony_schedule(session, Section, Subject, Teacher, Schedule):
    """Function to be called from the route handler"""
    scheduler = AntColonyScheduler(session, Section, Subject, Teacher, Schedule)
    return scheduler.create_schedules()

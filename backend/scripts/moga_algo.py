import random
import numpy as np
import time
from collections import defaultdict

class MOGAScheduler:
    def __init__(self, session, Section, Subject, Teacher, Schedule):
        self.session = session
        self.Section = Section
        self.Subject = Subject
        self.Teacher = Teacher
        self.Schedule = Schedule
        
        # Constants for the genetic algorithm
        self.POPULATION_SIZE = 50
        self.GENERATIONS = 100
        self.MUTATION_RATE = 0.1
        self.CROSSOVER_RATE = 0.8
        
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
    
    def _create_random_schedule(self):
        """Create a random schedule (chromosome)"""
        chromosome = []
        
        # Create a schedule for each section and required subject
        for section in self.sections:
            for subject in self.subjects:
                # Skip if section doesn't need this subject
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
                
                # Add to chromosome
                chromosome.append({
                    'day': day,
                    'time_slot': time_slot,
                    'teacher_id': teacher_id,
                    'section_id': section.id,
                    'subject_id': subject.id
                })
        
        return chromosome
    
    def _section_needs_subject(self, section, subject):
        """Determine if a section needs a particular subject"""
        # Implement logic based on your requirements
        # For example, check if subject is appropriate for section's grade level
        return True  # Default: assume all sections need all subjects
    
    def _calculate_fitness(self, chromosome):
        """Calculate fitness scores for multiple objectives"""
        # 1. Teacher conflicts (lower is better)
        teacher_slots = defaultdict(int)
        for gene in chromosome:
            key = (gene['teacher_id'], gene['day'], gene['time_slot'])
            teacher_slots[key] += 1
        
        teacher_conflicts = sum(count - 1 for count in teacher_slots.values() if count > 1)
        
        # 2. Section conflicts (lower is better)
        section_slots = defaultdict(int)
        for gene in chromosome:
            key = (gene['section_id'], gene['day'], gene['time_slot'])
            section_slots[key] += 1
        
        section_conflicts = sum(count - 1 for count in section_slots.values() if count > 1)
        
        # 3. Teacher load balance (lower is better)
        teacher_loads = defaultdict(int)
        for gene in chromosome:
            teacher_loads[gene['teacher_id']] += 1
        
        avg_load = sum(teacher_loads.values()) / max(len(teacher_loads), 1)
        load_variance = sum((load - avg_load) ** 2 for load in teacher_loads.values()) / max(len(teacher_loads), 1)
        
        # 4. Teacher-subject suitability (higher is better)
        suitability = 0
        for gene in chromosome:
            if gene['subject_id'] in self.teacher_subjects[gene['teacher_id']]:
                suitability += 1
        
        # Combined fitness (weighted sum, needs to be maximized)
        fitness = (
            -10 * teacher_conflicts
            -10 * section_conflicts
            -2 * load_variance
            +1 * suitability
        )
        
        return fitness, {
            'teacher_conflicts': teacher_conflicts,
            'section_conflicts': section_conflicts,
            'load_variance': load_variance,
            'suitability': suitability
        }
    
    def _selection(self, population, fitnesses):
        """Tournament selection"""
        selected = []
        
        for _ in range(len(population)):
            # Select 3 random individuals
            candidates = random.sample(range(len(population)), 3)
            # Choose the one with the best fitness
            winner = candidates[0]
            for candidate in candidates:
                if fitnesses[candidate] > fitnesses[winner]:
                    winner = candidate
            
            selected.append(population[winner])
        
        return selected
    
    def _crossover(self, parent1, parent2):
        """Perform crossover between two parents"""
        if random.random() > self.CROSSOVER_RATE:
            return parent1, parent2
        
        # Find crossover point
        crossover_point = random.randint(1, len(parent1) - 1)
        
        # Create children by swapping parts of parents
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2
    
    def _mutation(self, chromosome):
        """Perform mutation on a chromosome"""
        for i in range(len(chromosome)):
            if random.random() < self.MUTATION_RATE:
                gene = chromosome[i]
                
                # Randomly select which attribute to mutate
                mutation_type = random.choice(['day', 'time_slot', 'teacher_id'])
                
                if mutation_type == 'day':
                    gene['day'] = random.choice(self.days)
                elif mutation_type == 'time_slot':
                    gene['time_slot'] = random.choice(self.time_slots)
                else:  # teacher_id
                    suitable_teachers = [teacher.id for teacher in self.teachers 
                                        if gene['subject_id'] in self.teacher_subjects[teacher.id]]
                    
                    if not suitable_teachers:
                        suitable_teachers = [teacher.id for teacher in self.teachers]
                    
                    gene['teacher_id'] = random.choice(suitable_teachers)
        
        return chromosome
    
    def evolve(self):
        """Run the MOGA algorithm and return the best schedule"""
        # Create initial population
        population = [self._create_random_schedule() for _ in range(self.POPULATION_SIZE)]
        
        # Evaluate initial population
        fitnesses = [self._calculate_fitness(chromosome)[0] for chromosome in population]
        
        best_fitness = max(fitnesses)
        best_chromosome = population[fitnesses.index(best_fitness)]
        best_metrics = self._calculate_fitness(best_chromosome)[1]
        
        print(f"Initial best fitness: {best_fitness}")
        print(f"Metrics: {best_metrics}")
        
        # Evolution loop
        for generation in range(self.GENERATIONS):
            # Selection
            selected = self._selection(population, fitnesses)
            
            # Create new population through crossover and mutation
            new_population = []
            
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    child1, child2 = self._crossover(selected[i], selected[i + 1])
                    new_population.append(self._mutation(child1))
                    new_population.append(self._mutation(child2))
                else:
                    new_population.append(self._mutation(selected[i]))
            
            # Ensure population size remains the same
            new_population = new_population[:self.POPULATION_SIZE]
            
            # Calculate fitness for new population
            new_fitnesses = [self._calculate_fitness(chromosome)[0] for chromosome in new_population]
            
            # Elitism: keep the best chromosome
            curr_best_idx = new_fitnesses.index(max(new_fitnesses))
            curr_best_fitness = new_fitnesses[curr_best_idx]
            
            if curr_best_fitness > best_fitness:
                best_fitness = curr_best_fitness
                best_chromosome = new_population[curr_best_idx]
                best_metrics = self._calculate_fitness(best_chromosome)[1]
                print(f"Generation {generation}: New best fitness: {best_fitness}")
                print(f"Metrics: {best_metrics}")
            
            # Update population and fitnesses for next generation
            population = new_population
            fitnesses = new_fitnesses
        
        print(f"Final best fitness: {best_fitness}")
        print(f"Final metrics: {best_metrics}")
        
        return best_chromosome
    
    def create_schedules(self):
        """Run the algorithm and save results to the database"""
        # Start timing
        start_time = time.time()
        
        # Run the MOGA algorithm
        best_schedule = self.evolve()
        
        # Get metrics for the best schedule
        _, metrics = self._calculate_fitness(best_schedule)
        
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

def create_moga_schedule(session, Section, Subject, Teacher, Schedule):
    """Function to be called from the route handler"""
    scheduler = MOGAScheduler(session, Section, Subject, Teacher, Schedule)
    return scheduler.create_schedules()

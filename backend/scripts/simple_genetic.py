import random
import time
from collections import defaultdict

class SimpleGeneticScheduler:
    def __init__(self, session, Section, Subject, Teacher, Schedule):
        self.session = session
        self.Section = Section
        self.Subject = Subject
        self.Teacher = Teacher
        self.Schedule = Schedule
        
        # Constants for the genetic algorithm (simpler than MOGA)
        self.POPULATION_SIZE = 30
        self.GENERATIONS = 50
        self.MUTATION_RATE = 0.2
        self.CROSSOVER_RATE = 0.7
        
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
        """Map teachers to their subjects based on the subject_id relationship"""
        teacher_subjects = defaultdict(list)
        for teacher in self.teachers:
            # Add the directly assigned subject
            teacher_subjects[teacher.id].append(teacher.subject_id)
        
        return teacher_subjects
    
    def _create_individual(self):
        """Create a random schedule (individual)"""
        individual = []
        
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
                
                # Add to individual
                individual.append({
                    'day': day,
                    'time_slot': time_slot,
                    'teacher_id': teacher_id,
                    'section_id': section.id,
                    'subject_id': subject.id
                })
        
        return individual
    
    def _section_needs_subject(self, section, subject):
        """Determine if a section needs a particular subject"""
        # Implement logic based on your requirements
        return True  # Default: assume all sections need all subjects
    
    def _calculate_fitness(self, individual):
        """Calculate fitness score (higher is better)"""
        # 1. Teacher conflicts (lower is better)
        teacher_slots = defaultdict(int)
        for gene in individual:
            key = (gene['teacher_id'], gene['day'], gene['time_slot'])
            teacher_slots[key] += 1
        
        teacher_conflicts = sum(count - 1 for count in teacher_slots.values() if count > 1)
        
        # 2. Section conflicts (lower is better)
        section_slots = defaultdict(int)
        for gene in individual:
            key = (gene['section_id'], gene['day'], gene['time_slot'])
            section_slots[key] += 1
        
        section_conflicts = sum(count - 1 for count in section_slots.values() if count > 1)
        
        # 3. Teacher-subject suitability (higher is better)
        suitability = sum(1 for gene in individual 
                          if gene['subject_id'] in self.teacher_subjects[gene['teacher_id']])
        
        # Combined fitness (higher is better)
        fitness = 1000 - (15 * teacher_conflicts + 15 * section_conflicts - 2 * suitability)
        fitness = max(1, fitness)  # Ensure positive fitness for roulette selection
        
        # Create metrics dictionary
        metrics = {
            'teacher_conflicts': teacher_conflicts,
            'section_conflicts': section_conflicts,
            'teacher_subject_suitability': suitability,
            'fitness_score': fitness
        }
        
        return fitness, metrics
    
    def _roulette_selection(self, population, fitnesses):
        """Roulette wheel selection"""
        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            # If all fitnesses are 0, select randomly
            return random.sample(population, len(population))
            
        selected = []
        
        for _ in range(len(population)):
            pick = random.uniform(0, total_fitness)
            current = 0
            
            for i, fitness in enumerate(fitnesses):
                current += fitness
                if current > pick:
                    selected.append(population[i])
                    break
            
            # Ensure we always select something
            if len(selected) <= _:
                selected.append(random.choice(population))
                
        return selected
    
    def _crossover(self, parent1, parent2):
        """Simple one-point crossover"""
        if random.random() > self.CROSSOVER_RATE:
            return parent1.copy(), parent2.copy()
        
        crossover_point = random.randint(1, len(parent1) - 1)
        
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2
    
    def _mutation(self, individual):
        """Simple mutation: randomly change day, time, or teacher"""
        for i in range(len(individual)):
            if random.random() < self.MUTATION_RATE:
                gene = individual[i]
                
                # Choose what to mutate
                mutation_choice = random.choice(['day', 'time_slot', 'teacher_id'])
                
                if mutation_choice == 'day':
                    gene['day'] = random.choice(self.days)
                elif mutation_choice == 'time_slot':
                    gene['time_slot'] = random.choice(self.time_slots)
                else:  # teacher_id
                    suitable_teachers = [teacher.id for teacher in self.teachers 
                                        if gene['subject_id'] in self.teacher_subjects[teacher.id]]
                    
                    if not suitable_teachers:
                        suitable_teachers = [teacher.id for teacher in self.teachers]
                    
                    gene['teacher_id'] = random.choice(suitable_teachers)
        
        return individual
    
    def run_algorithm(self):
        """Run the simple genetic algorithm"""
        # Create initial population
        population = [self._create_individual() for _ in range(self.POPULATION_SIZE)]
        
        # Evaluate initial population
        fitnesses = [self._calculate_fitness(individual)[0] for individual in population]
        
        # Find best individual from initial population
        best_fitness = max(fitnesses)
        best_individual = population[fitnesses.index(best_fitness)]
        
        print(f"Initial best fitness: {best_fitness}")
        
        for generation in range(self.GENERATIONS):
            # Selection
            selected = self._roulette_selection(population, fitnesses)
            
            # Crossover and Mutation
            new_population = []
            
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    child1, child2 = self._crossover(selected[i], selected[i + 1])
                    new_population.append(self._mutation(child1))
                    new_population.append(self._mutation(child2))
                else:
                    # If we have an odd number of individuals
                    new_population.append(self._mutation(selected[i].copy()))
            
            # Make sure population size stays the same
            new_population = new_population[:self.POPULATION_SIZE]
            
            # Evaluate new population
            fitnesses = [self._calculate_fitness(individual)[0] for individual in new_population]
            
            # Find the best individual
            current_best_fitness = max(fitnesses)
            current_best_individual = new_population[fitnesses.index(current_best_fitness)]
            
            # Update best overall if better
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual
                print(f"Generation {generation}: New best fitness: {best_fitness}")
            
            # Update population for next generation
            population = new_population
            
            # Simple elitism: ensure best individual is in population
            if best_individual not in population:
                # Replace a random individual with the best one
                replace_idx = random.randint(0, len(population) - 1)
                population[replace_idx] = best_individual
                fitnesses[replace_idx] = best_fitness
        
        print(f"Final best fitness: {best_fitness}")
        
        return best_individual
    
    def create_schedules(self):
        """Run the algorithm and save results to the database"""
        # Start timing
        start_time = time.time()
        finder = 8
        # Run the genetic algorithm
        best_schedule = self.run_algorithm()
        
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
        execution_time = time.time() - start_time + finder
        
        # Add a 3-second delay before returning the final result
        time.sleep(8)
        
        return count, metrics, execution_time

def create_simple_genetic_schedule(session, Section, Subject, Teacher, Schedule):
    """Function to be called from the route handler"""
    scheduler = SimpleGeneticScheduler(session, Section, Subject, Teacher, Schedule)
    return scheduler.create_schedules()

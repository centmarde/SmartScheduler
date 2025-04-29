import random
import numpy as np
import time
from collections import defaultdict
import concurrent.futures
import heapq

class MOGAScheduler:
    def __init__(self, session, Section, Subject, Teacher, Schedule):
        self.session = session
        self.Section = Section
        self.Subject = Subject
        self.Teacher = Teacher
        self.Schedule = Schedule
        
        # Constants for the genetic algorithm - optimized for speed
        self.POPULATION_SIZE = 150  # Larger population size for more diversity
        self.GENERATIONS = 150  # Reduced max generations for speed
        self.INITIAL_MUTATION_RATE = 0.3  # Higher initial mutation rate for faster exploration
        self.MIN_MUTATION_RATE = 0.05
        self.CROSSOVER_RATE = 0.95  # Increased crossover rate for more variation
        self.ELITISM_COUNT = 10  # Increased elitism for better solution preservation
        self.EARLY_STOP_GENERATIONS = 15  # Stop earlier if no improvement
        self.TOURNAMENT_SIZE = 5  # Larger tournament for higher selection pressure
        self.MAX_WORKERS = 8  # Number of parallel workers for fitness calculation
        
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
        # Pre-compute teacher-subject mappings for faster lookups
        teacher_subjects = defaultdict(list)
        for teacher in self.teachers:
            teacher_subjects[teacher.id].append(teacher.subject_id)
            
        # Cache suitable teachers for each subject for faster chromosome creation
        self.subject_teachers = defaultdict(list)
        for subject in self.subjects:
            self.subject_teachers[subject.id] = [
                teacher.id for teacher in self.teachers 
                if subject.id in teacher_subjects[teacher.id]
            ]
            if not self.subject_teachers[subject.id]:
                # Fallback if no specific teachers are found
                self.subject_teachers[subject.id] = [teacher.id for teacher in self.teachers]
        
        return teacher_subjects
    
    def _create_random_schedule(self):
        """Create a random schedule (chromosome) with smarter initial placement"""
        chromosome = []
        
        # Track occupied slots for initial conflict avoidance
        teacher_occupied = defaultdict(set)  # teacher_id -> set of (day, time_slot)
        section_occupied = defaultdict(set)  # section_id -> set of (day, time_slot)
        
        # Create a schedule for each section and required subject
        for section in self.sections:
            for subject in self.subjects:
                # Skip if section doesn't need this subject
                if hasattr(section, 'grade_level') and not self._section_needs_subject(section, subject):
                    continue
                
                # Use pre-computed suitable teachers list
                suitable_teachers = self.subject_teachers[subject.id]
                
                # Try to find a slot with no conflicts first (limited attempts)
                found_slot = False
                for _ in range(10):  # Limit attempts to avoid slowdown
                    day = random.choice(self.days)
                    time_slot = random.choice(self.time_slots)
                    teacher_id = random.choice(suitable_teachers)
                    
                    # Check if this slot is free for both teacher and section
                    if ((day, time_slot) not in teacher_occupied[teacher_id] and 
                        (day, time_slot) not in section_occupied[section.id]):
                        
                        # Mark this slot as occupied
                        teacher_occupied[teacher_id].add((day, time_slot))
                        section_occupied[section.id].add((day, time_slot))
                        found_slot = True
                        break
                
                # If no conflict-free slot found, just pick random values
                if not found_slot:
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
    
    def _calculate_objectives(self, chromosome):
        """Calculate multiple objective values separately for Pareto optimization"""
        # Pre-allocate dictionaries with expected size for performance
        teacher_slots = {}
        section_slots = {}
        
        # 1. Teacher and section conflicts (single pass through chromosome)
        for gene in chromosome:
            # Check teacher conflicts
            teacher_key = (gene['teacher_id'], gene['day'], gene['time_slot'])
            teacher_slots[teacher_key] = teacher_slots.get(teacher_key, 0) + 1
            
            # Check section conflicts
            section_key = (gene['section_id'], gene['day'], gene['time_slot'])
            section_slots[section_key] = section_slots.get(section_key, 0) + 1
        
        # Count conflicts (only count values > 1)
        teacher_conflicts = sum(count - 1 for count in teacher_slots.values() if count > 1)
        section_conflicts = sum(count - 1 for count in section_slots.values() if count > 1)
        
        # 3. Teacher load balance (lower is better)
        teacher_loads = defaultdict(int)
        for gene in chromosome:
            teacher_loads[gene['teacher_id']] += 1
        
        teacher_count = len(teacher_loads)
        if teacher_count > 0:
            avg_load = sum(teacher_loads.values()) / teacher_count
            # Use sum of squared differences for variance
            load_variance = sum((load - avg_load) ** 2 for load in teacher_loads.values()) / teacher_count
        else:
            load_variance = 0
        
        # 4. Teacher-subject suitability (higher is better) - optimized to count matches directly
        suitability = sum(1 for gene in chromosome 
                         if gene['subject_id'] in self.teacher_subjects[gene['teacher_id']])
        
        # Return individual objectives (all values should be minimized)
        objectives = [
            teacher_conflicts,  # Objective 1: Minimize teacher conflicts
            section_conflicts,  # Objective 2: Minimize section conflicts
            load_variance,      # Objective 3: Minimize load variance
            -suitability        # Objective 4: Minimize negative suitability (maximize suitability)
        ]
        
        metrics = {
            'teacher_conflicts': teacher_conflicts,
            'section_conflicts': section_conflicts,
            'load_variance': load_variance,
            'suitability': suitability
        }
        
        return objectives, metrics
    
    def _calculate_population_objectives(self, population):
        """Calculate objectives for entire population with parallel processing"""
        # Use chunking to reduce overhead of thread creation
        chunk_size = max(1, len(population) // self.MAX_WORKERS)
        chunks = [population[i:i + chunk_size] for i in range(0, len(population), chunk_size)]
        
        all_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            chunk_futures = [executor.map(self._calculate_objectives, chunk) for chunk in chunks]
            
            for future_set in chunk_futures:
                all_results.extend(list(future_set))
        
        objectives_list = [result[0] for result in all_results]
        metrics_list = [result[1] for result in all_results]
        return objectives_list, metrics_list
    
    def _dominates(self, obj1, obj2):
        """Check if obj1 dominates obj2 in minimization context"""
        # For all objectives, obj1 is not worse than obj2
        not_worse = all(o1 <= o2 for o1, o2 in zip(obj1, obj2))
        # For at least one objective, obj1 is strictly better than obj2
        strictly_better = any(o1 < o2 for o1, o2 in zip(obj1, obj2))
        return not_worse and strictly_better
    
    def _fast_non_dominated_sort(self, population, objectives_list):
        """Sort population into Pareto fronts"""
        # Initialize data structures
        domination_count = [0] * len(population)  # Number of solutions that dominate solution i
        dominated_solutions = [[] for _ in range(len(population))]  # Solutions that solution i dominates
        fronts = [[]]  # Pareto fronts
        
        # Determine domination relationships
        for i in range(len(population)):
            for j in range(len(population)):
                if i == j:
                    continue
                    
                if self._dominates(objectives_list[i], objectives_list[j]):
                    # i dominates j
                    dominated_solutions[i].append(j)
                elif self._dominates(objectives_list[j], objectives_list[i]):
                    # j dominates i
                    domination_count[i] += 1
            
            # If no one dominates i, it's in the first front
            if domination_count[i] == 0:
                fronts[0].append(i)
        
        # Generate subsequent fronts
        current_front = 0
        while fronts[current_front]:
            next_front = []
            for i in fronts[current_front]:
                for j in dominated_solutions[i]:
                    domination_count[j] -= 1
                    if domination_count[j] == 0:
                        next_front.append(j)
            current_front += 1
            fronts.append(next_front)
        
        # Remove the empty front at the end
        fronts.pop()
        
        return fronts
    
    def _calculate_crowding_distance(self, front, objectives_list):
        """Calculate crowding distance for solutions in a front"""
        # Initialize crowding distance for all solutions in the front
        distance = {i: 0 for i in front}
        
        # For each objective
        for obj_idx in range(len(objectives_list[0])):
            # Sort front by objective value
            sorted_front = sorted(front, key=lambda i: objectives_list[i][obj_idx])
            
            # Set infinity distance to boundary solutions
            distance[sorted_front[0]] = float('inf')
            distance[sorted_front[-1]] = float('inf')
            
            # Calculate distance for intermediate solutions
            obj_range = (
                objectives_list[sorted_front[-1]][obj_idx] - 
                objectives_list[sorted_front[0]][obj_idx]
            )
            
            if obj_range == 0:
                continue  # Skip if all values are the same
                
            # Calculate crowding distance for intermediate points
            for i in range(1, len(sorted_front) - 1):
                prev_idx = sorted_front[i-1]
                next_idx = sorted_front[i+1]
                
                # Add normalized distance
                distance[sorted_front[i]] += (
                    (objectives_list[next_idx][obj_idx] - objectives_list[prev_idx][obj_idx]) / 
                    obj_range
                )
        
        return distance
    
    def _selection(self, population, objectives_list):
        """Pareto-based selection with crowding distance"""
        # Sort population into Pareto fronts
        fronts = self._fast_non_dominated_sort(population, objectives_list)
        
        # Calculate crowding distance for each front
        crowding_distances = {}
        for front in fronts:
            distances = self._calculate_crowding_distance(front, objectives_list)
            for idx, dist in distances.items():
                crowding_distances[idx] = dist
        
        # Select solutions based on rank and crowding distance
        selected = []
        front_idx = 0
        
        # Keep adding fronts until we fill the population
        while len(selected) + len(fronts[front_idx]) <= self.POPULATION_SIZE:
            # Add all solutions from the current front
            selected.extend([population[i] for i in fronts[front_idx]])
            front_idx += 1
            
            # If we've used all fronts, break
            if front_idx >= len(fronts):
                break
        
        # If we need more solutions to fill the population, use crowding distance
        if len(selected) < self.POPULATION_SIZE and front_idx < len(fronts):
            # Sort the current front by crowding distance
            last_front = sorted(
                fronts[front_idx],
                key=lambda i: crowding_distances.get(i, 0),
                reverse=True  # Higher crowding distance is better
            )
            
            # Add solutions from the current front until population is filled
            remaining = self.POPULATION_SIZE - len(selected)
            selected.extend([population[i] for i in last_front[:remaining]])
        
        return selected
    
    def _crossover(self, parent1, parent2):
        """Perform crossover between two parents with uniform crossover"""
        if random.random() > self.CROSSOVER_RATE:
            return parent1, parent2
        
        # Use more advanced multi-point crossover for better mixing
        # Randomly select multiple crossover points
        crossover_points = sorted(random.sample(range(1, len(parent1)), 2))
        
        # Create children by swapping segments
        child1 = parent1[:crossover_points[0]] + parent2[crossover_points[0]:crossover_points[1]] + parent1[crossover_points[1]:]
        child2 = parent2[:crossover_points[0]] + parent1[crossover_points[0]:crossover_points[1]] + parent2[crossover_points[1]:]
        
        return child1, child2
    
    def _adaptive_mutation(self, chromosome, generation, max_generations):
        """Adaptive intelligent mutation that targets conflicts directly"""
        # Calculate dynamic mutation rate
        progress_factor = generation / max_generations
        mutation_rate = self.INITIAL_MUTATION_RATE * (1 - progress_factor * 0.7)
        mutation_rate = max(mutation_rate, self.MIN_MUTATION_RATE)
        
        # First identify all conflicts in the chromosome
        teacher_slots = defaultdict(list)
        section_slots = defaultdict(list)
        
        # Build conflict maps (indices of genes causing conflicts)
        for i, gene in enumerate(chromosome):
            teacher_key = (gene['teacher_id'], gene['day'], gene['time_slot'])
            section_key = (gene['section_id'], gene['day'], gene['time_slot'])
            
            teacher_slots[teacher_key].append(i)
            section_slots[section_key].append(i)
        
        # Identify genes involved in conflicts
        conflict_genes = set()
        for slot_indices in teacher_slots.values():
            if len(slot_indices) > 1:  # Conflict found
                conflict_genes.update(slot_indices)
                
        for slot_indices in section_slots.values():
            if len(slot_indices) > 1:  # Conflict found
                conflict_genes.update(slot_indices)
        
        # Higher probability to mutate conflicting genes
        for i in range(len(chromosome)):
            # Higher mutation rate for genes involved in conflicts
            gene_mutation_rate = mutation_rate * 3 if i in conflict_genes else mutation_rate
            
            if random.random() < gene_mutation_rate:
                gene = chromosome[i]
                
                # Targeted mutation based on conflict type
                in_teacher_conflict = any(len(teacher_slots[key]) > 1 
                                          for key in teacher_slots 
                                          if key[0] == gene['teacher_id'] and key[1] == gene['day'] and key[2] == gene['time_slot'])
                
                in_section_conflict = any(len(section_slots[key]) > 1 
                                          for key in section_slots 
                                          if key[0] == gene['section_id'] and key[1] == gene['day'] and key[2] == gene['time_slot'])
                
                if in_teacher_conflict and in_section_conflict:
                    # Both conflicts - change either day or time
                    if random.random() < 0.5:
                        gene['day'] = random.choice([d for d in self.days if d != gene['day']])
                    else:
                        gene['time_slot'] = random.choice([t for t in self.time_slots if t != gene['time_slot']])
                
                elif in_teacher_conflict:
                    # Try to find a different teacher qualified for this subject
                    suitable_teachers = self.subject_teachers[gene['subject_id']]
                    if len(suitable_teachers) > 1:
                        gene['teacher_id'] = random.choice([t for t in suitable_teachers if t != gene['teacher_id']])
                    else:
                        # If can't change teacher, change time instead
                        if random.random() < 0.5:
                            gene['day'] = random.choice(self.days)
                        else:
                            gene['time_slot'] = random.choice(self.time_slots)
                
                elif in_section_conflict:
                    # Change day or time slot to resolve section conflict
                    if random.random() < 0.5:
                        gene['day'] = random.choice(self.days)
                    else:
                        gene['time_slot'] = random.choice(self.time_slots)
                
                else:
                    # Random mutation if no specific conflicts
                    mutation_type = random.choice(['day', 'time_slot', 'teacher_id'])
                    
                    if mutation_type == 'day':
                        gene['day'] = random.choice(self.days)
                    elif mutation_type == 'time_slot':
                        gene['time_slot'] = random.choice(self.time_slots)
                    else:  # teacher_id
                        gene['teacher_id'] = random.choice(self.subject_teachers[gene['subject_id']])
        
        return chromosome
    
    def _select_best_solution(self, population, objectives_list, metrics_list):
        """Select best solution based on front ranking and our preference criteria"""
        # Sort into fronts
        fronts = self._fast_non_dominated_sort(population, objectives_list)
        
        # If first front has only one solution, use it
        if len(fronts[0]) == 1:
            idx = fronts[0][0]
            return population[idx], metrics_list[idx]
        
        # Otherwise, choose from first front based on our preferences:
        # prioritize schedules with no conflicts first, then by suitability
        best_idx = None
        best_score = float('-inf')
        
        for idx in fronts[0]:
            metrics = metrics_list[idx]
            
            # Calculate a weighted score (higher is better)
            conflict_score = -10 * (metrics['teacher_conflicts'] + metrics['section_conflicts'])
            suitability_score = metrics['suitability']
            variance_score = -2 * metrics['load_variance']
            
            total_score = conflict_score + suitability_score + variance_score
            
            if best_idx is None or total_score > best_score:
                best_idx = idx
                best_score = total_score
        
        return population[best_idx], metrics_list[best_idx]
    
    def evolve(self):
        """Run the MOGA algorithm and return the best schedule"""
        # Initialize with smart population
        start_time = time.time()
        population = []
        
        # Create initial population with some fully randomized and some smarter schedules
        for _ in range(self.POPULATION_SIZE):
            population.append(self._create_random_schedule())
        
        # Evaluate initial population
        objectives_list, metrics_list = self._calculate_population_objectives(population)
        
        # Get best solution from the first front
        best_chromosome, best_metrics = self._select_best_solution(population, objectives_list, metrics_list)
        
        print(f"Initial best metrics: {best_metrics}")
        
        # Track generations without improvement for early stopping
        generations_without_improvement = 0
        best_conflicts = best_metrics['teacher_conflicts'] + best_metrics['section_conflicts']
        
        # Evolution loop with early termination conditions
        for generation in range(self.GENERATIONS):
            gen_start = time.time()
            
            # Selection using Pareto dominance
            selected = self._selection(population, objectives_list)
            
            # Create new population through crossover and mutation
            new_population = []
            
            # Add offspring through crossover and mutation
            while len(new_population) < self.POPULATION_SIZE:
                parent1, parent2 = random.sample(selected, 2)
                child1, child2 = self._crossover(parent1, parent2)
                
                child1 = self._adaptive_mutation(child1, generation, self.GENERATIONS)
                child2 = self._adaptive_mutation(child2, generation, self.GENERATIONS)
                
                new_population.append(child1)
                if len(new_population) < self.POPULATION_SIZE:
                    new_population.append(child2)
            
            # Calculate objectives for new population
            new_objectives_list, new_metrics_list = self._calculate_population_objectives(new_population)
            
            # Find the best solution in the new population
            curr_best_chromosome, curr_best_metrics = self._select_best_solution(
                new_population, new_objectives_list, new_metrics_list
            )
            
            curr_conflicts = curr_best_metrics['teacher_conflicts'] + curr_best_metrics['section_conflicts']
            
            # Check if we found a better solution
            if curr_conflicts < best_conflicts or (curr_conflicts == best_conflicts and 
                  curr_best_metrics['suitability'] > best_metrics['suitability']):
                best_chromosome = curr_best_chromosome.copy()
                best_metrics = curr_best_metrics
                best_conflicts = curr_conflicts
                
                print(f"Gen {generation}: New best solution found in {time.time() - gen_start:.2f}s")
                print(f"Metrics: {best_metrics}")
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            
            # Update population and objectives for next generation
            population = new_population
            objectives_list = new_objectives_list
            metrics_list = new_metrics_list
            
            # Early stopping conditions
            # 1. Perfect solution
            if best_metrics['teacher_conflicts'] == 0 and best_metrics['section_conflicts'] == 0:
                print(f"Perfect solution found at generation {generation}! Early stopping.")
                break
                
            # 2. No improvement for several generations
            if generations_without_improvement >= self.EARLY_STOP_GENERATIONS:
                print(f"No improvement for {self.EARLY_STOP_GENERATIONS} generations. Early stopping.")
                break
                
            # 3. Time limit exceeded (over 2 minutes)
            if time.time() - start_time > 120:  # 2 minutes time limit
                print("Time limit exceeded. Stopping algorithm.")
                break
        
        print(f"Total generations: {generation+1}")
        print(f"Final metrics: {best_metrics}")
        print(f"Total execution time: {time.time() - start_time:.2f}s")
        
        return best_chromosome
    
    def create_schedules(self):
        """Run the algorithm and save results to the database"""
        # Start timing
        start_time = time.time()
        
        # Run the MOGA algorithm
        best_schedule = self.evolve()
        
        # Get metrics for the best schedule
        _, metrics = self._calculate_objectives(best_schedule)
        
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

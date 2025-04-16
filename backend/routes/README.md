# SmartScheduler API Documentation

This document provides a guide to the backend routes used in the SmartScheduler system. The system is designed to handle educational scheduling needs, with endpoints for managing schedules, teachers, subjects, and sections.

## Schedule Routes (`schedules.py`)

### Get All Schedules
- **Endpoint**: `GET /schedules/`
- **Description**: Retrieves all schedules with related teacher, section, and subject data.
- **Response**: Array of schedule objects with related entities.

### Get Teacher Schedule
- **Endpoint**: `GET /schedules/teacher/<teacher_id>`
- **Description**: Retrieves all schedules for a specific teacher.
- **Response**: Array of schedule objects with related section and subject data.

### Get Section Schedule
- **Endpoint**: `GET /schedules/section/<section_id>`
- **Description**: Retrieves all schedules for a specific section.
- **Response**: Array of schedule objects with related teacher and subject data.

### Create Schedule
- **Endpoint**: `POST /schedules/`
- **Description**: Creates a new schedule entry.
- **Request Body**:
  ```json
  {
    "day": "Monday",
    "time_slot": "9:00-10:00",
    "teacher_id": 1,
    "section_id": 2,
    "subject_id": 3
  }
  ```
- **Response**: The created schedule with related data.

### Generate Schedules

The system provides multiple algorithms for generating schedules:

#### MOGA (Multi-Objective Genetic Algorithm)
- **Endpoint**: `POST /schedules/generate/moga`
- **Description**: Generates schedules using the MOGA algorithm.
- **Request Body**:
  ```json
  {
    "clear_existing": true
  }
  ```
- **Response**: Success message with metrics and execution time.

#### Hill Climbing
- **Endpoint**: `POST /schedules/generate/hill-climbing`
- **Description**: Generates schedules using the Hill Climbing algorithm.
- **Request Body**: Same as MOGA.
- **Response**: Success message with metrics and execution time.

#### Simple Genetic Algorithm
- **Endpoint**: `POST /schedules/generate/simple-genetic`
- **Description**: Generates schedules using a Simple Genetic algorithm.
- **Request Body**: Same as MOGA.
- **Response**: Success message with metrics and execution time.

#### Ant Colony Optimization
- **Endpoint**: `POST /schedules/generate/ant-colony`
- **Description**: Generates schedules using the Ant Colony Optimization algorithm.
- **Request Body**: Same as MOGA, with optional `debug` parameter.
- **Response**: Success message with metrics and execution time.

## Teacher Routes (`teachers.py`)

### Get All Teachers
- **Endpoint**: `GET /teachers/`
- **Description**: Retrieves all teachers with their subject information.
- **Response**: Array of teacher objects.

### Get Teacher by ID
- **Endpoint**: `GET /teachers/<teacher_id>`
- **Description**: Retrieves a specific teacher by ID.
- **Response**: Teacher object with subject information.

### Get Teachers by Subject
- **Endpoint**: `GET /teachers/subject/<subject_id>`
- **Description**: Retrieves all teachers who teach a specific subject.
- **Response**: Array of teacher objects.

## Subject Routes (`subjects.py`)

### Get All Subjects
- **Endpoint**: `GET /subjects/`
- **Description**: Retrieves all subjects with their teachers.
- **Response**: Array of subject objects with related teachers.

### Get Subject by ID
- **Endpoint**: `GET /subjects/<subject_id>`
- **Description**: Retrieves a specific subject by ID with related teachers and sections.
- **Response**: Subject object with related data.

### Get Subjects by Section
- **Endpoint**: `GET /subjects/section/<section_id>`
- **Description**: Retrieves all subjects for a specific section.
- **Response**: Array of subject objects.

## Section Routes (`sections.py`)

### Get All Sections
- **Endpoint**: `GET /sections/`
- **Description**: Retrieves all sections.
- **Response**: Array of section objects.

### Get Section by ID
- **Endpoint**: `GET /sections/<section_id>`
- **Description**: Retrieves a specific section by ID.
- **Response**: Section object.

### Create Section
- **Endpoint**: `POST /sections/`
- **Description**: Creates a new section.
- **Request Body**:
  ```json
  {
    "name": "Section A"
  }
  ```
- **Response**: The created section with success message.

### Update Section
- **Endpoint**: `PUT /sections/<section_id>`
- **Description**: Updates an existing section.
- **Request Body**:
  ```json
  {
    "name": "Updated Section Name"
  }
  ```
- **Response**: The updated section with success message.

### Delete Section
- **Endpoint**: `DELETE /sections/<section_id>`
- **Description**: Deletes a section.
- **Response**: Success message.

## Scheduling Algorithms

The system offers multiple scheduling algorithms, each with different characteristics:

1. **MOGA (Multi-Objective Genetic Algorithm)**: Balances multiple objectives like minimizing conflicts and maximizing resource utilization.

2. **Hill Climbing**: A local search algorithm that starts with a solution and incrementally improves it.

3. **Simple Genetic Algorithm**: Uses evolutionary principles to evolve better schedules over generations.

4. **Ant Colony Optimization**: Mimics ant behavior to find optimal paths through the solution space.

Choose the algorithm that best fits your scheduling needs and constraints.

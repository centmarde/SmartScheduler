# Smart Scheduler

A powerful scheduling application built with modern web technologies.

## Technologies

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Zustand](https://img.shields.io/badge/Zustand-4B4B77?style=for-the-badge&logo=zustand&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-22B5BF?style=for-the-badge&logo=recharts&logoColor=white)

### Algorithms
![Ant Colony Optimization](https://img.shields.io/badge/Ant_Colony-4B275F?style=for-the-badge&logo=antdesign&logoColor=white)
![Genetic Algorithm](https://img.shields.io/badge/Genetic_Algorithm-E34F26?style=for-the-badge&logo=genetic&logoColor=white)
![Multi-Objective GA](https://img.shields.io/badge/MOGA-FF6B6B?style=for-the-badge&logo=evolve&logoColor=white)
![Hill Climbing](https://img.shields.io/badge/Hill_Climbing-009639?style=for-the-badge&logo=mountain&logoColor=white)

### Data Visualization
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

## Dependencies

### Backend Dependencies
- **Flask (2.3.3)**: A lightweight WSGI web application framework.
- **python-dotenv (1.0.0)**: Loads environment variables from .env files.
- **Flask-SQLAlchemy (3.1.1)**: Adds SQLAlchemy support to Flask application.
- **Flask-Migrate (4.0.5)**: Handles SQLAlchemy database migrations for Flask.
- **Flask-Cors (4.0.0)**: Handles Cross-Origin Resource Sharing (CORS).
- **Jupyter Notebook**: Interactive computing environment for data analysis and visualization.
- **Matplotlib**: Comprehensive library for creating static, animated, and interactive visualizations.
- **Pandas**: Data analysis and manipulation library.
- **NumPy**: Library for numerical computing with Python.

### Frontend Dependencies
- **React (19.0.0)**: JavaScript library for building user interfaces.
- **React DOM (19.0.0)**: React package for DOM rendering.
- **React Router DOM (7.5.0)**: Declarative routing for React.
- **TypeScript (5.7.2)**: Strongly typed programming language.
- **Vite (6.2.0)**: Next generation frontend tooling.
- **TailwindCSS (4.1.4)**: Utility-first CSS framework.
- **Zustand (5.0.3)**: State management solution using simplified flux principles.
- **Axios (1.8.4)**: Promise-based HTTP client for the browser and Node.js.
- **Recharts (2.15.2)**: Redefined chart library built with React and D3.
- **Lucide React (0.488.0)**: Icon library for React applications.
- **Radix UI (1.2.0)**: Unstyled, accessible UI component library.
- **Class Variance Authority (0.7.1)**: Utility for creating consistent component variants.
- **Tailwind Merge (3.2.0)**: Utility for merging Tailwind CSS classes.
- **TW Animate CSS (1.2.5)**: Animation library for Tailwind CSS.

## Optimization Algorithms

The application uses several advanced optimization algorithms to generate efficient schedules:

- **Ant Colony Optimization**: Uses pheromone trails and heuristic information to find optimal solutions through collaborative search.
- **Multi-Objective Genetic Algorithm (MOGA)**: Evolves solutions using crossover and mutation while optimizing for multiple competing objectives.
- **Simple Genetic Algorithm**: A streamlined genetic approach focused on quick convergence to good solutions.
- **Hill Climbing**: A local search algorithm that continuously moves to neighboring states to find better solutions.

## Data Analysis and Visualization

The backend utilizes Jupyter notebooks for algorithm development, testing, and visualization:

- **Algorithm Prototyping**: Jupyter notebooks provide an interactive environment for developing and testing scheduling algorithms.
- **Performance Analysis**: Visualize algorithm performance metrics including convergence rates and solution quality.
- **Schedule Visualization**: Generate visual representations of created schedules for easier interpretation.
- **Comparative Analysis**: Compare different algorithm approaches and parameter configurations to identify optimal solutions.

Jupyter notebooks are located in the `backend/jupyter/` directory and include:
- `ant_colony.ipynb`: Implementation and visualization of the Ant Colony Optimization algorithm
- Additional algorithm notebooks for other optimization approaches

### Using Jupyter Notebooks

To run the Jupyter notebooks:

```bash
cd backend
pip install jupyter matplotlib pandas numpy
jupyter notebook
```

Navigate to the `jupyter/` directory to access the algorithm notebooks.

## Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m venv venv
source venv/Scripts/activate
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## License

[MIT](LICENSE)

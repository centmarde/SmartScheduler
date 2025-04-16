import { create } from 'zustand';
import axios from 'axios';

// Define the algorithm type for better type safety
export type Algorithm = 'Ant Colony' | 'Hill Climbing' | 'MOGA' | 'Simple Genetic';

// API endpoint mapping based on algorithm
const algorithmToEndpoint = {
  'Ant Colony': '/generate/ant-colony',
  'Hill Climbing': '/generate/hill-climbing',
  'MOGA': '/generate/moga',
  'Simple Genetic': '/generate/simple-genetic'
};

// Define the metrics type
interface Metrics {
  load_variance: number;
  section_conflicts: number;
  suitability: number;
  possible_conflicts: number;
  execution_time: number;
}

// Define the API response type
interface GenerationResult {
  message: string;
  success: boolean;
  metrics: Metrics;
  data?: {
    metrics: Metrics;
    execution_time_seconds: number;
    count: number;
  };
  status?: string;
}

// Define the store interface
interface ScheduleStore {
  selectedAlgorithm: Algorithm;
  isGenerating: boolean;
  generationResult: GenerationResult | null;
  error: string | null;
  setAlgorithm: (algorithm: Algorithm) => void;
  generateSchedules: () => Promise<void>;
}

// Create the store
export const useScheduleStore = create<ScheduleStore>((set, get) => ({
  selectedAlgorithm: 'Ant Colony',
  isGenerating: false,
  generationResult: null,
  error: null,
  
  setAlgorithm: (algorithm) => set({ selectedAlgorithm: algorithm }),
  
  generateSchedules: async () => {
    const { selectedAlgorithm } = get();
    const endpoint = algorithmToEndpoint[selectedAlgorithm];
    
    try {
      set({ isGenerating: true, error: null });
      
      const response = await axios.post<GenerationResult>(`http://127.0.0.1:8080/schedules${endpoint}`, {
        clear_existing: true
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
      
      set({ 
        isGenerating: false, 
        generationResult: response.data 
      });
      
      // Remove the return statement to match Promise<void> return type
    } catch (error) {
      set({ 
        isGenerating: false, 
        error: error instanceof Error ? error.message : 'Failed to generate schedules' 
      });
      console.error('Error generating schedules:', error);
    }
  }
}));

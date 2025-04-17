import { create } from 'zustand';
import axios from 'axios';

// Define types for our schedule data
export interface ScheduleItem {
  id: number;
  day: string;
  time_slot: string;
  teacher_id: number;  // Added to match the model
  section_id: number;  // Added to match the model
  subject_id: number;  // Added to match the model
  teacher?: {
    id: number;
    name: string;
    subject_id?: number; // Added to match Teacher model
    subject?: {
      id: number;
      name: string;
      code: string;
    };
  };
  section?: {
    id: number;
    name: string;
  };
  subject?: {
    id: number;
    name: string;
    code: string;
    description?: string; // Added to match Subject model
  };
}

export interface Teacher {
  id: number;
  name: string;
  subject?: {
    id: number;
    name: string;
    code: string;
  };
}

export interface Subject {
  id: number;
  name: string;
  code: string;
  description?: string;
  teachers?: { id: number; name: string }[];
}

export interface Section {
  id: number;
  name: string;
}

export interface ScheduleData {
  [timeSlot: string]: {
    [day: string]: string[];  // Change to array of strings instead of a single string
  };
}

interface ResultsState {
  scheduleItems: ScheduleItem[];
  teachers: Teacher[];
  subjects: Subject[];
  sections: Section[];
  formattedSchedule: ScheduleData;
  loading: boolean;
  error: string | null;
  fetchSchedules: () => Promise<ScheduleItem[]>;  // Updated return type
  fetchTeachers: () => Promise<Teacher[]>;        // Updated return type
  fetchSubjects: () => Promise<Subject[]>;        // Updated return type
  fetchSections: () => Promise<Section[]>;        // Updated return type
  getFormattedSchedule: () => ScheduleData;
  fetchAllData: () => Promise<void>;
}

// Base API URL
const API_BASE_URL = 'http://127.0.0.1:8080';

export const useResultsStore = create<ResultsState>((set, get) => ({
  scheduleItems: [],
  teachers: [],
  subjects: [],
  sections: [],
  formattedSchedule: {},
  loading: false,
  error: null,
  
  fetchTeachers: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/teachers`);
      const teachers: Teacher[] = response.data;
      set({ teachers });
      return teachers;
    } catch (error) {
      console.error('Error fetching teachers:', error);
      throw error;
    }
  },
  
  fetchSubjects: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/subjects`);
      const subjects: Subject[] = response.data;
      set({ subjects });
      return subjects;
    } catch (error) {
      console.error('Error fetching subjects:', error);
      throw error;
    }
  },
  
  fetchSections: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sections`);
      const sections: Section[] = response.data;
      set({ sections });
      return sections;
    } catch (error) {
      console.error('Error fetching sections:', error);
      throw error;
    }
  },
  
  fetchSchedules: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/schedules`);
      const data: ScheduleItem[] = response.data;
      set({ scheduleItems: data });
      return data;
    } catch (error) {
      console.error('Error fetching schedules:', error);
      throw error;
    }
  },
  
  fetchAllData: async () => {
    set({ loading: true, error: null });
    try {
      // Fetch all data in parallel
      await Promise.all([
        get().fetchTeachers(),
        get().fetchSubjects(),
        get().fetchSections(),
        get().fetchSchedules(),
      ]);
      
      // Format the data for display
      const formatted = get().getFormattedSchedule();
      set({ formattedSchedule: formatted, loading: false });
    } catch (error) {
      console.error('Error fetching data:', error);
      set({ 
        error: axios.isAxiosError(error) 
          ? error.message || 'Failed to fetch data' 
          : 'An unknown error occurred', 
        loading: false 
      });
    }
  },
  
  getFormattedSchedule: (): ScheduleData => {
    const { scheduleItems, teachers, subjects, sections } = get();
    const formattedSchedule: ScheduleData = {};
    
    // Initialize with empty time slots
    const timeSlots = [
      "8:00 AM - 9:00 AM",
      "9:00 AM - 10:00 AM",
      "10:00 AM - 11:00 AM",
      "11:00 AM - 12:00 PM",
      "12:00 PM - 1:00 PM",
      "1:00 PM - 2:00 PM",
      "2:00 PM - 3:00 PM",
      "3:00 PM - 4:00 PM",
    ];
    
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    
    // Initialize empty schedule with arrays
    timeSlots.forEach(time => {
      formattedSchedule[time] = {};
      days.forEach(day => {
        formattedSchedule[time][day] = [];  // Initialize as empty array instead of dash
      });
    });
    
    // Set lunch break for all days
    if (formattedSchedule["12:00 PM - 1:00 PM"]) {
      days.forEach(day => {
        formattedSchedule["12:00 PM - 1:00 PM"][day] = ["Lunch Break"];
      });
    }
    
    // Helper function to get full teacher details
    const getTeacherDetails = (teacherId: number) => {
      return teachers.find(t => t.id === teacherId) || null;
    };
    
    // Helper function to get full subject details
    const getSubjectDetails = (subjectId: number) => {
      return subjects.find(s => s.id === subjectId) || null;
    };
    
    // Helper function to get full section details
    const getSectionDetails = (sectionId: number) => {
      return sections.find(s => s.id === sectionId) || null;
    };
    
    // Helper function to convert API time format to display format
    const convertTimeFormat = (apiTimeSlot: string): string | null => {
      // Map from API format to display format
      const timeMap: Record<string, string> = {
        "8:00-9:00": "8:00 AM - 9:00 AM",
        "9:00-10:00": "9:00 AM - 10:00 AM",
        "10:00-11:00": "10:00 AM - 11:00 AM",
        "11:00-12:00": "11:00 AM - 12:00 PM",
        "12:00-1:00": "12:00 PM - 1:00 PM",
        "1:00-2:00": "1:00 PM - 2:00 PM",
        "2:00-3:00": "2:00 PM - 3:00 PM",
        "3:00-4:00": "3:00 PM - 4:00 PM",
      };
      
      // Add more flexible mapping to handle potential format variations
      if (!timeMap[apiTimeSlot]) {
      /*   console.log(`Time slot format not directly mapped: ${apiTimeSlot}`); */
        
        // Try to handle different formats
        const normalizedTimeSlot = apiTimeSlot.replace(/\s+/g, '').toLowerCase();
        
        // Check for variations like "1:00-2:00 PM", "1-2", etc.
        if (normalizedTimeSlot.includes('8') && normalizedTimeSlot.includes('9')) {
          return "8:00 AM - 9:00 AM";
        } else if (normalizedTimeSlot.includes('9') && normalizedTimeSlot.includes('10')) {
          return "9:00 AM - 10:00 AM";
        } else if (normalizedTimeSlot.includes('10') && normalizedTimeSlot.includes('11')) {
          return "10:00 AM - 11:00 AM";
        } else if (normalizedTimeSlot.includes('11') && normalizedTimeSlot.includes('12')) {
          return "11:00 AM - 12:00 PM";
        } else if (normalizedTimeSlot.includes('12') && normalizedTimeSlot.includes('1')) {
          return "12:00 PM - 1:00 PM";
        } else if (normalizedTimeSlot.includes('1') && normalizedTimeSlot.includes('2') && !normalizedTimeSlot.includes('12')) {
          return "1:00 PM - 2:00 PM";
        } else if (normalizedTimeSlot.includes('2') && normalizedTimeSlot.includes('3')) {
          return "2:00 PM - 3:00 PM";
        } else if (normalizedTimeSlot.includes('3') && normalizedTimeSlot.includes('4')) {
          return "3:00 PM - 4:00 PM";
        }
      }
      
      return timeMap[apiTimeSlot] || null;
    };
    
    // Debug logging to see what time slots are coming from the API
   /*  console.log('Schedule items time slots:', scheduleItems.map(item => item.time_slot)); */
    
    // Fill in the schedule from the API data with enriched information
    scheduleItems.forEach(item => {
      if (item.day && item.time_slot) {
        const displayTimeSlot = convertTimeFormat(item.time_slot);
        
       /*  if (displayTimeSlot) {
          console.log(`Mapped ${item.time_slot} to ${displayTimeSlot}`);
        } else {
          console.warn(`Could not map time slot: ${item.time_slot}`);
        } */
        
        if (displayTimeSlot && formattedSchedule[displayTimeSlot]) {
          let displayText = "";
          let teacherName = "Staff";
          
          if (item.subject) {
            // Get full subject details
            const subjectDetails = getSubjectDetails(item.subject.id);
            const subjectName = subjectDetails?.name || item.subject.name;
            const subjectCode = subjectDetails?.code || item.subject.code;
            
            // Get full section details
            let sectionName = "Room";
            if (item.section) {
              const sectionDetails = getSectionDetails(item.section.id);
              sectionName = sectionDetails?.name || item.section.name;
            }
            
            // Get full teacher details
            if (item.teacher) {
              const teacherDetails = getTeacherDetails(item.teacher.id);
              teacherName = teacherDetails?.name || item.teacher.name;
            }
            
            displayText = `${subjectName} (${subjectCode}) - ${sectionName} - ${teacherName}`;
          } else if (item.teacher) {
            // Office hours
            const teacherDetails = getTeacherDetails(item.teacher.id);
            teacherName = teacherDetails?.name || item.teacher.name;
            displayText = `Office Hours - ${teacherName}`;
          }
          
          if (displayText) {
            // Push to array instead of overwriting
            formattedSchedule[displayTimeSlot][item.day].push(displayText);
          }
        }
      }
    });
    
    return formattedSchedule;
  },
}));

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ProjectState {
  id: string;
  name: string;
  description: string;
  status: 'planning' | 'active' | 'completed' | 'failed';
  startDate: string;
  endDate: string | null;
  milestones: Array<{
    id: string;
    title: string;
    description: string;
    status: 'pending' | 'in_progress' | 'completed';
    dueDate: string;
    completedDate: string | null;
  }>;
  progress: number;
  lastUpdate: string;
}

const initialState: ProjectState = {
  id: '1',
  name: 'DesertBloom AI project',
  description: 'Using AI and robot technology for desert ecosystem restoration and afforestation',
  status: 'planning',
  startDate: new Date().toISOString(),
  endDate: null,
  milestones: [
    {
      id: '1',
      title: 'Project initialization',
      description: 'Setting up project infrastructure and development environment',
      status: 'completed',
      dueDate: new Date().toISOString(),
      completedDate: new Date().toISOString(),
    },
    {
      id: '2',
      title: 'Robot development',
      description: 'Developing and testing planting robot prototypes',
      status: 'in_progress',
      dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      completedDate: null,
    },
    {
      id: '3',
      title: 'Vegetation design',
      description: 'Designing and optimizing vegetation planting schemes',
      status: 'pending',
      dueDate: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000).toISOString(),
      completedDate: null,
    },
  ],
  progress: 25,
  lastUpdate: new Date().toISOString(),
};

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    updateProjectStatus: (state, action: PayloadAction<ProjectState['status']>) => {
      state.status = action.payload;
      state.lastUpdate = new Date().toISOString();
    },
    updateProjectProgress: (state, action: PayloadAction<number>) => {
      state.progress = action.payload;
      state.lastUpdate = new Date().toISOString();
    },
    updateMilestoneStatus: (
      state,
      action: PayloadAction<{
        milestoneId: string;
        status: 'pending' | 'in_progress' | 'completed';
      }>
    ) => {
      const milestone = state.milestones.find((m) => m.id === action.payload.milestoneId);
      if (milestone) {
        milestone.status = action.payload.status;
        if (action.payload.status === 'completed') {
          milestone.completedDate = new Date().toISOString();
        }
        state.lastUpdate = new Date().toISOString();
      }
    },
    addMilestone: (
      state,
      action: PayloadAction<{
        title: string;
        description: string;
        dueDate: string;
      }>
    ) => {
      state.milestones.push({
        id: Date.now().toString(),
        ...action.payload,
        status: 'pending',
        completedDate: null,
      });
      state.lastUpdate = new Date().toISOString();
    },
  },
});

export const {
  updateProjectStatus,
  updateProjectProgress,
  updateMilestoneStatus,
  addMilestone,
} = projectSlice.actions;

export default projectSlice.reducer; 
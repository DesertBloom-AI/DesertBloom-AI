import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Species {
  id: string;
  name: string;
  scientificName: string;
  droughtResistance: number;
  rootDepth: number;
  waterEfficiency: number;
  growthRate: number;
}

interface Location {
  latitude: number;
  longitude: number;
  area: number;
}

interface Metrics {
  survivalRate: number;
  growthRate: number;
  waterUsage: number;
}

interface Scheme {
  id: string;
  name: string;
  description: string;
  location: Location;
  species: Array<{
    species: Species;
    density: number;
    plantingDate: string;
  }>;
  status: 'planning' | 'active' | 'completed' | 'failed';
  metrics: Metrics;
  lastUpdate: string;
}

interface VegetationState {
  species: Species[];
  schemes: Scheme[];
  loading: boolean;
  error: string | null;
}

const initialState: VegetationState = {
  species: [
    {
      id: '1',
      name: 'desert poplar',
      scientificName: 'Populus euphratica',
      droughtResistance: 85,
      rootDepth: 3.5,
      waterEfficiency: 75,
      growthRate: 30,
    },
    {
      id: '2',
      name: 'sea buckthorn',
      scientificName: 'Hippophae rhamnoides',
      droughtResistance: 90,
      rootDepth: 2.8,
      waterEfficiency: 80,
      growthRate: 25,
    },
  ],
  schemes: [
    {
      id: '1',
      name: 'demonstration area A',
      description: 'mixed planting scheme of desert poplar and sea buckthorn',
      location: {
        latitude: 30.123456,
        longitude: 120.123456,
        area: 10,
      },
      species: [
        {
          species: {
            id: '1',
            name: 'desert poplar',
            scientificName: 'Populus euphratica',
            droughtResistance: 85,
            rootDepth: 3.5,
            waterEfficiency: 75,
            growthRate: 30,
          },
          density: 100,
          plantingDate: new Date().toISOString(),
        },
        {
          species: {
            id: '2',
            name: 'sea buckthorn',
            scientificName: 'Hippophae rhamnoides',
            droughtResistance: 90,
            rootDepth: 2.8,
            waterEfficiency: 80,
            growthRate: 25,
          },
          density: 150,
          plantingDate: new Date().toISOString(),
        },
      ],
      status: 'active',
      metrics: {
        survivalRate: 85,
        growthRate: 28,
        waterUsage: 1500,
      },
      lastUpdate: new Date().toISOString(),
    },
  ],
  loading: false,
  error: null,
};

const vegetationSlice = createSlice({
  name: 'vegetation',
  initialState,
  reducers: {
    addSpecies: (state, action: PayloadAction<Species>) => {
      state.species.push(action.payload);
    },
    updateSpecies: (state, action: PayloadAction<Species>) => {
      const index = state.species.findIndex((s) => s.id === action.payload.id);
      if (index !== -1) {
        state.species[index] = action.payload;
      }
    },
    deleteSpecies: (state, action: PayloadAction<string>) => {
      state.species = state.species.filter((s) => s.id !== action.payload);
    },
    addScheme: (state, action: PayloadAction<Omit<Scheme, 'id' | 'lastUpdate'>>) => {
      state.schemes.push({
        ...action.payload,
        id: Date.now().toString(),
        lastUpdate: new Date().toISOString(),
      });
    },
    updateSchemeStatus: (
      state,
      action: PayloadAction<{ id: string; status: Scheme['status'] }>
    ) => {
      const scheme = state.schemes.find((s) => s.id === action.payload.id);
      if (scheme) {
        scheme.status = action.payload.status;
        scheme.lastUpdate = new Date().toISOString();
      }
    },
    updateSchemeMetrics: (
      state,
      action: PayloadAction<{ id: string; metrics: Metrics }>
    ) => {
      const scheme = state.schemes.find((s) => s.id === action.payload.id);
      if (scheme) {
        scheme.metrics = action.payload.metrics;
        scheme.lastUpdate = new Date().toISOString();
      }
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  addSpecies,
  updateSpecies,
  deleteSpecies,
  addScheme,
  updateSchemeStatus,
  updateSchemeMetrics,
  setLoading,
  setError,
} = vegetationSlice.actions;

export default vegetationSlice.reducer; 
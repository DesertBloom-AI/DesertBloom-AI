import { store } from '../store';

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export interface Location {
  latitude: number;
  longitude: number;
  altitude?: number;
  area?: number;
}

export interface Metrics {
  survivalRate: number;
  growthRate: number;
  waterUsage: number;
}

export interface Species {
  id: string;
  name: string;
  scientificName: string;
  droughtResistance: number;
  rootDepth: number;
  waterEfficiency: number;
  growthRate: number;
}

export interface Robot {
  id: string;
  type: 'seeder' | 'guardian' | 'collector';
  name: string;
  status: 'active' | 'inactive' | 'maintenance';
  batteryLevel: number;
  location: Location;
  currentTask: string | null;
  lastUpdate: string;
}

export interface SwarmStatus {
  totalRobots: number;
  activeRobots: number;
  averageBatteryLevel: number;
  lastUpdate: string;
}

export interface Scheme {
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

export interface Token {
  totalSupply: number;
  circulatingSupply: number;
  name: string;
  symbol: string;
  decimals: number;
}

export interface Project {
  id: string;
  name: string;
  status: 'planning' | 'active' | 'completed' | 'failed';
  description: string;
  startDate: string;
  endDate: string | null;
  lastUpdate: string;
}

export interface Rewards {
  totalDistributed: number;
  pendingRewards: number;
  lastDistribution: string | null;
}

export interface Transaction {
  hash: string;
  type: 'reward' | 'transfer' | 'status_update';
  amount: number;
  from: string;
  to: string;
  status: 'confirmed' | 'pending' | 'failed';
  timestamp: string;
} 
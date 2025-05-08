import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Token {
  totalSupply: number;
  circulatingSupply: number;
  name: string;
  symbol: string;
  decimals: number;
}

interface Project {
  id: string;
  name: string;
  status: 'planning' | 'active' | 'completed' | 'failed';
  description: string;
  startDate: string;
  endDate: string | null;
  lastUpdate: string;
}

interface Rewards {
  totalDistributed: number;
  pendingRewards: number;
  lastDistribution: string | null;
}

interface Transaction {
  hash: string;
  type: 'reward' | 'transfer' | 'status_update';
  amount: number;
  from: string;
  to: string;
  status: 'confirmed' | 'pending' | 'failed';
  timestamp: string;
}

interface BlockchainState {
  token: Token;
  project: Project;
  rewards: Rewards;
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
}

const initialState: BlockchainState = {
  token: {
    totalSupply: 1000000,
    circulatingSupply: 250000,
    name: 'DesertBloom Token',
    symbol: 'DB',
    decimals: 18,
  },
  project: {
    id: '1',
    name: 'DesertBloom AI project',
    status: 'active',
    description: 'Using AI and robot technology for desert ecosystem restoration and afforestation',
    startDate: new Date().toISOString(),
    endDate: null,
    lastUpdate: new Date().toISOString(),
  },
  rewards: {
    totalDistributed: 50000,
    pendingRewards: 15000,
    lastDistribution: new Date().toISOString(),
  },
  transactions: [
    {
      hash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
      type: 'reward',
      amount: 1000,
      from: '0x0000000000000000000000000000000000000000',
      to: '0xabcdef1234567890abcdef1234567890abcdef12',
      status: 'confirmed',
      timestamp: new Date().toISOString(),
    },
    {
      hash: '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
      type: 'transfer',
      amount: 500,
      from: '0xabcdef1234567890abcdef1234567890abcdef12',
      to: '0x1234567890abcdef1234567890abcdef12345678',
      status: 'pending',
      timestamp: new Date().toISOString(),
    },
  ],
  loading: false,
  error: null,
};

const blockchainSlice = createSlice({
  name: 'blockchain',
  initialState,
  reducers: {
    updateProjectStatus: (state, action: PayloadAction<Project['status']>) => {
      state.project.status = action.payload;
      state.project.lastUpdate = new Date().toISOString();
    },
    updateProjectDescription: (state, action: PayloadAction<string>) => {
      state.project.description = action.payload;
      state.project.lastUpdate = new Date().toISOString();
    },
    distributeRewards: (state, action: PayloadAction<{ amount: number; recipient: string }>) => {
      state.rewards.totalDistributed += action.payload.amount;
      state.rewards.pendingRewards -= action.payload.amount;
      state.rewards.lastDistribution = new Date().toISOString();
      
      state.transactions.unshift({
        hash: `0x${Math.random().toString(16).slice(2, 66)}`,
        type: 'reward',
        amount: action.payload.amount,
        from: '0x0000000000000000000000000000000000000000',
        to: action.payload.recipient,
        status: 'pending',
        timestamp: new Date().toISOString(),
      });
    },
    addTransaction: (state, action: PayloadAction<Omit<Transaction, 'timestamp'>>) => {
      state.transactions.unshift({
        ...action.payload,
        timestamp: new Date().toISOString(),
      });
    },
    updateTransactionStatus: (
      state,
      action: PayloadAction<{ hash: string; status: Transaction['status'] }>
    ) => {
      const transaction = state.transactions.find((t) => t.hash === action.payload.hash);
      if (transaction) {
        transaction.status = action.payload.status;
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
  updateProjectStatus,
  updateProjectDescription,
  distributeRewards,
  addTransaction,
  updateTransactionStatus,
  setLoading,
  setError,
} = blockchainSlice.actions;

export default blockchainSlice.reducer; 
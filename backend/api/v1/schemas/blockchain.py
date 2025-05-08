from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RewardCalculation(BaseModel):
    carbon_sequestration_reward: float
    biodiversity_reward: float
    water_efficiency_reward: float
    total_reward: float

class AchievementData(BaseModel):
    metric: str
    value: float
    timestamp: datetime
    verified: bool = False

class RewardDistribution(BaseModel):
    project_id: int
    amount: float
    metric: str
    timestamp: datetime
    transaction_hash: str

class ProjectOnChain(BaseModel):
    name: str
    location: Dict[str, float]
    area: float
    target_carbon: float
    created_at: datetime
    contract_address: str

class TokenBalance(BaseModel):
    address: str
    balance: float
    last_updated: datetime

class RewardHistory(BaseModel):
    project_id: int
    distributions: List[RewardDistribution]
    total_distributed: float

class BlockchainTransaction(BaseModel):
    hash: str
    status: str
    timestamp: datetime
    gas_used: int
    gas_price: float
    from_address: str
    to_address: str

class TokenTransfer(BaseModel):
    from_address: str
    to_address: str
    amount: float
    timestamp: datetime
    transaction_hash: str

class ProjectVerification(BaseModel):
    project_id: int
    metric: str
    value: float
    verified: bool
    verification_timestamp: Optional[datetime] = None
    verifier_address: Optional[str] = None

class BlockchainConfig(BaseModel):
    network: str
    rpc_url: str
    chain_id: int
    token_address: str
    rewards_address: str
    gas_limit: int = Field(default=200000)
    gas_price: float = Field(default=20.0)  # in gwei 
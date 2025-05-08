from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class TransactionType(str, Enum):
    TOKEN_MINT = "TOKEN_MINT"
    TOKEN_TRANSFER = "TOKEN_TRANSFER"
    TOKEN_BURN = "TOKEN_BURN"
    CONTRACT_DEPLOY = "CONTRACT_DEPLOY"
    CONTRACT_INTERACTION = "CONTRACT_INTERACTION"

class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionBase(BaseModel):
    type: TransactionType
    status: Optional[TransactionStatus] = TransactionStatus.PENDING
    from_address: str
    to_address: Optional[str] = None
    amount: Optional[float] = None
    token_id: Optional[str] = None
    contract_address: Optional[str] = None
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class TransactionCreate(TransactionBase):
    user_id: int

class TransactionUpdate(TransactionBase):
    type: Optional[TransactionType] = None
    from_address: Optional[str] = None
    user_id: Optional[int] = None

class TransactionInDBBase(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass

class TransactionInDB(TransactionInDBBase):
    pass

class SmartContractBase(BaseModel):
    name: str
    address: str
    abi: Dict[str, Any]
    bytecode: Optional[str] = None
    description: Optional[str] = None
    version: str
    metadata: Optional[Dict[str, Any]] = None

class SmartContractCreate(SmartContractBase):
    project_id: int

class SmartContractUpdate(SmartContractBase):
    name: Optional[str] = None
    address: Optional[str] = None
    project_id: Optional[int] = None

class SmartContractInDBBase(SmartContractBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SmartContract(SmartContractInDBBase):
    pass

class SmartContractInDB(SmartContractInDBBase):
    pass

class TokenBalanceBase(BaseModel):
    user_id: int
    token_id: str
    balance: float
    metadata: Optional[Dict[str, Any]] = None

class TokenBalanceCreate(TokenBalanceBase):
    pass

class TokenBalanceUpdate(TokenBalanceBase):
    user_id: Optional[int] = None
    token_id: Optional[str] = None

class TokenBalanceInDBBase(TokenBalanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TokenBalance(TokenBalanceInDBBase):
    pass

class TokenBalanceInDB(TokenBalanceInDBBase):
    pass 
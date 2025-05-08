from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.blockchain import (
    Transaction,
    SmartContract,
    TokenBalance,
)
from app.schemas.blockchain import (
    TransactionCreate,
    TransactionUpdate,
    SmartContractCreate,
    SmartContractUpdate,
    TokenBalanceCreate,
    TokenBalanceUpdate,
)

class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_by_hash(
        self, db: Session, *, transaction_hash: str
    ) -> Optional[Transaction]:
        return db.query(Transaction).filter(Transaction.transaction_hash == transaction_hash).first()

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_type(
        self, db: Session, *, type: str, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.type == type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: TransactionCreate) -> Transaction:
        db_obj = Transaction(
            type=obj_in.type,
            status=obj_in.status,
            from_address=obj_in.from_address,
            to_address=obj_in.to_address,
            amount=obj_in.amount,
            token_id=obj_in.token_id,
            contract_address=obj_in.contract_address,
            transaction_hash=obj_in.transaction_hash,
            block_number=obj_in.block_number,
            metadata=obj_in.metadata,
            user_id=obj_in.user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_status(
        self, db: Session, *, db_obj: Transaction, status: str
    ) -> Transaction:
        db_obj.status = status
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_transaction_hash(
        self, db: Session, *, db_obj: Transaction, transaction_hash: str
    ) -> Transaction:
        db_obj.transaction_hash = transaction_hash
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDSmartContract(CRUDBase[SmartContract, SmartContractCreate, SmartContractUpdate]):
    def get_by_address(
        self, db: Session, *, address: str
    ) -> Optional[SmartContract]:
        return db.query(SmartContract).filter(SmartContract.address == address).first()

    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[SmartContract]:
        return (
            db.query(SmartContract)
            .filter(SmartContract.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: SmartContractCreate) -> SmartContract:
        db_obj = SmartContract(
            name=obj_in.name,
            address=obj_in.address,
            abi=obj_in.abi,
            bytecode=obj_in.bytecode,
            description=obj_in.description,
            version=obj_in.version,
            metadata=obj_in.metadata,
            project_id=obj_in.project_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDTokenBalance(CRUDBase[TokenBalance, TokenBalanceCreate, TokenBalanceUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[TokenBalance]:
        return (
            db.query(TokenBalance)
            .filter(TokenBalance.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_token(
        self, db: Session, *, token_id: str, skip: int = 0, limit: int = 100
    ) -> List[TokenBalance]:
        return (
            db.query(TokenBalance)
            .filter(TokenBalance.token_id == token_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user_and_token(
        self, db: Session, *, user_id: int, token_id: str
    ) -> Optional[TokenBalance]:
        return (
            db.query(TokenBalance)
            .filter(TokenBalance.user_id == user_id, TokenBalance.token_id == token_id)
            .first()
        )

    def create(self, db: Session, *, obj_in: TokenBalanceCreate) -> TokenBalance:
        db_obj = TokenBalance(
            user_id=obj_in.user_id,
            token_id=obj_in.token_id,
            balance=obj_in.balance,
            metadata=obj_in.metadata,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_balance(
        self, db: Session, *, db_obj: TokenBalance, balance: float
    ) -> TokenBalance:
        db_obj.balance = balance
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

transaction = CRUDTransaction(Transaction)
smart_contract = CRUDSmartContract(SmartContract)
token_balance = CRUDTokenBalance(TokenBalance) 
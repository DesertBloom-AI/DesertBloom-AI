from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/transactions/", response_model=List[schemas.TokenTransaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve token transactions.
    """
    if crud.user.is_superuser(current_user):
        transactions = crud.token_transaction.get_multi(db, skip=skip, limit=limit)
    else:
        transactions = crud.token_transaction.get_multi_by_user(
            db=db, user_address=current_user.blockchain_address, skip=skip, limit=limit
        )
    return transactions

@router.post("/transactions/", response_model=schemas.TokenTransaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.TokenTransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new token transaction.
    """
    if not current_user.blockchain_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no blockchain address",
        )
    if transaction_in.from_address != current_user.blockchain_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction must be initiated from user's address",
        )
    transaction = crud.token_transaction.create(db=db, obj_in=transaction_in)
    return transaction

@router.get("/contracts/", response_model=List[schemas.SmartContract])
def read_contracts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve smart contracts.
    """
    contracts = crud.smart_contract.get_multi(db, skip=skip, limit=limit)
    return contracts

@router.post("/contracts/", response_model=schemas.SmartContract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: schemas.SmartContractCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new smart contract.
    """
    contract = crud.smart_contract.create(db=db, obj_in=contract_in)
    return contract

@router.get("/contracts/{contract_id}", response_model=schemas.SmartContract)
def read_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get smart contract by ID.
    """
    contract = crud.smart_contract.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Smart contract not found",
        )
    return contract

@router.post("/contracts/{contract_id}/interactions/", response_model=schemas.ContractInteraction)
def create_contract_interaction(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    interaction_in: schemas.ContractInteractionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new contract interaction.
    """
    contract = crud.smart_contract.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Smart contract not found",
        )
    if not current_user.blockchain_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no blockchain address",
        )
    interaction = crud.contract_interaction.create_with_contract(
        db=db, obj_in=interaction_in, contract_id=contract_id
    )
    return interaction

@router.get("/contracts/{contract_id}/interactions/", response_model=List[schemas.ContractInteraction])
def read_contract_interactions(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all interactions for a smart contract.
    """
    contract = crud.smart_contract.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Smart contract not found",
        )
    interactions = crud.contract_interaction.get_multi_by_contract(
        db=db, contract_id=contract_id, skip=skip, limit=limit
    )
    return interactions 
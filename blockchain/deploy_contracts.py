from web3 import Web3
from pathlib import Path
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
RPC_URL = os.getenv('RPC_URL')

def load_contract_abi(contract_name):
    """Load contract ABI from JSON file"""
    contract_path = Path(f'blockchain/contracts/{contract_name}.json')
    with open(contract_path) as f:
        return json.load(f)['abi']

def load_contract_bytecode(contract_name):
    """Load contract bytecode from JSON file"""
    contract_path = Path(f'blockchain/contracts/{contract_name}.json')
    with open(contract_path) as f:
        return json.load(f)['bytecode']

def deploy_contract(w3, contract_name, *args):
    """Deploy a contract to the blockchain"""
    # Load contract data
    abi = load_contract_abi(contract_name)
    bytecode = load_contract_bytecode(contract_name)
    
    # Create contract
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build transaction
    transaction = contract.constructor(*args).build_transaction({
        'from': w3.eth.accounts[0],
        'nonce': w3.eth.get_transaction_count(w3.eth.accounts[0]),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt.contractAddress

def main():
    # Connect to blockchain
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    # Deploy token contract
    print("Deploying DesertBloomToken contract...")
    token_address = deploy_contract(w3, 'DesertBloomToken')
    print(f"Token contract deployed at: {token_address}")
    
    # Deploy rewards contract
    print("Deploying DesertBloomRewards contract...")
    rewards_address = deploy_contract(w3, 'DesertBloomRewards', token_address)
    print(f"Rewards contract deployed at: {rewards_address}")
    
    # Save contract addresses
    with open('blockchain/contract_addresses.json', 'w') as f:
        json.dump({
            'token_address': token_address,
            'rewards_address': rewards_address
        }, f, indent=2)
    
    print("Contract deployment complete!")

if __name__ == "__main__":
    main() 
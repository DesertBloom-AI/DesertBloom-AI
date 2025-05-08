from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_contracts():
    # Connect to Ethereum node
    w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL')))
    
    # Load account
    private_key = os.getenv('PRIVATE_KEY')
    account = w3.eth.account.from_key(private_key)
    w3.eth.default_account = account.address
    
    # Load contract ABIs
    with open('blockchain/contracts/DesertBloomToken.json', 'r') as f:
        token_json = json.load(f)
        token_abi = token_json['abi']
        token_bytecode = token_json['bytecode']
    
    with open('blockchain/contracts/DesertBloomRewards.json', 'r') as f:
        rewards_json = json.load(f)
        rewards_abi = rewards_json['abi']
        rewards_bytecode = rewards_json['bytecode']
    
    # Deploy Token Contract
    print("Deploying DesertBloomToken contract...")
    token_contract = w3.eth.contract(abi=token_abi, bytecode=token_bytecode)
    token_tx = token_contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_token_tx = w3.eth.account.sign_transaction(token_tx, private_key)
    token_tx_hash = w3.eth.send_raw_transaction(signed_token_tx.rawTransaction)
    token_receipt = w3.eth.wait_for_transaction_receipt(token_tx_hash)
    token_address = token_receipt['contractAddress']
    print(f"DesertBloomToken deployed at: {token_address}")
    
    # Deploy Rewards Contract
    print("Deploying DesertBloomRewards contract...")
    rewards_contract = w3.eth.contract(abi=rewards_abi, bytecode=rewards_bytecode)
    rewards_tx = rewards_contract.constructor(token_address).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_rewards_tx = w3.eth.account.sign_transaction(rewards_tx, private_key)
    rewards_tx_hash = w3.eth.send_raw_transaction(signed_rewards_tx.rawTransaction)
    rewards_receipt = w3.eth.wait_for_transaction_receipt(rewards_tx_hash)
    rewards_address = rewards_receipt['contractAddress']
    print(f"DesertBloomRewards deployed at: {rewards_address}")
    
    # Save contract addresses to environment file
    with open('.env', 'a') as f:
        f.write(f"\nTOKEN_CONTRACT_ADDRESS={token_address}")
        f.write(f"\nREWARDS_CONTRACT_ADDRESS={rewards_address}")
    
    print("\nDeployment completed successfully!")
    print(f"Token Contract: {token_address}")
    print(f"Rewards Contract: {rewards_address}")

if __name__ == "__main__":
    deploy_contracts() 
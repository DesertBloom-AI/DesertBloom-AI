from web3 import Web3
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DesertBloomRewardsInterface:
    """
    Interface for managing ecological restoration project rewards
    """
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL')))
        self.contract_address = os.getenv('REWARDS_CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        
        # Load contract ABI
        with open('blockchain/contracts/DesertBloomRewards.json', 'r') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Set default account
        self.w3.eth.default_account = self.w3.eth.account.from_key(self.private_key).address
    
    def create_project(self, project_id: str, name: str, description: str, reward_rate: int) -> Dict:
        """
        Create a new ecological restoration project
        """
        try:
            tx = self.contract.functions.createProject(
                project_id,
                name,
                description,
                reward_rate
            ).build_transaction({
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': receipt['transactionHash'].hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def contribute_to_project(self, project_id: str, contributor: str, contribution_data: Dict) -> Dict:
        """
        Record a contribution to an ecological restoration project
        """
        try:
            tx = self.contract.functions.contributeToProject(
                project_id,
                contributor,
                contribution_data
            ).build_transaction({
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': receipt['transactionHash'].hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def calculate_rewards(self, project_id: str, contributor: str) -> int:
        """
        Calculate pending rewards for a contributor in a project
        """
        return self.contract.functions.calculateRewards(project_id, contributor).call()
    
    def claim_project_rewards(self, project_id: str) -> Dict:
        """
        Claim rewards for contributions to a project
        """
        try:
            tx = self.contract.functions.claimProjectRewards(project_id).build_transaction({
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': receipt['transactionHash'].hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_project_details(self, project_id: str) -> Dict:
        """
        Get details of a specific project
        """
        return self.contract.functions.getProjectDetails(project_id).call()
    
    def get_contributor_stats(self, project_id: str, contributor: str) -> Dict:
        """
        Get statistics for a contributor in a project
        """
        return self.contract.functions.getContributorStats(project_id, contributor).call()
    
    def update_project_status(self, project_id: str, status: str) -> Dict:
        """
        Update the status of a project
        """
        try:
            tx = self.contract.functions.updateProjectStatus(project_id, status).build_transaction({
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': receipt['transactionHash'].hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 
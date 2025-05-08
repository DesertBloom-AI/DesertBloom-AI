from typing import Dict, List, Optional
from datetime import datetime
from web3 import Web3
from eth_account import Account
import json

class BlockchainService:
    def __init__(self):
        # Initialize Web3 connection (example using Ganache)
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        self.account = Account.from_key('your_private_key_here')
        
        # Load contract ABIs
        with open('blockchain/contracts/DesertBloomToken.json') as f:
            self.token_abi = json.load(f)['abi']
        with open('blockchain/contracts/DesertBloomRewards.json') as f:
            self.rewards_abi = json.load(f)['abi']
        
        # Contract addresses
        self.token_address = '0xYourTokenContractAddress'
        self.rewards_address = '0xYourRewardsContractAddress'
        
        # Initialize contracts
        self.token_contract = self.w3.eth.contract(
            address=self.token_address,
            abi=self.token_abi
        )
        self.rewards_contract = self.w3.eth.contract(
            address=self.rewards_address,
            abi=self.rewards_abi
        )

    def calculate_rewards(self, project_id: int, metrics: Dict) -> Dict:
        """Calculate token rewards based on project metrics"""
        return {
            "carbon_sequestration_reward": metrics["carbon_sequestration"] * 10,  # 10 tokens per ton
            "biodiversity_reward": metrics["biodiversity_index"] * 1000,  # 1000 tokens per 0.1 index
            "water_efficiency_reward": metrics["water_efficiency"] * 500,  # 500 tokens per 0.1 efficiency
            "total_reward": 0  # Will be calculated
        }

    def distribute_rewards(self, project_id: int, rewards: Dict) -> str:
        """Distribute rewards to project contributors"""
        try:
            # Build transaction
            transaction = self.rewards_contract.functions.distributeRewards(
                project_id,
                int(rewards["total_reward"] * 1e18)  # Convert to wei
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                self.account.key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            raise Exception(f"Failed to distribute rewards: {str(e)}")

    def verify_project_achievement(self, project_id: int, achievement_data: Dict) -> bool:
        """Verify project achievement for token rewards"""
        try:
            # Verify achievement on blockchain
            result = self.rewards_contract.functions.verifyAchievement(
                project_id,
                achievement_data["metric"],
                int(achievement_data["value"] * 1e18)
            ).call()
            
            return result
        except Exception as e:
            raise Exception(f"Failed to verify achievement: {str(e)}")

    def get_token_balance(self, address: str) -> float:
        """Get token balance for an address"""
        try:
            balance = self.token_contract.functions.balanceOf(address).call()
            return balance / 1e18  # Convert from wei
        except Exception as e:
            raise Exception(f"Failed to get token balance: {str(e)}")

    def get_reward_history(self, project_id: int) -> List[Dict]:
        """Get reward distribution history for a project"""
        try:
            events = self.rewards_contract.events.RewardDistributed.get_logs(
                fromBlock=0,
                argument_filters={'projectId': project_id}
            )
            
            return [{
                'timestamp': datetime.fromtimestamp(event['args']['timestamp']),
                'amount': event['args']['amount'] / 1e18,
                'metric': event['args']['metric']
            } for event in events]
        except Exception as e:
            raise Exception(f"Failed to get reward history: {str(e)}")

    def create_project_on_chain(self, project_data: Dict) -> str:
        """Create a new project on the blockchain"""
        try:
            transaction = self.rewards_contract.functions.createProject(
                project_data["name"],
                project_data["location"],
                int(project_data["area"] * 1e18),
                int(project_data["target_carbon"] * 1e18)
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                self.account.key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return self.w3.to_hex(tx_hash)
        except Exception as e:
            raise Exception(f"Failed to create project on chain: {str(e)}") 
from web3 import Web3
from typing import Dict, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DesertBloomTokenInterface:
    """
    Interface for interacting with the DesertBloom token smart contract
    """
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL')))
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        
        # Load contract ABI
        with open('blockchain/contracts/DesertBloomToken.json', 'r') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Set default account
        self.w3.eth.default_account = self.w3.eth.account.from_key(self.private_key).address
    
    def get_balance(self, address: str) -> int:
        """
        Get token balance for an address
        """
        return self.contract.functions.balanceOf(address).call()
    
    def stake_tokens(self, amount: int) -> Dict:
        """
        Stake tokens in the contract
        """
        try:
            # Build transaction
            tx = self.contract.functions.stake(amount).build_transaction({
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
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
    
    def unstake_tokens(self, amount: int) -> Dict:
        """
        Unstake tokens from the contract
        """
        try:
            tx = self.contract.functions.unstake(amount).build_transaction({
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
    
    def claim_rewards(self) -> Dict:
        """
        Claim staking rewards
        """
        try:
            tx = self.contract.functions.claimRewards().build_transaction({
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
    
    def get_pending_rewards(self, address: str) -> int:
        """
        Get pending rewards for an address
        """
        return self.contract.functions.getPendingRewards(address).call()
    
    def get_staked_amount(self, address: str) -> int:
        """
        Get staked amount for an address
        """
        return self.contract.functions.stakedAmount(address).call()
    
    def transfer_tokens(self, to_address: str, amount: int) -> Dict:
        """
        Transfer tokens to another address
        """
        try:
            tx = self.contract.functions.transfer(to_address, amount).build_transaction({
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
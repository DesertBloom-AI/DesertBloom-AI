from web3 import Web3
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ProjectStatusInterface:
    """
    Interface for managing ecological restoration project status
    """
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL')))
        self.contract_address = os.getenv('PROJECT_STATUS_CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        
        # Load contract ABI
        with open('blockchain/contracts/ProjectStatus.json', 'r') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Set default account
        self.w3.eth.default_account = self.w3.eth.account.from_key(self.private_key).address
    
    def create_project_status(
        self,
        project_id: str,
        status: str,
        progress: int,
        metrics: Dict
    ) -> Dict:
        """
        Create or update project status
        """
        try:
            tx = self.contract.functions.createProjectStatus(
                project_id,
                status,
                progress,
                json.dumps(metrics)
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
    
    def update_project_progress(
        self,
        project_id: str,
        progress: int,
        metrics: Dict
    ) -> Dict:
        """
        Update project progress and metrics
        """
        try:
            tx = self.contract.functions.updateProjectProgress(
                project_id,
                progress,
                json.dumps(metrics)
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
    
    def get_project_status(self, project_id: str) -> Dict:
        """
        Get current project status
        """
        return self.contract.functions.getProjectStatus(project_id).call()
    
    def get_project_history(self, project_id: str) -> List[Dict]:
        """
        Get project status history
        """
        return self.contract.functions.getProjectHistory(project_id).call()
    
    def add_project_milestone(
        self,
        project_id: str,
        milestone_name: str,
        description: str,
        target_date: int
    ) -> Dict:
        """
        Add a new project milestone
        """
        try:
            tx = self.contract.functions.addProjectMilestone(
                project_id,
                milestone_name,
                description,
                target_date
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
    
    def update_milestone_status(
        self,
        project_id: str,
        milestone_name: str,
        status: str,
        completion_date: Optional[int] = None
    ) -> Dict:
        """
        Update milestone status
        """
        try:
            tx = self.contract.functions.updateMilestoneStatus(
                project_id,
                milestone_name,
                status,
                completion_date or int(datetime.now().timestamp())
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
    
    def get_project_milestones(self, project_id: str) -> List[Dict]:
        """
        Get all project milestones
        """
        return self.contract.functions.getProjectMilestones(project_id).call()
    
    def add_project_alert(
        self,
        project_id: str,
        alert_type: str,
        message: str,
        severity: str
    ) -> Dict:
        """
        Add a new project alert
        """
        try:
            tx = self.contract.functions.addProjectAlert(
                project_id,
                alert_type,
                message,
                severity
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
    
    def get_project_alerts(self, project_id: str) -> List[Dict]:
        """
        Get all project alerts
        """
        return self.contract.functions.getProjectAlerts(project_id).call() 
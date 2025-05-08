from typing import Dict, List
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ProjectConfig:
    """
    Configuration settings for the DesertBloom project
    """
    def __init__(self):
        self.config_file = 'blockchain/config/project_settings.json'
        self.load_config()
    
    def load_config(self):
        """
        Load project configuration from JSON file
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """
        Save project configuration to JSON file
        """
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get_default_config(self) -> Dict:
        """
        Get default project configuration
        """
        return {
            "project_settings": {
                "name": "DesertBloom AI",
                "version": "1.0.0",
                "description": "Autonomous Desert Ecological Restoration and Afforestation System",
                "network": os.getenv('ETH_NETWORK', 'mainnet'),
                "gas_limit": 2000000,
                "gas_price_multiplier": 1.1
            },
            "token_settings": {
                "name": "DesertBloom Token",
                "symbol": "DBT",
                "decimals": 18,
                "total_supply": 1000000000 * 10**18,  # 1 billion tokens
                "distribution": {
                    "ecosystem_rewards": 70,  # 70%
                    "ecosystem_growth": 20,   # 20%
                    "public_goods": 10        # 10%
                }
            },
            "contribution_types": {
                "planting": {
                    "base_amount": 100 * 10**18,  # 100 tokens
                    "multiplier": 1,
                    "bonus": 0
                },
                "maintenance": {
                    "base_amount": 50 * 10**18,   # 50 tokens
                    "multiplier": 1,
                    "bonus": 0
                },
                "monitoring": {
                    "base_amount": 30 * 10**18,   # 30 tokens
                    "multiplier": 1,
                    "bonus": 0
                },
                "research": {
                    "base_amount": 200 * 10**18,  # 200 tokens
                    "multiplier": 1,
                    "bonus": 0
                }
            },
            "project_statuses": {
                "active": "Project is currently active and accepting contributions",
                "paused": "Project is temporarily paused",
                "completed": "Project has been completed",
                "cancelled": "Project has been cancelled"
            },
            "milestone_statuses": {
                "pending": "Milestone is pending",
                "in_progress": "Milestone is in progress",
                "completed": "Milestone has been completed",
                "delayed": "Milestone has been delayed"
            },
            "alert_severities": {
                "low": "Low priority alert",
                "medium": "Medium priority alert",
                "high": "High priority alert",
                "critical": "Critical alert requiring immediate attention"
            },
            "alert_types": {
                "environmental": "Environmental conditions alert",
                "technical": "Technical system alert",
                "maintenance": "Maintenance required alert",
                "safety": "Safety concern alert"
            },
            "network_settings": {
                "mainnet": {
                    "rpc_url": os.getenv('ETH_NODE_URL', ''),
                    "chain_id": 1,
                    "explorer_url": "https://etherscan.io"
                },
                "testnet": {
                    "rpc_url": os.getenv('ETH_TESTNET_NODE_URL', ''),
                    "chain_id": 5,
                    "explorer_url": "https://goerli.etherscan.io"
                }
            },
            "contract_addresses": {
                "token": os.getenv('TOKEN_CONTRACT_ADDRESS', ''),
                "rewards": os.getenv('REWARDS_CONTRACT_ADDRESS', ''),
                "project_status": os.getenv('PROJECT_STATUS_CONTRACT_ADDRESS', '')
            }
        }
    
    def get_project_settings(self) -> Dict:
        """
        Get project settings
        """
        return self.config["project_settings"]
    
    def get_token_settings(self) -> Dict:
        """
        Get token settings
        """
        return self.config["token_settings"]
    
    def get_contribution_types(self) -> Dict:
        """
        Get contribution type settings
        """
        return self.config["contribution_types"]
    
    def get_project_statuses(self) -> Dict:
        """
        Get project status definitions
        """
        return self.config["project_statuses"]
    
    def get_milestone_statuses(self) -> Dict:
        """
        Get milestone status definitions
        """
        return self.config["milestone_statuses"]
    
    def get_alert_severities(self) -> Dict:
        """
        Get alert severity definitions
        """
        return self.config["alert_severities"]
    
    def get_alert_types(self) -> Dict:
        """
        Get alert type definitions
        """
        return self.config["alert_types"]
    
    def get_network_settings(self) -> Dict:
        """
        Get network settings
        """
        return self.config["network_settings"]
    
    def get_contract_addresses(self) -> Dict:
        """
        Get contract addresses
        """
        return self.config["contract_addresses"]
    
    def update_contract_address(self, contract_type: str, address: str):
        """
        Update contract address
        """
        self.config["contract_addresses"][contract_type] = address
        self.save_config()
    
    def update_network_settings(self, network: str, settings: Dict):
        """
        Update network settings
        """
        self.config["network_settings"][network] = settings
        self.save_config()
    
    def update_contribution_type(self, type_name: str, settings: Dict):
        """
        Update contribution type settings
        """
        self.config["contribution_types"][type_name] = settings
        self.save_config() 
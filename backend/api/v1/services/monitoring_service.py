from typing import Dict, List
from datetime import datetime, timedelta
import numpy as np

class MonitoringService:
    @staticmethod
    def get_environmental_data(location: Dict[str, float], timeframe: str = "24h") -> dict:
        """Get environmental monitoring data"""
        return {
            "temperature": {
                "current": 35.5,
                "min": 28.3,
                "max": 42.1,
                "average": 34.8
            },
            "humidity": {
                "current": 15.5,
                "min": 10.2,
                "max": 25.6,
                "average": 18.4
            },
            "soil_moisture": {
                "current": 0.15,
                "min": 0.08,
                "max": 0.22,
                "average": 0.16
            },
            "wind": {
                "speed": 12.5,
                "direction": "NE",
                "gusts": 18.7
            },
            "solar_radiation": {
                "current": 850.5,
                "daily_accumulation": 6500.0
            }
        }

    @staticmethod
    def analyze_vegetation_health(project_id: int) -> dict:
        """Analyze vegetation health status"""
        return {
            "overall_health_index": 0.85,
            "species_health": {
                "Desert Sage": {
                    "health_index": 0.88,
                    "growth_rate": 0.92,
                    "stress_indicators": "None"
                },
                "Creosote Bush": {
                    "health_index": 0.82,
                    "growth_rate": 0.78,
                    "stress_indicators": "Mild Water Stress"
                }
            },
            "recommendations": [
                "Increase irrigation for Creosote Bush sector",
                "Monitor soil salinity in northern quadrant"
            ]
        }

    @staticmethod
    def get_water_management_data(project_id: int) -> dict:
        """Get water management statistics"""
        return {
            "current_usage": 850.5,  # liters/day
            "efficiency_rating": 0.92,
            "distribution": {
                "irrigation": 720.3,
                "misting": 80.2,
                "reserve": 50.0
            },
            "savings_potential": 45.5,  # liters/day
            "recommendations": [
                "Optimize night-time irrigation schedule",
                "Adjust misting frequency based on humidity levels"
            ]
        }

    @staticmethod
    def generate_ecosystem_report(project_id: int) -> dict:
        """Generate comprehensive ecosystem report"""
        return {
            "biodiversity_metrics": {
                "shannon_index": 2.45,
                "species_richness": 12,
                "evenness": 0.82
            },
            "soil_health": {
                "organic_matter": 0.08,
                "microbial_activity": 0.65,
                "nutrient_levels": {
                    "nitrogen": 0.12,
                    "phosphorus": 0.08,
                    "potassium": 0.15
                }
            },
            "ecosystem_services": {
                "carbon_sequestration": 2.5,  # tons/hectare
                "soil_stabilization": 0.85,
                "water_retention": 0.78
            },
            "wildlife_activity": {
                "insect_diversity": "Increasing",
                "bird_visits": 25,  # per day
                "small_mammals": "Present"
            }
        }

    @staticmethod
    def get_historical_trends(
        metric: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Get historical trend data for specified metric"""
        days = (end_date - start_date).days
        timestamps = [start_date + timedelta(days=x) for x in range(days)]
        
        # Simulate data generation for demonstration
        if metric == "temperature":
            base = 35.0
            variation = 5.0
        elif metric == "soil_moisture":
            base = 0.15
            variation = 0.05
        else:
            base = 0.5
            variation = 0.2

        values = [base + variation * np.random.randn() for _ in range(days)]
        
        return [
            {
                "timestamp": ts.isoformat(),
                "value": max(0, val)
            }
            for ts, val in zip(timestamps, values)
        ] 
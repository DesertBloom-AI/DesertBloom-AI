from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

class AIService:
    def __init__(self):
        # Initialize models and scalers
        self.growth_model = RandomForestRegressor(n_estimators=100)
        self.water_model = RandomForestRegressor(n_estimators=100)
        self.scaler = StandardScaler()
        
        # Load pre-trained models if available
        try:
            self.growth_model = joblib.load('ai/models/growth_model.joblib')
            self.water_model = joblib.load('ai/models/water_model.joblib')
            self.scaler = joblib.load('ai/models/scaler.joblib')
        except:
            print("No pre-trained models found. Models will need to be trained.")

    def predict_vegetation_growth(
        self,
        species: str,
        soil_conditions: Dict,
        climate_data: Dict,
        duration_days: int
    ) -> Dict:
        """Predict vegetation growth over time"""
        # Prepare input features
        features = np.array([
            soil_conditions["ph"],
            soil_conditions["moisture_content"],
            soil_conditions["organic_matter"],
            climate_data["average_temperature"],
            climate_data["average_rainfall"],
            duration_days
        ]).reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        growth_rate = self.growth_model.predict(features_scaled)[0]
        
        return {
            "predicted_growth_rate": growth_rate,
            "confidence_interval": [growth_rate * 0.9, growth_rate * 1.1],
            "factors_importance": {
                "soil_ph": 0.25,
                "moisture": 0.30,
                "temperature": 0.20,
                "rainfall": 0.15,
                "organic_matter": 0.10
            }
        }

    def optimize_water_usage(
        self,
        project_id: int,
        current_usage: Dict,
        weather_forecast: Dict
    ) -> Dict:
        """Optimize water usage based on AI predictions"""
        # Prepare input features
        features = np.array([
            current_usage["daily_usage"],
            weather_forecast["temperature"],
            weather_forecast["humidity"],
            weather_forecast["precipitation_probability"],
            current_usage["soil_moisture"]
        ]).reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        optimal_usage = self.water_model.predict(features_scaled)[0]
        
        return {
            "recommended_daily_usage": optimal_usage,
            "savings_potential": current_usage["daily_usage"] - optimal_usage,
            "optimization_factors": {
                "temperature_impact": 0.35,
                "humidity_impact": 0.25,
                "precipitation_impact": 0.20,
                "soil_condition_impact": 0.20
            }
        }

    def analyze_ecosystem_health(
        self,
        project_data: Dict,
        monitoring_data: Dict
    ) -> Dict:
        """Analyze overall ecosystem health using AI"""
        # Combine and process data
        features = {
            "vegetation_diversity": len(project_data["species_list"]),
            "soil_health_index": monitoring_data["soil_health"]["microbial_activity"],
            "water_efficiency": monitoring_data["water_management"]["efficiency_rating"],
            "carbon_sequestration": project_data["carbon_metrics"]["annual_sequestration"],
            "biodiversity_index": monitoring_data["biodiversity_metrics"]["shannon_index"]
        }
        
        # Calculate health score (example implementation)
        weights = {
            "vegetation_diversity": 0.25,
            "soil_health_index": 0.20,
            "water_efficiency": 0.20,
            "carbon_sequestration": 0.20,
            "biodiversity_index": 0.15
        }
        
        health_score = sum(
            value * weights[key]
            for key, value in features.items()
        )
        
        return {
            "overall_health_score": health_score,
            "component_scores": features,
            "recommendations": self._generate_recommendations(features)
        }

    def predict_climate_impact(
        self,
        project_data: Dict,
        climate_scenario: str = "moderate"
    ) -> Dict:
        """Predict climate change impact on the project"""
        # Climate scenario parameters
        scenarios = {
            "moderate": {
                "temperature_increase": 1.5,
                "precipitation_change": -0.1,
                "extreme_events": 1.2
            },
            "severe": {
                "temperature_increase": 2.5,
                "precipitation_change": -0.2,
                "extreme_events": 1.5
            }
        }
        
        scenario = scenarios[climate_scenario]
        
        # Calculate impacts
        impacts = {
            "water_requirements": project_data["water_requirements"] * (1 + scenario["temperature_increase"] * 0.1),
            "species_survival": max(0, 1 - scenario["temperature_increase"] * 0.15),
            "maintenance_costs": project_data["maintenance_costs"] * (1 + scenario["extreme_events"] * 0.2),
            "carbon_sequestration": project_data["carbon_sequestration"] * (1 - scenario["precipitation_change"])
        }
        
        return {
            "scenario": climate_scenario,
            "timeframe": "2050",
            "impacts": impacts,
            "adaptation_measures": self._generate_adaptation_measures(impacts)
        }

    def _generate_recommendations(self, features: Dict) -> List[str]:
        """Generate recommendations based on ecosystem health analysis"""
        recommendations = []
        
        if features["vegetation_diversity"] < 5:
            recommendations.append("Increase plant species diversity")
        if features["soil_health_index"] < 0.6:
            recommendations.append("Implement soil enrichment program")
        if features["water_efficiency"] < 0.8:
            recommendations.append("Optimize irrigation system")
        
        return recommendations

    def _generate_adaptation_measures(self, impacts: Dict) -> List[str]:
        """Generate adaptation measures based on climate impact predictions"""
        measures = []
        
        if impacts["water_requirements"] > 1.2:
            measures.append("Implement advanced water conservation systems")
        if impacts["species_survival"] < 0.8:
            measures.append("Introduce more drought-resistant species")
        if impacts["maintenance_costs"] > 1.3:
            measures.append("Develop automated maintenance systems")
        
        return measures 
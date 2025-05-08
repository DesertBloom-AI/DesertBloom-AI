from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class GrowthPrediction(BaseModel):
    predicted_growth_rate: float = Field(..., ge=0, le=1)
    confidence_interval: List[float]
    factors_importance: Dict[str, float]

class WaterOptimization(BaseModel):
    recommended_daily_usage: float
    savings_potential: float
    optimization_factors: Dict[str, float]

class EcosystemHealth(BaseModel):
    overall_health_score: float = Field(..., ge=0, le=1)
    component_scores: Dict[str, float]
    recommendations: List[str]

class ClimateImpact(BaseModel):
    scenario: str
    timeframe: str
    impacts: Dict[str, float]
    adaptation_measures: List[str]

class SoilAnalysis(BaseModel):
    ph: float = Field(..., ge=0, le=14)
    moisture_content: float = Field(..., ge=0, le=1)
    organic_matter: float = Field(..., ge=0, le=1)
    nutrient_levels: Dict[str, float]
    microbial_activity: float = Field(..., ge=0, le=1)

class SpeciesAnalysis(BaseModel):
    species_name: str
    growth_rate: float = Field(..., ge=0, le=1)
    survival_probability: float = Field(..., ge=0, le=1)
    water_requirements: float
    climate_tolerance: Dict[str, float]

class BiodiversityAnalysis(BaseModel):
    shannon_index: float
    species_richness: int
    evenness: float = Field(..., ge=0, le=1)
    dominant_species: List[str]
    threatened_species: List[str]

class CarbonAnalysis(BaseModel):
    sequestration_rate: float
    storage_capacity: float
    emission_reduction: float
    carbon_credits: float

class WaterAnalysis(BaseModel):
    current_usage: float
    optimal_usage: float
    efficiency_score: float = Field(..., ge=0, le=1)
    conservation_potential: float
    quality_metrics: Dict[str, float]

class AIRecommendation(BaseModel):
    category: str
    priority: str
    description: str
    implementation_cost: float
    expected_benefit: float
    timeframe: str

class AIConfig(BaseModel):
    model_version: str
    training_data_size: int
    last_training_date: datetime
    accuracy_metrics: Dict[str, float]
    feature_importance: Dict[str, float] 
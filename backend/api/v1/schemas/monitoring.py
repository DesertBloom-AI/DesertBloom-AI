from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class EnvironmentalMetric(BaseModel):
    current: float
    min: float
    max: float
    average: float

class WindData(BaseModel):
    speed: float
    direction: str
    gusts: float

class SolarData(BaseModel):
    current: float
    daily_accumulation: float

class EnvironmentalData(BaseModel):
    temperature: EnvironmentalMetric
    humidity: EnvironmentalMetric
    soil_moisture: EnvironmentalMetric
    wind: WindData
    solar_radiation: SolarData

class SpeciesHealth(BaseModel):
    health_index: float = Field(..., ge=0, le=1)
    growth_rate: float = Field(..., ge=0, le=1)
    stress_indicators: str

class VegetationHealth(BaseModel):
    overall_health_index: float = Field(..., ge=0, le=1)
    species_health: Dict[str, SpeciesHealth]
    recommendations: List[str]

class WaterDistribution(BaseModel):
    irrigation: float
    misting: float
    reserve: float

class WaterManagement(BaseModel):
    current_usage: float
    efficiency_rating: float = Field(..., ge=0, le=1)
    distribution: WaterDistribution
    savings_potential: float
    recommendations: List[str]

class BiodiversityMetrics(BaseModel):
    shannon_index: float
    species_richness: int
    evenness: float = Field(..., ge=0, le=1)

class SoilNutrients(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float

class SoilHealth(BaseModel):
    organic_matter: float
    microbial_activity: float = Field(..., ge=0, le=1)
    nutrient_levels: SoilNutrients

class EcosystemServices(BaseModel):
    carbon_sequestration: float
    soil_stabilization: float = Field(..., ge=0, le=1)
    water_retention: float = Field(..., ge=0, le=1)

class WildlifeActivity(BaseModel):
    insect_diversity: str
    bird_visits: int
    small_mammals: str

class EcosystemReport(BaseModel):
    biodiversity_metrics: BiodiversityMetrics
    soil_health: SoilHealth
    ecosystem_services: EcosystemServices
    wildlife_activity: WildlifeActivity

class HistoricalDataPoint(BaseModel):
    timestamp: datetime
    value: float

class HistoricalTrend(BaseModel):
    metric: str
    data: List[HistoricalDataPoint]
    unit: str 
"""
Script that use the config.yaml to download and extract the information from  online zip-file
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Dataclass that receives variables with paths
    """
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    """
    Entity for data validation
    """
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict
    
@dataclass(frozen=True)
class DataCleaningConfig:
    """
    Entity for data cleaning
    """
    root_dir: Path
    data_path: Path
    
@dataclass(frozen=True)
class DataPreparationConfig:
    """
    Entitty for data preparation
    """
    root_dir: Path
    data_path: Path
    save_path: Path
    
@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Entity for training the model
    """
    root_dir: Path
    data_path: Path
    save_path: Path
    model_name: Path
    n_steps: int
    split_ratio: float
    seed: int
    drop_out_rate: float
    input_size: int
    hidden_size: int
    num_stacked_layers: int
    learning_rate: float
    num_epochs: int
    batch_size: int

@dataclass(frozen=True)
class ModelEvaluationConfig:
    """
    Entity for Model Evaluation
    """
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metric_file_name: str
    mlflow_url: str
    batch_size: int
    num_epochs: int
    all_params: Path
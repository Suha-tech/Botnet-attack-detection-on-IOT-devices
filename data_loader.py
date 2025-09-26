import pandas as pd
import numpy as np
import os
from glob import glob
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, List
import logging
from pathlib import Path

class IoTDataLoader:
    def __init__(self, data_dir: str = 'data'):
        """Initialize the data loader
        
        Args:
            data_dir: Directory containing the N-BaIoT dataset
        """
        self.data_dir = Path(data_dir)
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.logger = logging.getLogger(__name__)
        
    def load_device_data(self, device_name: str) -> pd.DataFrame:
        """Load data for a specific device
        
        Args:
            device_name: Name of the IoT device
            
        Returns:
            DataFrame containing combined normal and attack data
        """
        device_path = self.data_dir / device_name
        
        try:
            # Load benign traffic
            benign_file = device_path / 'benign_traffic.csv'
            if not benign_file.exists():
                self.logger.warning(f"Benign traffic file not found for {device_name}")
                return self._generate_fallback_data(device_name)
                
            benign_data = pd.read_csv(benign_file)
            benign_data['label'] = 0  # Normal traffic
            
            # Load Mirai attack traffic
            mirai_path = device_path / 'mirai_attacks'
            mirai_files = list(mirai_path.glob('*.csv'))
            if not mirai_files:
                self.logger.warning(f"No Mirai attack files found for {device_name}")
                mirai_data = pd.DataFrame()
            else:
                mirai_data = pd.concat([pd.read_csv(f) for f in mirai_files])
                mirai_data['label'] = 1  # Attack traffic
            
            # Load Bashlite attack traffic
            gafgyt_path = device_path / 'gafgyt_attacks'
            gafgyt_files = list(gafgyt_path.glob('*.csv'))
            if not gafgyt_files:
                self.logger.warning(f"No Gafgyt attack files found for {device_name}")
                gafgyt_data = pd.DataFrame()
            else:
                gafgyt_data = pd.concat([pd.read_csv(f) for f in gafgyt_files])
                gafgyt_data['label'] = 1  # Attack traffic
            
            # Combine all data
            dfs_to_concat = [df for df in [benign_data, mirai_data, gafgyt_data] if not df.empty]
            if not dfs_to_concat:
                self.logger.error(f"No data available for {device_name}")
                return self._generate_fallback_data(device_name)
                
            combined_data = pd.concat(dfs_to_concat)
            
            # Store feature columns if not already stored
            if self.feature_columns is None:
                self.feature_columns = [col for col in combined_data.columns if col != 'label']
            
            return combined_data
            
        except Exception as e:
            self.logger.error(f"Error loading data for {device_name}: {str(e)}")
            return self._generate_fallback_data(device_name)
    
    def _generate_fallback_data(self, device_name: str) -> pd.DataFrame:
        """Generate synthetic data when real data is not available"""
        from .data_generator import DemoDataGenerator
        generator = DemoDataGenerator()
        
        # Generate synthetic data
        benign_data = generator.generate_features(n_samples=1000, is_attack=False)
        benign_data['label'] = 0
        
        attack_data = generator.generate_features(n_samples=500, is_attack=True)
        attack_data['label'] = 1
        
        combined_data = pd.concat([benign_data, attack_data])
        
        # Store feature columns if not already stored
        if self.feature_columns is None:
            self.feature_columns = [col for col in combined_data.columns if col != 'label']
        
        return combined_data
    
    def prepare_features(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for model training/prediction
        
        Args:
            data: Raw DataFrame containing IoT traffic data
            
        Returns:
            Tuple of (X, y) arrays
        """
        X = data[self.feature_columns].values
        y = data['label'].values
        return X, y
    
    def get_feature_names(self) -> List[str]:
        """Get list of feature names"""
        return self.feature_columns
    
    def fit_scaler(self, X: np.ndarray):
        """Fit the scaler on training data"""
        self.scaler.fit(X)
    
    def transform_features(self, X: np.ndarray) -> np.ndarray:
        """Transform features using fitted scaler"""
        return self.scaler.transform(X)
    
    def get_scaler(self) -> StandardScaler:
        """Get the fitted scaler"""
        return self.scaler 
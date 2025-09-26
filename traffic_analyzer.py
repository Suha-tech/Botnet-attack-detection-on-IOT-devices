import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

class TrafficAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def analyze_traffic_patterns(self, data: pd.DataFrame) -> Dict:
        """
        Analyze traffic patterns for normal and infected behavior
        
        Args:
            data: DataFrame containing IoT device traffic data
            
        Returns:
            Dictionary containing analysis results
        """
        results = {}
        
        # Basic statistics
        results['basic_stats'] = {
            'normal': data[data['label'] == 0].describe(),
            'infected': data[data['label'] == 1].describe()
        }
        
        # Traffic volume analysis
        results['traffic_volume'] = self._analyze_traffic_volume(data)
        
        # Feature correlation analysis
        results['correlations'] = self._analyze_correlations(data)
        
        return results
    
    def _analyze_traffic_volume(self, data: pd.DataFrame) -> Dict:
        """Analyze traffic volume patterns"""
        volume_stats = {
            'normal_mean': data[data['label'] == 0]['weight'].mean(),
            'infected_mean': data[data['label'] == 1]['weight'].mean(),
            'normal_std': data[data['label'] == 0]['weight'].std(),
            'infected_std': data[data['label'] == 1]['weight'].std()
        }
        return volume_stats
    
    def _analyze_correlations(self, data: pd.DataFrame) -> Dict:
        """Analyze feature correlations for normal vs infected traffic"""
        normal_corr = data[data['label'] == 0].corr()
        infected_corr = data[data['label'] == 1].corr()
        
        return {
            'normal': normal_corr,
            'infected': infected_corr
        } 
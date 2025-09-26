import numpy as np
from sklearn.ensemble import RandomForestClassifier
import psutil
import time
from typing import Dict, Union

class LightweightIDS:
    """Lightweight Intrusion Detection System using Random Forest"""
    
    def __init__(self):
        """Initialize the IDS with a pre-trained model"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.resource_usage = []
        
        # Train with sample data
        self._train_with_sample_data()
        
    def _train_with_sample_data(self):
        """Train the model with sample normal and attack data"""
        # Generate sample training data
        n_samples = 1000
        
        # Normal traffic patterns
        normal_traffic = np.random.normal(100, 10, n_samples)
        normal_cpu = np.random.uniform(20, 50, n_samples)
        normal_memory = np.random.uniform(30, 60, n_samples)
        normal_data = np.column_stack([normal_traffic, normal_cpu, normal_memory])
        normal_labels = np.zeros(n_samples)
        
        # Attack traffic patterns
        attack_traffic = np.random.normal(500, 100, n_samples)
        attack_cpu = np.random.uniform(60, 100, n_samples)
        attack_memory = np.random.uniform(70, 100, n_samples)
        attack_data = np.column_stack([attack_traffic, attack_cpu, attack_memory])
        attack_labels = np.ones(n_samples)
        
        # Combine data
        X = np.vstack([normal_data, attack_data])
        y = np.hstack([normal_labels, attack_labels])
        
        # Train the model
        self.model.fit(X, y)
        
    def predict(self, data: np.ndarray, threshold: float = 0.5) -> float:
        """
        Predict whether the input data represents an attack
        
        Args:
            data: Array of shape (n_samples, n_features) containing the input data
            threshold: Classification threshold (default: 0.5)
            
        Returns:
            Anomaly score between 0 and 1
        """
        # Monitor resource usage
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Make prediction
        prediction_prob = self.model.predict_proba(data)[:, 1][0]
        
        # Monitor resource usage
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Log performance metrics
        resource_stats = {
            'inference_time': end_time - start_time,
            'memory_usage': end_memory - start_memory,
            'cpu_percent': psutil.cpu_percent()
        }
        self.resource_usage.append(resource_stats)
        
        return prediction_prob
        
    def get_resource_usage_stats(self) -> Dict[str, float]:
        """Get average resource usage statistics"""
        if not self.resource_usage:
            return {
                'avg_inference_time': 0.0,
                'avg_memory_usage': 0.0,
                'avg_cpu_percent': 0.0
            }
            
        avg_stats = {
            'avg_inference_time': np.mean([stats['inference_time'] for stats in self.resource_usage]),
            'avg_memory_usage': np.mean([stats['memory_usage'] for stats in self.resource_usage]),
            'avg_cpu_percent': np.mean([stats['cpu_percent'] for stats in self.resource_usage])
        }
        
        return avg_stats 
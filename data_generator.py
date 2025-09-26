import pandas as pd
import numpy as np
from pathlib import Path

class DemoDataGenerator:
    def __init__(self, data_dir='data'):
        """Initialize the demo data generator"""
        self.data_dir = Path(data_dir)
        self.devices = {
            'Security Camera': 'Provision_PT_737E',
            'Smart Doorbell': 'Danmini_Doorbell',
            'Thermostat': 'Ecobee_Thermostat',
            'Baby Monitor': 'Philips_B120N10_Baby_Monitor'
        }
        
    def generate_features(self, n_samples=1000, is_attack=False):
        """Generate synthetic network traffic features"""
        # Base parameters - adjusted for more stability in normal traffic
        base_weight = 100 if not is_attack else 800
        base_mean = 50 if not is_attack else 400
        base_std = 5 if not is_attack else 60  # Reduced variation in normal traffic
        
        # Define feature names that match the model's expectations
        feature_names = [
            'packet_size', 'packet_rate', 'bandwidth_usage', 'connection_duration',
            'cpu_usage', 'memory_usage', 'error_rate', 'retransmission_rate',
            'device_type_Security Camera', 'device_type_Smart Doorbell',
            'device_type_Thermostat', 'device_type_Baby Monitor', 'device_type_Other',
            'protocol_type_TCP', 'protocol_type_UDP', 'protocol_type_HTTP'
        ]
        
        # Generate base network metrics
        data = {
            'packet_size': np.random.normal(base_weight, base_weight/20, n_samples),
            'packet_rate': np.random.normal(base_mean, base_mean/20, n_samples),
            'bandwidth_usage': np.random.normal(base_weight*8, base_weight/10, n_samples),
            'connection_duration': np.random.normal(base_mean/2, base_mean/20, n_samples),
            'cpu_usage': np.clip(np.random.normal(base_mean/2, base_std/2, n_samples), 0, 100),
            'memory_usage': np.clip(np.random.normal(base_mean/1.5, base_std/2, n_samples), 0, 100),
            'error_rate': np.clip(np.random.normal(0.02, 0.01, n_samples), 0, 1),
            'retransmission_rate': np.clip(np.random.normal(0.01, 0.005, n_samples), 0, 1),
            'device_type_Security Camera': np.ones(n_samples),
            'device_type_Smart Doorbell': np.zeros(n_samples),
            'device_type_Thermostat': np.zeros(n_samples),
            'device_type_Baby Monitor': np.zeros(n_samples),
            'device_type_Other': np.zeros(n_samples),
            'protocol_type_TCP': np.ones(n_samples),
            'protocol_type_UDP': np.zeros(n_samples),
            'protocol_type_HTTP': np.zeros(n_samples)
        }
        
        # Add attack patterns for attack data
        if is_attack:
            # Add sudden spikes and anomalies
            attack_features = ['packet_size', 'packet_rate', 'bandwidth_usage', 'cpu_usage', 
                             'error_rate', 'retransmission_rate']
            for feature in attack_features:
                if np.random.random() < 0.4:  # 40% chance of spike in attack traffic
                    spike_idx = np.random.randint(0, n_samples, size=int(n_samples*0.2))
                    data[feature][spike_idx] *= np.random.uniform(3, 8)  # More severe spikes
            
            # Ensure values stay within bounds
            data['cpu_usage'] = np.clip(data['cpu_usage'], 0, 100)
            data['memory_usage'] = np.clip(data['memory_usage'], 0, 100)
            data['error_rate'] = np.clip(data['error_rate'], 0, 1)
            data['retransmission_rate'] = np.clip(data['retransmission_rate'], 0, 1)
        
        return pd.DataFrame(data, columns=feature_names)
    
    def generate_demo_dataset(self):
        """Generate and save demo datasets for all devices"""
        for device_type, device_name in self.devices.items():
            device_dir = self.data_dir / device_name
            device_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate benign traffic
            benign_data = self.generate_features(n_samples=5000, is_attack=False)
            benign_data['label'] = 0
            benign_data.to_csv(device_dir / 'benign_traffic.csv', index=False)
            
            # Generate Mirai attack traffic
            mirai_dir = device_dir / 'mirai_attacks'
            mirai_dir.mkdir(exist_ok=True)
            mirai_data = self.generate_features(n_samples=2000, is_attack=True)
            mirai_data['label'] = 1
            mirai_data.to_csv(mirai_dir / 'mirai_attack_1.csv', index=False)
            
            # Generate Gafgyt attack traffic
            gafgyt_dir = device_dir / 'gafgyt_attacks'
            gafgyt_dir.mkdir(exist_ok=True)
            gafgyt_data = self.generate_features(n_samples=2000, is_attack=True)
            gafgyt_data['label'] = 1
            gafgyt_data.to_csv(gafgyt_dir / 'gafgyt_attack_1.csv', index=False)
            
        print("Demo dataset generated successfully!")

if __name__ == "__main__":
    generator = DemoDataGenerator()
    generator.generate_demo_dataset() 
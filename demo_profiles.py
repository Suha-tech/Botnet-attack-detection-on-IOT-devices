from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass
class DeviceProfile:
    name: str
    type: str
    normal_traffic_pattern: np.ndarray
    attack_traffic_pattern: np.ndarray
    normal_resource_usage: Dict[str, np.ndarray]
    attack_resource_usage: Dict[str, np.ndarray]

class DemoProfiles:
    """Predefined device profiles for demonstration"""
    
    @staticmethod
    def get_security_camera_profile() -> DeviceProfile:
        return DeviceProfile(
            name="Security_Camera_01",
            type="Security Camera",
            normal_traffic_pattern=np.array([
                100, 102, 98, 103, 97, 101, 99, 102, 98, 100,
                101, 99, 102, 98, 103, 97, 101, 99, 102, 98
            ]),
            attack_traffic_pattern=np.array([
                100, 150, 200, 300, 450, 600, 800, 1000, 1200, 1500,
                1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600
            ]),
            normal_resource_usage={
                'cpu': np.array([30, 32, 31, 33, 30, 31, 32, 31, 30, 31] * 2),
                'memory': np.array([45, 46, 44, 45, 46, 45, 44, 46, 45, 44] * 2)
            },
            attack_resource_usage={
                'cpu': np.array([30, 45, 60, 75, 85, 90, 95, 98, 99, 100] * 2),
                'memory': np.array([45, 50, 60, 70, 80, 85, 90, 95, 98, 100] * 2)
            }
        )
    
    @staticmethod
    def get_smart_doorbell_profile() -> DeviceProfile:
        return DeviceProfile(
            name="Smart_Doorbell_01",
            type="Smart Doorbell",
            normal_traffic_pattern=np.array([
                50, 52, 48, 53, 47, 51, 49, 52, 48, 50,
                51, 49, 52, 48, 53, 47, 51, 49, 52, 48
            ]),
            attack_traffic_pattern=np.array([
                50, 75, 100, 150, 225, 300, 400, 500, 600, 750,
                900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800
            ]),
            normal_resource_usage={
                'cpu': np.array([20, 22, 21, 23, 20, 21, 22, 21, 20, 21] * 2),
                'memory': np.array([35, 36, 34, 35, 36, 35, 34, 36, 35, 34] * 2)
            },
            attack_resource_usage={
                'cpu': np.array([20, 35, 50, 65, 75, 80, 85, 88, 89, 90] * 2),
                'memory': np.array([35, 40, 50, 60, 70, 75, 80, 85, 88, 90] * 2)
            }
        )
    
    @staticmethod
    def get_thermostat_profile() -> DeviceProfile:
        return DeviceProfile(
            name="Smart_Thermostat_01",
            type="Thermostat",
            normal_traffic_pattern=np.array([
                30, 32, 28, 33, 27, 31, 29, 32, 28, 30,
                31, 29, 32, 28, 33, 27, 31, 29, 32, 28
            ]),
            attack_traffic_pattern=np.array([
                30, 45, 60, 90, 135, 180, 240, 300, 360, 450,
                540, 600, 660, 720, 780, 840, 900, 960, 1020, 1080
            ]),
            normal_resource_usage={
                'cpu': np.array([15, 17, 16, 18, 15, 16, 17, 16, 15, 16] * 2),
                'memory': np.array([25, 26, 24, 25, 26, 25, 24, 26, 25, 24] * 2)
            },
            attack_resource_usage={
                'cpu': np.array([15, 25, 35, 45, 55, 60, 65, 70, 75, 80] * 2),
                'memory': np.array([25, 30, 40, 50, 60, 65, 70, 75, 80, 85] * 2)
            }
        )
    
    @classmethod
    def get_all_profiles(cls) -> List[DeviceProfile]:
        return [
            cls.get_security_camera_profile(),
            cls.get_smart_doorbell_profile(),
            cls.get_thermostat_profile()
        ] 
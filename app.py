import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import json
import os

from scripts.traffic_analyzer import TrafficAnalyzer
from scripts.lightweight_ids import LightweightIDS
from scripts.model_evaluation import ModelEvaluator

class IoTBotnetDetectionApp:
    def __init__(self):
        self.initialize_session_state()
        self.analyzer = TrafficAnalyzer()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'devices' not in st.session_state:
            st.session_state.devices = {}
        if 'monitoring_data' not in st.session_state:
            st.session_state.monitoring_data = {}
            
    def main(self):
        """Main application interface"""
        st.title("IoT Botnet Attack Detection System")
        
        # Sidebar for navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Device Management", "Real-time Monitoring", "Analysis Dashboard"]
        )
        
        if page == "Device Management":
            self.device_management_page()
        elif page == "Real-time Monitoring":
            self.monitoring_page()
        else:
            self.analysis_dashboard()
            
    def device_management_page(self):
        """Device management interface"""
        st.header("Device Management")
        
        # Add new device
        with st.form("add_device"):
            st.subheader("Add New Device")
            device_name = st.text_input("Device Name")
            device_type = st.selectbox(
                "Device Type",
                ["Security Camera", "Smart Doorbell", "Thermostat", "Baby Monitor", "Other"]
            )
            device_ip = st.text_input("Device IP Address")
            
            if st.form_submit_button("Add Device"):
                if device_name and device_ip:
                    self.add_device(device_name, device_type, device_ip)
                    st.success(f"Device {device_name} added successfully!")
                else:
                    st.error("Please fill in all required fields")
        
        # List existing devices
        st.subheader("Registered Devices")
        if st.session_state.devices:
            for name, info in st.session_state.devices.items():
                with st.expander(f"Device: {name}"):
                    st.write(f"Type: {info['type']}")
                    st.write(f"IP Address: {info['ip']}")
                    st.write(f"Status: {info['status']}")
                    if st.button(f"Remove {name}", key=f"remove_{name}"):
                        self.remove_device(name)
                        st.rerun()
        else:
            st.info("No devices registered yet")
            
    def monitoring_page(self):
        """Real-time monitoring interface"""
        st.header("Real-time Device Monitoring")
        
        if not st.session_state.devices:
            st.warning("No devices registered. Please add devices first.")
            return
            
        # Device selection
        selected_device = st.selectbox(
            "Select Device to Monitor",
            list(st.session_state.devices.keys())
        )
        
        if selected_device:
            # Simulate real-time monitoring
            if st.button("Start Monitoring"):
                with st.spinner("Monitoring device..."):
                    self.monitor_device(selected_device)
                    
            # Display current status
            device_info = st.session_state.devices[selected_device]
            status_color = "green" if device_info['status'] == "Normal" else "red"
            st.markdown(f"### Status: <font color='{status_color}'>{device_info['status']}</font>", 
                       unsafe_allow_html=True)
            
            # Display monitoring graphs
            if selected_device in st.session_state.monitoring_data:
                self.display_monitoring_graphs(selected_device)
                
    def analysis_dashboard(self):
        """Analysis dashboard interface"""
        st.header("Analysis Dashboard")
        
        if not st.session_state.devices:
            st.warning("No devices registered. Please add devices first.")
            return
            
        # Device selection for analysis
        selected_device = st.selectbox(
            "Select Device for Analysis",
            list(st.session_state.devices.keys())
        )
        
        if selected_device and selected_device in st.session_state.monitoring_data:
            data = st.session_state.monitoring_data[selected_device]
            
            # Traffic pattern analysis
            st.subheader("Traffic Pattern Analysis")
            fig_traffic = px.line(
                data, x='timestamp', y='traffic_volume',
                title="Traffic Volume Over Time"
            )
            st.plotly_chart(fig_traffic)
            
            # Anomaly detection results
            st.subheader("Anomaly Detection Results")
            anomaly_data = pd.DataFrame(data)
            fig_anomaly = px.scatter(
                anomaly_data,
                x='timestamp',
                y='anomaly_score',
                color='status',
                title="Anomaly Detection Results"
            )
            st.plotly_chart(fig_anomaly)
            
            # Resource usage
            st.subheader("Resource Usage")
            fig_resource = go.Figure()
            fig_resource.add_trace(go.Scatter(
                x=data['timestamp'],
                y=data['cpu_usage'],
                name="CPU Usage"
            ))
            fig_resource.add_trace(go.Scatter(
                x=data['timestamp'],
                y=data['memory_usage'],
                name="Memory Usage"
            ))
            fig_resource.update_layout(title="Resource Usage Over Time")
            st.plotly_chart(fig_resource)
            
    def add_device(self, name: str, device_type: str, ip: str):
        """Add a new device to monitoring"""
        st.session_state.devices[name] = {
            'type': device_type,
            'ip': ip,
            'status': 'Normal',
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def remove_device(self, name: str):
        """Remove a device from monitoring"""
        if name in st.session_state.devices:
            del st.session_state.devices[name]
        if name in st.session_state.monitoring_data:
            del st.session_state.monitoring_data[name]
            
    def monitor_device(self, device_name: str):
        """Simulate device monitoring and update data"""
        # Initialize monitoring data if not exists
        if device_name not in st.session_state.monitoring_data:
            st.session_state.monitoring_data[device_name] = {
                'timestamp': [],
                'traffic_volume': [],
                'anomaly_score': [],
                'status': [],
                'cpu_usage': [],
                'memory_usage': []
            }
            
        # Simulate new data point
        current_time = datetime.now()
        traffic_volume = np.random.normal(100, 20)
        anomaly_score = np.random.uniform(0, 1)
        status = "Attack Detected" if anomaly_score > 0.8 else "Normal"
        
        # Update device status
        st.session_state.devices[device_name]['status'] = status
        
        # Update monitoring data
        data = st.session_state.monitoring_data[device_name]
        data['timestamp'].append(current_time)
        data['traffic_volume'].append(traffic_volume)
        data['anomaly_score'].append(anomaly_score)
        data['status'].append(status)
        data['cpu_usage'].append(np.random.uniform(0, 100))
        data['memory_usage'].append(np.random.uniform(0, 100))
        
    def display_monitoring_graphs(self, device_name: str):
        """Display monitoring graphs for a device"""
        data = st.session_state.monitoring_data[device_name]
        
        # Traffic volume graph
        fig_traffic = px.line(
            x=data['timestamp'],
            y=data['traffic_volume'],
            title="Real-time Traffic Volume"
        )
        st.plotly_chart(fig_traffic)
        
        # Anomaly score graph
        fig_anomaly = px.scatter(
            x=data['timestamp'],
            y=data['anomaly_score'],
            color=data['status'],
            title="Anomaly Detection"
        )
        st.plotly_chart(fig_anomaly)

if __name__ == "__main__":
    app = IoTBotnetDetectionApp()
    app.main() 
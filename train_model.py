import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import os
import pickle
import joblib

def train_model(data_path='data/synthetic_iot_traffic.csv'):
    """
    Train the IoT botnet detection model
    
    Parameters:
    -----------
    data_path : str
        Path to the training data CSV file
    """
    # Load data
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Prepare features
    numeric_features = ['packet_size', 'packet_rate', 'bandwidth_usage', 
                       'connection_duration', 'cpu_usage', 'memory_usage',
                       'error_rate', 'retransmission_rate']
    
    categorical_features = ['protocol_type', 'device_type']
    
    # One-hot encode categorical features
    df_encoded = pd.get_dummies(df, columns=categorical_features)
    
    # Prepare X and y
    X = df_encoded[df_encoded.columns.difference(['timestamp', 'label', 'device', 'port_number'])]
    y = (df_encoded['label'] == 'attack').astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    print("\nModel Evaluation:")
    y_pred = model.predict(X_test_scaled)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Save model and scaler
    print("\nSaving model and scaler...")
    model_path = 'models/iot_botnet_detector.pkl'
    scaler_path = 'models/scaler.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")
    
    return model, scaler

if __name__ == "__main__":
    train_model() 
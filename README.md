# IoT Botnet Attack Detection System  

A **Streamlit-powered dashboard** for monitoring IoT devices, detecting abnormal traffic patterns, and visualizing potential botnet attacks. This system allows users to register IoT devices, monitor their behavior in real-time, and analyze anomalies with interactive charts.  

---

## 📌 Features  

### 🔧 Device Management  
- Register new IoT devices with name, type, and IP address.  
- View and remove existing devices.  

### 📡 Real-time Monitoring  
- Simulate traffic volume, CPU usage, and memory usage.  
- Display device status (✅ Normal / 🚨 Attack Detected).  
- Interactive graphs for traffic and anomaly scores.  

### 📊 Analysis Dashboard  
- Traffic pattern visualization (line charts).  
- Anomaly detection results (scatter plots).  
- CPU & memory usage trends over time.  

---

## 📂 Project Structure  

```
IoT-Botnet-Detection/
│── app.py                      # Main Streamlit app  
│── scripts/  
│   ├── traffic_analyzer.py     # Traffic analysis logic (placeholder / extendable)  
│   ├── lightweight_ids.py      # Lightweight IDS module (placeholder / extendable)  
│   ├── model_evaluation.py     # Model evaluation utilities (placeholder / extendable)  
│── requirements.txt            # Python dependencies  
│── README.md                   # Project documentation  
```

---

## ⚙️ Installation  

### 1. Create a virtual environment (recommended)  
```bash
python -m venv venv
```

Activate it:  
- **Windows**:  
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:  
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies  
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App  

Start the Streamlit app:  
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.  

---

## 📊 Example Workflow  

1. Go to **Device Management** and add an IoT device.  
2. Navigate to **Real-time Monitoring**, select the device, and click **Start Monitoring**.  
3. View traffic volume, anomaly detection, CPU, and memory usage graphs.  
4. Open the **Analysis Dashboard** for deeper insights.  

---

## 🛠️ Technologies Used  

- [Streamlit](https://streamlit.io/) → Interactive dashboard  
- [Plotly](https://plotly.com/python/) → Data visualization  
- [Pandas](https://pandas.pydata.org/) → Data handling  
- [NumPy](https://numpy.org/) → Numerical simulation  

---

## 🔮 Future Enhancements  

- Integrate real detection logic using:  
  - `TrafficAnalyzer`  
  - `LightweightIDS`  
  - `ModelEvaluator`  
- Store monitoring history in a database (SQLite/PostgreSQL).  
- Deploy on cloud (AWS / Azure / GCP).  
- Extend support to real IoT traffic datasets (CICIDS, Bot-IoT, etc.).  

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import List, Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="DRS 5G Alarm API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = "your-secret-key-here"
JWT_ALGORITHM = "HS256"

MOCK_USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'full_name': 'Administrator'},
    'operator': {'password': 'operator123', 'role': 'operator', 'full_name': 'Operator'},
    'hazemblg': {'password': 'hazem1234', 'role': 'admin', 'full_name': 'Hazem Ben Belgacem'}
}

def load_df():
    df = pd.read_excel("alarms1.xlsx", header=5, engine='openpyxl')
    if df.shape[1] > 18:
        df = df.iloc[:, :18]
    df.columns = [
        'Root_Alarm', 'Severity', 'Alarm_Name', 'First_Occurrence',
        'Last_Occurrence', 'Duplication_Count', 'Alarm_Type', 'Alarm_Group',
        'Location', 'Node', 'Managed_Object', 'Managed_Object_Instance',
        'Agent', 'Manager', 'Alarm_Sequence_Number', 'Additional_Text',
        'Acknowledgement_Status', 'Subnet'
    ]
    df['First_Occurrence'] = pd.to_datetime(df['First_Occurrence'], errors='coerce')
    df['Last_Occurrence'] = pd.to_datetime(df['Last_Occurrence'], errors='coerce')
    df['Duplication_Count'] = pd.to_numeric(df['Duplication_Count'], errors='coerce')
    df = df.dropna(how='all')
    return df

df = load_df()

@app.post("/login")
def login(username: str, password: str):
    if username in MOCK_USERS and MOCK_USERS[username]["password"] == password:
        user = MOCK_USERS[username]
        token = jwt.encode({
            'username': username,
            'role': user['role'],
            'full_name': user['full_name'],
            'exp': datetime.utcnow() + timedelta(hours=8)
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {"success": True, "token": token, "user": user}
    return {"success": False, "message": "Invalid credentials"}

@app.get("/kpis")
def get_kpis(dashboard_type: Optional[str] = None):
    filtered = df.copy()
    return {
        "total_alarms": len(filtered),
        "critical": len(filtered[filtered['Severity'] == 'Critical']),
        "major": len(filtered[filtered['Severity'] == 'Major']),
        "minor": len(filtered[filtered['Severity'] == 'Minor']),
        "warning": len(filtered[filtered['Severity'] == 'Warning']),
        "unacknowledged": len(filtered[filtered['Acknowledgement_Status'] == 'Unacknowledged']),
        "root_alarms": len(filtered[filtered['Root_Alarm'] == 'Root alarm']),
    }

@app.get("/alarms")
def get_alarms(
    dashboard_type: Optional[str] = None,
    limit: int = 50
):
    filtered = df.copy()
    if dashboard_type == "Radio":
        keywords = ['Radio', 'RAN', 'eNodeB', 'gNodeB', 'Cell', 'Antenna', 'RF']
        mask = filtered['Alarm_Name'].str.contains('|'.join(keywords), case=False, na=False)
        filtered = filtered[mask]
    elif dashboard_type == "FH":
        keywords = ['Transmission', 'FH', 'Microwave', 'Link', 'Transport']
        mask = filtered['Alarm_Name'].str.contains('|'.join(keywords), case=False, na=False)
        filtered = filtered[mask]
    elif dashboard_type == "Energy":
        keywords = ['Power', 'Battery', 'Energy', 'Voltage', 'AC', 'DC']
        mask = filtered['Alarm_Name'].str.contains('|'.join(keywords), case=False, na=False)
        filtered = filtered[mask]

    result = filtered.head(limit).copy()
    result['First_Occurrence'] = result['First_Occurrence'].astype(str)
    result['Last_Occurrence'] = result['Last_Occurrence'].astype(str)
    return result.replace({np.nan: None}).to_dict(orient='records')

@app.get("/severity-distribution")
def severity_distribution():
    return df['Severity'].value_counts().to_dict()

@app.get("/top-nodes")
def top_nodes(limit: int = 10):
    return df['Node'].value_counts().head(limit).to_dict()

@app.get("/timeline")
def timeline():
    filtered = df.dropna(subset=['First_Occurrence']).copy()
    filtered['Date'] = filtered['First_Occurrence'].dt.date.astype(str)
    return filtered.groupby('Date').size().reset_index(name='Count').to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

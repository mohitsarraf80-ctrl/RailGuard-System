from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(title="RailGuard Agents - Railway Safety Platform")

# Track Agent - Monitors track health
track_health = 100
defect_history = []

@app.get("/")
def root():
    """Main endpoint showing system status"""
    return {
        "system": "RailGuard Agents",
        "version": "1.0.0",
        "status": "operational",
        "agents": [
            {"name": "Track Monitor", "status": "active"},
            {"name": "Maintenance Planner", "status": "active"},
            {"name": "Emergency Coordinator", "status": "active"},
            {"name": "Traffic Optimizer", "status": "active"}
        ]
    }

@app.get("/health")
def system_health():
    """Overall system health check"""
    return {
        "overall_health": track_health,
        "agents_online": 4,
        "uptime_hours": 24,
        "timestamp": str(datetime.now())
    }

# AGENT 1: Track Monitoring Agent
@app.post("/track/detect")
def detect_track_defects():
    """Detects cracks, misalignments, and wear on tracks"""
    global track_health, defect_history
    
    # Simulate detection
    detection_score = random.random()
    
    if detection_score > 0.85:
        defect = {
            "type": "crack",
            "severity": "critical",
            "location": f"Section-{random.randint(1, 50)}",
            "timestamp": str(datetime.now())
        }
        defect_history.append(defect)
        track_health -= 20
        return {
            "alert": "CRITICAL",
            "defect": defect,
            "track_health": max(0, track_health),
            "action": "IMMEDIATE_INSPECTION_REQUIRED"
        }
    elif detection_score > 0.7:
        defect = {
            "type": "wear",
            "severity": "warning",
            "location": f"Section-{random.randint(1, 50)}",
            "timestamp": str(datetime.now())
        }
        defect_history.append(defect)
        track_health -= 8
        return {
            "alert": "WARNING",
            "defect": defect,
            "track_health": max(0, track_health),
            "action": "SCHEDULE_MAINTENANCE"
        }
    else:
        return {
            "alert": "NORMAL",
            "defect": None,
            "track_health": track_health,
            "action": "CONTINUE_MONITORING"
        }

@app.get("/track/history")
def get_track_defect_history():
    """Get all detected track defects"""
    return {
        "total_defects": len(defect_history),
        "defects": defect_history[-10:],  # Last 10 defects
        "current_health": track_health
    }

# AGENT 2: Predictive Maintenance Agent
@app.get("/maintenance/predict")
def predict_maintenance_needs():
    """Predicts equipment failures and schedules maintenance"""
    # Simulate predictive analysis
    failure_probability = random.random()
    
    if failure_probability > 0.8:
        return {
            "predictions": [
                {
                    "equipment": "Rail Switch A-12",
                    "failure_probability": 0.92,
                    "remaining_useful_hours": 48,
                    "priority": "CRITICAL",
                    "recommended_action": "REPLACE_WITHIN_24H"
                },
                {
                    "equipment": "Signal B-04",
                    "failure_probability": 0.75,
                    "remaining_useful_hours": 120,
                    "priority": "HIGH",
                    "recommended_action": "INSPECT_WITHIN_3_DAYS"
                }
            ],
            "maintenance_window": "Tonight 02:00-05:00"
        }
    elif failure_probability > 0.5:
        return {
            "predictions": [
                {
                    "equipment": "Track Section C-08",
                    "failure_probability": 0.65,
                    "remaining_useful_hours": 200,
                    "priority": "MEDIUM",
                    "recommended_action": "SCHEDULE_NEXT_WEEK"
                }
            ],
            "maintenance_window": "Wednesday 01:00-04:00"
        }
    else:
        return {
            "predictions": [],
            "status": "ALL_SYSTEMS_NOMINAL",
            "next_scheduled_maintenance": "7 days"
        }

@app.get("/maintenance/schedule")
def get_maintenance_schedule():
    """Get current maintenance schedule"""
    return {
        "scheduled_tasks": [
            {"id": "MT-001", "track": "Section A", "type": "Inspection", "date": "2026-06-15"},
            {"id": "MT-002", "track": "Section B", "type": "Repair", "date": "2026-06-16"},
            {"id": "MT-003", "track": "Section C", "type": "Replacement", "date": "2026-06-18"}
        ],
        "pending_emergencies": 0,
        "crew_available": 4
    }

# AGENT 3: Emergency Response Agent
@app.post("/emergency/report")
def report_emergency(incident_type: str = None, location: str = None):
    """Report and coordinate emergency response"""
    incident_id = f"INC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Simulate incident types
    if not incident_type:
        incident_type = random.choice(["derailment", "obstacle", "signal_failure", "trespassing"])
    
    severity_map = {
        "derailment": 5,
        "obstacle": 4,
        "signal_failure": 3,
        "trespassing": 2
    }
    
    severity = severity_map.get(incident_type, 3)
    
    return {
        "incident_id": incident_id,
        "type": incident_type,
        "severity": severity,
        "location": location or f"Km {random.randint(1, 500)}",
        "response_dispatched": True,
        "estimated_response_time": f"{5 if severity >= 4 else 15} minutes",
        "resources_dispatched": ["rescue_team", "medical" if severity >= 4 else "inspection_team"],
        "status": "ACTIVE"
    }

@app.get("/emergency/active")
def get_active_emergencies():
    """Get all active emergencies"""
    return {
        "active_incidents": [
            {
                "id": "INC_20260614_001",
                "type": "obstacle_on_track",
                "location": "Km 245",
                "reported_at": "10:30 AM",
                "status": "responding"
            }
        ],
        "response_teams_available": 3,
        "helpline": "911"
    }

# AGENT 4: Traffic Management Agent
@app.get("/traffic/status")
def get_traffic_status():
    """Get real-time traffic status and delays"""
    congestion_levels = ["FREE_FLOW", "MODERATE", "HEAVY", "GRIDLOCK"]
    current_congestion = random.choice(congestion_levels[:3])
    
    return {
        "active_trains": random.randint(20, 60),
        "average_speed_kmh": random.randint(40, 90),
        "congestion_level": current_congestion,
        "total_delays_minutes": random.randint(0, 45),
        "bottlenecks": [
            {"location": "Central Junction", "delay": 8, "trains_affected": 5},
            {"location": "North Corridor", "delay": 5, "trains_affected": 3}
        ],
        "recommended_actions": "Reduce speed in Central Junction" if current_congestion == "HEAVY" else "Normal operations"
    }

@app.post("/traffic/optimize")
def optimize_traffic_flow():
    """Optimize train schedules to reduce delays"""
    return {
        "optimization_applied": True,
        "delays_reduced_by_minutes": random.randint(5, 20),
        "rescheduled_trains": random.randint(2, 8),
        "new_estimated_arrivals": "Updated in system",
        "status": "OPTIMIZATION_COMPLETE"
    }

@app.get("/traffic/schedule")
def get_train_schedule():
    """Get current train schedule"""
    return {
        "trains": [
            {"id": "EXP-101", "route": "A→B", "status": "ON_TIME", "delay": 0},
            {"id": "LOC-205", "route": "C→D", "status": "DELAYED", "delay": 12},
            {"id": "EXP-108", "route": "E→F", "status": "ON_TIME", "delay": 0},
            {"id": "FRE-503", "route": "G→H", "status": "RUNNING", "delay": 5}
        ],
        "total_active": 4,
        "on_time_performance": "85%"
    }

# Dashboard Summary
@app.get("/dashboard")
def get_dashboard_summary():
    """Complete dashboard view with all agents' status"""
    return {
        "summary": {
            "track_health": track_health,
            "active_emergencies": 1,
            "active_trains": random.randint(20, 60),
            "avg_delay": random.randint(0, 15),
            "maintenance_tasks_pending": 3
        },
        "alerts": [
            "⚠️ Track Section A-12 shows wear - Schedule inspection",
            "✅ All systems operational"
        ] if track_health > 70 else [
            "🚨 CRITICAL: Track degradation detected",
            "⚠️ Emergency response dispatched"
        ],
        "last_updated": str(datetime.now())
    }

if __name__ == "__main__":
    import uvicorn
    print("🚂 RailGuard Agents Starting...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("📍 Health Check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
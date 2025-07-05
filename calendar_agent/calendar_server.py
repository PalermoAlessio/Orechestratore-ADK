#!/usr/bin/env python3
"""
Calendar Agent A2A Server - Implementazione Manuale FastAPI
"""

from fastapi import FastAPI
import uvicorn
import json

# AgentCard manuale (seguendo spec A2A)
AGENT_CARD = {
    "name": "CalendarAgent",
    "description": "Agente specializzato nella gestione calendario",
    "url": "http://localhost:8001",
    "skills": [
        {
            "id": "check_events",
            "name": "Controlla eventi",
            "description": "Controlla eventi calendario per data specificata"
        }
    ],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    },
    "defaultInputModes": ["text"],
    "defaultOutputModes": ["text"]
}

app = FastAPI(title="Calendar Agent A2A")

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """Endpoint AgentCard standard A2A"""
    return AGENT_CARD

@app.post("/tasks/send")
async def handle_task(task_data: dict):
    """Endpoint task A2A"""
    print(f"📅 Calendar Agent ricevuto task: {task_data}")

    # Logic basic per test
    message = task_data.get("message", "").lower()
    if "domani" in message or "tomorrow" in message:
        response = "Domani hai: 10:00 Riunione team, 14:00 Call cliente"
    else:
        response = "Nessun evento trovato per la data richiesta"

    return {
        "id": "task-123",
        "status": "completed",
        "artifacts": [
            {
                "type": "text",
                "content": response
            }
        ]
    }

if __name__ == "__main__":
    print("📅 Calendar Agent A2A Server avviato su http://localhost:8001")
    uvicorn.run(app, host="localhost", port=8001)

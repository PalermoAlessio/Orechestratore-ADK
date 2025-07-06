#!/usr/bin/env python3
"""
Calendar Agent A2A Server - Con Agent Funzionante Integrato
"""

import asyncio
import os
import uuid
import uvicorn
from fastapi import FastAPI
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types
from dotenv import load_dotenv
import datetime

load_dotenv()

# Agent Card A2A
AGENT_CARD = {
    "name": "CalendarAgent",
    "description": "Calendar Agent autonomo con Google Calendar MCP",
    "url": "http://localhost:8001",
    "skills": [
        {
            "id": "calendar_management",
            "name": "Gestione calendario completa",
            "description": "Accesso real-time Google Calendar"
        }
    ],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "ai_powered": True
    }
}

app = FastAPI(title="Calendar Agent A2A Server")

# Variabili globali
calendar_agent = None
calendar_runner = None
session_service = None

def create_working_calendar_agent():
    """Crea Calendar Agent che FUNZIONA (testato)"""

    # Trova credentials
    cred_paths = ["gcp-oauth.keys.json", "../gcp-oauth.keys.json", "calendar_agent/gcp-oauth.keys.json"]
    credentials_path = None

    for path in cred_paths:
        if os.path.exists(path):
            credentials_path = os.path.abspath(path)
            break

    if not credentials_path:
        raise ValueError("Credentials non trovate")

    print(f"✅ Credentials: {credentials_path}")

    # MCP toolset (configurazione testata e funzionante)
    calendar_mcp = MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=["@cocal/google-calendar-mcp"],
            env={
                "GOOGLE_OAUTH_CREDENTIALS": credentials_path,
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8"
            },
            encoding="utf-8"
        )
    )

    # Agent con prompt autonomo (testato e funzionante)
    agent = LlmAgent(
        name="CalendarAgentA2A",
        model="gemini-2.0-flash",
        instruction="""
        Sei un Calendar Agent autonomo per Foreman A2A.

        COMPORTAMENTO:
        - Decisioni autonome, nessuna domanda all'utente
        - Usa SEMPRE gli strumenti MCP per operazioni calendario
        - Per "impegni oggi/domani" controlla automaticamente tutti i calendari

        STRUMENTI:
        - list-calendars: lista calendari
        - list-events: eventi per date
        - create-event: crea eventi
        - search-events: cerca eventi

        RISPOSTE:
        - Dirette e complete
        - Include calendario di origine
        - Orari precisi
        - Italiano
        """,
        tools=[calendar_mcp]
    )

    print("🤖 Calendar Agent A2A creato (versione testata)")
    return agent

async def initialize_calendar_system():
    """Inizializza sistema Calendar Agent"""
    global calendar_agent, calendar_runner, session_service

    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ GOOGLE_API_KEY mancante")
        return False

    try:
        calendar_agent = create_working_calendar_agent()
        session_service = InMemorySessionService()
        calendar_runner = Runner(
            agent=calendar_agent,
            app_name="CalendarAgentA2A",
            session_service=session_service
        )

        print("✅ Calendar Agent A2A inizializzato!")
        return True

    except Exception as e:
        print(f"❌ Errore inizializzazione: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Startup FastAPI"""
    print("🚀 Calendar Agent A2A Server startup...")
    await initialize_calendar_system()

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """AgentCard A2A"""
    return AGENT_CARD

@app.post("/tasks/send")
async def handle_a2a_task(task_data: dict):
    """A2A Task Handler con Calendar Agent funzionante"""

    print(f"📅 A2A Task ricevuto: {task_data}")

    if not calendar_agent or not calendar_runner:
        return {
            "id": f"task-error-{datetime.datetime.now().timestamp()}",
            "status": "error",
            "artifacts": [{"type": "text", "content": "❌ Calendar Agent non inizializzato"}]
        }

    try:
        message = task_data.get("message", "")
        if not message:
            raise ValueError("Messaggio vuoto")

        # Crea sessione unica
        user_id = "foreman_client"
        session_id = str(uuid.uuid4())

        await session_service.create_session(
            app_name="CalendarAgentA2A",
            user_id=user_id,
            session_id=session_id
        )

        # Prepara contenuto
        content = types.Content(
            role='user',
            parts=[types.Part(text=message)]
        )

        print(f"🤖 Calendar Agent processando: '{message}'")

        # Timeout aumentato per MCP
        response_text = await asyncio.wait_for(
            _process_calendar_request(content, user_id, session_id),
            timeout=30.0
        )

        print(f"✅ Risposta A2A: {response_text[:100]}...")

        return {
            "id": f"task-{datetime.datetime.now().timestamp()}",
            "status": "completed",
            "artifacts": [
                {
                    "type": "text",
                    "content": response_text
                }
            ]
        }

    except asyncio.TimeoutError:
        return {
            "id": f"task-timeout-{datetime.datetime.now().timestamp()}",
            "status": "timeout",
            "artifacts": [{"type": "text", "content": "⏰ Timeout Calendar Agent (30s)"}]
        }

    except Exception as e:
        error_msg = f"❌ Errore Calendar Agent: {str(e)}"
        print(error_msg)

        return {
            "id": f"task-error-{datetime.datetime.now().timestamp()}",
            "status": "error",
            "artifacts": [{"type": "text", "content": error_msg}]
        }

async def _process_calendar_request(content, user_id, session_id):
    """Processa richiesta con Calendar Agent funzionante"""
    try:
        response_text = ""

        async for event in calendar_runner.run_async(
            new_message=content,
            user_id=user_id,
            session_id=session_id
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
                break

        return response_text if response_text else "❌ Nessuna risposta dall'agent"

    except Exception as e:
        return f"❌ Errore processing: {str(e)}"

@app.get("/health")
async def health_check():
    """Health check"""
    agent_status = "✅ Ready" if calendar_agent else "❌ Not initialized"
    runner_status = "✅ Ready" if calendar_runner else "❌ Not initialized"

    return {
        "status": "healthy",
        "calendar_agent": agent_status,
        "calendar_runner": runner_status,
        "version": "A2A_WORKING_VERSION",
        "timestamp": datetime.datetime.now().isoformat()
    }

def main():
    """Entry point Calendar Agent A2A Server"""
    print("🎯 Calendar Agent A2A Server - Versione Funzionante")
    print("📅 Integrazione: Calendar Agent testato + A2A Protocol")
    print("🔗 URL: http://localhost:8001")

    uvicorn.run(app, host="localhost", port=8001)

if __name__ == "__main__":
    main()

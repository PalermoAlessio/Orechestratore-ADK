#!/usr/bin/env python3
"""
Calendar Agent - Vero LlmAgent ADK + A2A Server + MCP Google Calendar
Versione STABILE con timeout anti-blocco
"""

import asyncio
import os
import uuid
import uvicorn
from fastapi import FastAPI, HTTPException
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types
from dotenv import load_dotenv
import datetime

# Carica environment
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# AGENT CARD A2A
# ═══════════════════════════════════════════════════════════════

AGENT_CARD = {
    "name": "CalendarAgent",
    "description": "Agente AI specializzato Google Calendar con timeout anti-blocco",
    "url": "http://localhost:8001",
    "skills": [
        {
            "id": "calendar_management",
            "name": "Gestione calendario veloce",
            "description": "Gestisce eventi calendario con timeout 10s garantito"
        }
    ],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "ai_powered": True,
        "timeout_protected": True
    },
    "defaultInputModes": ["text"],
    "defaultOutputModes": ["text"]
}

# ═══════════════════════════════════════════════════════════════
# CALENDAR AGENT (LlmAgent ADK + MCP Tool) - VERSIONE STABILE
# ═══════════════════════════════════════════════════════════════

def create_calendar_agent():
    """
    Crea il Calendar Agent con timeout protection
    """

    # Trova credentials
    credentials_paths = [
        "gcp-oauth.keys.json",
        "../gcp-oauth.keys.json",
        "calendar_agent/gcp-oauth.keys.json",
        os.path.expanduser("~/gcp-oauth.keys.json"),
        "credentials.json",
        "../credentials.json"
    ]

    credentials_path = None
    for path in credentials_paths:
        if os.path.exists(path):
            credentials_path = os.path.abspath(path)
            break

    if not credentials_path:
        print("❌ ERRORE: File credentials non trovato!")
        return None

    print(f"✅ Credentials trovate: {credentials_path}")

    # Configurazione MCP Google Calendar Server
    try:
        google_calendar_mcp = MCPToolset(
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
        print("✅ MCP Toolset creato")

    except Exception as e:
        print(f"❌ Errore MCP setup: {e}")
        return None

    # Calendar Agent con prompt ottimizzato
    calendar_agent = LlmAgent(
        name="CalendarAgent",
        model="gemini-2.0-flash",
        instruction="""
        You are a Calendar Agent with access to Google Calendar via MCP tools.

        IMPORTANT: When you use MCP tools, you get REAL results. Use those results in your response.

        AVAILABLE TOOLS:
        - list-events: Gets real events from a calendar
        - list-calendars: Gets real list of available calendars
        - search-events: Searches for specific events

        EXAMPLES OF CORRECT BEHAVIOR:

        User: "che impegni ho domani?"
        1. Call list-events for primary calendar for tomorrow (2025-07-07)
        2. If tool returns "no events found" → Say "Non ci sono eventi domani nel calendario principale"
        3. If tool returns events → List the actual events with times and details

        User: "che calendari ho?"
        1. Call list-calendars
        2. Show the EXACT calendar list returned by the tool

        User: "controlla calendario X"
        1. Use the calendar name/ID from list-calendars results
        2. Call list-events for that specific calendar
        3. Report the actual results

        CRITICAL: Always use the ACTUAL results from MCP tools in your responses.
        Don't make up information. If tools return data, use that data exactly.

        Respond in Italian. Be specific about which calendar you checked and what you found.
        """,
        description="Calendar Agent con MCP tools integration",
        tools=[google_calendar_mcp]
    )

    print("🤖 Calendar Agent creato!")
    print(f"🔧 Tool: Google Calendar MCP Server")
    print(f"🧠 Modello: gemini-2.0-flash (compatibile ADK)")
    print(f"📁 Credentials: {credentials_path}")

    return calendar_agent

# ═══════════════════════════════════════════════════════════════
# A2A SERVER (FastAPI per comunicazione con Foreman)
# ═══════════════════════════════════════════════════════════════

app = FastAPI(title="Calendar Agent A2A Server - Timeout Protected")

# Variabili globali per Agent e Runner
calendar_agent = None
calendar_runner = None
session_service = None
app_name = "CalendarAgent_A2A_Stable"

async def initialize_calendar_agent():
    """Inizializza Calendar Agent ADK"""
    global calendar_agent, calendar_runner, session_service

    try:
        # Verifica API key Gemini
        if not os.getenv('GOOGLE_API_KEY'):
            print("❌ ERRORE: GOOGLE_API_KEY non trovata nel file .env")
            return False

        # Crea agent
        calendar_agent = create_calendar_agent()
        if not calendar_agent:
            return False

        # Setup runner e sessione
        session_service = InMemorySessionService()
        calendar_runner = Runner(
            agent=calendar_agent,
            app_name=app_name,
            session_service=session_service
        )

        print("✅ Calendar Agent ADK inizializzato!")
        return True

    except Exception as e:
        print(f"❌ Errore inizializzazione Calendar Agent: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Evento di startup FastAPI"""
    print("🚀 Calendar Agent A2A Server startup...")
    success = await initialize_calendar_agent()
    if not success:
        print("❌ Calendar Agent non inizializzato correttamente!")
    else:
        print("✅ Calendar Agent A2A Server pronto!")

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """AgentCard A2A endpoint"""
    return AGENT_CARD

async def _process_calendar_request(content, user_id, session_id):
    """Process calendar request con timeout interno"""
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
        return f"❌ Errore interno: {str(e)}"

@app.post("/tasks/send")
async def handle_a2a_task(task_data: dict):
    """A2A Task endpoint con TIMEOUT PROTECTION"""
    print(f"📅 Calendar Agent ricevuto A2A task: {task_data}")

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

        # Crea sessione unica per questa richiesta A2A
        user_id = "foreman_client"
        session_id = str(uuid.uuid4())

        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        # Prepara contenuto per Calendar Agent
        content = types.Content(
            role='user',
            parts=[types.Part(text=message)]
        )

        # Chiama Calendar Agent con TIMEOUT AGGRESSIVO
        print(f"🤖 Calendar Agent processando: '{message}'")

        try:
            # TIMEOUT AGGRESSIVO per evitare blocchi
            timeout_task = asyncio.wait_for(
                _process_calendar_request(content, user_id, session_id),
                timeout=10.0  # 10 secondi MAX
            )

            response_text = await timeout_task

        except asyncio.TimeoutError:
            response_text = "⏰ TIMEOUT: Calendar Agent ha impiegato troppo tempo (>10s). Prova richiesta più semplice."
            print("⚠️ Calendar Agent timeout after 10s")
        except Exception as e:
            response_text = f"❌ Errore during processing: {str(e)}"

        if not response_text:
            response_text = "❌ Nessuna risposta dal Calendar Agent"

        print(f"✅ Calendar Agent risposta: {response_text[:100]}...")

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

    except Exception as e:
        error_msg = f"❌ Errore Calendar Agent: {str(e)}"
        print(error_msg)

        return {
            "id": f"task-error-{datetime.datetime.now().timestamp()}",
            "status": "error",
            "artifacts": [{"type": "text", "content": error_msg}]
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    agent_status = "✅ Ready" if calendar_agent else "❌ Not initialized"
    runner_status = "✅ Ready" if calendar_runner else "❌ Not initialized"

    return {
        "status": "healthy",
        "calendar_agent": agent_status,
        "calendar_runner": runner_status,
        "mcp_tools": len(calendar_agent.tools) if calendar_agent else 0,
        "version": "TIMEOUT_PROTECTED - 10s max per request",
        "timestamp": datetime.datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    """Entry point Calendar Agent A2A Server - TIMEOUT PROTECTED"""
    print("🎯 Calendar Agent A2A Server - Timeout Protection Attivo")
    print("=" * 60)

    # Verifica setup
    print("🔧 Verifica setup...")

    # Verifica API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ GOOGLE_API_KEY mancante nel file .env")
        return

    # Verifica Node.js per MCP server
    import subprocess
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js non trovato (necessario per MCP server)")
            return
    except FileNotFoundError:
        print("❌ Node.js non installato (necessario per MCP server)")
        return

    # Verifica credentials Google Calendar
    credentials_found = any(os.path.exists(p) for p in [
        "gcp-oauth.keys.json", "../gcp-oauth.keys.json",
        "credentials.json", "../credentials.json"
    ])

    if credentials_found:
        print("✅ Google Calendar credentials trovate")
    else:
        print("❌ Google Calendar credentials mancanti")
        return

    print("✅ Setup verificato!")
    print("\n🚀 Architettura A2A:")
    print("   Foreman (orchestratore)")
    print("   ↓ HTTP A2A")
    print("   Calendar Agent (LlmAgent + FastAPI) ← Tu sei qui")
    print("   ↓ MCP stdio")
    print("   Google Calendar MCP Server (Node.js)")

    print(f"\n📡 Avviando Calendar Agent con TIMEOUT PROTECTION su http://localhost:8001")
    print("🔗 Endpoints:")
    print("   GET  /.well-known/agent.json")
    print("   POST /tasks/send")
    print("   GET  /health")
    print("⏰ TIMEOUT: 10 secondi massimo per richiesta")

    # Avvia server FastAPI
    uvicorn.run(app, host="localhost", port=8001)

if __name__ == "__main__":
    main()

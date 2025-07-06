#!/usr/bin/env python3
"""
Calendar Agent DEBUG - Test standalone per diagnosticare problemi MCP
"""

import asyncio
import os
import uuid
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

async def test_calendar_agent_standalone():
    """Test Calendar Agent in modalità standalone per debug"""

    print("🔍 CALENDAR AGENT DEBUG TEST")
    print("=" * 50)

    # ═══════════════════════════════════════════════════════════════
    # STEP 1: Verifica environment
    # ═══════════════════════════════════════════════════════════════

    print("\n1. 🔧 Verifica Environment:")

    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ GOOGLE_API_KEY mancante")
        return
    print("✅ GOOGLE_API_KEY presente")

    # Trova credentials Google Calendar
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
        print("❌ Google Calendar credentials non trovate")
        print("💡 Posiziona gcp-oauth.keys.json in:")
        for path in credentials_paths[:3]:
            print(f"   - {path}")
        return

    print(f"✅ Credentials trovate: {credentials_path}")

    # ═══════════════════════════════════════════════════════════════
    # STEP 2: Test MCP Server Connection
    # ═══════════════════════════════════════════════════════════════

    print("\n2. 📡 Test MCP Server Connection:")

    try:
        # Configurazione MCP con debugging
        google_calendar_mcp = MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=["@cocal/google-calendar-mcp"],
                env={
                    "GOOGLE_OAUTH_CREDENTIALS": credentials_path,
                    "LANG": "C.UTF-8",
                    "LC_ALL": "C.UTF-8",
                    "DEBUG": "1"  # Enable debug mode
                },
                encoding="utf-8"
            )
        )
        print("✅ MCP toolset creato")

        # ═══════════════════════════════════════════════════════════════
        # STEP 3: Crea Calendar Agent semplificato
        # ═══════════════════════════════════════════════════════════════

        print("\n3. 🤖 Crea Calendar Agent:")

        calendar_agent = LlmAgent(
            name="CalendarAgentDebug",
            model="gemini-2.0-flash",
            instruction="""
            Sei un Calendar Agent di test.

            Quando ricevi una richiesta:
            1. Usa SEMPRE gli MCP tools per accedere al calendario Google
            2. Mostra TUTTI i dettagli che trovi
            3. Se ci sono errori, spiegali in dettaglio
            4. Non inventare mai dati - usa solo quello che trovi realmente

            Rispondi in italiano e sii molto dettagliato negli errori.
            """,
            description="Calendar Agent per debug MCP connection",
            tools=[google_calendar_mcp]
        )
        print("✅ Calendar Agent creato")

        # ═══════════════════════════════════════════════════════════════
        # STEP 4: Setup Runner e test
        # ═══════════════════════════════════════════════════════════════

        print("\n4. 🏃 Setup Runner:")

        session_service = InMemorySessionService()
        app_name = "CalendarAgentDebug"
        runner = Runner(
            agent=calendar_agent,
            app_name=app_name,
            session_service=session_service
        )

        user_id = "debug_user"
        session_id = str(uuid.uuid4())

        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        print("✅ Runner configurato")

        # ═══════════════════════════════════════════════════════════════
        # STEP 5: Test query calendario
        # ═══════════════════════════════════════════════════════════════

        print("\n5. 📅 Test Query Calendario:")
        print("Invio richiesta: 'Che impegni ho questa settimana?'")

        content = types.Content(
            role='user',
            parts=[types.Part(text="Che impegni ho questa settimana? Mostrami tutti i dettagli che trovi nel calendario Google.")]
        )

        print("\n📤 Richiesta inviata al Calendar Agent...")
        print("⏳ Attendendo risposta MCP...")

        response_text = ""
        async for event in runner.run_async(
            new_message=content,
            user_id=user_id,
            session_id=session_id
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
                break

        print("\n📥 RISPOSTA CALENDAR AGENT:")
        print("-" * 50)
        print(response_text)
        print("-" * 50)

        # ═══════════════════════════════════════════════════════════════
        # STEP 6: Analisi risultato
        # ═══════════════════════════════════════════════════════════════

        print("\n6. 📊 Analisi Risultato:")

        if "errore" in response_text.lower() or "error" in response_text.lower():
            print("❌ ERRORI RILEVATI nella risposta")
        elif "non hai impegni" in response_text.lower() or "calendario vuoto" in response_text.lower():
            print("⚠️  Calendario risulta vuoto - verifica se è corretto")
        elif len(response_text) < 50:
            print("⚠️  Risposta molto breve - possibile problema MCP")
        else:
            print("✅ Risposta dettagliata ricevuta")

        print(f"\nLunghezza risposta: {len(response_text)} caratteri")

        # Test aggiuntivo con richiesta specifica
        print("\n7. 🔍 Test aggiuntivo - Lista calendari disponibili:")

        content2 = types.Content(
            role='user',
            parts=[types.Part(text="Mostrami quali calendari hai disponibili e accesso.")]
        )

        response_text2 = ""
        async for event in runner.run_async(
            new_message=content2,
            user_id=user_id,
            session_id=session_id
        ):
            if event.is_final_response():
                response_text2 = event.content.parts[0].text
                break

        print("📥 RISPOSTA CALENDARI:")
        print("-" * 30)
        print(response_text2)
        print("-" * 30)

    except Exception as e:
        print(f"\n❌ ERRORE DURANTE TEST: {str(e)}")
        print(f"Tipo errore: {type(e).__name__}")
        import traceback
        print("Stack trace completo:")
        traceback.print_exc()

def main():
    """Entry point test debug"""
    print("🎯 Calendar Agent Standalone Debug Test")
    asyncio.run(test_calendar_agent_standalone())

if __name__ == "__main__":
    main()

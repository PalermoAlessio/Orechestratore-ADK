import asyncio
import os
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from orchestrator import create_orchestrator

async def chat_loop():
    """Loop principale di conversazione v1.2 FIXED"""

    # Verificare API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ ERRORE: GOOGLE_API_KEY non trovata nel file .env")
        print("💡 Crea file .env con: GOOGLE_API_KEY=your_api_key_here")
        return

    print("🚀 Inizializzazione Foreman v1.2 FIXED con architettura separata...")

    try:
        # Creare agente orchestratore v1.2 FIXED
        orchestrator = create_orchestrator()

        # Setup runner e sessione
        session_service = InMemorySessionService()
        app_name = "Foreman_v1.2_FIXED"
        runner = Runner(
            agent=orchestrator,
            app_name=app_name,
            session_service=session_service
        )

        # ID utente e sessione
        user_id = "user_local"
        session_id = str(uuid.uuid4())

        # Creare sessione
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        print("✅ Foreman v1.2 FIXED pronto! Architettura multi-agent funzionante")
        print("💡 Comandi di test:")
        print("   - 'Crea un file test.txt con il contenuto Hello World'")
        print("   - 'Leggi il contenuto del file test.txt'")
        print("   - 'Lista tutti i file nella directory'")
        print("   - 'Cerca informazioni su Python online'")
        print("   - 'Cerca info su MCP e salvale in un file ricerca.txt'")
        print("=" * 60)

        while True:
            # Input utente
            user_input = input("\n🧑 Tu: ").strip()

            # Comandi uscita
            if user_input.lower() in ['quit', 'exit', 'bye', 'esci']:
                print("👋 Arrivederci!")
                break

            if not user_input:
                continue

            # Debug info per development
            if user_input.lower() == 'debug':
                print(f"🔧 Debug Info:")
                print(f"   Session ID: {session_id}")
                print(f"   User ID: {user_id}")
                print(f"   App Name: {app_name}")
                print(f"   Workspace: {os.path.expanduser('~/foreman_workspace')}")
                continue

            # Preparare messaggio per ADK
            content = types.Content(
                role='user',
                parts=[types.Part(text=user_input)]
            )

            print("🤖 Foreman v1.2 FIXED:", end=" ", flush=True)

            try:
                # Chiamare agente e mostrare risposta
                async for event in runner.run_async(
                    new_message=content,
                    user_id=user_id,
                    session_id=session_id
                ):
                    if event.is_final_response():
                        print(event.content.parts[0].text)
                        break

            except Exception as e:
                print(f"\n❌ Errore durante l'elaborazione: {str(e)}")
                print("💡 Prova con una richiesta più semplice o digita 'debug' per info.")

    except Exception as e:
        print(f"❌ Errore v1.2 FIXED: {str(e)}")
        print("🔧 Verifica:")
        print("   1. Node.js installato: node --version")
        print("   2. npm installato: npm --version")
        print("   3. MCP server: npm list -g @modelcontextprotocol/server-filesystem")
        print("   4. Directory ~/foreman_workspace/ accessibile")
        print("   5. GOOGLE_API_KEY in file .env")
        print("   6. Virtual environment python attivo")

def main():
    """Entry point applicazione v1.2 FIXED"""
    print("🎯 Foreman v1.2 FIXED - Architettura Multi-Agent")
    print("🔧 Risolve: 'Tool use with function calling is unsupported'")
    print("=" * 60)

    # Eseguire loop conversazione
    asyncio.run(chat_loop())

if __name__ == "__main__":
    main()

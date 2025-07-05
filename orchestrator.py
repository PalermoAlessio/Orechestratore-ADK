from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from a2a_calendar_tool import a2a_calendar_check

import os
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()

def create_orchestrator():
    """
    Foreman v1.3 A2A ENHANCED - MILESTONE A2A RAGGIUNTO!

    ✅ AgentTool per google_search (risolve issue #134)
    ✅ MCP con encoding robusto (risolve UTF-8 errors)
    ✅ A2A Calendar Agent integration (primo agente A2A)
    ✅ Architettura multi-agent distribuita funzionante
    """

    # ═══════════════════════════════════════════════════════════════
    # AGENTE GOOGLE SEARCH via AgentTool
    # ═══════════════════════════════════════════════════════════════
    search_agent = LlmAgent(
        name="GoogleSearchAgent",
        model="gemini-2.0-flash",
        description="Specialized agent for Google Search operations",
        instruction="""
        Sei un agente specializzato nella ricerca Google.

        Usa google_search per trovare informazioni aggiornate e accurate.
        Fornisci sempre risposte dettagliate basate sui risultati di ricerca.
        Rispondi sempre in italiano.
        """,
        tools=[google_search]
    )

    # Wrappa come AgentTool (WORKAROUND UFFICIALE)
    search_agent_tool = AgentTool(agent=search_agent)

    # ═══════════════════════════════════════════════════════════════
    # MCP FILESYSTEM con ENCODING ROBUSTO
    # ═══════════════════════════════════════════════════════════════
    work_directory = os.path.expanduser("~/foreman_workspace")
    os.makedirs(work_directory, exist_ok=True)

    # Configurazione MCP con encoding robusto (rimosso parametro non supportato)
    filesystem_mcp = MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=[
                "@modelcontextprotocol/server-filesystem",
                work_directory
                # Rimosso --encoding=utf8 (non supportato dal server)
            ],
            env={
                "LANG": "C.UTF-8",      # ← Locale più robusto
                "LC_ALL": "C.UTF-8",    # ← Evita problemi di encoding locale
                "NODE_OPTIONS": "--max-old-space-size=4096"  # ← Più memoria per Node.js
            },
            encoding="utf-8"  # ← Encoding solo lato client Python
        )
    )

    # ═══════════════════════════════════════════════════════════════
    # ORCHESTRATORE PRINCIPALE v1.3 A2A ENHANCED
    # ═══════════════════════════════════════════════════════════════
    orchestrator = LlmAgent(
        name="Foreman",
        model="gemini-2.0-flash",
        instruction=f"""
        Sei Foreman v1.3 A2A ENHANCED, il primo orchestratore multi-agent con A2A protocol!

        🚀 NUOVA CAPACITÀ A2A: Ora puoi comunicare con agenti A2A specializzati!

        STRUMENTI DISPONIBILI:
        1. GoogleSearchAgent: per ricerche web e informazioni aggiornate online
        2. MCPToolset: per operazioni su file/directory in {work_directory}
        3. 🆕 A2ACalendarTool: per comunicare con Calendar Agent via A2A protocol

        DECISION LOGIC INTELLIGENTE v1.3:

        📡 USA GoogleSearchAgent QUANDO la richiesta riguarda:
        ✓ Notizie attuali, eventi recenti
        ✓ Persone famose, personaggi pubblici (Papa, presidenti, etc.)
        ✓ Dati che cambiano nel tempo (prezzi, classifiche, risultati sportivi)
        ✓ Domande che richiedono informazioni aggiornate da internet
        ✓ Verifiche di informazioni online
        ✓ "Cerca informazioni su..."

        📁 USA MCPToolset QUANDO la richiesta riguarda:
        ✓ "Crea un file..."
        ✓ "Leggi il contenuto di..."
        ✓ "Lista i file..." / "Mostrami i file..."
        ✓ "Salva in un file..."
        ✓ "Modifica il file..."
        ✓ Qualsiasi operazione su filesystem locale

        📅 🆕 USA A2ACalendarTool QUANDO la richiesta riguarda:
        ✓ "Che impegni ho..." / "Che eventi ho..."
        ✓ "calendario" / "agenda" / "meeting" / "appuntamenti"
        ✓ "sono libero..." / "quando ho tempo..."
        ✓ "domani" / "oggi" / "questa settimana" (in contesto calendario)
        ✓ "riunioni" / "call" / "eventi"
        ✓ Qualsiasi richiesta relativa alla gestione calendario

        💬 RISPONDI DIRETTAMENTE per:
        ✓ Saluti (ciao, buongiorno, etc.)
        ✓ Ringraziamenti
        ✓ Domande sulla tua funzione
        ✓ Conversazioni casuali
        ✓ Spiegazioni concettuali di base

        🔄 WORKFLOW COMBINATI A2A - Esempi:
        ✓ "Cerca info su [argomento] e salvale in un file"
           → 1) GoogleSearchAgent → 2) MCPToolset
        ✓ "Controlla i miei impegni e cerca informazioni sui partecipanti"
           → 1) A2ACalendarTool → 2) GoogleSearchAgent
        ✓ "Salva i miei impegni di domani in un file"
           → 1) A2ACalendarTool → 2) MCPToolset

        🎯 COMPORTAMENTO A2A:
        - Quando usi A2ACalendarTool, spiega che stai comunicando con un agente specializzato
        - Se Calendar Agent non risponde, offri di usare altri strumenti
        - Celebra quando l'A2A communication funziona perfettamente!
        - Sii orgoglioso di essere il primo orchestratore A2A multi-agent

        ARCHITETTURA DISTRIBUITA:
        - Tu sei l'orchestratore principale (processo principale)
        - Calendar Agent è un processo A2A indipendente (porta 8001)
        - Comunicazione via HTTP + JSON-RPC (standard A2A)
        - Discovery automatico via AgentCard

        Workspace directory: {work_directory}
        Calendar Agent URL: http://localhost:8001
        """,
        description="Foreman v1.3 A2A ENHANCED - Multi-Agent Orchestrator with A2A Protocol",
        tools=[
            search_agent_tool,    # ← AgentTool per ricerca (workaround issue #134)
            filesystem_mcp,       # ← MCP con encoding robusto
            a2a_calendar_check    # ← 🆕 A2A Calendar function (callable ADK compatible)
        ]
    )

    print(f"🎉 Foreman v1.3 A2A ENHANCED - MILESTONE RAGGIUNTO!")
    print(f"🌐 GoogleSearch: ✅ ATTIVATO (via AgentTool workaround)")
    print(f"📁 MCP Filesystem: ✅ ATTIVATO (encoding robusto)")
    print(f"📅 A2A Calendar Agent: ✅ ATTIVATO (callable function, ADK compatible)")
    print(f"🧠 Modello: gemini-2.0-flash")
    print(f"🏗️ Architettura: Multi-Agent A2A Protocol")
    print(f"🔧 Issues risolti: #134 (function calling) + UTF-8 encoding + A2A integration")
    print(f"📁 Workspace: {work_directory}")
    print(f"📅 Calendar Agent: http://localhost:8001")
    print(f"✨ Ready for distributed multi-agent workflows!")

    return orchestrator

def get_adk_version():
    """Recupera versione ADK installata"""
    try:
        import google.adk
        return getattr(google.adk, '__version__', 'unknown')
    except:
        return 'unknown'

# ═══════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS per testing e debug A2A
# ═══════════════════════════════════════════════════════════════════════

def test_workspace_encoding():
    """Test encoding del workspace per debug"""
    workspace = os.path.expanduser("~/foreman_workspace")

    try:
        # Test creazione file con caratteri UTF-8
        test_file = os.path.join(workspace, "test_encoding.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test UTF-8: àèìòù ñ 中文 🚀\n")

        # Test lettura
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"✅ Workspace encoding test OK: {content.strip()}")
        os.remove(test_file)
        return True

    except Exception as e:
        print(f"❌ Workspace encoding test FAILED: {e}")
        return False

def test_a2a_calendar_connectivity():
    """Test connettività con Calendar Agent A2A"""
    import asyncio
    from a2a_calendar_tool import test_calendar_agent_connectivity

    return asyncio.run(test_calendar_agent_connectivity())

if __name__ == "__main__":
    # Test rapido se eseguito direttamente
    print("🧪 Testing Foreman v1.3 A2A ENHANCED components...")
    print("\n1. Workspace encoding test:")
    test_workspace_encoding()
    print("\n2. A2A Calendar Agent connectivity test:")
    test_a2a_calendar_connectivity()
    print("\n🎯 Foreman v1.3 A2A ENHANCED ready!")

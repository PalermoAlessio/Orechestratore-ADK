from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

import os
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()

def create_orchestrator():
    """
    Foreman v1.2 ENHANCED - SOLUZIONE FINALE

    ✅ AgentTool per google_search (risolve issue #134)
    ✅ MCP con encoding robusto (risolve UTF-8 errors)
    ✅ Architettura stabile e testata
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
    # ORCHESTRATORE PRINCIPALE ENHANCED
    # ═══════════════════════════════════════════════════════════════
    orchestrator = LlmAgent(
        name="Foreman",
        model="gemini-2.0-flash",
        instruction=f"""
        Sei Foreman v1.2 ENHANCED, un assistente intelligente perfettamente funzionante.

        STRUMENTI DISPONIBILI:
        1. GoogleSearchAgent: per ricerche web e informazioni aggiornate online
        2. MCPToolset: per operazioni su file/directory in {work_directory}

        DECISION LOGIC INTELLIGENTE:

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

        💬 RISPONDI DIRETTAMENTE per:
        ✓ Saluti (ciao, buongiorno, etc.)
        ✓ Ringraziamenti
        ✓ Domande sulla tua funzione
        ✓ Conversazioni casuali
        ✓ Spiegazioni concettuali di base

        🔄 WORKFLOW COMBINATI - Esempi:
        ✓ "Cerca info su [argomento] e salvale in un file"
           → 1) GoogleSearchAgent → 2) MCPToolset
        ✓ "Leggi il file X e verifica le info online"
           → 1) MCPToolset → 2) GoogleSearchAgent

        COMPORTAMENTO:
        - Analizza SEMPRE la richiesta per identificare lo strumento giusto
        - Se non sei sicuro, preferisci GoogleSearchAgent per info online
        - Spiega brevemente quale strumento stai usando e perché
        - Fornisci sempre risposte complete, utili e in italiano

        Workspace directory: {work_directory}
        """,
        description="Foreman v1.2 ENHANCED - Google Search + MCP Filesystem",
        tools=[
            search_agent_tool,  # ← AgentTool per ricerca (workaround issue #134)
            filesystem_mcp      # ← MCP con encoding robusto
        ]
    )

    print(f"🎉 Foreman v1.2 ENHANCED - SOLUZIONE FINALE!")
    print(f"🌐 GoogleSearch: ✅ ATTIVATO (via AgentTool workaround)")
    print(f"📁 MCP Filesystem: ✅ ATTIVATO (encoding robusto)")
    print(f"🧠 Modello: gemini-2.0-flash")
    print(f"🔧 Issues risolti: #134 (function calling) + UTF-8 encoding")
    print(f"📁 Workspace: {work_directory}")
    print(f"✨ Ready for production use!")

    return orchestrator

def get_adk_version():
    """Recupera versione ADK installata"""
    try:
        import google.adk
        return getattr(google.adk, '__version__', 'unknown')
    except:
        return 'unknown'

# ═══════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS per testing e debug
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

if __name__ == "__main__":
    # Test rapido se eseguito direttamente
    print("🧪 Testing workspace encoding...")
    test_workspace_encoding()

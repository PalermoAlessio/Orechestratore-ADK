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
    Foreman v2.0 Single-Agent - Architettura Semplificata

    ✅ AgentTool per google_search
    ✅ MCP Filesystem
    ✅ Architettura single-agent pulita
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

    # Wrappa come AgentTool
    search_agent_tool = AgentTool(agent=search_agent)

    # ═══════════════════════════════════════════════════════════════
    # MCP FILESYSTEM
    # ═══════════════════════════════════════════════════════════════
    work_directory = os.path.expanduser("~/foreman_workspace")
    os.makedirs(work_directory, exist_ok=True)

    filesystem_mcp = MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=[
                "@modelcontextprotocol/server-filesystem",
                work_directory
            ],
            env={
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "NODE_OPTIONS": "--max-old-space-size=4096"
            },
            encoding="utf-8"
        )
    )

    # ═══════════════════════════════════════════════════════════════
    # ORCHESTRATORE PRINCIPALE v2.0 Single-Agent
    # ═══════════════════════════════════════════════════════════════
    orchestrator = LlmAgent(
        name="Foreman",
        model="gemini-2.0-flash",
        instruction=f"""
        Sei Foreman v2.0 Single-Agent, assistente AI con due capacità principali:

        🌐 RICERCA WEB (GoogleSearchAgent):
        - Notizie, informazioni aggiornate, persone famose, etc.

        📁 FILESYSTEM (MCP):
        - Crea, leggi, modifica file nella directory ~/foreman_workspace/

        Scegli automaticamente lo strumento giusto in base alla richiesta.
        """,
        description="Foreman v2.0 Single-Agent - AI Assistant with GoogleSearch and MCP Filesystem",
        tools=[
            search_agent_tool,
            filesystem_mcp,
        ]
    )

    print(f"🎯 Foreman v2.0 Single-Agent - Architettura Semplificata")
    print(f"🌐 GoogleSearch: ✅ ATTIVATO")
    print(f"📁 MCP Filesystem: ✅ ATTIVATO")
    print(f"📁 Workspace: {work_directory}")
    print(f"✨ Ready for single-agent workflows!")

    return orchestrator

if __name__ == "__main__":
    # Test rapido se eseguito direttamente
    print("🧪 Testing Foreman v2.0 Single-Agent components...")
    # Qui potrebbero essere aggiunti test specifici per v2.0
    print("✅ Foreman v2.0 Single-Agent ready!")
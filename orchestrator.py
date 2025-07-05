from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

import os
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()





def create_orchestrator():
    """Crea l'agente orchestratore v1.2 FIXED con agenti separati"""

    
    # Configurazione workspace per MCP
    work_directory = os.path.expanduser("~/foreman_workspace")
    os.makedirs(work_directory, exist_ok=True)

    # Configurazione MCP Filesystem
    filesystem_mcp = MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=["@modelcontextprotocol/server-filesystem", work_directory],
            env={"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"},
            encoding="utf-8"
        )
    )

    orchestrator = LlmAgent(
        name="Foreman",
        model="gemini-2.5-flash",  # Modello unico per orchestrazione e tool use
        instruction=f"""
        Sei Foreman v1.2, un assistente intelligente e coordinatore di agenti specializzati.

        Hai accesso diretto al seguente strumento:
        - MCPToolset: per operazioni su file e directory locali nella directory: {work_directory}.

        Quando l'utente chiede:
        - Operazioni su file/directory: usa MCPToolset.

        Sempre:
        - Analizza la richiesta dell'utente.
        - Scegli lo strumento appropriato.
        - Esegui il compito.
        - Sintetizza la risposta finale.

        Workspace directory: {work_directory}
        Rispondi sempre in italiano.
        """,
        description="Orchestratore Foreman v1.2 con strumenti diretti",
        tools=[filesystem_mcp]
    )

    print(f"✅ Foreman v1.2 FIXED inizializzato (ADK {get_adk_version()})")
    print(f"📁 Workspace: {os.path.expanduser('~/foreman_workspace')}")
    

    return orchestrator

def get_adk_version():
    """Recupera versione ADK installata"""
    try:
        import google.adk
        return getattr(google.adk, '__version__', 'unknown')
    except:
        return 'unknown'

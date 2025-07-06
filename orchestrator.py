from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

import os
from dotenv import load_dotenv
from datetime import datetime

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
    # MCP GOOGLE CALENDAR
    # ═══════════════════════════════════════════════════════════════
    credentials_path = os.path.abspath("google-credentials.json")

    calendar_mcp = MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=["@cocal/google-calendar-mcp"],
            env={
                "GOOGLE_OAUTH_CREDENTIALS": credentials_path,
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
            },
            encoding="utf-8"
        )
    )


    # ═══════════════════════════════════════════════════════════════
    # ORCHESTRATORE PRINCIPALE v2.0 Single-Agent
    # ═══════════════════════════════════════════════════════════════

    # Iniezione del contesto temporale
    now = datetime.now().strftime("%A, %d %B %Y, %H:%M:%S")

    orchestrator = LlmAgent(
        name="Foreman",
        model="gemini-2.0-flash",
        instruction=f"""
<identity>
Sono Foreman v2.0, un assistente AI specializzato nell'orchestrazione intelligente di strumenti multipli per ottimizzare la tua produttività. Il mio ruolo è analizzare le tue richieste, selezionare automaticamente gli strumenti più appropriati e coordinarli per completare i task in modo efficiente. Mi concentro su risultati concreti e task completion, non su conversazioni generiche.
</identity>

<system_info>
📅 **Data e Ora Correnti**: {now}
Uso queste informazioni per interpretare correttamente le tue richieste temporali come "oggi", "domani", "questa settimana", ecc.
</system_info>

<available_tools>
Orchestro tre categorie di strumenti MCP per completare i tuoi task:

**🗂️ GESTIONE FILE** - Operazioni su file system locale
**🌐 RICERCA WEB** - Accesso a informazioni aggiornate online
**📅 GESTIONE CALENDARIO** - Controllo e gestione eventi Google Calendar

I server MCP forniscono le proprie descrizioni tecniche dettagliate. La mia responsabilità è selezionare e coordinare gli strumenti giusti per ogni specifica richiesta.
</available_tools>

<calendar_configuration>
Ho accesso ai tuoi calendari organizzati per categorie. Ecco come li gestisco:

**🏥 HEALTH_AND_WELLNESS**: `ecec45bc081eb53af85714d3ac609d392e175344eec3f702ef22c9d57c9ae4db@group.calendar.google.com`
- Visite mediche, dentista, controlli sanitari, sport, palestra, fisioterapia

**💼 WORK_AND_PROFESSIONAL**: `f72572c2108e8bd20c0754c6369520148284bf63d3c6807cf80dd18beb64b990@group.calendar.google.com`
- Riunioni, meeting di lavoro, conferenze, scadenze, videochiamate

**🎉 RECREATIONAL_ACTIVITIES**: `f506b0bcf9a05458893504ce3985b11423f6196686bedb8bf1c68f71fe95db5d@group.calendar.google.com`
- Feste, concerti, eventi culturali, cene sociali, hobby

**✈️ TRAVEL_AND_VACATION**: `8bcc238a98b488d8b52a2cf79da1c0a86a536ed0929ef3649131dec7d07cb4e3@group.calendar.google.com`
- Vacanze, viaggi, weekend fuori porta, festività

**📋 DEFAULT_GENERIC**: `alessiopalermo34@gmail.com`
- Eventi generici o quando la categoria non è chiara
</calendar_configuration>

<operational_procedures>
**VISUALIZZAZIONE EVENTI**
Eseguo `list-events` su tutti i calendari configurati, consolido i risultati e presento una vista unificata organizzata cronologicamente.

**CREAZIONE EVENTI**
Analizzo il contenuto dell'evento per determinare il calendario appropriato secondo la categorizzazione definita, quindi eseguo `create-event` con i parametri ottimizzati.

**WORKFLOW MULTI-TOOL**
Per task complessi, orchesto sequenze di strumenti mantenendo contesto tra le chiamate e ottimizzando per efficienza e affidabilità.
</operational_procedures>

<interaction_style>
- **Orientato ai risultati**: Sempre task completion, mai conversazioni vuote
- **Comunicazione precisa**: Descrivo azioni e risultati con chiarezza tecnica
- **Gestione autonoma**: Seleziono strumenti senza richiedere conferme inutili
- **Trasparenza operativa**: Comunico cosa sto facendo quando necessario
- **Linguaggio italiano**: Mantengo accuratezza tecnica con linguaggio accessibile
</interaction_style>

<execution_logic>
1. **Analisi della richiesta** → Identifico intent primario e requisiti secondari
2. **Selezione strumenti** → Determino tool ottimali basandomi su capabilities e context
3. **Orchestrazione** → Eseguo workflow con gestione errori e ottimizzazioni
4. **Delivery** → Fornisco output completo con validazione dei risultati
</execution_logic>
""",
        description="Foreman v2.0 Single-Agent - AI Assistant with GoogleSearch, MCP Filesystem and Google Calendar",
        tools=[
            search_agent_tool,
            filesystem_mcp,
            calendar_mcp,
        ]
    )

    print(f"🎯 Foreman v2.0 Single-Agent - Architettura Semplificata")
    print(f"🌐 GoogleSearch: ✅ ATTIVATO")
    print(f"📁 MCP Filesystem: ✅ ATTIVATO")
    print(f"📅 Google Calendar: ✅ ATTIVATO (Verifica credenziali in '{credentials_path}')")
    print(f"📁 Workspace: {work_directory}")
    print(f"✨ Ready for single-agent workflows!")

    return orchestrator

if __name__ == "__main__":
    # Test rapido se eseguito direttamente
    print("🧪 Testing Foreman v2.0 Single-Agent components...")
    # Qui potrebbero essere aggiunti test specifici per v2.0
    print("✅ Foreman v2.0 Single-Agent ready!")

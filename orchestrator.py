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
# RUOLO E OBIETTIVO
Sei Foreman v2.0, un assistente AI e orchestratore di tool avanzato. Il tuo unico scopo è analizzare la richiesta dell'utente e delegare il lavoro al toolset più appropriato.

# INFORMAZIONI DI SISTEMA
- **Data e Ora Correnti**: {now}
- Usa questa informazione per interpretare qualsiasi richiesta relativa al tempo (es. "oggi", "domani").

# ELENCO CALENDARI DI RIFERIMENTO
Questo è l'elenco completo dei calendari disponibili. Usalo per tutte le operazioni.
- **HEALTH_AND_WELLNESS**: `ecec45bc081eb53af85714d3ac609d392e175344eec3f702ef22c9d57c9ae4db@group.calendar.google.com`
  - **Keywords**: Visita medica, dentista, oculista, cardiologo, esami clinici, controlli sanitari, ospedalizzazione, fisioterapista, osteopata, massaggi, trattamenti benessere, terapie, cure mediche, check-up, screening, sport, palestra.
- **WORK_AND_PROFESSIONAL**: `f72572c2108e8bd20c0754c6369520148284bf63d3c6807cf80dd18beb64b990@group.calendar.google.com`
  - **Keywords**: Riunioni, meeting di lavoro, presentazioni aziendali, conferenze, corsi di formazione professionale, colloqui, networking, scadenze, deadline di progetto, conference call, videochiamate di lavoro.
- **RECREATIONAL_ACTIVITIES**: `f506b0bcf9a05458893504ce3985b11423f6196686bedb8bf1c68f71fe95db5d@group.calendar.google.com`
  - **Keywords**: Feste, celebrazioni, concerti, spettacoli, eventi culturali, mostre, cene sociali, aperitivi, hobby, interessi personali, mercati.
- **TRAVEL_AND_VACATION**: `8bcc238a98b488d8b52a2cf79da1c0a86a536ed0929ef3649131dec7d07cb4e3@group.calendar.google.com`
  - **Keywords**: Vacanze, viaggi di piacere, viaggi di lavoro, weekend fuori porta, festività, soggiorni, permessi retribuiti.
- **DEFAULT_GENERIC**: `alessiopalermo34@gmail.com`
  - **Uso**: Eventi non chiaramente categorizzabili nelle altre sezioni, promemoria generici, richieste ambigue per contesto ma con dati sufficienti per la creazione.


# MATRICE DI DECISIONE DEI TOOLSET
Analizza la richiesta e scegli il toolset appropriato.

### 🗂️ GESTIONE FILE (Filesystem)
- **Toolset**: `filesystem_mcp`
- **Keywords**: crea file, leggi, scrivi, salva, lista file, directory.

### 🌐 RICERCA WEB (Web Search)
- **Toolset**: `search_agent_tool`
- **Keywords**: cerca, trova informazioni, notizie, ricerca web, online.

### 📅 GESTIONE CALENDARIO (Google Calendar)
- **Toolset**: `calendar_mcp`
- **Keywords**: evento, calendario, impegni, meeting, appuntamento, riunione.

# PROCEDURE SPECIFICHE OBBLIGATORIE

### **Visualizzazione Eventi**
- **Quando**: La richiesta è di vedere, mostrare, elencare o trovare impegni/eventi.
- **Azione**: DEVI usare il tool `list-events` del `calendar_mcp` **iterando su TUTTI i calendari** definiti nell'ELENCO CALENDARI DI RIFERIMENTO. Non fermarti al primo. Consolida i risultati in un'unica risposta.

### **Creazione Eventi**
- **Quando**: La richiesta è di creare o aggiungere un evento.
- **Azione**:
    1. Analizza il titolo dell'evento (es. "Visita medica", "Riunione progetto") per determinare il calendario più appropriato dall'ELENCO CALENDARI.
    2. Usa il tool `create-event` con l'ID del calendario corretto.
    3. Se non è chiaro, usa `DEFAULT_GENERIC`.

# LOGICA DI ORCHESTRAZIONE
1.  **Analisi**: Decomponi la richiesta.
2.  **Selezione**: Scegli il toolset dalla MATRICE.
3.  **Procedura**: Se esiste una PROCEDURA SPECIFICA per il tipo di richiesta, SEGUILA ALLA LETTERA.
4.  **Task Complessi**: Se necessario, orchestra più tool in sequenza (es. cerca e poi salva).

# REGOLE DI INTERAZIONE
- Comunica solo il risultato finale.
- Non fare domande di chiarimento, ad eccezione dei conflitti di calendario gestiti dal tool.

Rispondi sempre in italiano.
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
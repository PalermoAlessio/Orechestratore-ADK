# 🤖 Orchestratore ADK "Foreman"

> **La Bibbia di Riferimento del Progetto Foreman**  
> Sistema di orchestrazione intelligente basato su Google ADK con supporto MCP

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![ADK](https://img.shields.io/badge/Google_ADK-1.0.0+-green.svg)](https://github.com/google/adk-python)
[![MCP](https://img.shields.io/badge/MCP-1.10.0+-orange.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Indice

- [🎯 Obiettivo del Progetto](#-obiettivo-del-progetto)
- [🏗️ Architettura](#️-architettura)
- [📊 Cronologia Versioni](#-cronologia-versioni)
- [🚀 Quick Start](#-quick-start)
- [📁 Struttura Progetto](#-struttura-progetto)
- [🔧 Configurazione](#-configurazione)
- [💻 Utilizzo](#-utilizzo)
- [🧪 Testing](#-testing)
- [🐛 Troubleshooting](#-troubleshooting)
- [🛣️ Roadmap](#️-roadmap)
- [🤝 Contribuire](#-contribuire)

## 🎯 Obiettivo del Progetto

**Foreman** è un assistente AI orchestratore che migra da N8N verso un'architettura distribuita usando Google ADK (Agent Development Kit) e protocollo A2A (Agent2Agent). 

### Motivazioni Migrazione
- **Controllo Programmatico**: Python invece di workflow grafici
- **Multi-LLM**: Diversi modelli per agenti diversi (Gemini + Claude + altri)
- **Modularity**: Agenti completamente indipendenti e sostituibili
- **Scalabilità**: Distribuzione agenti su macchine diverse
- **Standardizzazione**: Protocolli aperti (A2A, MCP) supportati dall'industria

### Sistema Originale N8N
```
Telegram Polling → Input Processing → Orchestratore Centrale → Sub-Workflow Tools → Response
                    (audio/testo)     (LangChain Agent)     (4 agenti come tool)
```

### Architettura Target ADK + A2A
```
Telegram (long polling Python)
    ↓
Orchestratore ADK (processo principale)
    ↓ (comunicazione via A2A protocol)
┌─ Sheets Agent (processo A2A indipendente)
├─ Calendar Agent (processo A2A indipendente)  
├─ Obsidian Agent (processo A2A indipendente)
└─ Search Agent (processo A2A indipendente)
```

## 🏗️ Architettura

### Componenti Principali

#### 🧠 Orchestratore "Foreman"
- **Engine**: Google ADK + Gemini 2.0 Flash
- **Ruolo**: Coordinatore centrale per task decomposition
- **Capacità**: Natural language understanding + tool orchestration
- **Memory**: Session state management per conversazioni multi-turno

#### 🔧 Tool Ecosystem
- **Tool Nativi ADK**: Funzionalità base integrate
- **Server MCP**: Accesso filesystem, database, API esterne
- **Tool A2A**: Comunicazione con agenti distribuiti
- **Tool Legacy**: Integrazione sistemi esistenti

#### 🌐 Connectivity Layer
- **Input**: Terminale (v1.x) → Telegram (v2.x) → API Server (v3.x)
- **Output**: Text response → Multimodal → Streaming
- **Protocols**: MCP per tool, A2A per agenti, HTTP per integrations

## 📊 Cronologia Versioni

### ✅ v1.0 - Orchestratore Base (Completato)
**Data**: Gennaio 2025  
**Obiettivo**: Proof of concept ADK funzionante

**Funzionalità**:
- [x] Input da tastiera (terminale)
- [x] Processing con Gemini 2.0 Flash
- [x] Conversazione multi-turno con memoria
- [x] Response testuale diretta

**Tecnologie**: ADK, Gemini, sessioni in-memory

### ✅ v1.1 - Tool Search Integrato (Completato)
**Data**: Gennaio 2025  
**Obiettivo**: Aggiungere capacità di ricerca web

**Funzionalità**:
- [x] Tool `google_search` integrato
- [x] Grounding con dati real-time
- [x] Combinazione knowledge base + web search
- [x] Error handling per API failures

**Tecnologie**: ADK + google_search tool

### ✅ v1.2 - Integrazione MCP Filesystem (Completato)
**Data**: Gennaio 2025  
**Obiettivo**: Primo server MCP per accesso filesystem locale

**Funzionalità**:
- [x] Server MCP Filesystem (Node.js)
- [x] MCPToolset integration con ADK
- [x] Workspace `~/foreman_workspace/`
- [x] Operazioni CRUD su file system
- [x] Combinazione MCP + tool nativi

**Tecnologie**: ADK 1.0.0+, MCP SDK 1.10.0+, Node.js filesystem server

**Limitazioni Correnti**:
- ⚠️ Ricerca online temporaneamente disabilitata
- 📝 Supporto solo filesystem locale
- 🔧 Configurazione manuale workspace

### 🚧 v1.3 - Stabilizzazione e Multi-MCP (In Pianificazione)
**Data**: Febbraio 2025  
**Obiettivo**: Risolvere ricerca online + aggiungere server MCP

**Pianificato**:
- [ ] Fix ricerca online google_search
- [ ] Database MCP server (SQLite)
- [ ] Email MCP server 
- [ ] Calendario MCP server
- [ ] Tool filtering e configurazione avanzata

### 🚧 v2.0 - Telegram Integration (In Pianificazione)
**Data**: Marzo 2025  
**Obiettivo**: Input multimodale da Telegram

**Pianificato**:
- [ ] Bot Telegram con long polling
- [ ] Audio processing (Whisper)
- [ ] ADK API Server mode
- [ ] File upload/download via Telegram

### 🚧 v3.0 - Multi-Agent A2A (In Pianificazione)
**Data**: Aprile 2025  
**Obiettivo**: Architettura distribuita completa

**Pianificato**:
- [ ] Primo agente A2A indipendente
- [ ] Protocollo Agent2Agent testing
- [ ] Migrazione agenti N8N esistenti
- [ ] Deployment distribuito

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.9+ 
- **Node.js**: 18.0.0+ (per server MCP filesystem)
- **Sistema**: macOS, Linux, o WSL (Windows non completamente supportato)

### Installazione Rapida

```bash
# 1. Clone repository
git clone https://github.com/PalermoAlessio/Orechestratore-ADK.git
cd Orechestratore-ADK

# 2. Setup Python environment
python -m venv adk_env
source adk_env/bin/activate  # Linux/macOS
# o: adk_env\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install MCP filesystem server
npm install -g @modelcontextprotocol/server-filesystem

# 5. Configure environment
cp .env.example .env
# Editare .env con la tua API key Gemini

# 6. Setup workspace
mkdir -p ~/foreman_workspace
echo "Test file for Foreman" > ~/foreman_workspace/test.txt

# 7. Run Foreman
python main.py
```

### Primo Test
```
🧑 Tu: Ciao Foreman, come stai?
🤖 Foreman v1.2: Ciao! Sto benissimo, grazie. Sono pronto ad aiutarti...

🧑 Tu: Leggi il file test.txt
🤖 Foreman v1.2: Ho letto il file test.txt. Il contenuto è: "Test file for Foreman"

🧑 Tu: Crea un file note.md con il titolo "Appunti Foreman"
🤖 Foreman v1.2: Ho creato il file note.md con il titolo richiesto...
```

## 📁 Struttura Progetto

```
Orechestratore-ADK/
├── 📄 README.md                    # Questo file - La Bibbia di Riferimento
├── 📄 LICENSE                      # Licenza MIT
├── 📄 .gitignore                   # File da ignorare
├── 📄 requirements.txt             # Dipendenze Python
├── 📄 .env.example                 # Template configurazione
├── 📄 .env                         # Configurazione (NON in git)
│
├── 📁 src/                         # Codice sorgente principale
│   ├── 📄 main.py                  # Entry point applicazione
│   ├── 📄 orchestrator.py          # Agente Foreman ADK
│   └── 📁 config/                  # Configurazioni
│       ├── 📄 __init__.py
│       └── 📄 settings.py          # Settings centralizzati
│
├── 📁 tools/                       # Tool custom e utility
│   ├── 📄 __init__.py
│   ├── 📄 search_tools.py          # Google search integration
│   └── 📄 mcp_tools.py             # MCP servers configuration
│
├── 📁 tests/                       # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 test_orchestrator.py     # Test orchestratore
│   ├── 📄 test_mcp_integration.py  # Test integrazione MCP
│   └── 📄 test_e2e.py              # Test end-to-end
│
├── 📁 docs/                        # Documentazione aggiuntiva
│   ├── 📄 CHANGELOG.md             # Storia modifiche
│   ├── 📄 TROUBLESHOOTING.md       # Risoluzione problemi
│   ├── 📄 API.md                   # Documentazione API
│   └── 📁 versions/                # Guide specifiche versioni
│       ├── 📄 v1.0-guide.md
│       ├── 📄 v1.1-guide.md
│       └── 📄 v1.2-guide.md
│
├── 📁 scripts/                     # Script utility
│   ├── 📄 setup.sh                 # Setup automatico
│   ├── 📄 test.sh                  # Run tutti i test
│   └── 📄 deploy.sh                # Deploy script
│
└── 📁 workspace/                   # Workspace temporaneo (ignorato da git)
    └── 📄 .gitkeep
```

## 🔧 Configurazione

### Environment Variables (.env)
```bash
# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=FALSE

# Foreman Configuration
FOREMAN_VERSION=1.2
FOREMAN_WORKSPACE=~/foreman_workspace
FOREMAN_LOG_LEVEL=INFO

# MCP Configuration  
MCP_FILESYSTEM_PATH=~/foreman_workspace
MCP_TIMEOUT_SECONDS=30

# Future Configuration (v2.0+)
# TELEGRAM_BOT_TOKEN=your_bot_token
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_claude_key
```

### Settings.py
```python
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class ForemanConfig:
    version: str = "1.2"
    workspace: Path = Path.home() / "foreman_workspace"
    model: str = "gemini-2.0-flash"
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # MCP Settings
    mcp_timeout: int = 30
    mcp_servers: list = None
    
    def __post_init__(self):
        if self.mcp_servers is None:
            self.mcp_servers = ["filesystem"]
        
        # Ensure workspace exists
        self.workspace.mkdir(exist_ok=True)

# Global config instance
config = ForemanConfig()
```

## 💻 Utilizzo

### Comandi Base
```python
# In main.py
python main.py                    # Avvia Foreman
python main.py --version         # Mostra versione
python main.py --config         # Mostra configurazione
python main.py --test           # Run test rapido
```

### Esempi Interazione

#### 💬 Conversazione Base
```
🧑 Tu: Ciao Foreman, presentati
🤖 Foreman: Sono Foreman v1.2, il tuo assistente AI...
```

#### 📁 Gestione File
```
🧑 Tu: Lista tutti i file nella directory di lavoro
🤖 Foreman: [usa MCP filesystem per listare ~/foreman_workspace/]

🧑 Tu: Crea un file progetti.md con la lista dei miei progetti
🤖 Foreman: [usa MCP per creare file con contenuto]

🧑 Tu: Leggi e riassumi il contenuto di progetti.md
🤖 Foreman: [usa MCP per leggere + AI per riassumere]
```

#### 🔍 Ricerca e Archiviazione (v1.3+)
```
🧑 Tu: Cerca informazioni su "Google ADK" e salvale in research.md
🤖 Foreman: [google_search + MCP filesystem per salvare]
```

#### 📊 Analisi Dati (Future)
```
🧑 Tu: Carica il CSV vendite.csv e analizza i trend
🤖 Foreman: [MCP database + AI analysis]
```

## 🧪 Testing

### Test Suite Completa
```bash
# Run tutti i test
python -m pytest tests/

# Test specifici
python -m pytest tests/test_orchestrator.py -v
python -m pytest tests/test_mcp_integration.py -v

# Test con coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Manuali
```bash
# Test orchestratore standalone
python tests/manual_test_orchestrator.py

# Test MCP connectivity
python tests/manual_test_mcp.py

# Test end-to-end completo
python tests/manual_test_e2e.py
```

### Test di Integrazione
```bash
# Test server MCP filesystem
npx @modelcontextprotocol/server-filesystem ~/foreman_workspace --test

# Test API Gemini
python tests/test_gemini_api.py

# Test workspace permissions
python tests/test_workspace_access.py
```

## 🐛 Troubleshooting

### Problemi Comuni

#### ❌ "No module named 'google.adk'"
```bash
# Soluzione: Verificare installazione ADK
pip show google-adk
pip install --upgrade google-adk>=1.0.0
```

#### ❌ "MCP filesystem server not found"
```bash
# Soluzione: Verificare Node.js e server
node --version  # Deve essere 18.0.0+
npm install -g @modelcontextprotocol/server-filesystem
```

#### ❌ "Permission denied su workspace"
```bash
# Soluzione: Fix permessi
mkdir -p ~/foreman_workspace
chmod 755 ~/foreman_workspace
```

#### ❌ "API key Gemini invalida"
```bash
# Soluzione: Verificare .env
cat .env | grep GOOGLE_API_KEY
# Ottenere key da: https://aistudio.google.com/
```

#### ⚠️ "Ricerca online non funziona"
```bash
# Problema noto v1.2: google_search temporaneamente disabilitato
# Fix pianificato in v1.3
# Workaround: Commentare google_search in orchestrator.py
```

### Log e Debugging
```bash
# Enable debug logging
export FOREMAN_LOG_LEVEL=DEBUG
python main.py

# Check MCP connection
python -c "from tools.mcp_tools import test_mcp_connection; test_mcp_connection()"

# Monitor workspace access
tail -f ~/foreman_workspace/.foreman_access.log
```

## 🛣️ Roadmap

### 🎯 Milestone Immediati

#### v1.3 - Stabilizzazione (Febbraio 2025)
**Priorità**: 🔥 Alta  
**Obiettivo**: Sistema robusto e stabile

- [ ] **Fix ricerca online**: Risolvere google_search integration
- [ ] **Multi-MCP servers**: Database SQLite + Email + Calendar
- [ ] **Error handling**: Gestione robusta fallimenti MCP
- [ ] **Configuration**: UI per gestione server MCP
- [ ] **Performance**: Ottimizzazione timeout e caching
- [ ] **Testing**: Suite completa automatizzata

#### v2.0 - Telegram Integration (Marzo 2025) 
**Priorità**: 🔥 Alta  
**Obiettivo**: Input multimodale da Telegram

- [ ] **Bot Telegram**: Long polling + message handling
- [ ] **Audio processing**: Whisper integration per voice input
- [ ] **ADK API Server**: Architettura client-server
- [ ] **File handling**: Upload/download file via Telegram
- [ ] **Multi-session**: Gestione utenti multipli
- [ ] **Security**: Autenticazione e authorization

### 🚀 Milestone Avanzati

#### v3.0 - Multi-Agent A2A (Aprile 2025)
**Priorità**: 🟡 Media  
**Obiettivo**: Architettura distribuita completa

- [ ] **A2A Protocol**: Implementazione Agent2Agent
- [ ] **Distributed Agents**: Sheets, Calendar, Obsidian agents
- [ ] **Discovery**: Agent discovery automatico
- [ ] **Load Balancing**: Distribuzione carico tra agenti
- [ ] **Monitoring**: Dashboard stato sistema distribuito

#### v4.0 - Enterprise Features (Maggio 2025)
**Priorità**: 🟢 Bassa  
**Obiettivo**: Deployment produzione

- [ ] **Cloud Deployment**: Google Cloud Run + Vertex AI
- [ ] **Authentication**: OAuth2 + JWT tokens
- [ ] **Multi-tenancy**: Isolamento utenti/organizzazioni  
- [ ] **Analytics**: Metriche uso e performance
- [ ] **API Gateway**: Rate limiting + versioning
- [ ] **Documentation**: API docs complete

### 🔬 Ricerca e Sviluppo

#### Sperimentazione Continua
- **Multi-LLM**: Claude + GPT-4 + modelli locali
- **Advanced MCP**: Server custom per domain specifici
- **UI/UX**: Web interface per configurazione
- **Mobile**: App mobile per accesso Foreman
- **Voice**: Interface vocale completa
- **Plugins**: Ecosystem plugin di terze parti

## 🤝 Contribuire

### Come Contribuire

#### 🐛 Bug Reports
1. Controllare [Issues esistenti](https://github.com/PalermoAlessio/Orechestratore-ADK/issues)
2. Creare nuovo issue con template
3. Includere logs, versioni, steps to reproduce

#### 💡 Feature Requests  
1. Discutere in [Discussions](https://github.com/PalermoAlessio/Orechestratore-ADK/discussions)
2. Creare issue con tag "enhancement"
3. Proporre implementation plan

#### 🔧 Pull Requests
1. Fork del repository
2. Creare feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Aprire Pull Request

### Development Setup
```bash
# Development installation
git clone https://github.com/PalermoAlessio/Orechestratore-ADK.git
cd Orechestratore-ADK

# Development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Run tests before PR
python -m pytest tests/ --cov=src
```

### Code Standards
- **Python**: PEP 8 + Black formatting
- **Documentation**: Docstrings per tutte le funzioni
- **Testing**: Coverage > 80%
- **Typing**: Type hints obbligatori
- **Git**: Conventional Commits

---

## 📞 Supporto e Contatti

- **Repository**: [github.com/PalermoAlessio/Orechestratore-ADK](https://github.com/PalermoAlessio/Orechestratore-ADK)
- **Issues**: [GitHub Issues](https://github.com/PalermoAlessio/Orechestratore-ADK/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PalermoAlessio/Orechestratore-ADK/discussions)
- **Documentation**: [Wiki](https://github.com/PalermoAlessio/Orechestratore-ADK/wiki)

---

**Made with ❤️ by [Alessio Palermo](https://github.com/PalermoAlessio)**

*"From N8N workflows to distributed AI agents - The evolution continues"*

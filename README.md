# 🤖 Foreman v2.0 - Personal AI Assistant

> **Versione:** 2.0 (Single-Agent Multi-Tool)
> **Obiettivo:** Un assistente personale AI modulare ed estensibile, costruito con Google ADK e un'architettura multi-server MCP.

---

## 🎯 Visione del Progetto

**Foreman v2.0** è un assistente personale AI progettato per dimostrare capacità avanzate di orchestrazione di strumenti attraverso un singolo agente intelligente. Sfruttando il framework **Google ADK** e integrando server **MCP (Model-Context-Protocol)** multipli, il sistema offre funzionalità modulari e facilmente estendibili per ottimizzare la produttività personale e professionale.

---

## 🏗️ Architettura

Il sistema si basa su un'architettura a tre livelli:

1.  **🧠 Central Intelligence (ADK Agent):**
    *   Un singolo agente **LlmAgent** di Google ADK.
    *   Utilizza il modello **Gemini 2.0 Flash**.
    *   Un sistema di **Prompt Engineering** avanzato per la selezione intelligente degli strumenti.

2.  **🔧 Tool Layer (MCP Servers):**
    *   Ogni funzionalità è fornita da un server MCP indipendente (es. Filesystem, Web Search, Obsidian, etc.).
    *   Questa modularità permette di aggiungere o rimuovere capacità senza modificare l'agente centrale.

3.  **🔌 Interface Layer:**
    *   **Fase 1:** Interfaccia a riga di comando (attuale).
    *   **Fase 2:** Bot Telegram.
    *   **Fase 3:** Interfaccia Web.

---

## 📦 Stack Tecnologico

*   **Core:** Python 3.9+, Google ADK `~1.2.1`, MCP `~1.10.0`
*   **Modello AI:** Google Gemini 2.0 Flash
*   **MCP Servers:** Node.js `~18.0.0`
*   **Gestione Dipendenze:** `pip` (Python), `npm` (Node.js)

---

## 🚀 Stato del Progetto e Piano di Sviluppo

Questo README funge da traccia vivente dello sviluppo.

### **Phase 1: Foundation (In Corso)**

#### **Settimana 1: Core Setup**
- [x] **Ambiente di Sviluppo:** Setup dell'ambiente virtuale Python e installazione ADK.
- [x] **Agente Base:** Creata la struttura iniziale del progetto con un LlmAgent e interfaccia terminale.
- [x] **Prima Integrazione MCP:** Integrato e testato con successo il server **File System MCP**.
- [ ] **Integrazione Ricerca Web:** Aggiungere la capacità di ricerca web (Brave Search MCP o Google Search ADK).

#### **Settimana 2: Multi-Tool Foundation**
- [ ] **Prompt Engineering v1:** Implementare la logica di base per la selezione degli strumenti.
- [ ] **Testing Framework:** Impostare test unitari e di integrazione.

### **Phase 2: Knowledge & Memory (Non Iniziato)**
- [ ] **Integrazione Obsidian:** Collegare l'agente a un vault Obsidian tramite MCP.
- [ ] **Gestione Memoria Avanzata:** Implementare memoria persistente tra le sessioni.

### **Phase 3: Productivity Tools (Non Iniziato)**
- [ ] **Trascrizione Audio:** Integrazione con Whisper MCP.
- [ ] **Elaborazione Documenti:** Integrazione con PDF MCP.
- [ ] **Gestione Calendario:** Integrazione con Google Calendar MCP.

### **Phase 4: Polish & Production (Non Iniziato)**
- [ ] **Ottimizzazione Performance:** Caching, pooling delle connessioni MCP.
- [ ] **Gestione Errori Avanzata:** Implementare strategie di recovery robuste.
- [ ] **Documentazione Finale e Portfolio:** Pulizia del codice, diagrammi e demo.

---

## ⚡ Quick Start

1.  **Clona il repository e accedi alla cartella:**
    ```bash
    git clone <your-repo>/foreman-v2.git
    cd foreman-v2
    ```

2.  **Imposta l'ambiente virtuale e installa le dipendenze:**
    ```bash
    python -m venv adk_env
    source adk_env/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configura le API Keys:**
    *   Copia il file `.env.example` in un nuovo file chiamato `.env`.
    *   Inserisci la tua `GOOGLE_API_KEY` nel file `.env`.

4.  **Avvia l'agente:**
    ```bash
    python main.py
    ```

5.  **Interagisci con l'agente:**
    *   `"Crea un file di prova chiamato test.txt"`
    *   `"Leggi il file test.txt"`

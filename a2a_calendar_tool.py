#!/usr/bin/env python3
"""
A2A Calendar Tool - Client per comunicare con Calendar Agent (ADK Compatible)
"""

import httpx
import asyncio
import json

# ═══════════════════════════════════════════════════════════════
# A2A CALENDAR FUNCTION (ADK CALLABLE COMPATIBLE)
# ═══════════════════════════════════════════════════════════════

async def a2a_calendar_check(query: str) -> str:
    """
    Funzione callable compatibile ADK per comunicare con Calendar Agent via A2A

    Args:
        query: Richiesta relativa al calendario (es. "che impegni ho domani?")

    Returns:
        Risposta del Calendar Agent o messaggio di errore
    """
    calendar_url = "http://localhost:8001"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # 1. Scarica AgentCard (discovery)
            try:
                card_response = await client.get(
                    f"{calendar_url}/.well-known/agent.json"
                )
                agent_card = card_response.json()
                print(f"🔍 A2A Agent discovered: {agent_card['name']}")
            except Exception as e:
                return f"❌ Calendar Agent non disponibile: impossibile scaricare AgentCard ({str(e)})"

            # 2. Invia task A2A
            task_data = {"message": query}
            task_response = await client.post(
                f"{calendar_url}/tasks/send",
                json=task_data,
                headers={"Content-Type": "application/json"}
            )

            if task_response.status_code != 200:
                return f"❌ Errore Calendar Agent: HTTP {task_response.status_code}"

            result = task_response.json()

            # 3. Estrai contenuto dalla risposta A2A
            if "artifacts" in result and len(result["artifacts"]) > 0:
                content = result["artifacts"][0]["content"]
                print(f"✅ A2A Task completed: {result['id']}")
                return content
            else:
                return "❌ Nessuna risposta dal Calendar Agent"

    except asyncio.TimeoutError:
        return "❌ Calendar Agent timeout (5s) - verificare che sia in esecuzione su porta 8001"
    except Exception as e:
        return f"❌ Errore comunicazione A2A: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# LEGACY CLASS (per backward compatibility e testing)
# ═══════════════════════════════════════════════════════════════

class A2ACalendarTool:
    """Legacy class wrapper - mantenuta per compatibility"""

    def __init__(self):
        self.calendar_url = "http://localhost:8001"
        self.name = "a2a_calendar_tool"
        self.description = "Tool per comunicare con Calendar Agent via A2A protocol"

    async def check_calendar(self, query: str) -> str:
        """Legacy method - usa la funzione callable"""
        return await a2a_calendar_check(query)

# ═══════════════════════════════════════════════════════════════
# TEST FUNCTIONS
# ═══════════════════════════════════════════════════════════════

async def test_a2a_callable():
    """Test della funzione callable direttamente"""
    print("🧪 Testing A2A Calendar Callable Function...")
    result = await a2a_calendar_check("che impegni ho domani?")
    print(f"📅 Risultato A2A Callable: {result}")
    return result

async def test_a2a_legacy():
    """Test della classe legacy"""
    print("🧪 Testing A2A Calendar Legacy Class...")
    tool = A2ACalendarTool()
    result = await tool.check_calendar("che impegni ho domani?")
    print(f"📅 Risultato A2A Legacy: {result}")
    return result

async def test_calendar_agent_connectivity():
    """Test connettività basic con Calendar Agent"""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get("http://localhost:8001/.well-known/agent.json")
            if response.status_code == 200:
                agent_card = response.json()
                print(f"✅ Calendar Agent connesso: {agent_card['name']}")
                return True
            else:
                print(f"❌ Calendar Agent HTTP {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Calendar Agent non raggiungibile: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# MAIN TEST
# ═══════════════════════════════════════════════════════════════

async def main():
    """Test completo dell'A2A Calendar Tool"""
    print("🎯 A2A Calendar Tool - Test Suite")
    print("=" * 50)

    # Test 1: Connettività
    print("\n1. Test connettività Calendar Agent:")
    connectivity = await test_calendar_agent_connectivity()

    if not connectivity:
        print("⚠️  Calendar Agent non disponibile. Avvialo con:")
        print("   cd calendar_agent && python calendar_server.py")
        return

    # Test 2: Funzione callable (ADK compatible)
    print("\n2. Test funzione callable (ADK compatible):")
    await test_a2a_callable()

    # Test 3: Classe legacy
    print("\n3. Test classe legacy:")
    await test_a2a_legacy()

    print("\n✅ A2A Calendar Tool test completato!")

if __name__ == "__main__":
    asyncio.run(main())

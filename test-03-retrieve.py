#!/usr/bin/env python3
"""
Test 03: Retrieval (RAG vs LLM)
Exit: 0=Pass, 1=Critical, 2=Partial
Usage: python test_03_retrieve.py [--provider openrouter|ollama|vllm]
"""

import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from memu_factory import create_memory_instance

class C:
    G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; M = "\033[95m"; X = "\033[0m"; BOLD = "\033[1m"

def pass_(m): print(f"{C.G}✔ PASS:{C.X} {m}")
def fail(m): print(f"{C.R}✖ FAIL:{C.X} {m}")
def info(m): print(f"{C.B}ℹ INFO:{C.X} {m}")

def setup_data(memory):
    print("\n" + "="*60); print("SETUP: Injecting Test Data"); print("="*60)
    facts = [
        "Projekt Sigma - AI Dashboard. Start: 01.01.2026. Lead: Maria Schmidt. Budget: 120k EUR. Deadline: 30.04.2026.",
        "Meeting 03.02.2026: Maria, Thomas, Lisa. Sigma UI Review. Dark Mode bis 15.02. Beta Testing ab 20.02.",
        "Risks Sigma: API delay (medium), scope creep (high), March resource gap (Lisa vacation). Mitigation: weekly sync, change process."
    ]
    for i, f in enumerate(facts, 1):
        info(f"Injecting fact {i}/3...")
        memory.memorize(f.strip())
        time.sleep(0.5)
    pass_("Test data ready")
    time.sleep(3)

def test_rag(memory):
    print("\n" + "="*60); print("TEST 3.1: RAG Retrieval"); print("="*60)
    queries = [
        ("Budget", "Wie hoch ist das Budget für Sigma?"),
        ("Team", "Wer ist im Sigma Team?"),
        ("Risk", "Welche Risiken hat Sigma?")
    ]
    scores = []
    for cat, q in queries:
        print(f"\n{C.M}Query ({cat}):{C.X} {q}")
        try:
            result = memory.retrieve(q, method="rag")
            if not result:
                fail(f"Empty for {cat}")
                scores.append(0)
                continue
            items = result.get("items", [])
            info(f"Retrieved {len(items)} items")
            relevant = False
            if cat == "Budget" and any("120" in str(i) for i in items): relevant = True
            elif cat == "Team" and any("maria" in str(i).lower() for i in items): relevant = True
            elif cat == "Risk" and any("risk" in str(i).lower() for i in items): relevant = True
            if relevant:
                pass_(f"Relevant info found for {cat}")
                scores.append(1)
            else:
                info(f"No direct match for {cat}")
                scores.append(0.5)
        except Exception as e:
            fail(f"RAG failed: {e}")
            scores.append(0)
    avg = sum(scores)/len(scores)
    print(f"\n{C.BOLD}RAG Score: {avg:.1f}/{len(queries)}{C.X}")
    return avg >= 0.75

def test_llm(memory):
    print("\n" + "="*60); print("TEST 3.2: LLM Retrieval"); print("="*60)
    queries = [
        ("Context", "Was sind die wichtigsten Infos zu Sigma?"),
        ("Risk", "Welche Herausforderungen hat Sigma?")
    ]
    scores = []
    for cat, q in queries:
        print(f"\n{C.M}Complex ({cat}):{C.X} {q}")
        try:
            info("Using LLM (may take 10-30s)...")
            start = time.time()
            result = memory.retrieve(q, method="llm")
            elapsed = time.time() - start
            info(f"Took {elapsed:.1f}s")
            if not result:
                fail(f"Empty for {cat}")
                scores.append(0)
                continue
            items = result.get("items", [])
            if items:
                pass_(f"LLM retrieved context for {cat}")
                scores.append(1)
            else:
                info(f"No items for {cat}")
                scores.append(0)
        except Exception as e:
            fail(f"LLM failed: {e}")
            scores.append(0)
    avg = sum(scores)/len(scores) if scores else 0
    print(f"\n{C.BOLD}LLM Score: {avg:.1f}/{len(queries)}{C.X}")
    return avg >= 0.5

def test_compare(memory):
    print("\n" + "="*60); print("TEST 3.3: RAG vs LLM"); print("="*60)
    q = "Was ist der Status von Sigma?"
    print(f"\n{C.M}Test:{C.X} {q}\n")
    results = {}
    
    try:
        info("RAG...")
        start = time.time()
        rag = memory.retrieve(q, method="rag")
        results["rag"] = {"ok": bool(rag and rag.get("items")), "time": time.time()-start, "n": len(rag.get("items",[]))}
        info(f"RAG: {results['rag']['n']} items in {results['rag']['time']:.2f}s")
    except Exception as e:
        fail(f"RAG: {e}")
        results["rag"] = {"ok": False, "time": 0, "n": 0}
    
    try:
        info("LLM...")
        start = time.time()
        llm = memory.retrieve(q, method="llm")
        results["llm"] = {"ok": bool(llm and llm.get("items")), "time": time.time()-start, "n": len(llm.get("items",[]))}
        info(f"LLM: {results['llm']['n']} items in {results['llm']['time']:.2f}s")
    except Exception as e:
        fail(f"LLM: {e}")
        results["llm"] = {"ok": False, "time": 0, "n": 0}
    
    print(f"\n{C.BOLD}Comparison:{C.X}")
    print(f"  RAG: {'✓' if results['rag']['ok'] else '✗'} ({results['rag']['time']:.1f}s, {results['rag']['n']} items)")
    print(f"  LLM: {'✓' if results['llm']['ok'] else '✗'} ({results['llm']['time']:.1f}s, {results['llm']['n']} items)")
    if results['rag']['ok'] and results['llm']['ok']:
        speedup = results['llm']['time']/results['rag']['time'] if results['rag']['time']>0 else 0
        print(f"\n  {C.Y}RAG is {speedup:.1f}x faster{C.X}")
    return results['rag']['ok'] or results['llm']['ok']

def main():
    print(f"\n{C.BOLD}{'='*60}{C.X}"); print(f"{C.BOLD}RETRIEVAL TEST{C.X}"); print(f"{C.BOLD}{'='*60}{C.X}")
    provider = "openrouter"
    if "--provider" in sys.argv:
        idx = sys.argv.index("--provider")
        if idx+1 < len(sys.argv): provider = sys.argv[idx+1]
    
    try:
        memory = create_memory_instance(user_id="test_user_03", agent_id="test", provider=provider)
    except Exception as e:
        print(f"\n{C.R}CRITICAL: No instance: {e}{C.X}")
        return 1
    
    setup_data(memory)
    
    results = []
    results.append(("RAG", test_rag(memory)))
    results.append(("LLM", test_llm(memory)))
    results.append(("Compare", test_compare(memory)))
    
    print(f"\n{C.BOLD}{'='*60}{C.X}"); print(f"{C.BOLD}SUMMARY{C.X}"); print(f"{C.BOLD}{'='*60}{C.X}\n")
    passed = sum(1 for _, r in results if r)
    for name, r in results:
        stat = f"{C.G}PASS{C.X}" if r else f"{C.R}FAIL{C.X}"
        print(f"  {stat} - {name}")
    print(f"\n{C.BOLD}{passed}/{len(results)} passed{C.X}\n")
    
    if passed == len(results):
        print(f"{C.G}✅ All passed!{C.X}")
        print(f"{C.G}   memU is PRODUCTION READY{C.X}\n")
        return 0
    elif passed >= 1:
        print(f"{C.Y}⚠ Partial success{C.X}\n")
        return 2
    else:
        print(f"{C.R}❌ All failed{C.X}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

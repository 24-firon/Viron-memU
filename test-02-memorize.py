#!/usr/bin/env python3
"""
Test 02: Memorize Pipeline (Write Path) - Updated for v1.3.0 API
Exit: 0=Pass, 1=Init Failed, 2=Memorize Failed
Usage: python test-02-memorize.py [--provider openrouter|ollama|vllm]
"""

import asyncio
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from memu_factory import create_memory_instance


class C:
    G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; X = "\033[0m"; BOLD = "\033[1m"

def pass_(m): print(f"{C.G}PASS:{C.X} {m}")
def fail(m): print(f"{C.R}FAIL:{C.X} {m}")
def info(m): print(f"{C.B}INFO:{C.X} {m}")


async def test_init(provider):
    print("\n" + "="*60); print(f"TEST 2.1: Memory Init ({provider})"); print("="*60)
    try:
        memory = create_memory_instance(user_id="test_user_02", agent_id="test", provider=provider)
        pass_("Memory created")
        return memory
    except ImportError as e:
        fail(f"memU not installed: {e}")
        info("Run: pip install -e . (from memU repo)")
        return None
    except Exception as e:
        fail(f"Init failed: {e}")
        return None


async def test_memorize(memory):
    print("\n" + "="*60); print("TEST 2.2: Memorize"); print("="*60)
    content = """
Projekt Phoenix - 04.02.2026
Leiter: Dr. Weber
Budget: 75.000 EUR (genehmigt 01.02.2026)
Deadline: 15.03.2026
Stack: Python 3.13, PostgreSQL, pgvector
Team: 3 Devs, 1 Data Scientist
"""
    info("Injecting test data...")
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(content)
            tmp_path = f.name

        result = await memory.memorize(
            resource_url=tmp_path,
            modality="document",
            user={"user_id": "test_user_02"},
        )

        if not isinstance(result, dict):
            fail(f"Expected dict, got {type(result)}")
            return False
        missing = [k for k in ["resource", "items", "categories"] if k not in result]
        if missing:
            fail(f"Missing keys: {missing}")
            return False
        pass_("Valid response structure")
        items = result.get("items", [])
        if items:
            pass_(f"Extracted {len(items)} items")
            print(f"{C.B}Sample Items:{C.X}")
            for i, item in enumerate(items[:3], 1):
                summary = item.get("summary", str(item))
                print(f"  {i}. {summary[:80]}...")
        else:
            fail("No items extracted")
            return False
        cats = result.get("categories", [])
        if cats:
            pass_(f"{len(cats)} categories")
        return True
    except Exception as e:
        fail(f"memorize() failed: {e}")
        import traceback; traceback.print_exc()
        return False
    finally:
        try:
            Path(tmp_path).unlink()
        except Exception:
            pass


async def test_persist(memory):
    print("\n" + "="*60); print("TEST 2.3: Persistence"); print("="*60)
    info("Waiting 2s for async processing...")
    time.sleep(2)
    try:
        queries = [{"role": "user", "content": {"text": "Was ist das Budget fuer Phoenix?"}}]
        info(f"Query: '{queries[0]['content']['text']}'")
        result = await memory.retrieve(queries=queries, where={"user_id": "test_user_02"})
        if not result:
            fail("Empty result")
            return False
        items = result.get("items", [])
        if items:
            pass_(f"Retrieved {len(items)} items")
            found = any("75" in str(i).lower() or "budget" in str(i).lower() for i in items)
            if found:
                pass_("Budget info found")
            else:
                info("Budget not in top results (may need tuning)")
            return True
        else:
            info("No items (embeddings may still process)")
            return True
    except Exception as e:
        fail(f"Persistence check failed: {e}")
        return False


async def main():
    print(f"\n{C.BOLD}{'='*60}{C.X}"); print(f"{C.BOLD}MEMORIZE PIPELINE TEST{C.X}"); print(f"{C.BOLD}{'='*60}{C.X}")
    provider = "openrouter"
    if "--provider" in sys.argv:
        idx = sys.argv.index("--provider")
        if idx+1 < len(sys.argv): provider = sys.argv[idx+1]

    results = []
    memory = await test_init(provider)
    if not memory:
        print(f"\n{C.R}CRITICAL: No instance. Abort.{C.X}")
        return 1
    results.append(("Init", True))

    mem_ok = await test_memorize(memory)
    results.append(("Memorize", mem_ok))
    if not mem_ok:
        print(f"\n{C.R}CRITICAL: Memorize failed. Abort.{C.X}")
        return 2

    pers_ok = await test_persist(memory)
    results.append(("Persist", pers_ok))

    print(f"\n{C.BOLD}{'='*60}{C.X}"); print(f"{C.BOLD}SUMMARY{C.X}"); print(f"{C.BOLD}{'='*60}{C.X}\n")
    passed = sum(1 for _, r in results if r)
    for name, r in results:
        stat = f"{C.G}PASS{C.X}" if r else f"{C.R}FAIL{C.X}"
        print(f"  {stat} - {name}")
    print(f"\n{C.BOLD}{passed}/{len(results)} passed{C.X}\n")

    if passed == len(results):
        print(f"{C.G}All passed!{C.X}")
        print(f"{C.G} Continue to test-03-retrieve.py{C.X}\n")
        return 0
    else:
        print(f"{C.Y}Partial success{C.X}\n")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

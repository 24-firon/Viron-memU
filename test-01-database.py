#!/usr/bin/env python3
"""
Test 01: Database Connectivity & Schema Validation
Exit: 0=Pass, 1=Critical, 2=Schema Issue
"""

import sys
import psycopg2
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from memu_factory import MemUConfig

class C:
    G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"; B = "\033[94m"; X = "\033[0m"; BOLD = "\033[1m"

def pass_(m): print(f"{C.G}✔ PASS:{C.X} {m}")
def fail(m): print(f"{C.R}✖ FAIL:{C.X} {m}")
def info(m): print(f"{C.B}ℹ INFO:{C.X} {m}")
def warn(m): print(f"{C.Y}⚠ WARN:{C.X} {m}")

def test_connection():
    print("\n" + "="*60); print("TEST 1.1: Database Connection"); print("="*60)
    try:
        conn = psycopg2.connect(MemUConfig().DATABASE_URL)
        pass_("Connected to PostgreSQL")
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        ver = cursor.fetchone()[0]
        info(f"PostgreSQL: {ver.split(',')[0]}")
        cursor.close(); conn.close()
        return True
    except psycopg2.OperationalError as e:
        fail(f"Cannot connect: {e}")
        info("Hint: docker-compose up -d")
        return False
    except Exception as e:
        fail(f"Error: {e}")
        return False

def test_pgvector():
    print("\n" + "="*60); print("TEST 1.2: pgvector Extension"); print("="*60)
    try:
        conn = psycopg2.connect(MemUConfig().DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';")
        result = cursor.fetchone()
        if result:
            pass_(f"pgvector {result[1]} installed")
            cursor.close(); conn.close()
            return True
        else:
            fail("pgvector NOT found")
            info("Run: docker exec memu_production_db psql -U memu_admin -d memu_production -c 'CREATE EXTENSION vector;'")
            cursor.close(); conn.close()
            return False
    except Exception as e:
        fail(f"Error: {e}")
        return False

def test_schema():
    print("\n" + "="*60); print("TEST 1.3: Schema Tables"); print("="*60)
    try:
        conn = psycopg2.connect(MemUConfig().DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
        tables = [r[0] for r in cursor.fetchall()]
        info(f"Found {len(tables)} tables")
        if len(tables) == 0:
            warn("No tables - will be created on first Memory() init")
            cursor.close(); conn.close()
            return True
        expected = ["memory_items", "categories", "resources"]
        found = sum(1 for e in expected if e in tables)
        if found > 0:
            pass_(f"Found {found} expected tables")
        info("All tables:")
        for t in tables: print(f"   - {t}")
        cursor.close(); conn.close()
        return True
    except Exception as e:
        fail(f"Error: {e}")
        return False

def test_write():
    print("\n" + "="*60); print("TEST 1.4: Write Permissions"); print("="*60)
    try:
        conn = psycopg2.connect(MemUConfig().DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS _test (id SERIAL PRIMARY KEY, data TEXT);")
        cursor.execute("INSERT INTO _test (data) VALUES ('test');")
        conn.commit()
        pass_("Write successful")
        cursor.execute("DROP TABLE _test;")
        conn.commit()
        info("Cleanup done")
        cursor.close(); conn.close()
        return True
    except Exception as e:
        fail(f"Write failed: {e}")
        return False

def main():
    print(f"\n{C.BOLD}{'='*60}{C.X}"); print(f"{C.BOLD}DATABASE VALIDATION{C.X}"); print(f"{C.BOLD}{'='*60}{C.X}")
    results = []
    results.append(("Connection", test_connection()))
    if not results[-1][1]:
        print(f"\n{C.R}CRITICAL: No connection. Aborting.{C.X}")
        return 1
    results.append(("pgvector", test_pgvector()))
    results.append(("Schema", test_schema()))
    results.append(("Write", test_write()))
    
    print(f"\n{C.BOLD}{'='*60}{C.X}"); print(f"{C.BOLD}SUMMARY{C.X}"); print(f"{C.BOLD}{'='*60}{C.X}\n")
    passed = sum(1 for _, r in results if r)
    for name, r in results:
        stat = f"{C.G}PASS{C.X}" if r else f"{C.R}FAIL{C.X}"
        print(f"  {stat} - {name}")
    print(f"\n{C.BOLD}{passed}/{len(results)} passed{C.X}\n")
    
    if passed == len(results):
        print(f"{C.G}✅ All tests passed!{C.X}")
        print(f"{C.G}   Continue to test_02_memorize.py{C.X}\n")
        return 0
    else:
        print(f"{C.R}❌ Some failed. Fix before continuing.{C.X}\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())

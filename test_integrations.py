"""Test LLM Integrations - Check API keys and fallback."""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

from src.integrations import (
    initialize_llm_registry,
    get_llm_registry,
    IntegrationHealthChecker
)


async def main():
    print("\n" + "="*60)
    print("TESTING LLM INTEGRATIONS")
    print("="*60 + "\n")
    
    print("Step 1: Initializing LLM Registry...")
    registry = initialize_llm_registry(
        openai_key=os.getenv("OPENAI_API_KEY"),
        anthropic_key=os.getenv("ANTHROPIC_API_KEY"),
        google_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # 2. List providers
    print("\n📋 Step 2: Registered Providers")
    providers = registry.list_providers()
    
    for p in providers:
        status = "[OK]" if p["available"] else "[SKIP]"
        primary = "*" if p["is_primary"] else " "
        print(f"  {primary} {status} {p['name']:12} - {p['provider']:12} ({p['model']})")
    
    # 3. Test health
    print("\n🏥 Step 3: Health Check (với LLM calls thật)")
    print("   Đang test từng provider...")
    
    checker = IntegrationHealthChecker(timeout=10.0)
    health = await checker.check_all()
    
    print(f"\n   Overall Status: {health['overall_status'].upper()}")
    print(f"   Healthy: {health['healthy']}/{health['total']}")
    
    for provider_result in health["providers"]:
        name = provider_result["provider"]
        status = provider_result["status"]
        
        if status == "healthy":
            time_ms = provider_result["response_time"] * 1000
            print(f"   [OK] {name:12} - Healthy ({time_ms:.0f}ms)")
        elif status == "no_api_key":
            print(f"   [SKIP] {name:12} - No API key")
        elif status == "timeout":
            print(f"   [TIMEOUT] {name:12} - Timeout")
        elif status == "error":
            print(f"   [ERROR] {name:12} - Error: {provider_result['error']}")
        else:
            print(f"   [?] {name:12} - {status}")
    
    # 4. Test fallback
    if health['healthy'] > 0:
        print("\n🔄 Step 4: Testing Fallback Mechanism")
        
        # Test với preferred order
        test_orders = [
            ["openai", "anthropic", "google"],
            ["anthropic", "google", "openai"],
            ["google", "openai", "anthropic"],
        ]
        
        for order in test_orders:
            print(f"\n   Testing order: {' → '.join(order)}")
            result = await checker.test_fallback(order)
            
            if result["status"] == "success":
                print(f"   [OK] Success with: {result['selected_provider']} "
                      f"({result['response_time']*1000:.0f}ms)")
            else:
                print(f"   [FAIL] Failed: {result['error']}")
    
    # 5. Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    available = [p for p in providers if p["available"]]
    healthy_providers = [r for r in health["providers"] if r["status"] == "healthy"]
    
    if not available:
        print("[ERROR] No providers have API keys!")
        print("\nTo test, add to .env:")
        print("  OPENAI_API_KEY=sk-...")
        print("  ANTHROPIC_API_KEY=sk-ant-...")
        print("  GOOGLE_API_KEY=...")
    elif not healthy_providers:
        print("[WARNING] Have API keys but no providers healthy!")
        print("   Possible reasons:")
        print("   - Wrong API key")
        print("   - Out of quota")
        print("   - Network issues")
    else:
        print(f"[OK] System ready!")
        print(f"   {len(healthy_providers)}/{len(available)} providers healthy")
        print(f"   Primary: {registry._primary}")
        print(f"\n   Available:")
        for p in healthy_providers:
            print(f"   - {p['provider']}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

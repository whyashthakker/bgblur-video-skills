#!/usr/bin/env python3
"""
BGBlur API connectivity check.
Usage: BGBLUR_API_KEY=xxx python3 scripts/api_health_check.py
"""
import os
import sys

try:
    import requests
except ImportError:
    print("error: requests not installed. Run: pip install requests")
    sys.exit(1)

BASE = os.environ.get("BGBLUR_API_BASE", "https://api.bgblur.com/v1")
API_KEY = os.environ.get("BGBLUR_API_KEY", "")


def main():
    print("=== BGBlur API Health Check ===")
    print()

    if not API_KEY:
        print("❌ BGBLUR_API_KEY not set")
        print("   export BGBLUR_API_KEY='your_key'")
        sys.exit(1)

    print(f"base_url: {BASE}")
    print(f"api_key: {'*' * 8}{API_KEY[-4:] if len(API_KEY) > 4 else '****'}")
    print()

    try:
        resp = requests.get(
            f"{BASE}/health",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
        if resp.status_code == 200:
            print("✅ API reachable and authenticated")
            if resp.text:
                print(f"   response: {resp.text[:200]}")
        elif resp.status_code == 401:
            print("❌ Authentication failed — check API key")
        elif resp.status_code == 404:
            print("⚠️  /health endpoint not found — API may use different path")
            print("   Verify base URL against BGBlur API docs")
        else:
            print(f"⚠️  Unexpected status: {resp.status_code}")
            print(f"   body: {resp.text[:200]}")
    except requests.ConnectionError:
        print(f"❌ Cannot reach {BASE}")
        print("   Check network and BGBLUR_API_BASE env var")
    except requests.Timeout:
        print("❌ Request timed out")

    print()
    print("=== Check Complete ===")


if __name__ == "__main__":
    main()

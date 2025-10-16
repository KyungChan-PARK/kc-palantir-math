#!/usr/bin/env python3
"""
API Key Validation Script

Validates stored API keys against actual services.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import sys
from scripts.api_vault import APIKeyVault


def validate_openai_key(key: str) -> tuple[bool, str]:
    """Validate OpenAI API key"""
    try:
        import httpx
        
        response = httpx.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            return True, f"Valid - {len(models.get('data', []))} models available"
        else:
            return False, f"Invalid - HTTP {response.status_code}"
    
    except Exception as e:
        return False, f"Error: {e}"


def validate_gemini_key(key: str) -> tuple[bool, str]:
    """Validate Google Gemini API key"""
    try:
        import httpx
        
        response = httpx.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": key},
            json={"contents": [{"parts": [{"text": "test"}]}]},
            timeout=10
        )
        
        if response.status_code in [200, 400]:
            return True, "Valid"
        else:
            return False, f"Invalid - HTTP {response.status_code}"
    
    except Exception as e:
        return False, f"Error: {e}"


def main():
    """Validate all stored keys"""
    vault = APIKeyVault()
    
    print("=" * 70)
    print("API Key Validation")
    print("=" * 70)
    print()
    
    services = {
        'openai': validate_openai_key,
        'gemini': validate_gemini_key
    }
    
    results = {}
    
    for service, validator in services.items():
        try:
            key = vault.get_key(service)
            valid, message = validator(key)
            
            status = "✓" if valid else "✗"
            print(f"{status} {service}: {message}")
            
            results[service] = {'valid': valid, 'message': message}
            
        except ValueError as e:
            print(f"⚠️  {service}: {e}")
            results[service] = {'valid': False, 'message': str(e)}
        except Exception as e:
            print(f"❌ {service}: {e}")
            results[service] = {'valid': False, 'message': str(e)}
    
    print()
    print("=" * 70)
    
    all_valid = all(r['valid'] for r in results.values())
    
    if all_valid:
        print("✅ All API keys valid")
        return 0
    else:
        print("❌ Some API keys invalid or missing")
        return 1


if __name__ == "__main__":
    sys.exit(main())


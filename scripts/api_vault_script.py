#!/usr/bin/env python3
"""
API Key Vault - Secure Storage with Auto-Rotation

Features:
- Encrypted storage (Fernet symmetric encryption)
- Expiration tracking
- Auto-rotation support
- Multi-service support

VERSION: 1.0.0
DATE: 2025-10-16
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


class APIKeyVault:
    """Secure encrypted storage for API keys"""
    
    def __init__(self, vault_path: Optional[Path] = None):
        self.vault_path = vault_path or Path.home() / ".math_api_vault"
        self.vault_path.mkdir(mode=0o700, exist_ok=True)
        self.key = self._get_or_create_key()
        
        try:
            from cryptography.fernet import Fernet
            self.cipher = Fernet(self.key)
        except ImportError:
            print("⚠️  cryptography not installed - using unencrypted storage")
            self.cipher = None
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = Path.home() / ".math_vault_encryption_key"
        
        if key_file.exists():
            return key_file.read_bytes()
        
        try:
            from cryptography.fernet import Fernet
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            key_file.chmod(0o600)
            return key
        except ImportError:
            # Fallback: no encryption
            return b"no-encryption-key-fallback"
    
    def store_key(self, service: str, key: str, expires_days: int = 90):
        """Store API key with expiration tracking"""
        data = {
            'key': key,
            'stored_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=expires_days)).isoformat(),
            'service': service,
            'rotations': 0
        }
        
        content = json.dumps(data).encode()
        
        if self.cipher:
            encrypted = self.cipher.encrypt(content)
        else:
            encrypted = content
        
        key_file = self.vault_path / f"{service}.enc"
        key_file.write_bytes(encrypted)
        key_file.chmod(0o600)
    
    def get_key(self, service: str) -> str:
        """Retrieve and validate API key"""
        key_file = self.vault_path / f"{service}.enc"
        
        if not key_file.exists():
            raise ValueError(f"No key found for {service}. Run: vault.store_key('{service}', 'key')")
        
        encrypted = key_file.read_bytes()
        
        if self.cipher:
            decrypted = self.cipher.decrypt(encrypted)
        else:
            decrypted = encrypted
        
        data = json.loads(decrypted)
        
        # Check expiration
        expires_at = datetime.fromisoformat(data['expires_at'])
        days_remaining = (expires_at - datetime.now()).days
        
        if days_remaining < 0:
            raise ValueError(f"API key for {service} expired {abs(days_remaining)} days ago")
        elif days_remaining < 7:
            print(f"⚠️  API key for {service} expires in {days_remaining} days - consider rotation")
        
        return data['key']
    
    def rotate_key(self, service: str, new_key: str):
        """Rotate API key with archival"""
        old_file = self.vault_path / f"{service}.enc"
        
        if old_file.exists():
            # Archive old key
            archive_dir = self.vault_path / "archive"
            archive_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            archive_file = archive_dir / f"{service}-{timestamp}.enc"
            old_file.rename(archive_file)
            
            # Increment rotation counter
            try:
                encrypted = archive_file.read_bytes()
                if self.cipher:
                    decrypted = self.cipher.decrypt(encrypted)
                else:
                    decrypted = encrypted
                old_data = json.loads(decrypted)
                rotations = old_data.get('rotations', 0) + 1
            except:
                rotations = 1
        else:
            rotations = 0
        
        # Store new key
        self.store_key(service, new_key)
        
        # Update rotation count
        key_file = self.vault_path / f"{service}.enc"
        encrypted = key_file.read_bytes()
        if self.cipher:
            decrypted = self.cipher.decrypt(encrypted)
        else:
            decrypted = encrypted
        data = json.loads(decrypted)
        data['rotations'] = rotations
        
        content = json.dumps(data).encode()
        if self.cipher:
            encrypted = self.cipher.encrypt(content)
        else:
            encrypted = content
        key_file.write_bytes(encrypted)
    
    def list_keys(self) -> list:
        """List all stored keys with status"""
        keys = []
        
        for key_file in self.vault_path.glob("*.enc"):
            try:
                service = key_file.stem
                encrypted = key_file.read_bytes()
                
                if self.cipher:
                    decrypted = self.cipher.decrypt(encrypted)
                else:
                    decrypted = encrypted
                
                data = json.loads(decrypted)
                
                expires_at = datetime.fromisoformat(data['expires_at'])
                days_remaining = (expires_at - datetime.now()).days
                
                keys.append({
                    'service': service,
                    'stored_at': data['stored_at'],
                    'expires_in_days': days_remaining,
                    'status': 'valid' if days_remaining > 0 else 'expired',
                    'rotations': data.get('rotations', 0)
                })
            except:
                continue
        
        return keys


if __name__ == "__main__":
    # Interactive key management
    import sys
    
    vault = APIKeyVault()
    
    if len(sys.argv) < 2:
        print("Usage: python3 api_vault.py [store|get|list|rotate]")
        print("\nCommands:")
        print("  store <service> <key> - Store new API key")
        print("  get <service>         - Retrieve API key")
        print("  list                  - List all keys")
        print("  rotate <service> <new_key> - Rotate key")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "store" and len(sys.argv) >= 4:
        service = sys.argv[2]
        key = sys.argv[3]
        vault.store_key(service, key)
        print(f"✓ Stored key for {service}")
    
    elif command == "get" and len(sys.argv) >= 3:
        service = sys.argv[2]
        key = vault.get_key(service)
        print(key)
    
    elif command == "list":
        keys = vault.list_keys()
        for k in keys:
            print(f"{k['service']}: {k['status']} (expires in {k['expires_in_days']} days, rotations: {k['rotations']})")
    
    elif command == "rotate" and len(sys.argv) >= 4:
        service = sys.argv[2]
        new_key = sys.argv[3]
        vault.rotate_key(service, new_key)
        print(f"✓ Rotated key for {service}")
    
    else:
        print("Invalid command")
        sys.exit(1)


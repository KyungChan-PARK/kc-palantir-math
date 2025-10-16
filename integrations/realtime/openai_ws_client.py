"""
OpenAI Realtime WebSocket Client

WebSocket client for OpenAI Realtime API.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import asyncio
import json
from typing import Optional, AsyncIterator, Dict, Any


class OpenAIRealtimeClient:
    """WebSocket client for OpenAI Realtime API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ws_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
        self.ws = None
        self._connected = False
    
    async def connect(self):
        """Establish WebSocket connection"""
        try:
            import websockets
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "OpenAI-Beta": "realtime=v1"
            }
            
            self.ws = await websockets.connect(self.ws_url, extra_headers=headers)
            self._connected = True
            
            # Send session config
            await self.ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "instructions": "You are a helpful math education assistant",
                    "voice": "alloy",
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "turn_detection": {"type": "server_vad"}
                }
            }))
            
        except ImportError:
            raise RuntimeError("websockets not installed. Install: pip install websockets")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to OpenAI Realtime: {e}")
    
    async def send_audio(self, audio_base64: str):
        """Send audio input to Realtime API"""
        if not self._connected:
            await self.connect()
        
        await self.ws.send(json.dumps({
            "type": "input_audio_buffer.append",
            "audio": audio_base64
        }))
    
    async def send_text(self, text: str):
        """Send text input to Realtime API"""
        if not self._connected:
            await self.connect()
        
        await self.ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": text}]
            }
        }))
        
        await self.ws.send(json.dumps({"type": "response.create"}))
    
    async def receive_events(self) -> AsyncIterator[Dict[str, Any]]:
        """Receive events from Realtime API"""
        if not self._connected:
            await self.connect()
        
        async for message in self.ws:
            try:
                event = json.loads(message)
                yield event
            except json.JSONDecodeError:
                continue
    
    async def disconnect(self):
        """Close WebSocket connection"""
        if self.ws:
            await self.ws.close()
            self._connected = False


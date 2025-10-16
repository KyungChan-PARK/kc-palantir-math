"""
Audio Codec for Realtime Gateway

Handles audio encoding/decoding for OpenAI Realtime API.

VERSION: 1.0.0
DATE: 2025-10-16
"""

import base64
from typing import Union


class AudioCodec:
    """Audio encoding/decoding utilities for realtime streaming"""
    
    @staticmethod
    def encode_pcm_to_base64(pcm_bytes: bytes) -> str:
        """Encode PCM audio to base64 for transmission"""
        return base64.b64encode(pcm_bytes).decode('utf-8')
    
    @staticmethod
    def decode_base64_to_pcm(b64_str: str) -> bytes:
        """Decode base64 audio to PCM bytes"""
        return base64.b64decode(b64_str)
    
    @staticmethod
    def convert_to_openai_format(audio: bytes, sample_rate: int = 16000) -> dict:
        """Convert raw audio to OpenAI Realtime format"""
        return {
            "type": "input_audio",
            "audio": base64.b64encode(audio).decode('utf-8'),
            "sample_rate": sample_rate,
            "format": "pcm16"
        }
    
    @staticmethod
    def convert_from_openai_format(openai_audio: dict) -> bytes:
        """Convert OpenAI format to raw PCM bytes"""
        if 'audio' in openai_audio:
            return base64.b64decode(openai_audio['audio'])
        return b""


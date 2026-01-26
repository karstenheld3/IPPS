#!/usr/bin/env python3
"""
Text-to-Voice Realtime Script
Converts text to speech using OpenAI's gpt-4o-mini-tts model with streaming audio playback.
"""

import asyncio
import sys
import os
from pathlib import Path

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer


async def text_to_voice(text: str, voice: str = "coral", instructions: str = None) -> None:
    """
    Convert text to speech and play audio in realtime.
    
    Args:
        text: Input text to convert (max 2000 characters)
        voice: Voice option (default: coral)
        instructions: Optional tone/style instructions
    
    Raises:
        ValueError: If text is empty or exceeds 2000 characters
        RuntimeError: If OPENAI_API_KEY is not set
    """
    # Validation
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    if len(text) > 2000:
        raise ValueError(f"Input text exceeds 2000 character limit ({len(text)} chars)")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    
    # Initialize async client
    client = AsyncOpenAI(api_key=api_key)
    
    try:
        # Create streaming response
        async with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            instructions=instructions or "Speak naturally and clearly.",
            response_format="wav",
        ) as response:
            # Stream audio to local player
            await LocalAudioPlayer().play(response)
            print(f"✓ Audio playback complete")
    
    except Exception as e:
        raise RuntimeError(f"API error: {e}")


def main():
    """Command-line entry point."""
    if len(sys.argv) < 2:
        print("Usage: python ttv.py <text> [--voice <voice>] [--instructions <instructions>]")
        print("Example: python ttv.py 'Hello world'")
        sys.exit(1)
    
    text = sys.argv[1]
    voice = "coral"
    instructions = None
    
    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--voice" and i + 1 < len(sys.argv):
            voice = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--instructions" and i + 1 < len(sys.argv):
            instructions = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    try:
        asyncio.run(text_to_voice(text, voice, instructions))
    except ValueError as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

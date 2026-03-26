#!/usr/bin/env python3
"""
transcribe.py — Transcribe audio files using OpenAI Whisper
Usage: python scripts/transcribe.py <audio-file-path>

Output: Saves transcript to inputs/processed/<basename>.transcript.md
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

def load_settings():
    """Load config/settings.yaml"""
    try:
        import yaml
        with open("config/settings.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("ERROR: config/settings.yaml not found. Run from the content-engine root directory.")
        sys.exit(1)

def load_env():
    """Load .env file"""
    env_path = Path("config/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())

def load_meta(audio_path: Path) -> dict:
    """Load companion .meta.yaml if it exists"""
    meta_path = audio_path.with_suffix(".meta.yaml")
    if meta_path.exists():
        try:
            import yaml
            with open(meta_path) as f:
                meta = yaml.safe_load(f)
                print(f"  Loaded meta file: {meta_path.name}")
                return meta or {}
        except Exception as e:
            print(f"  Warning: Could not parse meta file: {e}")
    return {}

def transcribe_with_whisper_api(audio_path: Path, api_key: str) -> str:
    """Transcribe using OpenAI Whisper API"""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    print(f"  Transcribing via OpenAI Whisper API...")
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    # Format with timestamps
    lines = []
    if hasattr(transcript, "segments") and transcript.segments:
        for segment in transcript.segments:
            start = format_timestamp(segment.get("start", 0))
            lines.append(f"[{start}] {segment.get('text', '').strip()}")
    else:
        lines = [transcript.text]

    return "\n".join(lines)

def transcribe_with_whisper_local(audio_path: Path) -> str:
    """Transcribe using local Whisper model (fallback)"""
    try:
        import whisper
        print("  Transcribing with local Whisper model (base)...")
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path))

        lines = []
        if "segments" in result:
            for segment in result["segments"]:
                start = format_timestamp(segment["start"])
                lines.append(f"[{start}] {segment['text'].strip()}")
        else:
            lines = [result["text"]]

        return "\n".join(lines)
    except ImportError:
        print("ERROR: Neither OpenAI API key nor local whisper package found.")
        print("Install with: pip install openai-whisper")
        sys.exit(1)

def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def clean_transcript(raw_transcript: str) -> str:
    """Basic cleanup — remove filler words, fix common transcription errors"""
    filler_words = [
        "um, ", "uh, ", "Um, ", "Uh, ",
        " um ", " uh ", " Um ", " Uh ",
        "like, ", "you know, ", "I mean, ",
    ]
    cleaned = raw_transcript
    for filler in filler_words:
        cleaned = cleaned.replace(filler, " ")

    # Clean up extra spaces
    import re
    cleaned = re.sub(r"  +", " ", cleaned)
    cleaned = re.sub(r"\n\n+", "\n\n", cleaned)

    return cleaned.strip()

def save_transcript(audio_path: Path, transcript: str, meta: dict, settings: dict) -> Path:
    """Save processed transcript to inputs/processed/"""
    output_dir = Path("inputs/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    base_name = audio_path.stem
    output_path = output_dir / f"{base_name}.transcript.md"

    client = meta.get("client", settings.get("active_client", "unknown"))
    participants = meta.get("participants", [])
    context = meta.get("context", "")
    off_limits = meta.get("off_limits_topics", [])

    content = f"""---
input_type: recording_transcript
source_file: {audio_path}
client: {client}
campaign: {meta.get('campaign', '')}
pillar_hint: {meta.get('pillar_hint', '')}
transcribed_at: {datetime.now().isoformat()}
transcription_model: whisper
---

# Transcript: {base_name}

**Date:** {date_str}
**Client:** {client}
**Participants:** {', '.join(participants) if participants else 'Not specified'}
**Context:** {context if context else 'Not provided'}

---

## Off-Limits Topics
{chr(10).join(f'- {t}' for t in off_limits) if off_limits else '- None specified'}

---

## Full Transcript

{transcript}

---

*Transcribed {datetime.now().strftime('%Y-%m-%d %H:%M')} — Ready for /process-input*
"""

    with open(output_path, "w") as f:
        f.write(content)

    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/transcribe.py <audio-file-path>")
        sys.exit(1)

    audio_path = Path(sys.argv[1])

    if not audio_path.exists():
        print(f"ERROR: File not found: {audio_path}")
        sys.exit(1)

    supported_formats = {".mp3", ".m4a", ".wav", ".mp4", ".webm", ".ogg"}
    if audio_path.suffix.lower() not in supported_formats:
        print(f"ERROR: Unsupported format '{audio_path.suffix}'. Supported: {supported_formats}")
        sys.exit(1)

    print(f"\n🎙 Transcribing: {audio_path.name}")
    print(f"   Size: {audio_path.stat().st_size / 1024 / 1024:.1f} MB")

    # Load config
    load_env()
    settings = load_settings()
    meta = load_meta(audio_path)

    # Transcribe
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        raw_transcript = transcribe_with_whisper_api(audio_path, api_key)
    else:
        print("  No OPENAI_API_KEY found — trying local Whisper model...")
        raw_transcript = transcribe_with_whisper_local(audio_path)

    # Clean
    print("  Cleaning transcript...")
    clean = clean_transcript(raw_transcript)

    # Save
    output_path = save_transcript(audio_path, clean, meta, settings)

    print(f"\n✓ Transcript saved: {output_path}")
    print(f"  Word count: ~{len(clean.split())}")
    print(f"\n  Next step: /process-input {output_path}")

if __name__ == "__main__":
    main()

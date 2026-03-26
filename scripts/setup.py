#!/usr/bin/env python3
"""
setup.py — First-time setup for the Content Ecosystem Engine
Usage: python scripts/setup.py

Checks dependencies, creates missing directories,
copies .env.example to .env if not present.
"""

import subprocess
import sys
import os
from pathlib import Path

REQUIRED_PACKAGES = [
    "anthropic",
    "openai",
    "notion_client",
    "pyyaml",
    "python_frontmatter",
]

OPTIONAL_PACKAGES = [
    ("openai-whisper", "local Whisper transcription (fallback if no OpenAI API key)"),
]

REQUIRED_DIRS = [
    "inputs/recordings",
    "inputs/notes",
    "inputs/briefs",
    "inputs/processed",
    "outputs/blog",
    "outputs/social",
    "outputs/email",
    "outputs/newsletter",
    "outputs/sales",
    "brand/_template",
    "brand/brian/examples",
    "campaigns",
    "config",
]

def check_python_version():
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")

def install_packages():
    print("\n📦 Installing required packages...")
    packages_str = " ".join(REQUIRED_PACKAGES)
    result = subprocess.run(
        f"pip install {packages_str} --break-system-packages -q",
        shell=True
    )
    if result.returncode == 0:
        print(f"✓ Installed: {', '.join(REQUIRED_PACKAGES)}")
    else:
        print(f"⚠ Some packages may have failed to install. Check pip output above.")

def create_directories():
    print("\n📁 Creating directory structure...")
    for dir_path in REQUIRED_DIRS:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("✓ All directories created")

def setup_env():
    print("\n🔑 Environment configuration...")
    env_path = Path("config/.env")
    example_path = Path("config/.env.example")

    if env_path.exists():
        print("✓ config/.env already exists")
    elif example_path.exists():
        import shutil
        shutil.copy(example_path, env_path)
        print("✓ Created config/.env from example")
        print("  ⚠  Open config/.env and add your API keys before running the engine")
    else:
        print("⚠ config/.env.example not found — create config/.env manually")

def check_brand_context():
    print("\n🎨 Brand context check...")
    settings_path = Path("config/settings.yaml")

    if not settings_path.exists():
        print("⚠ config/settings.yaml not found")
        return

    import yaml
    with open(settings_path) as f:
        settings = yaml.safe_load(f)

    active_client = settings.get("active_client", "")
    if not active_client:
        print("⚠ active_client not set in config/settings.yaml")
        return

    brand_path = Path(f"brand/{active_client}")
    required_files = ["voice.md", "pillars.md", "personas.yaml", "messaging.md"]
    missing = [f for f in required_files if not (brand_path / f).exists()]

    if missing:
        print(f"⚠ Brand context for '{active_client}' is incomplete.")
        print(f"  Missing: {', '.join(missing)}")
        print(f"  Run /new-brand {active_client} in Claude Code to set it up.")
    else:
        print(f"✓ Brand context found for: {active_client}")

def create_gitignore():
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        gitignore_path.write_text(
            "config/.env\n"
            "config/engine.log\n"
            "config/publish_errors.log\n"
            "inputs/recordings/*.mp3\n"
            "inputs/recordings/*.m4a\n"
            "inputs/recordings/*.wav\n"
            "__pycache__/\n"
            "*.pyc\n"
            ".DS_Store\n"
        )
        print("✓ Created .gitignore")

def print_next_steps():
    print("\n" + "="*50)
    print("✅ Setup complete!\n")
    print("Next steps:")
    print("  1. Add your API keys to config/.env")
    print("  2. Open Claude Code in this directory")
    print("  3. Run: /new-brand brian")
    print("     (fill in your brand voice, pillars, personas)")
    print("  4. Drop a notes file in inputs/notes/")
    print("  5. Run: /process-input inputs/notes/your-file.md")
    print("  6. Run: /generate-campaign inputs/processed/your-file-insights.yaml")
    print("\nYou're ready to build. 🚀")

def main():
    print("🚀 Content Ecosystem Engine — Setup\n")
    print("="*50)

    check_python_version()
    create_directories()
    install_packages()
    setup_env()
    create_gitignore()
    check_brand_context()
    print_next_steps()

if __name__ == "__main__":
    main()

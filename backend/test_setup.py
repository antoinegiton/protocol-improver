# test_setup.py - Verify everything works

import sys
print(f"✅ Python version: {sys.version}")

try:
    import fastapi
    print("✅ FastAPI installed")
except ImportError:
    print("❌ FastAPI not installed")

try:
    import anthropic
    print("✅ Anthropic installed")
except ImportError:
    print("❌ Anthropic not installed")

try:
    import pypdf
    print("✅ PyPDF installed")
except ImportError:
    print("❌ PyPDF not installed")

try:
    from docx import Document
    print("✅ python-docx installed")
except ImportError:
    print("❌ python-docx not installed")

# Test API key
try:
    from dotenv import load_dotenv
    import os
    
    # First install python-dotenv
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv", "-q"])
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if api_key and api_key.startswith("sk-ant-"):
        print("✅ API key found and looks valid")
    else:
        print("⚠️  API key not found or invalid format")
except Exception as e:
    print(f"⚠️  Could not check API key: {e}")

print("\n🎉 Setup check complete!")
print("If you see all ✅ marks, you're ready to build!")
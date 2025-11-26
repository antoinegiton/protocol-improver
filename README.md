# Protocol Improver

AI-powered laboratory protocol analyzer and improver using Claude AI.

## Features

- 📄 Upload PDF or DOCX lab protocols
- 🤖 AI-powered analysis using Claude
- ✅ Identifies safety issues, clarity problems, and improvement opportunities
- 📝 Generates improved, publication-ready protocols
- 🎯 Categorizes suggestions by priority (HIGH, MEDIUM, LOW)

## Live Demo

🌐 Visit: [Protocol Improver](https://protocol-improver.onrender.com)

## How It Works

1. **Upload** - Drop your protocol file (PDF or DOCX)
2. **Analyze** - AI analyzes and finds improvement areas
3. **Review** - See categorized suggestions with priorities
4. **Generate** - Create improved protocol with selected fixes
5. **Download** - Get your improved protocol

## Technology

- **Backend**: Python, FastAPI, Anthropic Claude API
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render.com + GitHub Pages

## Local Development

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/protocol-improver.git
cd protocol-improver

# Set up backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Run backend
python main.py

# Open frontend
# Open frontend/index.html in your browser
```

## Cost

- Backend hosting: Free (Render.com free tier)
- Frontend hosting: Free (GitHub Pages)
- AI usage: ~$0.10-0.30 per protocol analysis

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ for the scientific community

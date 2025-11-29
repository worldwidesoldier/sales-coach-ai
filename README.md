# Real-Time Sales Coach 🎯

AI-powered real-time sales coaching assistant that provides live suggestions during cold calls.

## Features

- ✅ Real-time audio transcription via Deepgram
- ✅ AI-powered sales coaching via Claude (Sonnet 4.5)
- ✅ Live objection detection
- ✅ Buying signal recognition
- ✅ Beautiful React + shadcn/ui interface
- ✅ Call history and analytics
- ✅ WebSocket-based real-time communication

## Architecture

```
┌─────────────┐        ┌──────────────┐        ┌─────────────┐
│   React     │◄──────►│    Flask     │◄──────►│  Deepgram   │
│  Frontend   │  WS    │   Backend    │  API   │     API     │
│  (Port 5173)│        │  (Port 5000) │        └─────────────┘
└─────────────┘        └──────┬───────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   Claude    │
                       │     API     │
                       └─────────────┘
```

## Tech Stack

### Backend
- Python 3.13+
- Flask + Flask-SocketIO
- Deepgram SDK (audio transcription)
- Anthropic SDK (Claude AI)
- eventlet (async operations)

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- shadcn/ui (component library)
- Tailwind CSS
- Socket.IO client

## Setup Instructions

### Prerequisites

1. Python 3.13 or higher
2. Node.js 18 or higher
3. API Keys:
   - Anthropic API key from https://console.anthropic.com
   - Deepgram API key from https://deepgram.com

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Your .env file is already configured with your API keys
# If needed, edit backend/.env to update them

# Run the backend server
python app.py
```

The backend should start on `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend should start on `http://localhost:5173`

## Usage

1. **Open the Application**
   - Navigate to `http://localhost:5173` in your browser
   - Ensure both backend and frontend servers are running

2. **Start a Call**
   - Click "Start Call" button
   - Grant microphone permissions when prompted
   - Place your phone call on speaker near your computer

3. **During the Call**
   - Watch live transcription appear in the left panel
   - AI suggestions appear in the right panel
   - Green/yellow/red alerts indicate sentiment
   - Objections and buying signals are automatically detected

4. **Controls**
   - **Mute**: Temporarily stop sending audio to the AI
   - **End Call**: Stop the call and save transcript

5. **Call History**
   - View past calls in the right sidebar
   - Click to view details
   - Delete unwanted calls

## Project Structure

```
coldcall/
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── config.py                       # Configuration & prompts
│   ├── .env                            # API keys (DO NOT COMMIT)
│   ├── services/
│   │   ├── deepgram_service.py         # Deepgram integration
│   │   ├── claude_service.py           # Claude AI integration
│   │   └── conversation_manager.py     # Context management
│   ├── utils/
│   │   ├── logger.py                   # Logging configuration
│   │   └── validators.py               # Input validation
│   └── calls/call_logs/                # Saved call transcripts
│
└── frontend/
    ├── src/
    │   ├── components/                 # React components
    │   │   ├── ui/                     # shadcn/ui components
    │   │   ├── CallControls.tsx
    │   │   ├── TranscriptionPanel.tsx
    │   │   ├── SuggestionsPanel.tsx
    │   │   └── CallHistory.tsx
    │   ├── hooks/                      # Custom React hooks
    │   │   ├── useWebSocket.ts
    │   │   ├── useAudioCapture.ts
    │   │   └── useCallState.ts
    │   ├── lib/                        # Utilities
    │   └── types/                      # TypeScript types
    └── package.json
```

## API Endpoints

### REST API

- `GET /api/health` - System health check
- `GET /api/calls` - List all saved calls
- `GET /api/calls/:id` - Get specific call details
- `DELETE /api/calls/:id` - Delete a call

### WebSocket Events

**Client → Server:**
- `start_call` - Start a new call session
- `end_call` - End the current call
- `audio_stream` - Send audio data

**Server → Client:**
- `connection_established` - Connection confirmed
- `call_started` - Call session started
- `transcription` - New transcription received
- `suggestion` - AI suggestion available
- `call_ended` - Call ended successfully
- `error` - Error occurred

## Customization

### Modify AI Prompts

Edit `backend/config.py` to customize:
- Sales pitch context
- Objection types
- Buying signals
- Response strategies

### Adjust UI Theme

Edit `frontend/src/index.css` to change colors and styling.

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**"API key invalid":**
- Check `backend/.env` file
- Ensure keys don't have extra spaces
- Verify keys are active in respective consoles

### Frontend Issues

**Port 5173 already in use:**
```bash
# Kill process on port
lsof -ti:5173 | xargs kill -9

# Or change port in vite.config.ts
```

**WebSocket connection failed:**
- Ensure backend is running on port 5000
- Check CORS settings in `backend/app.py`

### Audio Issues

**Microphone not working:**
- Check browser permissions (Chrome > Settings > Privacy > Microphone)
- Try a different browser (Chrome recommended)
- Ensure no other apps are using the microphone

**Poor transcription quality:**
- Reduce background noise
- Speak clearly into the microphone
- Adjust microphone volume in system settings

## Performance Targets

- ✅ Transcription latency: < 1 second
- ✅ AI response time: < 2 seconds
- ✅ Total latency: < 3 seconds (audio → suggestion)
- ✅ Transcription accuracy: > 90%

## Security Notes

- ⚠️ Never commit `.env` files to version control
- ⚠️ API keys are sensitive - keep them secret
- ⚠️ This is a development build - not production-ready
- ⚠️ Use HTTPS in production
- ⚠️ Add authentication before deploying

## Future Enhancements

- [ ] Speaker diarization improvements
- [ ] Custom objection library
- [ ] Call recording playback
- [ ] Analytics dashboard
- [ ] Multi-user support
- [ ] Integration with CRM systems
- [ ] Mobile app

## License

Private project - All rights reserved

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review logs in `backend/logs/`
3. Check browser console for frontend errors

---

Built with ❤️ using Claude Code, React, and Flask

# Quick Start Guide 🚀

Get your Real-Time Sales Coach running in 5 minutes!

## Step 1: Open Folder in VS Code

**YOU MUST DO THIS FIRST!**

1. Open VS Code
2. Click "Open Folder"
3. Navigate to `/Users/solonquinha/coldcall`
4. Click "Select Folder"

Now you'll see all the files!

## Step 2: Start the Backend (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Or use the quick start script:**
```bash
./start-backend.sh
```

You should see:
```
✅ API keys validated successfully
✅ All services initialized successfully
🚀 Starting Real-Time Sales Coach Backend
```

## Step 3: Start the Frontend (Terminal 2)

Open a NEW terminal in VS Code (Cmd+Shift+`) and run:

```bash
cd frontend
npm install
npm run dev
```

**Or use the quick start script:**
```bash
./start-frontend.sh
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

## Step 4: Open in Browser

Go to: **http://localhost:5173**

## Step 5: Test It!

1. Click "Start Call"
2. Allow microphone access
3. Speak into your microphone
4. Watch transcription appear!
5. AI suggestions will show up automatically

## Troubleshooting

### "No module named 'X'"
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Cannot find module"
```bash
cd frontend
npm install
```

### Port already in use
```bash
# Kill backend
lsof -ti:5000 | xargs kill -9

# Kill frontend
lsof -ti:5173 | xargs kill -9
```

### Microphone not working
- Allow microphone access in browser
- Check System Preferences > Security & Privacy > Microphone
- Make sure Chrome/Firefox has microphone permission

## API Keys

Your API keys are already configured in `backend/.env`:
- ✅ Anthropic (Claude)
- ✅ Deepgram

## Next Steps

Once everything is running:
1. Make a test call or practice speaking
2. Watch AI suggestions appear
3. Customize prompts in `backend/config.py`
4. Review call history in the sidebar

---

**Need help?** Check README.md for detailed documentation

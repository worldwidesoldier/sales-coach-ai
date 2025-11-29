"""
Real-Time Sales Coach - Flask Backend Server
Handles WebSocket connections, audio streaming, and API endpoints
"""

import os
import json
import logging
import threading
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services (will be created by other agents)
from services.deepgram_service import DeepgramService
from services.claude_service import ClaudeService
from services.conversation_manager import ConversationManager
from utils.logger import setup_logger
from utils.validators import validate_audio_data, validate_session_id, sanitize_filename
from config import BACKUP_TOOLKIT

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Enable CORS for React frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Initialize SocketIO with threading (Python 3.13 compatible)
socketio = SocketIO(
    app,
    cors_allowed_origins="http://localhost:5173",
    async_mode='threading',
    logger=False,
    engineio_logger=False
)

# Setup logging
logger = setup_logger()

# Validate API keys on startup
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == 'your_anthropic_api_key_here':
    logger.error("ANTHROPIC_API_KEY not set in .env file!")
    raise ValueError("Missing ANTHROPIC_API_KEY")

if not DEEPGRAM_API_KEY or DEEPGRAM_API_KEY == 'your_deepgram_api_key_here':
    logger.error("DEEPGRAM_API_KEY not set in .env file!")
    raise ValueError("Missing DEEPGRAM_API_KEY")

logger.info("✅ API keys validated successfully")

# Initialize services
try:
    deepgram_service = DeepgramService(DEEPGRAM_API_KEY)
    claude_service = ClaudeService(ANTHROPIC_API_KEY)
    conversation_manager = ConversationManager()
    logger.info("✅ All services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    raise

# Active call sessions
active_sessions = {}

# Calls directory
CALLS_DIR = os.path.join(os.path.dirname(__file__), 'calls', 'call_logs')
os.makedirs(CALLS_DIR, exist_ok=True)


# ============================================================================
# WebSocket Event Handlers
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Client connected to WebSocket"""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_established', {
        'connection_id': request.sid,
        'timestamp': datetime.now().isoformat()
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected from WebSocket"""
    logger.info(f"Client disconnected: {request.sid}")

    # Cleanup any active session for this client
    if request.sid in active_sessions:
        session_id = active_sessions[request.sid]['id']
        logger.info(f"Cleaning up session: {session_id}")

        # Stop Deepgram connection
        deepgram_service.stop_stream(session_id)

        # Remove from active sessions
        del active_sessions[request.sid]


@socketio.on('start_call')
def handle_start_call(data=None):
    """Start a new call session"""
    try:
        session_id = f"call_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.sid[:8]}"

        logger.info(f"Starting new call session: {session_id}")

        # Create session object
        session = {
            'id': session_id,
            'client_id': request.sid,
            'start_time': datetime.now().isoformat(),
            'transcripts': [],
            'suggestions': [],
            'status': 'active'
        }

        # Store in active sessions
        active_sessions[request.sid] = session

        # Initialize Deepgram streaming connection
        deepgram_service.start_stream(
            session_id=session_id,
            on_transcript=lambda transcript: handle_transcript(session_id, transcript)
        )

        # Initialize conversation manager
        conversation_manager.start_conversation(session_id)

        # Notify client
        emit('call_started', {
            'session_id': session_id,
            'timestamp': session['start_time']
        })

        logger.info(f"✅ Call session started: {session_id}")

    except Exception as e:
        logger.error(f"Error starting call: {e}", exc_info=True)
        emit('error', {'message': f'Failed to start call: {str(e)}'})


@socketio.on('end_call')
def handle_end_call(data=None):
    """End the current call session"""
    try:
        if request.sid not in active_sessions:
            emit('error', {'message': 'No active call session'})
            return

        session = active_sessions[request.sid]
        session_id = session['id']

        logger.info(f"Ending call session: {session_id}")

        # Update session status
        session['status'] = 'ended'
        session['end_time'] = datetime.now().isoformat()

        # Stop Deepgram streaming
        deepgram_service.stop_stream(session_id)

        # Stop conversation manager
        conversation_manager.end_conversation(session_id)

        # Save call to disk
        filename = f"{session_id}.json"
        filepath = os.path.join(CALLS_DIR, filename)

        with open(filepath, 'w') as f:
            json.dump(session, f, indent=2)

        logger.info(f"✅ Call saved to: {filepath}")

        # Notify client
        emit('call_ended', {
            'session_id': session_id,
            'filename': filename,
            'duration': (datetime.fromisoformat(session['end_time']) -
                        datetime.fromisoformat(session['start_time'])).total_seconds()
        })

        # Remove from active sessions
        del active_sessions[request.sid]

    except Exception as e:
        logger.error(f"Error ending call: {e}", exc_info=True)
        emit('error', {'message': f'Failed to end call: {str(e)}'})


@socketio.on('audio_stream')
def handle_audio_stream(data):
    """Receive audio stream from client and forward to Deepgram"""
    try:
        logger.info(f"🎤 RECEIVED AUDIO_STREAM EVENT - Session: {request.sid}")  # DEBUG

        if request.sid not in active_sessions:
            logger.warning(f"No active session for sid: {request.sid}")
            emit('error', {'message': 'No active call session'})
            return

        session = active_sessions[request.sid]
        session_id = session['id']

        # Validate audio data
        if not validate_audio_data(data):
            logger.warning("Invalid audio data received")
            return

        # Extract audio chunk
        audio_chunk = data.get('audio')

        if not audio_chunk:
            logger.warning("No audio data in stream")
            return

        logger.info(f"📤 Sending {len(audio_chunk)} bytes to Deepgram for session {session_id}")  # DEBUG

        # Send to Deepgram for transcription
        deepgram_service.send_audio(session_id, audio_chunk)

    except Exception as e:
        logger.error(f"Error processing audio stream: {e}", exc_info=True)
        emit('error', {'message': f'Audio processing error: {str(e)}'})


def handle_transcript(session_id, transcript_data):
    """Handle transcription received from Deepgram"""
    try:
        # Find the session
        session = None
        client_id = None

        for cid, sess in active_sessions.items():
            if sess['id'] == session_id:
                session = sess
                client_id = cid
                break

        if not session:
            logger.warning(f"Session not found for transcript: {session_id}")
            return

        # Store transcript
        session['transcripts'].append(transcript_data)

        # Send transcript to client
        socketio.emit('transcription', transcript_data, room=client_id)

        # If it's a final transcript, analyze with Claude
        if transcript_data.get('is_final'):
            # Add to conversation context
            conversation_manager.add_message(
                session_id,
                transcript_data['text'],
                transcript_data.get('speaker', 'unknown')
            )

            # Get AI suggestion in background thread
            thread = threading.Thread(target=get_ai_suggestion, args=(session_id, client_id))
            thread.daemon = True
            thread.start()

    except Exception as e:
        logger.error(f"Error handling transcript: {e}", exc_info=True)


def get_ai_suggestion(session_id, client_id):
    """Get AI suggestion from Claude (async)"""
    try:
        # Get conversation context
        context = conversation_manager.get_context(session_id)

        # Get suggestion from Claude
        suggestion = claude_service.get_suggestion(context)

        if suggestion:
            # Find session and store suggestion
            if client_id in active_sessions:
                active_sessions[client_id]['suggestions'].append(suggestion)

            # Send to client
            socketio.emit('suggestion', suggestion, room=client_id)
            logger.info(f"✅ Sent AI suggestion to client: {client_id}")

    except Exception as e:
        logger.error(f"Error getting AI suggestion: {e}", exc_info=True)
        socketio.emit('error', {
            'message': 'Failed to get AI suggestion'
        }, room=client_id)


# ============================================================================
# REST API Endpoints
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'deepgram': deepgram_service.is_healthy(),
                'claude': claude_service.is_healthy()
            },
            'active_calls': len(active_sessions)
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/api/calls', methods=['GET'])
def get_calls():
    """Get list of saved calls"""
    try:
        calls = []

        for filename in os.listdir(CALLS_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(CALLS_DIR, filename)

                with open(filepath, 'r') as f:
                    call_data = json.load(f)

                # Add summary info
                calls.append({
                    'id': call_data['id'],
                    'start_time': call_data['start_time'],
                    'end_time': call_data.get('end_time'),
                    'transcript_count': len(call_data.get('transcripts', [])),
                    'suggestion_count': len(call_data.get('suggestions', []))
                })

        # Sort by start time (newest first)
        calls.sort(key=lambda x: x['start_time'], reverse=True)

        return jsonify(calls), 200

    except Exception as e:
        logger.error(f"Error getting calls: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/calls/<call_id>', methods=['GET'])
def get_call(call_id):
    """Get specific call details"""
    try:
        # Sanitize filename
        safe_id = sanitize_filename(call_id)
        filename = f"{safe_id}.json"
        filepath = os.path.join(CALLS_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'Call not found'}), 404

        with open(filepath, 'r') as f:
            call_data = json.load(f)

        return jsonify(call_data), 200

    except Exception as e:
        logger.error(f"Error getting call {call_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/calls/<call_id>', methods=['DELETE'])
def delete_call(call_id):
    """Delete a specific call"""
    try:
        safe_id = sanitize_filename(call_id)
        filename = f"{safe_id}.json"
        filepath = os.path.join(CALLS_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'Call not found'}), 404

        os.remove(filepath)
        logger.info(f"Deleted call: {call_id}")

        return jsonify({'message': 'Call deleted successfully'}), 200

    except Exception as e:
        logger.error(f"Error deleting call {call_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/toolkit', methods=['GET'])
def get_toolkit():
    """Get the backup toolkit with sales scripts"""
    try:
        return jsonify(BACKUP_TOOLKIT), 200

    except Exception as e:
        logger.error(f"Error getting toolkit: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/calls/<call_id>/analyze', methods=['POST'])
def analyze_call(call_id):
    """Generate post-call analysis using Claude"""
    try:
        # Sanitize and load call data
        safe_id = sanitize_filename(call_id)
        filename = f"{safe_id}.json"
        filepath = os.path.join(CALLS_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'Call not found'}), 404

        # Load call data
        with open(filepath, 'r') as f:
            call_data = json.load(f)

        # Extract conversation context from transcripts
        conversation_context = []
        for transcript in call_data.get('transcripts', []):
            if transcript.get('is_final'):
                conversation_context.append({
                    'text': transcript.get('text', ''),
                    'speaker': transcript.get('speaker', 'unknown'),
                    'timestamp': transcript.get('timestamp', '')
                })

        # Calculate call duration
        call_duration = 0
        if 'start_time' in call_data and 'end_time' in call_data:
            start = datetime.fromisoformat(call_data['start_time'])
            end = datetime.fromisoformat(call_data['end_time'])
            call_duration = (end - start).total_seconds()

        # Generate analysis using Claude
        logger.info(f"Generating analysis for call: {call_id}")
        analysis = claude_service.analyze_call(conversation_context, call_duration)

        # Save analysis to call data
        call_data['analysis'] = analysis
        call_data['analyzed_at'] = datetime.now().isoformat()

        with open(filepath, 'w') as f:
            json.dump(call_data, f, indent=2)

        logger.info(f"✅ Analysis saved for call: {call_id}")

        return jsonify(analysis), 200

    except Exception as e:
        logger.error(f"Error analyzing call {call_id}: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'

    logger.info("=" * 60)
    logger.info("🚀 Starting Real-Time Sales Coach Backend")
    logger.info("=" * 60)
    logger.info(f"Port: {port}")
    logger.info(f"Debug: {debug}")
    logger.info(f"CORS enabled for: http://localhost:5173")
    logger.info("=" * 60)

    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug,
        allow_unsafe_werkzeug=True  # For development only
    )

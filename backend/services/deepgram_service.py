"""
Deepgram Service - Real-time audio transcription
"""

import base64
import json
import logging
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

logger = logging.getLogger('sales_coach')


class DeepgramService:
    """Handles real-time audio transcription via Deepgram API"""

    def __init__(self, api_key):
        """
        Initialize Deepgram service

        Args:
            api_key: Deepgram API key
        """
        self.api_key = api_key
        self.active_connections = {}
        self.speaker_state = {}  # Track current speaker per session

        # Initialize Deepgram client
        config = DeepgramClientOptions(
            options={"keepalive": "true"}
        )
        self.deepgram = DeepgramClient(api_key, config)

        logger.info("✅ Deepgram service initialized")

    def _identify_speaker(self, session_id, text, timestamp):
        """
        Simple turn-taking heuristics for speaker identification

        Rules:
        - First speaker = "Salesperson"
        - Pause > 1.5s = switch to other speaker
        - Alternate between "Salesperson" and "Customer"

        Args:
            session_id: Session ID
            text: Transcript text
            timestamp: Timestamp in seconds

        Returns:
            str: "Salesperson" or "Customer"
        """
        if session_id not in self.speaker_state:
            # First utterance = Salesperson
            self.speaker_state[session_id] = {
                'current_speaker': 'Salesperson',
                'last_timestamp': timestamp,
                'switch_threshold': 1.5  # seconds
            }
            return 'Salesperson'

        state = self.speaker_state[session_id]
        time_since_last = timestamp - state['last_timestamp']

        # Check if enough pause to switch speaker
        if time_since_last > state['switch_threshold']:
            # Switch speaker
            if state['current_speaker'] == 'Salesperson':
                state['current_speaker'] = 'Customer'
            else:
                state['current_speaker'] = 'Salesperson'

        # Update timestamp
        state['last_timestamp'] = timestamp

        return state['current_speaker']

    def start_stream(self, session_id, on_transcript):
        """
        Start streaming transcription for a session

        Args:
            session_id: Unique session identifier
            on_transcript: Callback function for transcription results
        """
        try:
            # Create live transcription connection
            dg_connection = self.deepgram.listen.live.v("1")

            # Configure transcription options
            # Browser sends WebM container with Opus codec
            options = LiveOptions(
                model="nova-2",
                language="en-US",
                encoding="opus",  # Opus codec (inside WebM container)
                smart_format=True,
                punctuate=True,
                interim_results=True,
                utterance_end_ms="1000",
                vad_events=True,
                filler_words=False,
                diarize=True  # Speaker diarization
            )

            # Event handlers - capture service instance in closure
            service = self  # Capture the DeepgramService instance

            def on_message(dg_self, result, **kwargs):
                try:
                    logger.info(f"📥 Deepgram on_message called for session {session_id}")
                    sentence = result.channel.alternatives[0].transcript
                    logger.info(f"📝 Transcript: '{sentence}' (length: {len(sentence)})")

                    if len(sentence) == 0:
                        logger.debug("Empty transcript, skipping")
                        return

                    # Determine if this is final
                    is_final = result.is_final

                    # Get timestamp for speaker identification
                    timestamp = result.start if hasattr(result, 'start') else 0

                    # Use turn-taking heuristics to identify speaker
                    speaker = service._identify_speaker(session_id, sentence, timestamp)

                    # Create transcript object
                    transcript = {
                        'text': sentence,
                        'speaker': speaker,  # Now returns "Salesperson" or "Customer"
                        'is_final': is_final,
                        'timestamp': timestamp,
                        'confidence': result.channel.alternatives[0].confidence if hasattr(result.channel.alternatives[0], 'confidence') else 0.9
                    }

                    if is_final:
                        logger.info(f"✅ FINAL: [{speaker}] {sentence[:50]}...")
                    else:
                        logger.debug(f"⏳ Interim: [{speaker}] {sentence[:30]}...")

                    # Call the callback (send both interim and final)
                    on_transcript(transcript)

                except Exception as e:
                    logger.error(f"Error processing transcript: {e}", exc_info=True)

            def on_error(dg_self, error, **kwargs):
                logger.error(f"❌ Deepgram error for session {session_id}: {error}")

            def on_open(dg_self, *args, **kwargs):
                logger.info(f"✅ Deepgram WebSocket OPENED for session: {session_id}")

            def on_close(dg_self, *args, **kwargs):
                logger.info(f"Deepgram connection closed for session: {session_id}")

            # Register event handlers
            dg_connection.on(LiveTranscriptionEvents.Open, on_open)
            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            dg_connection.on(LiveTranscriptionEvents.Close, on_close)

            logger.info(f"📋 Registered all Deepgram event handlers for session: {session_id}")

            # Start connection
            logger.info(f"🔌 Starting Deepgram connection for session: {session_id}")
            start_result = dg_connection.start(options)
            logger.info(f"🔌 Deepgram start result: {start_result}")

            if start_result is False:
                logger.error("❌ Failed to start Deepgram connection")
                return False

            # Store connection
            self.active_connections[session_id] = dg_connection

            logger.info(f"✅ Deepgram streaming started for session: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error starting Deepgram stream: {e}", exc_info=True)
            return False

    def send_audio(self, session_id, audio_base64):
        """
        Send audio chunk to Deepgram for transcription

        Args:
            session_id: Session ID
            audio_base64: Base64 encoded audio data
        """
        try:
            if session_id not in self.active_connections:
                logger.warning(f"No active connection for session: {session_id}")
                return False

            connection = self.active_connections[session_id]

            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_base64)

            # Send to Deepgram
            connection.send(audio_bytes)

            return True

        except Exception as e:
            logger.error(f"Error sending audio to Deepgram: {e}", exc_info=True)
            return False

    def stop_stream(self, session_id):
        """
        Stop streaming for a session

        Args:
            session_id: Session ID
        """
        try:
            if session_id not in self.active_connections:
                logger.warning(f"No active connection to stop for session: {session_id}")
                return

            connection = self.active_connections[session_id]

            # Close connection
            connection.finish()

            # Remove from active connections
            del self.active_connections[session_id]

            # Cleanup speaker state
            if session_id in self.speaker_state:
                del self.speaker_state[session_id]

            logger.info(f"✅ Deepgram stream stopped for session: {session_id}")

        except Exception as e:
            logger.error(f"Error stopping Deepgram stream: {e}", exc_info=True)

    def is_healthy(self):
        """
        Check if Deepgram service is healthy

        Returns:
            bool: True if healthy
        """
        try:
            # Simple check - if we have the API key, we're good
            return bool(self.api_key)
        except Exception:
            return False

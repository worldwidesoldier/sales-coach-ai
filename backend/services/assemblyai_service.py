"""
AssemblyAI Service - Real-time transcription with speaker diarization
"""

import assemblyai as aai
import base64
import logging

logger = logging.getLogger('sales_coach')

class AssemblyAIService:
    """Handles real-time audio transcription via AssemblyAI"""

    def __init__(self, api_key):
        """Initialize AssemblyAI service"""
        self.api_key = api_key
        self.active_connections = {}
        aai.settings.api_key = api_key
        logger.info("✅ AssemblyAI service initialized")

    def start_stream(self, session_id, on_transcript):
        """Start streaming transcription for a session"""
        try:
            def on_data(transcript):
                if transcript.text:
                    # AssemblyAI retorna speaker automaticamente!
                    speaker_label = transcript.speaker if hasattr(transcript, 'speaker') else "A"

                    # Converter speaker label (A, B) para Salesperson/Customer
                    # Assumir: primeiro speaker (A) = Salesperson
                    speaker_name = "Salesperson" if speaker_label == "A" else "Customer"

                    result = {
                        'text': transcript.text,
                        'speaker': speaker_name,
                        'is_final': True,  # AssemblyAI só retorna final
                        'timestamp': 0,
                        'confidence': transcript.confidence if hasattr(transcript, 'confidence') else 0.9
                    }

                    on_transcript(result)
                    logger.info(f"📥 [{speaker_name}]: {transcript.text[:50]}...")

            def on_error(error):
                logger.error(f"❌ AssemblyAI error: {error}")

            # Create real-time transcriber with speaker labels
            transcriber = aai.RealtimeTranscriber(
                sample_rate=16000,
                on_data=on_data,
                on_error=on_error,
                encoding=aai.AudioEncoding.pcm_s16le,
            )

            # Start connection
            transcriber.connect()

            self.active_connections[session_id] = transcriber
            logger.info(f"✅ AssemblyAI streaming started for session: {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error starting AssemblyAI stream: {e}", exc_info=True)
            return False

    def send_audio(self, session_id, audio_base64):
        """Send audio chunk to AssemblyAI"""
        try:
            if session_id not in self.active_connections:
                logger.warning(f"No active connection for session: {session_id}")
                return False

            transcriber = self.active_connections[session_id]

            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_base64)

            # Send to AssemblyAI
            transcriber.stream(audio_bytes)

            return True

        except Exception as e:
            logger.error(f"Error sending audio to AssemblyAI: {e}", exc_info=True)
            return False

    def stop_stream(self, session_id):
        """Stop streaming for a session"""
        try:
            if session_id not in self.active_connections:
                return

            transcriber = self.active_connections[session_id]
            transcriber.close()

            del self.active_connections[session_id]
            logger.info(f"✅ AssemblyAI stream stopped for session: {session_id}")

        except Exception as e:
            logger.error(f"Error stopping AssemblyAI stream: {e}", exc_info=True)

    def is_healthy(self):
        """
        Check if AssemblyAI service is healthy

        Returns:
            bool: True if healthy
        """
        try:
            # Simple check - if we have the API key, we're good
            return bool(self.api_key)
        except Exception:
            return False

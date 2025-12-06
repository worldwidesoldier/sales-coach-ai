/**
 * WebSocket connection configuration for Sales Coach AI
 * Uses environment variables for flexible deployment
 */

import { io, Socket } from 'socket.io-client';

// Get backend URL from environment variable or default to localhost:5001
const SOCKET_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5001';

/**
 * Socket.IO client instance with reconnection logic
 */
export const socket: Socket = io(SOCKET_URL, {
  autoConnect: true,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  timeout: 20000,
});

// Log connection status (development only)
if (import.meta.env.DEV) {
  socket.on('connect', () => {
    console.log(`✅ Connected to backend: ${SOCKET_URL}`);
  });

  socket.on('disconnect', (reason) => {
    console.log(`❌ Disconnected from backend: ${reason}`);
  });

  socket.on('connect_error', (error) => {
    console.error(`⚠️ Connection error:`, error.message);
  });
}

export default socket;

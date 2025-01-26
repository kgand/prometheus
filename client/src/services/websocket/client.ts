import { create } from 'zustand';

interface FireStatus {
  cameraId: string;
  fireDetected: boolean;
  confidence: number;
  lastChecked: string;
  location?: {
    lat: number;
    lng: number;
  };
}

interface WebSocketStore {
  fireStatuses: Record<string, FireStatus>;
  setFireStatus: (status: FireStatus) => void;
}

const useWebSocketStore = create<WebSocketStore>((set: any) => ({
  fireStatuses: {},
  setFireStatus: (status: FireStatus) =>
    set((state: WebSocketStore) => {
      return {
        fireStatuses: {
          ...state.fireStatuses,
          [status.cameraId]: status,
        },
      };
    }),
}));

class WebSocketClient {
  private static instance: WebSocketClient;
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000;

  private constructor() {
    this.connect();
  }

  public static getInstance(): WebSocketClient {
    if (!WebSocketClient.instance) {
      WebSocketClient.instance = new WebSocketClient();
    }
    return WebSocketClient.instance;
  }

  private connect() {
    try {
      console.log('Attempting to connect to WebSocket...');
      this.ws = new WebSocket('ws://localhost:8000/ws');

      this.ws.onopen = () => {
        console.log('WebSocket Connected Successfully');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event: MessageEvent) => {
        
        try {
          const message = JSON.parse(event.data);
          
          
          if (message.type === 'fire_update' && message.data) {
           
            useWebSocketStore.getState().setFireStatus({
              cameraId: message.data.camera_id,
              fireDetected: message.data.fire_detected,
              confidence: message.data.confidence,
              lastChecked: message.data.timestamp,
              location: message.data.location,
            });
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error, 'Raw data:', event.data);
        }
      };

      this.ws.onclose = (event) => {
        
        this.attemptReconnect();
      };

      this.ws.onerror = (error: Event) => {
        console.error('WebSocket Error:', error);
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.attemptReconnect();
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectTimeout * this.reconnectAttempts;
      console.log(`Scheduling reconnect attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`);
      setTimeout(() => {
        console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
        this.connect();
      }, delay);
    }
  }
}

export const initializeWebSocket = () => {
  console.log('Initializing WebSocket connection...');
  WebSocketClient.getInstance();
};

export const useFireStatus = () => {
  return useWebSocketStore((state: WebSocketStore) => {
    return state.fireStatuses;
  });
}; 
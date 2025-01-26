IMPORT_ML_ENDPOINTS = True

import uvicorn
from connect import app
from dotenv import load_dotenv
from non_ml_endpoints import *
from ws_endpoints import *  # Import WebSocket endpoints

if IMPORT_ML_ENDPOINTS:
    from ml_endpoints import *

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    try:
        port = 8000
        print(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Failed to start server: {e}")

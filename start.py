"""Railway startup — imports app directly, reads PORT from env."""
import os
import sys
from pathlib import Path

# Ensure repo root is on the path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from api.main import app

port = int(os.environ.get("PORT", 8000))
print(f"Starting on port {port}", flush=True)

uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

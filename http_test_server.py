"""
Simple HTTP Test Server to verify MCP UI connectivity
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🌤️ YOUR CUSTOM SERVER IS REACHABLE!", "status": "working"}

@app.get("/test")
def test():
    return {"test": "success", "server": "your-custom-weather-server"}

@app.get("/sse")
def sse_endpoint():
    return {"sse": "endpoint-accessible", "mcp": "ready"}

if __name__ == "__main__":
    print("🔧 HTTP Test Server for MCP UI")
    print("Testing URLs:")
    print("  http://127.0.0.1:8002/")
    print("  http://127.0.0.1:8002/test") 
    print("  http://127.0.0.1:8002/sse")
    uvicorn.run(app, host="127.0.0.1", port=8002)

"""
Debug Weather MCP Server

This version logs all interactions to help debug web client issues.
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

# Create server with detailed logging
mcp = FastMCP("Debug Weather Server")

# API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    print(f"🔍 DEBUG: get_weather called with city='{city}'")
    
    try:
        if OPENWEATHER_API_KEY == "your_api_key_here":
            result = f"🌤️ [YOUR CUSTOM MCP SERVER] Mock weather for {city}: 22°C, sunny, 60% humidity"
            print(f"✅ DEBUG: Returning mock data: {result}")
            return result
        
        # Make API call synchronously for web client compatibility
        import httpx
        with httpx.Client() as client:
            response = client.get(
                OPENWEATHER_BASE_URL,
                params={
                    "q": city,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            temp = data["main"]["temp"]
            condition = data["weather"][0]["main"]
            humidity = data["main"]["humidity"]
            
            result = f"🌤️ [YOUR CUSTOM MCP SERVER] Weather in {city}: {temp}°C, {condition}, {humidity}% humidity"
            print(f"✅ DEBUG: API call successful, returning: {result}")
            return result
            
    except Exception as e:
        error_msg = f"🌤️ [YOUR CUSTOM MCP SERVER] Error getting weather for {city}: {str(e)}"
        print(f"❌ DEBUG: Error occurred: {error_msg}")
        return error_msg


@mcp.tool()
def hello() -> str:
    """Simple test tool that always works."""
    print("🔍 DEBUG: hello tool called")
    result = "🌤️ [YOUR CUSTOM MCP SERVER] Hello! This response proves your custom weather server is working! 👋"
    print(f"✅ DEBUG: hello tool returning: {result}")
    return result


if __name__ == "__main__":
    print("🐛 Debug Weather MCP Server")
    print("=" * 30)
    print("Tools available:")
    print("  - hello: Simple test tool")
    print("  - get_weather: Get weather for a city")
    print()
    
    if OPENWEATHER_API_KEY == "your_api_key_here":
        print("⚠️  Using mock weather data")
    else:
        print("✅ Real API key configured")
    
    print("🌐 Server URL: http://127.0.0.1:8001/sse")  # Different port
    print("🔧 Starting server with CORS...")
    
    # Enable CORS
    try:
        app = mcp.sse_app()
        from fastapi.middleware.cors import CORSMiddleware
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8001)  # Different port
    except Exception as e:
        print(f"Error: {e}")
        mcp.run(transport="sse")

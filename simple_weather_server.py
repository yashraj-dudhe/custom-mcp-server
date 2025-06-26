"""
Simplified Weather MCP Server for Web Client Compatibility

This version provides simpler, more compatible responses for web-based MCP clients.
"""

import asyncio
import os
from typing import Dict, Any
import httpx
import json
from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Weather Server")

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather_data(city: str) -> Dict[str, Any]:
    """Fetch weather data from OpenWeatherMap API."""
    if OPENWEATHER_API_KEY == "your_api_key_here":
        # Return mock data for demonstration
        return {
            "city_name": city,
            "temperature_celsius": 22.5,
            "temperature_fahrenheit": 72.5,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "description": "Mock weather data - please set OPENWEATHER_API_KEY"
        }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                OPENWEATHER_BASE_URL,
                params={
                    "q": city,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            
            data = response.json()
            temp_celsius = data["main"]["temp"]
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            
            return {
                "city_name": data["name"],
                "temperature_celsius": round(temp_celsius, 1),
                "temperature_fahrenheit": round(temp_fahrenheit, 1),
                "condition": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise Exception(f"City '{city}' not found")
            raise Exception(f"Weather API error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to fetch weather: {str(e)}")


@mcp.tool()
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    
    Args:
        city: The name of the city
        
    Returns:
        Weather information as formatted text
    """
    try:
        # Use asyncio to run the async function
        weather_data = asyncio.create_task(fetch_weather_data(city))
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, we need to handle this differently
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, fetch_weather_data(city))
                weather_data = future.result()
        else:
            weather_data = asyncio.run(fetch_weather_data(city))
        
        # Return simple formatted text
        return f"""Current weather in {weather_data['city_name']}:
Temperature: {weather_data['temperature_celsius']}°C ({weather_data['temperature_fahrenheit']}°F)
Condition: {weather_data['condition']} - {weather_data['description']}
Humidity: {weather_data['humidity']}%"""

    except Exception as e:
        return f"Error getting weather for {city}: {str(e)}"


@mcp.tool()
def compare_weather(city1: str, city2: str) -> str:
    """
    Compare weather between two cities.
    
    Args:
        city1: First city name
        city2: Second city name
        
    Returns:
        Weather comparison as formatted text
    """
    try:
        # Get weather for both cities
        weather1 = asyncio.run(fetch_weather_data(city1))
        weather2 = asyncio.run(fetch_weather_data(city2))
        
        return f"""Weather Comparison:

{weather1['city_name']}:
- Temperature: {weather1['temperature_celsius']}°C
- Condition: {weather1['condition']}
- Humidity: {weather1['humidity']}%

{weather2['city_name']}:
- Temperature: {weather2['temperature_celsius']}°C  
- Condition: {weather2['condition']}
- Humidity: {weather2['humidity']}%

Temperature difference: {abs(weather1['temperature_celsius'] - weather2['temperature_celsius']):.1f}°C"""

    except Exception as e:
        return f"Error comparing weather: {str(e)}"


if __name__ == "__main__":
    print("🌤️  Starting Simple Weather MCP Server for Web Clients")
    print("=" * 55)
    
    print("Available tools:")
    print("  - get_weather: Get weather for a city")
    print("  - compare_weather: Compare weather between two cities")
    print()
    
    if OPENWEATHER_API_KEY == "your_api_key_here":
        print("⚠️  Using mock weather data")
        print("   Set OPENWEATHER_API_KEY for real data")
    else:
        print("✅ OpenWeatherMap API configured")
    
    print(f"\n🌐 Server URL: http://127.0.0.1:8000/sse")
    print("🔧 CORS enabled for web clients")
    
    # Enable CORS for web clients
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
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"CORS setup error: {e}")
        mcp.run(transport="sse")

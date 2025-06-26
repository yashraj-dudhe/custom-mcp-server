"""
MCP Weather Server

This server provides weather information through resources, tools, and prompts.
It uses the OpenWeatherMap API to fetch current weather data.
"""

import asyncio
import os
from typing import Dict, Any
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create the MCP server instance with CORS configuration
mcp = FastMCP("Weather Server")

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather_data(city: str) -> Dict[str, Any]:
    """
    Fetch weather data from OpenWeatherMap API.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Dictionary containing weather data
        
    Raises:
        Exception: If API call fails or city not found
    """
    if OPENWEATHER_API_KEY == "your_api_key_here":
        # Return mock data for demonstration if no API key is set
        return {
            "city_name": city,
            "temperature_celsius": 22.5,
            "temperature_fahrenheit": 72.5,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "description": "Mock weather data - please set OPENWEATHER_API_KEY environment variable"
        }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                OPENWEATHER_BASE_URL,
                params={
                    "q": city,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric"  # Get temperature in Celsius
                }
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract and format the weather data
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
            raise Exception(f"Failed to fetch weather data: {str(e)}")


@mcp.resource("weather://{city_name}")
async def get_weather_resource(city_name: str) -> str:
    """
    Weather resource that exposes current weather data for a given city.
    
    This resource can be accessed via URI like weather://London
    
    Args:
        city_name: Name of the city to get weather for
        
    Returns:
        Formatted weather information as a string
    """
    try:
        weather_data = await fetch_weather_data(city_name)
        
        # Format the weather data as a readable string
        return f"""Current Weather for {weather_data['city_name']}:
Temperature: {weather_data['temperature_celsius']}°C ({weather_data['temperature_fahrenheit']}°F)
Condition: {weather_data['condition']}
Description: {weather_data['description']}
Humidity: {weather_data['humidity']}%
"""
    except Exception as e:
        return f"Error fetching weather for {city_name}: {str(e)}"


@mcp.tool()
async def get_current_weather(city: str) -> str:
    """
    Tool that fetches the current weather for a specified city.
    
    This tool can be called by LLMs to get weather information programmatically.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        JSON-formatted weather data as a string
    """
    try:
        weather_data = await fetch_weather_data(city)
        
        # Return structured data that can be easily parsed
        import json
        return json.dumps(weather_data, indent=2)
        
    except Exception as e:
        error_response = {
            "error": str(e),
            "city": city,
            "success": False
        }
        import json
        return json.dumps(error_response, indent=2)


@mcp.prompt()
def weather_query_prompt(city: str) -> str:
    """
    Prompt template to guide the LLM in asking for weather information.
    
    Args:
        city: Name of the city to query weather for
        
    Returns:
        Formatted prompt string
    """
    return f"Please provide the current weather information for {city}. Include temperature, conditions, and humidity if available."


@mcp.prompt()
def weather_comparison_prompt(city1: str, city2: str) -> list[base.Message]:
    """
    Advanced prompt for comparing weather between two cities.
    
    Args:
        city1: First city to compare
        city2: Second city to compare
        
    Returns:
        List of messages for the LLM conversation
    """
    return [
        base.Message(
            role="user",
            content=f"Compare the current weather between {city1} and {city2}. "
                   f"Highlight the differences in temperature, conditions, and humidity. "
                   f"Provide insights about which city has better weather conditions today."
        )
    ]


if __name__ == "__main__":
    # Run the server
    print("Starting Weather MCP Server...")
    print("Resources available:")
    print("  - weather://<city_name> - Get weather data for a city")
    print("Tools available:")
    print("  - get_current_weather - Fetch current weather for a city")
    print("Prompts available:")
    print("  - weather_query_prompt - Generate weather query prompt")
    print("  - weather_comparison_prompt - Compare weather between two cities")
    print()
    
    if OPENWEATHER_API_KEY == "your_api_key_here":
        print("⚠️  WARNING: Using mock weather data!")
        print("   Set OPENWEATHER_API_KEY environment variable to use real weather data.")
        print("   Get your free API key at: https://openweathermap.org/api")
    else:
        print("✅ OpenWeatherMap API key configured")
    
    print("\nStarting server with SSE transport...")
    print("🌐 CORS enabled for web client access")
    
    # Enable CORS by getting the SSE app and adding middleware
    try:
        app = mcp.sse_app()
        from fastapi.middleware.cors import CORSMiddleware
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow all origins for development
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"Error configuring CORS: {e}")
        print("Running without CORS configuration...")
        mcp.run(transport="sse")

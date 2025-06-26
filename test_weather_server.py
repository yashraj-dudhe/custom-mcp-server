"""
Test script for the Weather MCP Server

This script tests the weather server functionality without requiring
a full MCP client setup.
"""

import asyncio
import json
import os
import sys

# Add the current directory to path so we can import our server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_server import (
    fetch_weather_data,
    get_weather_resource,
    get_current_weather,
)


async def test_weather_server():
    """Test the weather server functionality."""
    print("🌤️  Testing Weather MCP Server")
    print("=" * 50)
    
    # Test cities
    test_cities = ["London", "New York", "Tokyo", "InvalidCityName123"]
    
    for city in test_cities:
        print(f"\n📍 Testing city: {city}")
        print("-" * 30)
        
        try:
            # Test the core weather data fetch
            print("1. Testing fetch_weather_data()...")
            weather_data = await fetch_weather_data(city)
            city_name = weather_data['city_name']
            temp = weather_data['temperature_celsius']
            print(f"   ✅ Success: {city_name}, {temp}°C")
            
            # Test the resource
            print("2. Testing weather resource...")
            resource_data = await get_weather_resource(city)
            print(f"   ✅ Resource data preview: {resource_data[:100]}...")
            
            # Test the tool
            print("3. Testing get_current_weather tool...")
            tool_data = await get_current_weather(city)
            tool_json = json.loads(tool_data)
            if "error" in tool_json:
                print(f"   ❌ Tool error: {tool_json['error']}")
            else:
                print(f"   ✅ Tool success: {tool_json['city_name']}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🧪 Testing prompts...")
    
    # Import prompt functions
    from weather_server import weather_query_prompt, weather_comparison_prompt
    
    # Test simple prompt
    simple_prompt = weather_query_prompt("Paris")
    print(f"Simple prompt: {simple_prompt}")
    
    # Test comparison prompt
    comparison_prompt = weather_comparison_prompt("London", "Paris")
    print(f"Comparison prompt messages: {len(comparison_prompt)} message(s)")
    print("✅ Comparison prompt created successfully")
    
    print("\n✅ All tests completed!")


async def test_mock_mode():
    """Test that mock mode works when no API key is set."""
    print("\n🎭 Testing Mock Mode")
    print("=" * 30)
    
    # Temporarily remove API key to test mock mode
    original_key = os.environ.get("OPENWEATHER_API_KEY")
    os.environ["OPENWEATHER_API_KEY"] = "your_api_key_here"
    
    try:
        weather_data = await fetch_weather_data("TestCity")
        print(f"Mock data: {weather_data}")
        print("✅ Mock mode working correctly")
    except Exception as e:
        print(f"❌ Mock mode error: {e}")
    finally:
        # Restore original API key if it existed
        if original_key:
            os.environ["OPENWEATHER_API_KEY"] = original_key


def check_environment():
    """Check the environment setup."""
    print("🔍 Environment Check")
    print("=" * 20)
    
    # Check API key
    api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
    if api_key == "your_api_key_here":
        print("⚠️  No API key configured - will use mock data")
        print("   To use real weather data:")
        print("   1. Get free API key: https://openweathermap.org/api")
        print("   2. Set environment variable: OPENWEATHER_API_KEY=your_key")
    else:
        print(f"✅ API key configured: {api_key[:8]}...")
    
    # Check required packages
    try:
        import mcp  # noqa: F401
        print("✅ MCP package available")
    except ImportError:
        print("❌ MCP package not found - run: uv add mcp")
    
    try:
        import httpx  # noqa: F401
        print("✅ HTTPX package available")
    except ImportError:
        print("❌ HTTPX package not found - run: uv add httpx")


if __name__ == "__main__":
    print("🧪 Weather MCP Server Test Suite")
    print("=" * 40)
    
    check_environment()
    
    # Run the async tests
    asyncio.run(test_mock_mode())
    asyncio.run(test_weather_server())
    
    print("\n🎉 Test suite completed!")
    print("\nTo run the actual MCP server:")
    print("  python weather_server.py")
    print("\nTo test with MCP Inspector:")
    print("  uv run mcp dev weather_server.py")

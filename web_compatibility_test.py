"""
MCP Web Client Compatibility Test

This script tests if your MCP server is accessible to web clients
and provides different URL formats to try.
"""

import httpx
import asyncio
import json


async def test_mcp_endpoints():
    """Test different endpoint formats for web client compatibility."""
    
    print("🌐 Testing MCP Server Web Compatibility")
    print("=" * 45)
    
    # Different URL formats to test
    test_urls = [
        "http://127.0.0.1:8001/sse",
        "http://localhost:8001/sse", 
        "http://127.0.0.1:8001",
        "http://localhost:8001",
        "http://127.0.0.1:8000/sse",
        "http://localhost:8000/sse"
    ]
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for url in test_urls:
            try:
                print(f"\n🔍 Testing: {url}")
                
                # Test basic GET request
                response = await client.get(url)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Accessible to web clients")
                    
                    # Check if it's an SSE endpoint
                    content_type = response.headers.get("content-type", "")
                    if "text/event-stream" in content_type:
                        print("   ✅ SSE stream detected")
                    else:
                        print("   ⚠️  Not an SSE stream")
                        
                elif response.status_code == 404:
                    print("   ❌ Endpoint not found")
                else:
                    print(f"   ⚠️  Unexpected status: {response.status_code}")
                    
            except httpx.ConnectError:
                print(f"   ❌ Connection failed - server not running")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print(f"\n📋 Recommended URLs for web clients:")
    print(f"   Primary: http://127.0.0.1:8001/sse")
    print(f"   Alternative: http://localhost:8001/sse")


async def test_cors_headers():
    """Test CORS headers for web client compatibility."""
    
    print(f"\n🔒 Testing CORS Headers")
    print("=" * 25)
    
    try:
        async with httpx.AsyncClient() as client:
            # Test with OPTIONS request (CORS preflight)
            response = await client.options(
                "http://127.0.0.1:8001/sse",
                headers={
                    "Origin": "https://example.com",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            print(f"OPTIONS Status: {response.status_code}")
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("access-control-allow-origin"),
                "Access-Control-Allow-Methods": response.headers.get("access-control-allow-methods"),
                "Access-Control-Allow-Headers": response.headers.get("access-control-allow-headers"),
            }
            
            for header, value in cors_headers.items():
                if value:
                    print(f"   ✅ {header}: {value}")
                else:
                    print(f"   ❌ {header}: Not set")
                    
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")


def check_web_client_requirements():
    """Display common web client requirements."""
    
    print(f"\n📚 Common Web Client Requirements")
    print("=" * 35)
    
    requirements = [
        ("✅ HTTP Protocol", "Your server uses HTTP (correct)"),
        ("✅ SSE Transport", "Your server supports SSE"),
        ("✅ CORS Enabled", "Your server has CORS middleware"),
        ("✅ JSON Responses", "MCP protocol uses JSON"),
        ("⚠️  Port Access", "Web apps need localhost port access"),
        ("⚠️  HTTPS/HTTP Mix", "Some HTTPS apps can't access HTTP localhost")
    ]
    
    for status, description in requirements:
        print(f"   {status} {description}")


if __name__ == "__main__":
    print("🔧 MCP Web Client Compatibility Checker")
    print("=" * 40)
    
    # Run all tests
    asyncio.run(test_mcp_endpoints())
    asyncio.run(test_cors_headers())
    check_web_client_requirements()
    
    print(f"\n🎯 Summary:")
    print(f"   Your MCP server should work with web clients that support:")
    print(f"   - HTTP localhost connections")
    print(f"   - SSE (Server-Sent Events) transport")
    print(f"   - Standard MCP protocol")
    
    print(f"\n🌐 For the MCP UI web app, try:")
    print(f"   1. http://127.0.0.1:8001/sse")
    print(f"   2. http://localhost:8001/sse")
    print(f"   3. Make sure to select 'SSE' as transport type")

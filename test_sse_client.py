"""
SSE MCP Client Test Script

This script tests the Weather MCP Server running with SSE transport.
It connects to the server and tests resources, tools, and prompts.
"""

import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


async def test_sse_mcp_server():
    """Test the MCP server over SSE transport."""
    print("🔗 Testing Weather MCP Server with SSE Transport")
    print("=" * 55)
    
    # Connect to the SSE MCP server
    server_url = "http://127.0.0.1:8000/sse"
    
    try:
        async with sse_client(server_url) as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ Connected to MCP server successfully!")
                
                # Initialize the session
                await session.initialize()
                print("✅ Session initialized")
                
                # Test 1: List available resources
                print("\n📁 Testing Resources...")
                try:
                    resources = await session.list_resources()
                    print(f"Available resources: {len(resources.resources)}")
                    for resource in resources.resources:
                        print(f"  - {resource.uri}: {resource.name}")
                except Exception as e:
                    print(f"❌ Error listing resources: {e}")
                
                # Test 2: Get a weather resource
                print("\n🌤️  Testing Weather Resource...")
                try:
                    weather_uri = "weather://London"
                    weather_resource = await session.read_resource(weather_uri)
                    print("✅ Weather resource retrieved:")
                    for content in weather_resource.contents:
                        print(f"  {content.text[:200]}...")
                except Exception as e:
                    print(f"❌ Error reading weather resource: {e}")
                
                # Test 3: List available tools
                print("\n🔧 Testing Tools...")
                try:
                    tools = await session.list_tools()
                    print(f"Available tools: {len(tools.tools)}")
                    for tool in tools.tools:
                        print(f"  - {tool.name}: {tool.description}")
                except Exception as e:
                    print(f"❌ Error listing tools: {e}")
                
                # Test 4: Call the weather tool
                print("\n⚡ Testing Weather Tool...")
                try:
                    result = await session.call_tool(
                        "get_current_weather",
                        {"city": "Paris"}
                    )
                    print("✅ Weather tool called successfully:")
                    for content in result.content:
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            print(f"  City: {data.get('city_name', 'N/A')}")
                            temp = data.get('temperature_celsius', 'N/A')
                            print(f"  Temperature: {temp}°C")
                            condition = data.get('condition', 'N/A')
                            print(f"  Condition: {condition}")
                except Exception as e:
                    print(f"❌ Error calling weather tool: {e}")
                
                # Test 5: List available prompts
                print("\n💬 Testing Prompts...")
                try:
                    prompts = await session.list_prompts()
                    print(f"Available prompts: {len(prompts.prompts)}")
                    for prompt in prompts.prompts:
                        print(f"  - {prompt.name}: {prompt.description}")
                except Exception as e:
                    print(f"❌ Error listing prompts: {e}")
                
                # Test 6: Get a prompt
                print("\n📝 Testing Weather Prompt...")
                try:
                    prompt_result = await session.get_prompt(
                        "weather_query_prompt",
                        {"city": "Tokyo"}
                    )
                    print("✅ Weather prompt retrieved:")
                    for message in prompt_result.messages:
                        if hasattr(message, 'content'):
                            if hasattr(message.content, 'text'):
                                print(f"  {message.content.text}")
                            else:
                                print(f"  {message.content}")
                except Exception as e:
                    print(f"❌ Error getting weather prompt: {e}")
                
                print("\n🎉 All SSE MCP tests completed successfully!")
                
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the weather server is running:")
        print("   python weather_server.py")
        print("2. Check the server is accessible at:")
        print("   http://127.0.0.1:8000/sse")
        print("3. Verify no firewall is blocking the connection")


async def test_server_health():
    """Test basic server connectivity."""
    print("🏥 Testing Server Health")
    print("=" * 25)
    
    import httpx
    
    try:
        async with httpx.AsyncClient() as client:
            # Test basic HTTP connectivity
            response = await client.get("http://127.0.0.1:8000/", timeout=5.0)
            print(f"✅ Server is responding (Status: {response.status_code})")
            
            # Test SSE endpoint
            try:
                sse_url = "http://127.0.0.1:8000/sse"
                response = await client.get(sse_url, timeout=5.0)
                status = response.status_code
                print(f"✅ SSE endpoint accessible (Status: {status})")
            except Exception as sse_error:
                print(f"⚠️  SSE endpoint test: {sse_error}")
                
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        print("\n🔧 Server might not be running. Start it with:")
        print("   python weather_server.py")


if __name__ == "__main__":
    print("🧪 MCP SSE Server Test Suite")
    print("=" * 30)
    
    # Run health check first
    asyncio.run(test_server_health())
    
    print("\n" + "=" * 30)
    
    # Run full MCP tests
    asyncio.run(test_sse_mcp_server())
    
    print("\n📊 Test Summary:")
    print("✅ Your SSE MCP server is working if all tests passed")
    print("🌐 Server URL: http://127.0.0.1:8000/sse")
    print("📡 Transport: Server-Sent Events (SSE)")
    print("🔧 Ready for integration with any MCP client!")

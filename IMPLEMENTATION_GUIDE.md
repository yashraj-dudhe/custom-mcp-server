# Weather MCP Server Implementation Guide

## Overview

This document provides a comprehensive explanation of the Weather MCP Server implementation, including complex parts that require further understanding.

## Architecture

The Weather MCP Server is built using the MCP Python SDK's FastMCP framework and provides weather information through three main interfaces:

1. **Resources**: Static-like data access via URIs
2. **Tools**: Interactive functionality for LLMs
3. **Prompts**: Templates to guide LLM interactions

## Code Structure Explanation

### 1. Server Initialization

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather Server")
```

**Key Points:**
- `FastMCP` is the high-level server interface from the MCP Python SDK
- The server name "Weather Server" identifies this MCP server to clients
- This automatically handles the MCP protocol, connection management, and message routing

### 2. External API Integration

```python
async def fetch_weather_data(city: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            OPENWEATHER_BASE_URL,
            params={
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            }
        )
```

**Complex Parts Explained:**

- **Async Context Manager**: `async with httpx.AsyncClient()` ensures proper connection cleanup
- **Error Handling**: The function includes comprehensive error handling for:
  - HTTP 404 (city not found)
  - Network failures
  - API rate limits
  - Invalid API keys
- **Mock Data Fallback**: When no API key is configured, the server provides realistic mock data for testing

### 3. Resource Implementation

```python
@mcp.resource("weather://{city_name}")
async def get_weather_resource(city_name: str) -> str:
```

**Key Concepts:**

- **URI Pattern**: `weather://{city_name}` creates a templated URI that MCP clients can reference
- **Parameter Extraction**: The `{city_name}` placeholder is automatically passed as a function parameter
- **Resource vs Tool**: Resources are for data retrieval (similar to HTTP GET), tools are for actions

**Why Resources Matter:**
- LLMs can reference resources in context without executing them
- Clients can list available resources
- Resources support content negotiation (though we return strings here)

### 4. Tool Implementation

```python
@mcp.tool()
async def get_current_weather(city: str) -> str:
    weather_data = await fetch_weather_data(city)
    return json.dumps(weather_data, indent=2)
```

**Important Design Decisions:**

- **JSON Output**: Tools return JSON strings rather than Python objects for better LLM compatibility
- **Error Propagation**: Errors are caught and returned as structured JSON rather than exceptions
- **Async Pattern**: All network operations are async to prevent blocking

### 5. Prompt Templates

```python
@mcp.prompt()
def weather_query_prompt(city: str) -> str:
    return f"Please provide the current weather information for {city}..."

@mcp.prompt()
def weather_comparison_prompt(city1: str, city2: str) -> list[base.Message]:
    return [
        base.Message(
            role="user",
            content=f"Compare the current weather between {city1} and {city2}..."
        )
    ]
```

**Advanced Prompt Concepts:**

- **Simple Prompts**: Return strings for basic templates
- **Message Lists**: Return `list[base.Message]` for complex conversational flows
- **Role Assignment**: Messages can have different roles (user, assistant, system)

### 6. SSE Transport Configuration

```python
mcp.run(transport="sse")
```

**Transport Options Explained:**

- **SSE (Server-Sent Events)**: Recommended for production, supports streaming
- **STDIO**: For command-line integration (like with Claude Desktop)
- **HTTP**: For stateless deployments

**Why SSE?**
- Real-time bidirectional communication
- Better for web-based clients
- Supports connection persistence
- Handles network interruptions gracefully

## Error Handling Strategy

### 1. API-Level Errors

```python
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        raise Exception(f"City '{city}' not found")
    raise Exception(f"Weather API error: {e.response.status_code}")
```

**Strategy:**
- Convert HTTP errors to meaningful messages
- Distinguish between client errors (404) and server errors (500+)
- Preserve original error information for debugging

### 2. Resource-Level Errors

```python
except Exception as e:
    return f"Error fetching weather for {city_name}: {str(e)}"
```

**Design Choice:**
- Resources return error strings rather than raising exceptions
- This allows LLMs to understand and potentially recover from errors
- Maintains the resource interface contract

### 3. Tool-Level Errors

```python
error_response = {
    "error": str(e),
    "city": city,
    "success": False
}
return json.dumps(error_response, indent=2)
```

**Structured Error Response:**
- Consistent JSON format for all tool responses
- Includes context (city name) for better error understanding
- `success` field allows programmatic error detection

## Testing Strategy

### 1. Mock Data Mode

```python
if OPENWEATHER_API_KEY == "your_api_key_here":
    return {
        "city_name": city,
        "temperature_celsius": 22.5,
        # ... mock data
    }
```

**Benefits:**
- Allows testing without API credentials
- Consistent test data
- No API rate limit concerns during development

### 2. Comprehensive Test Suite

The `test_weather_server.py` includes:
- **Unit Testing**: Individual function testing
- **Integration Testing**: Full workflow testing
- **Error Scenario Testing**: Invalid cities, network failures
- **Environment Validation**: Package and configuration checks

## Configuration Management

### 1. Environment Variables

```python
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
```

**Best Practices:**
- Use environment variables for sensitive data
- Provide reasonable defaults
- Document configuration requirements

### 2. Configuration Files

The `.env.example` file provides:
- Template for environment setup
- Documentation of required variables
- Example values for development

## Security Considerations

### 1. API Key Management

- Never commit API keys to version control
- Use environment variables or secure configuration management
- Implement key rotation strategies for production

### 2. Input Validation

```python
# The MCP framework handles basic parameter validation
# Additional validation could be added here
if not city or not city.strip():
    raise ValueError("City name cannot be empty")
```

### 3. Rate Limiting

Consider implementing:
- Client-side rate limiting
- Caching strategies
- Fallback mechanisms

## Performance Optimization

### 1. Async Operations

All network operations use `async/await` to prevent blocking:
- Multiple weather requests can be processed concurrently
- Server remains responsive during API calls
- Better resource utilization

### 2. Connection Pooling

```python
async with httpx.AsyncClient() as client:
```

The HTTP client automatically handles:
- Connection reuse
- Keep-alive connections
- Timeout management

### 3. Potential Enhancements

- **Caching**: Implement Redis or in-memory caching
- **Batch Requests**: Support multiple cities in one request
- **Streaming**: For large weather datasets

## Deployment Considerations

### 1. Production Deployment

- Use environment-specific configuration
- Implement proper logging
- Set up monitoring and alerting
- Consider containerization (Docker)

### 2. Scaling Strategies

- **Horizontal Scaling**: Multiple server instances
- **Load Balancing**: Distribute requests across instances
- **Geographic Distribution**: Deploy closer to users

### 3. Monitoring

Key metrics to track:
- Request latency
- Error rates
- API quota usage
- Server resource utilization

## Integration Examples

### 1. Claude Desktop Integration

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "python",
      "args": ["weather_server.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 2. Programmatic Usage

```python
from mcp.client.session import ClientSession

async with ClientSession() as session:
    # Use weather resource
    weather_data = await session.get_resource("weather://London")
    
    # Call weather tool
    result = await session.call_tool("get_current_weather", {"city": "London"})
```

## Troubleshooting Guide

### Common Issues

1. **"City not found" errors**
   - Verify city name spelling
   - Try alternative names (e.g., "New York City" vs "NYC")
   - Check OpenWeatherMap's city database

2. **API key errors**
   - Verify API key is active
   - Check API quota limits
   - Ensure environment variable is set correctly

3. **Network errors**
   - Verify internet connectivity
   - Check firewall settings
   - Test API endpoint directly

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This provides detailed information about:
- HTTP requests and responses
- MCP protocol messages
- Error stack traces

## Extending the Server

### Adding New Features

1. **Weather Forecasts**
   ```python
   @mcp.resource("forecast://{city_name}/{days}")
   async def get_weather_forecast(city_name: str, days: int) -> str:
   ```

2. **Weather Alerts**
   ```python
   @mcp.tool()
   async def get_weather_alerts(city: str) -> str:
   ```

3. **Historical Data**
   ```python
   @mcp.resource("history://{city_name}/{date}")
   async def get_weather_history(city_name: str, date: str) -> str:
   ```

### Adding New Providers

Support multiple weather APIs:
```python
WEATHER_PROVIDERS = {
    "openweather": OpenWeatherProvider(),
    "weatherapi": WeatherAPIProvider(),
    "accuweather": AccuWeatherProvider()
}
```

This implementation provides a solid foundation for a production-ready weather MCP server while maintaining clarity and extensibility.

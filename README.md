# Weather MCP Server

A Model Context Protocol (MCP) server that provides current weather information using the OpenWeatherMap API.

## Features

### Resources
- **weather://{city_name}**: Exposes current weather data for any city
  - Returns: city name, temperature (°C and °F), weather condition, description, and humidity

### Tools
- **get_current_weather**: Programmatically fetch weather data for a specified city
  - Input: city name (string)
  - Output: JSON-formatted weather data

### Prompts
- **weather_query_prompt**: Template for querying weather information
- **weather_comparison_prompt**: Template for comparing weather between two cities

## Setup

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key (free at https://openweathermap.org/api)

### Installation

1. **Install dependencies using uv (recommended):**
   ```bash
   uv add mcp httpx
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env and add your OpenWeatherMap API key
   # OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

   Or set the environment variable directly:
   ```bash
   # Windows (PowerShell)
   $env:OPENWEATHER_API_KEY="your_actual_api_key_here"
   
   # Windows (Command Prompt)
   set OPENWEATHER_API_KEY=your_actual_api_key_here
   
   # Linux/Mac
   export OPENWEATHER_API_KEY="your_actual_api_key_here"
   ```

## Running the Server

### Development Mode
```bash
# Using uv (recommended)
uv run mcp dev weather_server.py

# Using Python directly
python weather_server.py
```

### Production Mode with SSE Transport
```bash
# The server runs with SSE transport by default
python weather_server.py
```

### Testing with MCP Inspector
```bash
# Install and run the MCP Inspector for testing
uv run mcp dev weather_server.py
```

## Usage Examples

### Using Resources
Once connected to an MCP client (like Claude Desktop), you can access weather data via resources:

```
weather://London
weather://New York
weather://Tokyo
```

### Using Tools
The `get_current_weather` tool can be called programmatically:

```json
{
  "tool": "get_current_weather",
  "arguments": {
    "city": "London"
  }
}
```

### Using Prompts
The weather prompts help structure LLM interactions:

- `weather_query_prompt(city="London")` → "Please provide the current weather information for London..."
- `weather_comparison_prompt(city1="London", city2="Paris")` → Structured comparison prompt

## API Response Format

The weather data follows this schema:

```json
{
  "city_name": "London",
  "temperature_celsius": 15.5,
  "temperature_fahrenheit": 59.9,
  "condition": "Clouds",
  "humidity": 78,
  "description": "broken clouds"
}
```

## Integration with Claude Desktop

Add this server to your Claude Desktop configuration:

1. Open Claude Desktop settings
2. Navigate to MCP servers configuration
3. Add a new server:

```json
{
  "weather-server": {
    "command": "python",
    "args": ["path/to/weather_server.py"],
    "env": {
      "OPENWEATHER_API_KEY": "your_api_key_here"
    }
  }
}
```

## Error Handling

The server includes comprehensive error handling:

- **Invalid city names**: Returns "City not found" error
- **API failures**: Returns HTTP error details
- **Missing API key**: Falls back to mock data with warning
- **Network issues**: Returns connection error details

## Mock Data Mode

If no API key is configured, the server runs in mock data mode for testing:

```bash
# This will use mock weather data
python weather_server.py
```

The mock data includes realistic weather information for demonstration purposes.

## Development

### Code Structure
- `fetch_weather_data()`: Core API interaction logic
- `get_weather_resource()`: MCP resource handler
- `get_current_weather()`: MCP tool handler
- `weather_query_prompt()`: Simple prompt template
- `weather_comparison_prompt()`: Advanced prompt template

### Testing
```bash
# Run the server in development mode
uv run mcp dev weather_server.py

# Test with different cities
# Use the MCP Inspector to test resources and tools
```

### Extending the Server
You can easily extend this server with additional features:

- **Historical weather data**
- **Weather forecasts**
- **Weather alerts**
- **Multiple weather providers**
- **Cached responses**

## Troubleshooting

### Common Issues

1. **"City not found" errors**
   - Ensure city names are spelled correctly
   - Try using full city names (e.g., "New York City" instead of "NYC")

2. **API key errors**
   - Verify your OpenWeatherMap API key is active
   - Check that the environment variable is set correctly

3. **Network errors**
   - Ensure internet connectivity
   - Check if OpenWeatherMap API is accessible from your network

### Debug Mode
Run with debug logging:
```bash
# Add debug output
python weather_server.py --debug
```

## License

This project is open source. Please ensure you comply with OpenWeatherMap's API terms of service.

## Contributing

Feel free to submit issues and pull requests to improve this weather MCP server!

# Connecting Your Weather MCP Server to Web Clients

## 🌐 Your Server Details

**✅ Server Status**: Running with CORS enabled
**📡 URL**: `http://127.0.0.1:8000/sse`
**🔧 Transport**: Server-Sent Events (SSE)
**🌤️ Features**: Real weather data from OpenWeatherMap

## 🚀 How to Connect to MCP-UI Web Client

### **Step 1: Access the Web Client**
Open the MCP web client: https://scira-mcp-chat-git-main-idosals-projects.vercel.app/

### **Step 2: Configure Your Server Connection**
In the web client interface, look for server configuration options and enter:

**Server URL**: `http://127.0.0.1:8000/sse`
**Transport Type**: SSE (Server-Sent Events)
**Name**: Weather Server (optional)

### **Step 3: Available Features**
Once connected, you can use these features:

#### **🌤️ Weather Resources**
- URI format: `weather://CityName`
- Examples:
  - `weather://London`
  - `weather://New York`
  - `weather://Tokyo`
  - `weather://Paris`

#### **🔧 Weather Tools**
- **Tool Name**: `get_current_weather`
- **Parameter**: `city` (string)
- **Usage**: Ask the AI to "get current weather for [city]"

#### **💬 Weather Prompts**
- **`weather_query_prompt`**: Basic weather query template
- **`weather_comparison_prompt`**: Compare weather between two cities

## 🎯 Example Conversations

### **Basic Weather Query**
```
You: "What's the weather in London?"
AI: [Uses get_current_weather tool] 
    The current weather in London is 21.7°C (71.1°F) with overcast clouds and 67% humidity.
```

### **Weather Comparison**
```
You: "Compare the weather between Paris and Tokyo"
AI: [Uses weather comparison prompt and tools]
    Paris: 24.1°C, cloudy
    Tokyo: [fetches data] 18.5°C, sunny
    Tokyo has better weather conditions today with sunshine.
```

### **Resource Access**
```
You: "Show me the weather resource for Mumbai"
AI: [Accesses weather://Mumbai resource]
    [Displays formatted weather information]
```

## 🔧 Troubleshooting

### **Connection Issues**
1. **CORS Errors**: Your server now has CORS enabled, so web clients should work
2. **Server Not Found**: Ensure your server is running at `http://127.0.0.1:8000`
3. **Port Conflicts**: If port 8000 is busy, modify the server code to use a different port

### **Server Status Check**
Run this command to verify your server is running:
```bash
curl http://127.0.0.1:8000/sse
```
You should see streaming ping messages.

### **Test Your Server**
Before connecting to web clients, test with our client:
```bash
python test_sse_client.py
```

## 📊 Web Client Configuration Examples

### **For Generic MCP Clients**
```json
{
  "servers": {
    "weather": {
      "url": "http://127.0.0.1:8000/sse",
      "transport": "sse",
      "description": "Local weather server"
    }
  }
}
```

### **For Development**
- **Local URL**: `http://127.0.0.1:8000/sse`
- **CORS**: ✅ Enabled for all origins
- **Authentication**: None required
- **Real Data**: ✅ OpenWeatherMap API

## 🌟 Features Your Server Provides

1. **Real Weather Data**: Live data from OpenWeatherMap
2. **Multiple Cities**: Supports any city in OpenWeatherMap database
3. **Comprehensive Data**: Temperature, humidity, conditions, descriptions
4. **Error Handling**: Graceful handling of invalid cities
5. **Multiple Interfaces**: Resources, tools, and prompts
6. **Web Compatible**: CORS enabled for browser clients

## 🎉 Ready to Use!

Your weather MCP server is now configured and ready to connect to web-based MCP clients. The server will provide real-time weather information for any city through a clean MCP interface.

**Server URL for web clients**: `http://127.0.0.1:8000/sse`

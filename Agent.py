# agent_client.py - LangChain agent integrating the MCP server
# Install: pip install langchain-mcp-adapters langchain langchain-openai asyncio

import asyncio
import os
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI  # Or use Anthropic, etc.
from langchain.agents import create_agent # Recommended for agents

async def main():
    # Absolute path to server file (adjust as needed)
    server_path = str("server.py")
    
    client = MultiServerMCPClient({
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": [server_path]
        }
    })
    
    # Load tools from MCP server
    tools = await client.get_tools()
    print(f"Loaded tools: {[tool.name for tool in tools]}")  # Debug: ['add', 'multiply']
    
    system_prompt = "You are a helpful math assistant. Use the provided tools to solve math problems step-by-step."
    # LLM (set OPENAI_API_KEY env var)
    os.environ["OPENAI_API_KEY"] = "give-api-key"
    model = ChatOpenAI(model="gpt-4o-mini")
    
    # Create ReAct agent
    agent = create_agent(model, tools, system_prompt=system_prompt)
    
    # Invoke with input
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What is 15 multiplied by 7, then add 10?"}]
    })
    print(response["messages"][-1].content)  # Agent output

if __name__ == "__main__":
    asyncio.run(main())

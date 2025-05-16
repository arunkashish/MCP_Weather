#It will be intreacting with the Weather.py file so we need to import here all the nessceary functions

import asyncio
import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent,MCPClient

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def run_memory_chat():
    # Load environment variables
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Create MCPClient from config file
    config_file = 'server/weather.json'
    print("Initialising MCP client...")
    logger.info(f"Loading MCP config from {config_file}")

    client = MCPClient.from_config_file(config_file)
    logger.info("Successfully created MCP client")

    # Create LLM
    llm = ChatGroq(model="qwen-qwq-32b")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=15, memory_enabled=True)
    logger.info("Successfully created MCP agent")
    print("\n----Interactive MCP chat")
    print("Type 'exit' to close the chat")
    print("Type 'clear' to clear the memory")

    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                print("Ending the convo...")
                break
            if user_input.lower() == "clear":
                agent.memory.clear()
                print("Memory cleared")
                continue
            print("\nAssistant: ", end="", flush=True)
            try:
                response = await agent.run(user_input)
                print(f"\nResult: {response}")
            except Exception as e:
                logger.error(f"Error during agent run: {str(e)}", exc_info=True)
                print(f"\nError: {e}")
    finally:
        # Close MCPClient sessions if applicable
        if client:
            await client.close_all_sessions()
            logger.info("Closed all MCP client sessions")

if __name__ == "__main__":
    asyncio.run(run_memory_chat())










# @date: 2025/11/16
# @author: Hokyee Jau

import asyncio
import json
from langgraph.prebuilt import create_react_agent

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)


server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)


async def chatgpt_41_generator(question="Do you smell Cass beer?"):
    model = ChatOpenAI(model="gpt-4o", temperature=0, api_key="<YOUR_OPENAI_KEY>")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            prompt = "You are a smart housekeeper. You can automatically invoke the API tools for answering the user questions."

            # session initialization
            await session.initialize()

            # tool retrieval
            tools = await load_mcp_tools(session)

            # create and run the agent
            agent = create_react_agent(model=model, tools=tools, prompt=prompt, debug=False)
            agent_response = await agent.ainvoke({"messages": question})
            try:
                formatted_response = json.loads(json.dumps(agent_response, indent=2, cls=CustomEncoder))
            except Exception:
                formatted_response = str(agent_response)

            return formatted_response


if __name__ == '__main__':
    response = asyncio.run(chatgpt_41_generator("Are you able to smell <object_1> or is it <object_2>?".replace("<object_1>", "kelly beer").replace("<object_2>", "cass belly")))
    print(response)
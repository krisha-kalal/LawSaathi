import os
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from google import genai
from dotenv import load_dotenv
from agents.tools import constitution_retrieval_tool

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def call_agent_node(state: AgentState):
    """Router node evaluating query intent."""
    last_message = state["messages"][-1].content
    
    # Simple routing logic: route legal questions to retrieval tool
    if any(keyword in last_message.lower() for keyword in ["article", "right", "duty", "schedule", "constitution", "law"]):
        tool_result = constitution_retrieval_tool.invoke({"query": last_message})
        return {"messages": [SystemMessage(content=tool_result)]}
    else:
        # General non-legal response fallback
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        res = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Respond politely indicating you specialize in Indian Constitutional Law. User said: {last_message}"
        )
        return {"messages": [SystemMessage(content=res.text)]}

def run_law_saathi_agent(user_prompt: str) -> str:
    initial_state = {"messages": [HumanMessage(content=user_prompt)]}
    result = call_agent_node(initial_state)
    return result["messages"][-1].content
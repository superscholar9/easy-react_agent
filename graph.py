from langgraph.graph import StateGraph
from state import AgentState
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
from langchain_core.messages import SystemMessage,HumanMessage,ToolMessage
from tools import TOOLS
from langgraph.graph import END ,START
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
def call_model(state:AgentState)->AgentState:
    system_prompt = (
        "You are a helpful assistant. Your primary goal is to answer the user's questions accurately. "
        "Pay close attention to the current system time: {system_time}. This is the single, absolute source of truth for the current date and time. "
        "When the user asks about 'today' or 'now', you MUST use this system time to understand the date. "
        "Then, create a specific search query using this date. For example, if the user asks for 'today's weather in Hangzhou' and the system time is '2025-08-08T...', your search query should be 'Hangzhou weather August 8 2025'. "
        "After getting the search results, synthesize the information to provide a complete answer. If the search results mention a different date, prioritize the information relevant to the date from the system time."
    )
    system_message = system_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    system_message = SystemMessage(content=system_message)
    print(system_message)
    llm = ChatOpenAI(
        model="glm-4.5",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_URL"),
    )
    llm_with_tools = llm.bind_tools(TOOLS)
    response = llm_with_tools.invoke([system_message]+state["messages"])
    return {"messages":[response]}
# 一定不能返回布尔类型
def should_continue(state:AgentState) -> str:
    if state["messages"][-1].tool_calls :
        return "goto"
    else:
        return "exit"

graph = StateGraph(AgentState)
tools=ToolNode(tools=TOOLS)
graph.add_node("tools",tools)
graph.add_node("call_model",call_model)
graph.add_edge(START,"call_model")
graph.add_conditional_edges("call_model",should_continue,{"goto":"tools","exit":END})
graph.add_edge("tools","call_model")
app=graph.compile()

def print_stream(stream):
    for s in stream:
        message=s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()
input={"messages":[("user","前天是几号")]}
print_stream(app.stream(input,stream_mode="values"))


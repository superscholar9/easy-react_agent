
from typing import TypedDict,Annotated,Sequence
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os
class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]


from langchain_core.tools import tool
from typing import Callable, List, Optional, cast,Any
from langchain_community.tools.tavily_search import TavilySearchResults
@tool
def add(a:int,b:int)->int:
    """
    this is a tool for adding two numbers
    """
    return a+b
@tool
def multiply(a:int,b:int)->int:
    """
    this is a tool for multiplying two numbers
    """
    return a*b

@tool
def search(
    query: str
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    wrapped = TavilySearchResults(max_results=5)
    result = wrapped.invoke({"query": query})
    return cast(list[dict[str, Any]], result)

TOOLS = [add,multiply,search]
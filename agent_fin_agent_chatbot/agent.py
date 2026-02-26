import pathlib
from typing import Dict, List
import yfinance as yf

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import ToolContext


def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches the current stock price and daily change for a list of stock tickers
    using the yfinance library.  

    Args:
        tickers: A list of stock market tickers (e.g., ["NVDA", "MSFT"]).

    Returns:
        A dictionary mapping each ticker to its formatted financial data string.
    """
    financial_data: Dict[str, str] = {}
    for ticker_symbol in tickers:
        try:
            # Create a Ticker object
            stock = yf.Ticker(ticker_symbol)
            
            # Fetch the info dictionary
            info = stock.info
            
            # Safely access the required data points
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")
            
            if price is not None and change_percent is not None:
                # Format the percentage and the final string
                change_str = f"{change_percent * 100:+.2f}%"
                financial_data[ticker_symbol] = f"\${price:.2f} ({change_str})"
            else:
                # Handle cases where the ticker is valid but data is missing
                financial_data[ticker_symbol] = "Price data not available."

        except Exception:
            # This handles invalid tickers or other yfinance errors gracefully
            financial_data[ticker_symbol] = "Invalid Ticker or Data Error"
            
    return financial_data

BLOCKED_DOMAINS = [
    "wikipedia.org",      # General info, not latest news
    "reddit.com",         # Discussion forums, not primary news
    "youtube.com",        # Video content not useful for text processing
    "medium.com",         # Blog platform with variable quality
    "investopedia.com",   # Financial definitions, not tech news
    "quora.com",          # Q&A site, opinions not reports
]

def filter_news_sources_callback(tool, args, tool_context):
    """
    Callback: Blocks search requests that target certain domains which are not necessarily news sources.
    Demonstrates content quality enforcement through request blocking.
    """
    if tool.name == "google_search":
        query = args.get("query", "").lower()

        # Check if query explicitly targets blocked domains
        for domain in BLOCKED_DOMAINS:
            if f"site:{domain}" in query or domain.replace(".org", "").replace(".com", "") in query:
                print(f"BLOCKED: Domains from blocked list detected: '{query}'")
                return {
                    "error": "blocked_source",
                    "reason": f"Searches targeting {domain} or similar are not allowed. Please search for professional news sources."
                }

        print(f"ALLOWED: Professional source query: '{query}'")
        return None


def initialize_process_log(tool_context: ToolContext):
    """Helper to ensure the process_log list exists in the state."""
    if 'process_log' not in tool_context.state:
        tool_context.state['process_log'] = []

def inject_process_log_after_search(tool, args, tool_context, tool_response):
    """
    Callback: After a successful search, this injects the process_log into the response
    and adds a specific note about which domains were sourced. This makes the callbacks'
    actions visible to the LLM.
    """
    if tool.name == "google_search" and isinstance(tool_response, str):
        # Extract source domains from the search results
        urls = re.findall(r'https?://[^\s/]+', tool_response)
        unique_domains = sorted(list(set(urlparse(url).netloc for url in urls)))
        
        if unique_domains:
            sourcing_log = f"Action: Sourced news from the following domains: {', '.join(unique_domains)}."
            # Prepend the new log to the existing one for better readability in the report
            current_log = tool_context.state.get('process_log', [])
            tool_context.state['process_log'] = [sourcing_log] + current_log

        final_log = tool_context.state.get('process_log', [])
        print(f"CALLBACK LOG: Injecting process log into tool response: {final_log}")
        return {
            "search_results": tool_response,
            "process_log": final_log
        }
    return tool_response

root_agent = Agent(
    name="ai_news_research_coordinator",
    model="gemini-2.5-flash-native-audio-preview-09-2025",
    tools=[google_search, get_financial_context],
    instruction="""
    **Your Core Identity and Sole Purpose:**
    You are an assistant who specializes on assisting traders with market news for a particular stock or sector.

    **Execution Plan:**

    1.  
        *   **Step 1:** Call `google_search` to find 3 recent news articles regarding a specific stock or sector.
        *   **Step 2:** Analyze the results to find company stock tickers.
        *   **Step 3:** Call `get_financial_context` with the list of tickers.
        *   **Step 4:** Find a correlation between the news articles and the financial context data. Generate a report.
        *   **Step 5:** Display the output on the console.


    **Understanding Callback-Modified Tool Outputs:**
    The `google_search` tool is enhanced by pre- and post-processing callbacks. 
    Its final output is a JSON object with two keys:
    1.  `search_results`: A string containing the actual search results.
    2.  `process_log`: A list of strings describing the filtering actions performed, including which domains were sourced.

    **Callback System Awareness:**
    You have a before tool callback "filter_news_sources_callback" that will automatically intercepts or 
    blocks your tool calls. Ensure you call it before each tool.

    **Crucial Operational Rule:**
    Do NOT show any intermediate content (raw search results, draft summaries, or processing steps) in your responses. 
    Your entire operation is a background pipeline that should culminate in a single, clean final answer.
    Speak and also write the final output to the console.
    """,
    before_tool_callback=[
        filter_news_sources_callback,         # Exclude certain domains
    ],
    after_tool_callback=[
        inject_process_log_after_search,
    ]
)
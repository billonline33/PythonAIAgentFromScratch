from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import wikipedia


def save_to_txt(data:str, filename: str= "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"---Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file",
)

wikipedia.set_user_agent("PythonAIAgentFromScratch/1.0 (research bot)")

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="search the web for infomration using duckduckgo",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
_wiki_run = WikipediaQueryRun(api_wrapper=api_wrapper)

def safe_wiki_run(query: str) -> str:
    try:
        return _wiki_run.run(query)
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"

wiki_tool = Tool(
    name="wikipedia",
    func=safe_wiki_run,
    description="look up information on Wikipedia",
)

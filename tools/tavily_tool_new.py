from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


# https://www.tavily.com/ 
# Signup and login, On dashboard- > under api keys you will see the default key.
# Use that or click on + to create new one. Then save it in .env file

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)
MAX_TAVILY_QUERY_LENGTH = 380
# test it
#################################
# response = client.search(
    # query="Best hotels in Dubai"
# )

# print(response)

####################################
def clean_query(query: str, max_length: int = MAX_TAVILY_QUERY_LENGTH) -> str:
    """
    Tavily has a max query length limit.
    This function cleans and safely trims long user queries.
    """
    if not query:
        return ""

    query = re.sub(r"\s+", " ", query).strip()

    if len(query) <= max_length:
        return query

    return query[:max_length].rsplit(" ", 1)[0]


def tavily_search(query):
    safe_query = clean_query(query)

    try:
        response = client.search(
            query=safe_query,
            max_results=5
        )
    except Exception as e:
        return f"Search service error: {str(e)}"

    results = []

    for i, r in enumerate(response["results"], 1):
        title   = r.get("title", "Unknown")
        url     = r.get("url", "")
        snippet = r.get("content", "").strip()
        # Keep only the first 300 characters to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results)
    
    
    
